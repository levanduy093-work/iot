import paho.mqtt.client as mqtt
from time import sleep, time
from seeed_dht import DHT
from grove.gpio import GPIO

# ThingSpeak MQTT Configuration
# Bạn cần thay đổi các thông tin sau theo Channel của bạn:
# Channel ID: [YOUR_CHANNEL_ID]
# username  = '[YOUR_USERNAME]'
# client_ID = '[YOUR_CLIENT_ID]'
# password  = '[YOUR_PASSWORD]'

# Cấu hình pin
DHT11_PIN = 5           # D5 - Cảm biến nhiệt độ và độ ẩm DHT11
LED_RED_PIN = 16        # D16 - LED đỏ (cảnh báo nhiệt độ)
LED_YELLOW_PIN = 18     # D18 - LED vàng (cảnh báo độ ẩm)
BUZZER_PIN = 12         # D12 - Buzzer (cảnh báo âm thanh)

# Ngưỡng điều khiển
TEMP_THRESHOLD_HIGH = 40   # Bật LED đỏ khi nhiệt độ > 40°C
TEMP_THRESHOLD_LOW = 30    # Tắt LED đỏ khi nhiệt độ < 30°C
TEMP_BUZZER_THRESHOLD = 50 # Bật buzzer khi nhiệt độ > 50°C
HUMI_THRESHOLD_HIGH = 70   # Bật LED vàng khi độ ẩm > 70%
HUMI_THRESHOLD_LOW = 40    # Tắt LED vàng khi độ ẩm < 40%

# ThingSpeak MQTT Configuration (từ on_kiemtra_2_mqtt)
# Channel ID: 3153408
CHANNEL_ID = "3153408"
CLIENT_ID = "Dg0MFSkPJAIJMgchHjw1BwY"
USERNAME = "Dg0MFSkPJAIJMgchHjw1BwY"
PASSWORD = "8p9YF6bT68Hxjny5ChF13Vrm"

# Khởi tạo MQTT client
client = mqtt.Client(client_id=CLIENT_ID)
client.username_pw_set(USERNAME, password=PASSWORD)
client.connect("mqtt3.thingspeak.com", 1883, 60)

# Khởi tạo cảm biến DHT11 (kết nối với port D5)
sensor = DHT('11', DHT11_PIN)

# Khởi tạo LED class
class GroveLED(GPIO):
    def __init__(self, pin):
        super(GroveLED, self).__init__(pin, GPIO.OUT)

    def on(self):
        self.write(1)

    def off(self):
        self.write(0)

# Khởi tạo Buzzer class
class GroveBuzzer(GPIO):
    def __init__(self, pin):
        super(GroveBuzzer, self).__init__(pin, GPIO.OUT)

    def on(self):
        self.write(1)

    def off(self):
        self.write(0)

# Khởi tạo LED đỏ và LED vàng
led_red = GroveLED(LED_RED_PIN)      # LED đỏ - điều khiển theo nhiệt độ
led_yellow = GroveLED(LED_YELLOW_PIN) # LED vàng - điều khiển theo độ ẩm

# Khởi tạo buzzer (kết nối với pin 12)
buzzer = GroveBuzzer(BUZZER_PIN)

# Biến trạng thái LED và buzzer
led_red_state = False
led_yellow_state = False
buzzer_state = False
buzzer_last_toggle_time = 0
buzzer_is_on = False

def thingspeak_mqtt(temp, humi):
    """Gửi dữ liệu nhiệt độ và độ ẩm lên ThingSpeak qua MQTT"""
    # Field1: Nhiệt độ, Field2: Độ ẩm
    topic = "channels/%s/publish" % (CHANNEL_ID)
    payload = "field1=%s&field2=%s&status=MQTTPUBLISH" % (temp, humi)
    client.publish(topic, payload)

def control_leds(temp, humi):
    """Điều khiển LED dựa trên nhiệt độ và độ ẩm"""
    global led_red_state, led_yellow_state
    
    # Điều khiển LED đỏ theo nhiệt độ
    # Sáng khi nhiệt độ > 40°C, tắt khi nhiệt độ < 30°C
    if temp > TEMP_THRESHOLD_HIGH:
        if not led_red_state:
            led_red.on()
            led_red_state = True
            print("LED ĐỎ: BẬT (Nhiệt độ > 40°C)")
    elif temp < TEMP_THRESHOLD_LOW:
        if led_red_state:
            led_red.off()
            led_red_state = False
            print("LED ĐỎ: TẮT (Nhiệt độ < 30°C)")
    
    # Điều khiển LED vàng theo độ ẩm
    # Sáng khi độ ẩm > 70%, tắt khi độ ẩm < 40%
    if humi > HUMI_THRESHOLD_HIGH:
        if not led_yellow_state:
            led_yellow.on()
            led_yellow_state = True
            print("LED VÀNG: BẬT (Độ ẩm > 70%)")
    elif humi < HUMI_THRESHOLD_LOW:
        if led_yellow_state:
            led_yellow.off()
            led_yellow_state = False
            print("LED VÀNG: TẮT (Độ ẩm < 40%)")

def control_buzzer(temp):
    """Điều khiển buzzer khi nhiệt độ vượt quá 50°C"""
    global buzzer_state, buzzer_last_toggle_time, buzzer_is_on
    
    # Chuông: 1s bip, 1s không và lặp lại, khi nhiệt độ vượt quá 50°C
    current_time = time()
    
    if temp > TEMP_BUZZER_THRESHOLD:
        if not buzzer_state:
            buzzer_state = True
            buzzer_last_toggle_time = current_time
            buzzer_is_on = True
            buzzer.on()
            print("CHUÔNG: BẬT (Nhiệt độ > 50°C)")
        else:
            # Kiểm tra xem đã đến lúc toggle chưa (mỗi 1 giây)
            if current_time - buzzer_last_toggle_time >= 1.0:
                buzzer_last_toggle_time = current_time
                buzzer_is_on = not buzzer_is_on
                if buzzer_is_on:
                    buzzer.on()
                else:
                    buzzer.off()
    else:
        if buzzer_state:
            buzzer.off()
            buzzer_state = False
            buzzer_is_on = False
            print("CHUÔNG: TẮT (Nhiệt độ <= 50°C)")

def main():
    """Chương trình chính"""
    print("="*60)
    print("HỆ THỐNG GIÁM SÁT NHIỆT ĐỘ VÀ ĐỘ ẨM (MQTT)")
    print("="*60)
    print("Đang khởi động...")
    print(f"Ngưỡng nhiệt độ: LED đỏ Bật > {TEMP_THRESHOLD_HIGH}°C, Tắt < {TEMP_THRESHOLD_LOW}°C")
    print(f"Ngưỡng độ ẩm: LED vàng Bật > {HUMI_THRESHOLD_HIGH}%, Tắt < {HUMI_THRESHOLD_LOW}%")
    print(f"Buzzer: Bật khi nhiệt độ > {TEMP_BUZZER_THRESHOLD}°C")
    print("="*60)
    
    try:
        while True:
            # Đọc dữ liệu từ cảm biến DHT11
            try:
                humi, temp = sensor.read()
            except Exception as e:
                print(f"Lỗi khi đọc cảm biến: {e}")
                sleep(5)
                continue
            
            if humi is None or temp is None:
                print("Đọc cảm biến thất bại (None); thử lại sau 5s…")
                sleep(5)
                continue
            
            # Hiển thị lên Terminal
            print("\n" + "="*60)
            print("Nhiệt độ: {0}°C | Độ ẩm: {1}%".format(temp, humi))
            print("="*60)
            
            # Điều khiển LED dựa trên ngưỡng
            control_leds(temp, humi)
            
            # Điều khiển buzzer khi nhiệt độ > 50°C
            control_buzzer(temp)
            
            # Gửi dữ liệu lên ThingSpeak qua MQTT
            thingspeak_mqtt(temp, humi)
            print("Đã gửi dữ liệu lên ThingSpeak qua MQTT")
            print("="*60)
            
            # Nếu buzzer đang hoạt động, kiểm tra và toggle mỗi 1 giây
            # Nếu không, chờ 10 giây trước khi đọc lần tiếp theo
            if buzzer_state:
                # Kiểm tra buzzer mỗi 1 giây khi đang hoạt động
                sleep(1)
            else:
                # Chờ 10 giây trước khi đọc lần tiếp theo
                sleep(10)
            
    except KeyboardInterrupt:
        print("\n\nĐang tắt hệ thống...")
        led_red.off()
        led_yellow.off()
        buzzer.off()
        client.disconnect()
        print("Hệ thống đã tắt.")

if __name__ == '__main__':
    main()

