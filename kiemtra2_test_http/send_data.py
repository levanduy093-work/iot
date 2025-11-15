from urllib import request, parse
from time import sleep, time
from grove.adc import ADC
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.display.jhd1802 import JHD1802
from grove.gpio import GPIO

# ThingSpeak HTTP Configuration
# Bạn cần thay đổi các thông tin sau theo Channel của bạn:
# Channel ID: [YOUR_CHANNEL_ID]
# API Key (Write): [YOUR_WRITE_API_KEY]
# API Key (Read): [YOUR_READ_API_KEY]

# Cấu hình pin
LIGHT_SENSOR_PIN = 0      # A0 - Cảm biến ánh sáng
ULTRASONIC_PIN = 5        # D5 - Cảm biến khoảng cách
LED_RED_PIN = 16          # D16 - LED đỏ
LED_YELLOW_PIN = 18       # D18 - LED vàng
BUZZER_PIN = 12           # D12 - Buzzer
VIBRATION_MOTOR_PIN = 13  # D13 - Motor rung (có thể thay đổi)

# Ngưỡng điều khiển
LIGHT_THRESHOLD_HIGH = 600  # Bật LED đỏ + buzzer khi > 600
LIGHT_THRESHOLD_LOW = 400   # Tắt LED đỏ + buzzer khi < 400
DISTANCE_THRESHOLD_CLOSE = 20  # Bật LED vàng + motor rung khi < 20cm
DISTANCE_THRESHOLD_FAR = 40    # Tắt LED vàng + motor rung khi > 40cm

# Khởi tạo các class
class GroveLED(GPIO):
    def __init__(self, pin):
        super(GroveLED, self).__init__(pin, GPIO.OUT)

    def on(self):
        self.write(1)

    def off(self):
        self.write(0)

class GroveBuzzer(GPIO):
    def __init__(self, pin):
        super(GroveBuzzer, self).__init__(pin, GPIO.OUT)

    def on(self):
        self.write(1)

    def off(self):
        self.write(0)

class GroveVibrationMotor(GPIO):
    def __init__(self, pin):
        super(GroveVibrationMotor, self).__init__(pin, GPIO.OUT)

    def on(self):
        self.write(1)

    def off(self):
        self.write(0)

class GroveLightSensor:
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC(address=0x08)

    @property
    def value(self):
        return self.adc.read(self.channel)  # trả về 0–1000

# Khởi tạo các thiết bị
light_sensor = GroveLightSensor(LIGHT_SENSOR_PIN)
ultrasonic_sensor = GroveUltrasonicRanger(ULTRASONIC_PIN)
lcd = JHD1802()
led_red = GroveLED(LED_RED_PIN)
led_yellow = GroveLED(LED_YELLOW_PIN)
buzzer = GroveBuzzer(BUZZER_PIN)
vibration_motor = GroveVibrationMotor(VIBRATION_MOTOR_PIN)

# Biến trạng thái
led_red_state = False
led_yellow_state = False
buzzer_state = False
vibration_motor_state = False

def make_param_thingspeak(light_value, distance_value):
    """Tạo tham số để gửi lên ThingSpeak"""
    params = parse.urlencode({
        'field1': f"{light_value:.1f}",      # Cường độ ánh sáng
        'field2': f"{distance_value:.1f}",   # Khoảng cách (cm)
    }).encode()
    return params

def thingspeak_post_http(params, api_key_write):
    """Gửi dữ liệu lên ThingSpeak qua HTTP"""
    req = request.Request('https://api.thingspeak.com/update', method="POST")
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('X-THINGSPEAKAPIKEY', api_key_write)
    try:
        with request.urlopen(req, data=params, timeout=10) as r:
            response_data = r.read().decode().strip()
        return response_data
    except Exception as e:
        print(f"Lỗi HTTP khi gửi lên ThingSpeak: {e}")
        return None

def control_led_red_buzzer(light_value):
    """Điều khiển LED đỏ và buzzer dựa trên cường độ ánh sáng"""
    global led_red_state, buzzer_state
    
    if light_value > LIGHT_THRESHOLD_HIGH:
        # Bật LED đỏ và buzzer khi ánh sáng > 600
        if not led_red_state:
            led_red.on()
            led_red_state = True
            print("LED ĐỎ: BẬT (Ánh sáng > 600)")
        if not buzzer_state:
            buzzer.on()
            buzzer_state = True
            print("BUZZER: BẬT (Ánh sáng > 600)")
    elif light_value < LIGHT_THRESHOLD_LOW:
        # Tắt LED đỏ và buzzer khi ánh sáng < 400
        if led_red_state:
            led_red.off()
            led_red_state = False
            print("LED ĐỎ: TẮT (Ánh sáng < 400)")
        if buzzer_state:
            buzzer.off()
            buzzer_state = False
            print("BUZZER: TẮT (Ánh sáng < 400)")

def control_led_yellow_vibration(distance_value):
    """Điều khiển LED vàng và motor rung dựa trên khoảng cách"""
    global led_yellow_state, vibration_motor_state
    
    if distance_value < DISTANCE_THRESHOLD_CLOSE:
        # Bật LED vàng và motor rung khi khoảng cách < 20cm
        if not led_yellow_state:
            led_yellow.on()
            led_yellow_state = True
            print(f"LED VÀNG: BẬT (Khoảng cách < 20cm: {distance_value:.1f}cm)")
        if not vibration_motor_state:
            vibration_motor.on()
            vibration_motor_state = True
            print(f"MOTOR RUNG: BẬT (Khoảng cách < 20cm: {distance_value:.1f}cm)")
    elif distance_value > DISTANCE_THRESHOLD_FAR:
        # Tắt LED vàng và motor rung khi khoảng cách > 40cm
        if led_yellow_state:
            led_yellow.off()
            led_yellow_state = False
            print(f"LED VÀNG: TẮT (Khoảng cách > 40cm: {distance_value:.1f}cm)")
        if vibration_motor_state:
            vibration_motor.off()
            vibration_motor_state = False
            print(f"MOTOR RUNG: TẮT (Khoảng cách > 40cm: {distance_value:.1f}cm)")

def display_on_lcd(light_value, distance_value):
    """Hiển thị dữ liệu trên LCD 16x2"""
    try:
        # Dòng 1: Hiển thị ánh sáng
        lcd.setCursor(0, 0)
        lcd.write(f"Light: {light_value:>4.0f}  ")
        
        # Dòng 2: Hiển thị khoảng cách
        lcd.setCursor(1, 0)
        lcd.write(f"Dist: {distance_value:>5.1f}cm")
    except Exception as e:
        print(f"Lỗi khi hiển thị LCD: {e}")

def main():
    """Chương trình chính"""
    print("="*60)
    print("HỆ THỐNG GIÁM SÁT ÁNH SÁNG VÀ KHOẢNG CÁCH")
    print("="*60)
    print("Đang khởi động...")
    print(f"Ngưỡng ánh sáng: Bật > {LIGHT_THRESHOLD_HIGH}, Tắt < {LIGHT_THRESHOLD_LOW}")
    print(f"Ngưỡng khoảng cách: Bật < {DISTANCE_THRESHOLD_CLOSE}cm, Tắt > {DISTANCE_THRESHOLD_FAR}cm")
    print("="*60)
    
    # ThingSpeak HTTP Configuration (từ on_kiemtra_2_http)
    # Channel ID: 3153408
    # API Key (Write): AHHO5UL59ZCYUYCV
    # API Key (Read): N251PNZ5EG0MWI2Y
    API_KEY_WRITE = "AHHO5UL59ZCYUYCV"
    
    READ_INTERVAL = 10  # Đọc cảm biến và gửi dữ liệu mỗi 10 giây
    last_sent_ts = 0.0
    
    # Khởi tạo LCD
    try:
        lcd.setCursor(0, 0)
        lcd.write("Initializing...")
        sleep(1)
    except Exception as e:
        print(f"Cảnh báo: Không thể khởi tạo LCD: {e}")
    
    try:
        while True:
            # Đọc dữ liệu từ cảm biến ánh sáng
            try:
                light_value = light_sensor.value
            except Exception as e:
                print(f"Lỗi khi đọc cảm biến ánh sáng: {e}")
                light_value = 0
            
            # Đọc dữ liệu từ cảm biến khoảng cách
            try:
                distance_value = ultrasonic_sensor.get_distance()
            except Exception as e:
                print(f"Lỗi khi đọc cảm biến khoảng cách: {e}")
                distance_value = 0
            
            # Hiển thị lên Terminal
            print("\n" + "="*60)
            print(f"Cường độ ánh sáng: {light_value:.1f}")
            print(f"Khoảng cách: {distance_value:.1f} cm")
            print("="*60)
            
            # Hiển thị lên LCD
            display_on_lcd(light_value, distance_value)
            
            # Điều khiển LED đỏ và buzzer dựa trên ánh sáng
            control_led_red_buzzer(light_value)
            
            # Điều khiển LED vàng và motor rung dựa trên khoảng cách
            control_led_yellow_vibration(distance_value)
            
            # Gửi dữ liệu lên ThingSpeak qua HTTP (mỗi 10 giây)
            now = time()
            if now - last_sent_ts >= READ_INTERVAL:
                params = make_param_thingspeak(light_value, distance_value)
                resp = thingspeak_post_http(params, API_KEY_WRITE)
                if resp and resp != '0':
                    print(f"✓ Đã gửi dữ liệu lên ThingSpeak, entry id: {resp}")
                    last_sent_ts = now
                else:
                    print(f"✗ ThingSpeak update thất bại (response: {resp})")
                    last_sent_ts = now
            
            print("="*60)
            sleep(READ_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\nĐang tắt hệ thống...")
        led_red.off()
        led_yellow.off()
        buzzer.off()
        vibration_motor.off()
        try:
            lcd.setCursor(0, 0)
            lcd.write("System OFF    ")
            lcd.setCursor(1, 0)
            lcd.write("                ")
        except:
            pass
        print("Hệ thống đã tắt.")

if __name__ == '__main__':
    main()

