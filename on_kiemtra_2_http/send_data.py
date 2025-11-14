from urllib import request, parse
from time import sleep, time
from seeed_dht import DHT
from grove.gpio import GPIO

# ThingSpeak HTTP Configuration
# Channel ID: 3153408
# API Key (Write): AHHO5UL59ZCYUYCV
# API Key (Read): N251PNZ5EG0MWI2Y

# Khởi tạo cảm biến DHT11 (kết nối với port D5)
sensor = DHT('11', 5)

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
# Giả sử LED đỏ kết nối với pin 16, LED vàng kết nối với pin 18
led_red = GroveLED(16)    # LED đỏ - điều khiển theo nhiệt độ
led_yellow = GroveLED(18) # LED vàng - điều khiển theo độ ẩm

# Khởi tạo buzzer (kết nối với pin 12)
buzzer = GroveBuzzer(12)

# Biến trạng thái LED và buzzer
led_red_state = False
led_yellow_state = False
buzzer_state = False
buzzer_last_toggle_time = 0
buzzer_is_on = False

def make_param_thingspeak(temp, humi, led_yellow_status, led_red_status):
    """Tạo tham số để gửi lên ThingSpeak"""
    params = parse.urlencode({
        'field1': f"{temp:.1f}",      # Nhiệt độ
        'field2': f"{humi:.1f}",      # Độ ẩm
        'field3': f"{led_yellow_status}",  # LED vàng (1=ON, 0=OFF)
        'field4': f"{led_red_status}"      # LED đỏ (1=ON, 0=OFF)
    }).encode()
    return params

def thingspeak_post_http(params):
    """Gửi dữ liệu lên ThingSpeak qua HTTP"""
    api_key_write = "AHHO5UL59ZCYUYCV"
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

def control_leds(temp, humi):
    """Điều khiển LED dựa trên nhiệt độ và độ ẩm"""
    global led_red_state, led_yellow_state
    
    # Điều khiển LED đỏ theo nhiệt độ
    # Sáng khi nhiệt độ > 40°C, tắt khi nhiệt độ < 30°C
    if temp > 40:
        if not led_red_state:
            led_red.on()
            led_red_state = True
            print("LED ĐỎ: BẬT (Nhiệt độ > 40°C)")
    elif temp < 30:
        if led_red_state:
            led_red.off()
            led_red_state = False
            print("LED ĐỎ: TẮT (Nhiệt độ < 30°C)")
    
    # Điều khiển LED vàng theo độ ẩm
    # Sáng khi độ ẩm > 70%, tắt khi độ ẩm < 40%
    if humi > 70:
        if not led_yellow_state:
            led_yellow.on()
            led_yellow_state = True
            print("LED VÀNG: BẬT (Độ ẩm > 70%)")
    elif humi < 40:
        if led_yellow_state:
            led_yellow.off()
            led_yellow_state = False
            print("LED VÀNG: TẮT (Độ ẩm < 40%)")

def control_buzzer(temp):
    """Điều khiển buzzer khi nhiệt độ vượt quá 50°C"""
    global buzzer_state, buzzer_last_toggle_time, buzzer_is_on
    
    # Chuông: 1s bip, 1s không và lặp lại, khi nhiệt độ vượt quá 50°C
    current_time = time()
    
    if temp > 50:
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
    print("=== HỆ THỐNG GIÁM SÁT NHIỆT ĐỘ VÀ ĐỘ ẨM (HTTP) ===")
    print("Đang khởi động...")
    
    READ_INTERVAL = 10  # Đọc cảm biến mỗi 10 giây
    SEND_INTERVAL = 15  # Gửi lên ThingSpeak mỗi 15 giây (ThingSpeak rate limit)
    last_sent_ts = 0.0
    
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
            print("\n" + "="*50)
            print("Nhiệt độ: {0}°C | Độ ẩm: {1}%".format(temp, humi))
            
            # Điều khiển LED dựa trên ngưỡng
            control_leds(temp, humi)
            
            # Điều khiển buzzer khi nhiệt độ > 50°C
            control_buzzer(temp)
            
            # Gửi dữ liệu lên ThingSpeak qua HTTP (mỗi 15 giây)
            now = time()
            if now - last_sent_ts >= SEND_INTERVAL:
                led_yellow_status = 1 if led_yellow_state else 0
                led_red_status = 1 if led_red_state else 0
                params = make_param_thingspeak(temp, humi, led_yellow_status, led_red_status)
                resp = thingspeak_post_http(params)
                if resp and resp != '0':
                    print("Đã gửi dữ liệu lên ThingSpeak, entry id: {0}".format(resp))
                    last_sent_ts = now
                else:
                    print("ThingSpeak update thất bại hoặc chưa đến lượt (response: {0})".format(resp))
            
            print("="*50)
            
            # Nếu buzzer đang hoạt động, kiểm tra và toggle mỗi 1 giây
            # Nếu không, chờ 10 giây trước khi đọc lần tiếp theo
            if buzzer_state:
                # Kiểm tra buzzer mỗi 1 giây khi đang hoạt động
                sleep(1)
            else:
                # Chờ 10 giây trước khi đọc lần tiếp theo
                sleep(READ_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\nĐang tắt hệ thống...")
        led_red.off()
        led_yellow.off()
        buzzer.off()
        print("Hệ thống đã tắt.")

if __name__ == '__main__':
    main()

