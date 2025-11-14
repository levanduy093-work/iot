import paho.mqtt.client as mqtt
from time import sleep
from seeed_dht import DHT
from grove.display.jhd1802 import JHD1802
from grove.gpio import GPIO

# ThingSpeak MQTT Configuration
# Channel ID: 3127848
# username  = 'Dg0MFSkPJAIJMgchHjw1BwY'
# client_ID = 'Dg0MFSkPJAIJMgchHjw1BwY'
# password  = '8p9YF6bT68Hxjny5ChF13Vrm'

# Khởi tạo MQTT client
client = mqtt.Client(client_id="Dg0MFSkPJAIJMgchHjw1BwY")
client.username_pw_set("Dg0MFSkPJAIJMgchHjw1BwY",
                       password="8p9YF6bT68Hxjny5ChF13Vrm")
client.connect("mqtt3.thingspeak.com", 1883, 60)

# Khởi tạo LCD 16x2
lcd = JHD1802()

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

# Khởi tạo LED đỏ và LED vàng
# Giả sử LED đỏ kết nối với pin 16, LED vàng kết nối với pin 18
led_red = GroveLED(16)    # LED đỏ - điều khiển theo nhiệt độ
led_yellow = GroveLED(18) # LED vàng - điều khiển theo độ ẩm

# Biến trạng thái LED
led_red_state = False
led_yellow_state = False

def thingspeak_mqtt(temp, humi, led_yellow_status, led_red_status):
    """Gửi dữ liệu nhiệt độ, độ ẩm và trạng thái LED lên ThingSpeak qua MQTT"""
    Channel_ID = "3153408"
    # Field1: Nhiệt độ, Field2: Độ ẩm, Field3: LED vàng, Field4: LED đỏ
    client.publish("channels/%s/publish" % (Channel_ID),
                   "field1=%s&field2=%s&field3=%s&field4=%s&status=MQTTPUBLISH" 
                   % (temp, humi, led_yellow_status, led_red_status))

def control_leds(temp, humi):
    """Điều khiển LED dựa trên nhiệt độ và độ ẩm"""
    global led_red_state, led_yellow_state
    
    # Điều khiển LED đỏ theo nhiệt độ
    if temp > 30:
        if not led_red_state:
            led_red.on()
            led_red_state = True
            print("LED ĐỎ: BẬT (Nhiệt độ > 30°C)")
    elif temp < 25:
        if led_red_state:
            led_red.off()
            led_red_state = False
            print("LED ĐỎ: TẮT (Nhiệt độ < 25°C)")
    
    # Điều khiển LED vàng theo độ ẩm
    if humi > 60:
        if not led_yellow_state:
            led_yellow.on()
            led_yellow_state = True
            print("LED VÀNG: BẬT (Độ ẩm > 60%)")
    elif humi < 30:
        if led_yellow_state:
            led_yellow.off()
            led_yellow_state = False
            print("LED VÀNG: TẮT (Độ ẩm < 30%)")

def display_on_lcd(temp, humi):
    """Hiển thị nhiệt độ và độ ẩm lên LCD 16x2"""
    lcd.setCursor(0, 0)
    lcd.write('Temp: {0:2}C      '.format(temp))
    
    lcd.setCursor(1, 0)
    lcd.write('Humi: {0:2}%      '.format(humi))

def main():
    """Chương trình chính"""
    print("=== HỆ THỐNG GIÁM SÁT NHIỆT ĐỘ VÀ ĐỘ ẨM ===")
    print("Đang khởi động...")
    
    try:
        while True:
            # Đọc dữ liệu từ cảm biến DHT11
            humi, temp = sensor.read()
            
            # Hiển thị lên Terminal
            print("\n" + "="*50)
            print("Nhiệt độ: {0}°C | Độ ẩm: {1}%".format(temp, humi))
            
            # Hiển thị lên LCD 16x2
            display_on_lcd(temp, humi)
            
            # Điều khiển LED dựa trên ngưỡng
            control_leds(temp, humi)
            
            # Gửi dữ liệu lên ThingSpeak qua MQTT (1=ON, 0=OFF)
            led_yellow_status = 1 if led_yellow_state else 0
            led_red_status = 1 if led_red_state else 0
            thingspeak_mqtt(temp, humi, led_yellow_status, led_red_status)
            print("Đã gửi dữ liệu lên ThingSpeak")
            print("="*50)
            
            # Chờ 10 giây trước khi đọc lần tiếp theo
            sleep(10)
            
    except KeyboardInterrupt:
        print("\n\nĐang tắt hệ thống...")
        led_red.off()
        led_yellow.off()
        lcd.clear()
        client.disconnect()
        print("Hệ thống đã tắt.")

if __name__ == '__main__':
    main()