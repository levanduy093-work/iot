import paho.mqtt.client as mqtt
import time
import os
from grove.adc import ADC
from grove.gpio import GPIO
from grove.display.jhd1802 import JHD1802

# ========================================
# CẤU HÌNH THINGSPEAK MQTT
# ========================================
CHANNEL_ID = "3153408"  # Thay đổi theo Channel ID của bạn

# Đọc MQTT credentials từ file send_data_mqtt_key.txt
def load_mqtt_credentials(key_file):
    """Đọc MQTT credentials từ file"""
    credentials = {}
    key_path = os.path.join(os.path.dirname(__file__), '..', key_file)
    if not os.path.exists(key_path):
        key_path = os.path.join(os.path.dirname(__file__), key_file)
    
    if os.path.exists(key_path):
        with open(key_path, 'r') as f:
            for line in f:
                line = line.strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    if key == 'username':
                        credentials['username'] = value
                    elif key == 'clientId':
                        credentials['client_id'] = value
                    elif key == 'password':
                        credentials['password'] = value
    else:
        print(f"Warning: File {key_path} không tồn tại, sử dụng giá trị mặc định")
        credentials = {
            'username': 'Dg0MFSkPJAIJMgchHjw1BwY',
            'client_id': 'Dg0MFSkPJAIJMgchHjw1BwY',
            'password': '8p9YF6bT68Hxjny5ChF13Vrm'
        }
    return credentials

# Load credentials từ file
mqtt_creds = load_mqtt_credentials('send_data_mqtt_key.txt')
CLIENT_ID = mqtt_creds.get('client_id', 'Dg0MFSkPJAIJMgchHjw1BwY')
USERNAME = mqtt_creds.get('username', 'Dg0MFSkPJAIJMgchHjw1BwY')
PASSWORD = mqtt_creds.get('password', '8p9YF6bT68Hxjny5ChF13Vrm')

MQTT_HOST = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

# ========================================
# CẤU HÌNH PIN VÀ CẢM BIẾN
# ========================================
LIGHT_SENSOR_CHANNEL = 0      # Port A0 (Analog)
ULTRASONIC_PIN = 5             # Port D5 (Digital)
BLUE_LIGHT_PIN = 16            # Port D16 (Blue Light)
LED_YELLOW_PIN = 18            # Port D18 (LED vàng)
BUZZER_PIN = 12                # Port D12 (Buzzer)
VIBRATION_MOTOR_PIN = 22       # Port D22 (Motor rung)

# ========================================
# CẤU HÌNH THỜI GIAN
# ========================================
DISPLAY_INTERVAL = 20          # Hiển thị và gửi dữ liệu mỗi 20 giây
READ_INTERVAL = 1              # Đọc cảm biến mỗi 1 giây

# ========================================
# ĐỊNH NGHĨA CÁC CLASS
# ========================================

class GroveLightSensor:
    """Cảm biến ánh sáng Grove"""
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC(address=0x08)
    
    @property
    def value(self):
        return self.adc.read(self.channel)  # Trả về 0-1000

class GroveUltrasonicRanger:
    """Cảm biến khoảng cách siêu âm Grove"""
    def __init__(self, pin):
        self.dio = GPIO(pin)
    
    def _get_distance(self):
        """Đọc khoảng cách từ cảm biến siêu âm"""
        usleep = lambda x: time.sleep(x / 1000000.0)
        _TIMEOUT1 = 1000
        _TIMEOUT2 = 10000
        
        self.dio.dir(GPIO.OUT)
        self.dio.write(0)
        usleep(2)
        self.dio.write(1)
        usleep(10)
        self.dio.write(0)
        self.dio.dir(GPIO.IN)
        
        t0 = time.time()
        count = 0
        while count < _TIMEOUT1:
            if self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT1:
            return None
        
        t1 = time.time()
        count = 0
        while count < _TIMEOUT2:
            if not self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT2:
            return None
        
        t2 = time.time()
        dt = int((t1 - t0) * 1000000)
        if dt > 530:
            return None
        
        distance = ((t2 - t1) * 1000000 / 29 / 2)  # cm
        return distance
    
    def get_distance(self):
        """Lấy khoảng cách (retry nếu None)"""
        while True:
            dist = self._get_distance()
            if dist:
                return dist

class GroveLED(GPIO):
    """LED Grove"""
    def __init__(self, pin):
        super(GroveLED, self).__init__(pin, GPIO.OUT)
    
    def on(self):
        self.write(1)
    
    def off(self):
        self.write(0)

class GroveBuzzer(GPIO):
    """Buzzer Grove"""
    def __init__(self, pin):
        super(GroveBuzzer, self).__init__(pin, GPIO.OUT)
    
    def on(self):
        self.write(1)
    
    def off(self):
        self.write(0)

class GroveVibrationMotor(GPIO):
    """Motor rung Grove"""
    def __init__(self, pin):
        super(GroveVibrationMotor, self).__init__(pin, GPIO.OUT)
    
    def on(self):
        self.write(1)
    
    def off(self):
        self.write(0)

# ========================================
# KHỞI TẠO CÁC THIẾT BỊ
# ========================================
light_sensor = GroveLightSensor(LIGHT_SENSOR_CHANNEL)
ultrasonic = GroveUltrasonicRanger(ULTRASONIC_PIN)
blue_light = GroveLED(BLUE_LIGHT_PIN)
led_yellow = GroveLED(LED_YELLOW_PIN)
buzzer = GroveBuzzer(BUZZER_PIN)
vibration_motor = GroveVibrationMotor(VIBRATION_MOTOR_PIN)
lcd = JHD1802()

# ========================================
# CẤU HÌNH MQTT
# ========================================
client = mqtt.Client(client_id=CLIENT_ID)
client.username_pw_set(USERNAME, password=PASSWORD)

def on_connect(client, userdata, flags, rc):
    """Callback khi kết nối MQTT"""
    if rc == 0:
        print("✓ Đã kết nối MQTT thành công")
    else:
        print(f"✗ Kết nối MQTT thất bại (rc={rc})")

def on_publish(client, userdata, mid):
    """Callback khi publish thành công"""
    print(f"  → Đã gửi dữ liệu lên ThingSpeak (MID={mid})")

client.on_connect = on_connect
client.on_publish = on_publish
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)
client.loop_start()

# ========================================
# HÀM ĐIỀU KHIỂN
# ========================================

# Biến trạng thái toàn cục
blue_light_state = False
led_yellow_state = False
buzzer_state = False
motor_state = False

def control_blue_light_buzzer(light_value):
    """Điều khiển Blue Light và buzzer theo cường độ ánh sáng"""
    global blue_light_state, buzzer_state
    
    # Blue Light và buzzer: Sáng/kêu khi ánh sáng > 500, tắt khi < 200
    if light_value > 500:
        if not blue_light_state:
            blue_light.on()
            buzzer.on()
            blue_light_state = True
            buzzer_state = True
            print(f"Blue Light và Buzzer: BẬT (Ánh sáng > 500)")
    elif light_value < 200:
        if blue_light_state:
            blue_light.off()
            buzzer.off()
            blue_light_state = False
            buzzer_state = False
            print(f"Blue Light và Buzzer: TẮT (Ánh sáng < 200)")
    # Giữ nguyên trạng thái nếu 200 <= light_value <= 500

def control_led_yellow_motor(distance):
    """Điều khiển LED vàng và motor rung theo khoảng cách"""
    global led_yellow_state, motor_state
    
    # LED vàng và motor rung: Sáng/rung khi khoảng cách < 20cm, tắt khi > 40cm
    if distance < 20:
        if not led_yellow_state:
            led_yellow.on()
            vibration_motor.on()
            led_yellow_state = True
            motor_state = True
            print(f"LED vàng và Motor rung: BẬT (Khoảng cách < 20cm)")
    elif distance > 40:
        if led_yellow_state:
            led_yellow.off()
            vibration_motor.off()
            led_yellow_state = False
            motor_state = False
            print(f"LED vàng và Motor rung: TẮT (Khoảng cách > 40cm)")
    # Giữ nguyên trạng thái nếu 20 <= distance <= 40

def thingspeak_mqtt_publish(light_value, distance):
    """Gửi dữ liệu lên ThingSpeak qua MQTT"""
    topic = f"channels/{CHANNEL_ID}/publish"
    payload = f"field1={light_value}&field2={distance:.1f}&status=MQTTPUBLISH"
    client.publish(topic, payload)

def display_on_lcd(light_value, distance):
    """Hiển thị dữ liệu trên LCD"""
    try:
        lcd.setCursor(0, 0)
        lcd.write(f"Light: {light_value:>4}")
        lcd.setCursor(1, 0)
        lcd.write(f"Dist: {distance:>5.1f}cm")
    except Exception as e:
        print(f"Lỗi hiển thị LCD: {e}")

# ========================================
# CHƯƠNG TRÌNH CHÍNH
# ========================================

def main():
    """Chương trình chính"""
    print("=" * 60)
    print("HỆ THỐNG GIÁM SÁT ÁNH SÁNG VÀ KHOẢNG CÁCH")
    print("=" * 60)
    print(f"Đọc cảm biến mỗi {READ_INTERVAL} giây")
    print(f"Hiển thị và gửi dữ liệu mỗi {DISPLAY_INTERVAL} giây")
    print("=" * 60)
    
    last_display_time = time.time()
    
    try:
        while True:
            # Đọc cảm biến ánh sáng
            try:
                light_value = light_sensor.value
            except Exception as e:
                print(f"Lỗi đọc cảm biến ánh sáng: {e}")
                light_value = 0
            
            # Đọc cảm biến khoảng cách
            try:
                distance = ultrasonic.get_distance()
            except Exception as e:
                print(f"Lỗi đọc cảm biến khoảng cách: {e}")
                distance = 0
            
            # Điều khiển Blue Light và buzzer
            control_blue_light_buzzer(light_value)
            
            # Điều khiển LED vàng và motor rung
            control_led_yellow_motor(distance)
            
            # Kiểm tra xem đã đến lúc hiển thị và gửi dữ liệu chưa
            current_time = time.time()
            if current_time - last_display_time >= DISPLAY_INTERVAL:
                # Hiển thị trên Terminal
                print("\n" + "=" * 60)
                print(f"Thời gian: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Cường độ ánh sáng: {light_value}")
                print(f"Khoảng cách: {distance:.1f} cm")
                print(f"Blue Light: {'BẬT' if blue_light_state else 'TẮT'}")
                print(f"Buzzer: {'BẬT' if buzzer_state else 'TẮT'}")
                print(f"LED vàng: {'BẬT' if led_yellow_state else 'TẮT'}")
                print(f"Motor rung: {'BẬT' if motor_state else 'TẮT'}")
                print("=" * 60)
                
                # Hiển thị trên LCD
                display_on_lcd(light_value, distance)
                
                # Gửi dữ liệu lên ThingSpeak
                try:
                    thingspeak_mqtt_publish(light_value, distance)
                    print("✓ Đã gửi dữ liệu lên ThingSpeak")
                except Exception as e:
                    print(f"✗ Lỗi gửi dữ liệu lên ThingSpeak: {e}")
                
                last_display_time = current_time
            
            # Chờ trước khi đọc lần tiếp theo
            time.sleep(READ_INTERVAL)
    
    except KeyboardInterrupt:
        print("\n\nĐang tắt hệ thống...")
        blue_light.off()
        led_yellow.off()
        buzzer.off()
        vibration_motor.off()
        client.loop_stop()
        client.disconnect()
        print("Hệ thống đã tắt.")
        exit(0)

if __name__ == '__main__':
    main()

