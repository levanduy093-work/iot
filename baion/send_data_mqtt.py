# ---- Thingspeak MQTT (paho-mqtt 2.x) ----
import paho.mqtt.client as mqtt
from time import sleep, time
from seeed_dht import DHT

# Channel ID: 3127848
# Author: mwa0000039454674
CLIENT_ID = "IQYGJxEjIxMmMxAzJSw1ISs"
USERNAME  = "IQYGJxEjIxMmMxAzJSw1ISs"
PASSWORD  = "aMJjEGryTWE/mhhIDZB7SKLD"
CHANNEL_ID = "3127848"

# Quan trọng: dùng keyword client_id=... (không truyền positional)
client = mqtt.Client(client_id=CLIENT_ID)
client.username_pw_set(username=USERNAME, password=PASSWORD)

# Thingspeak MQTT3 (TCP 1883). Nếu dùng TLS: port 8883 + client.tls_set()
client.connect("mqtt3.thingspeak.com", 1883, 60)

def thingspeak_mqtt(temp, humi):
    client.publish(f"channels/{CHANNEL_ID}/publish", f"field3={temp}&field4={humi}&status=MQTTPUBLISH")

def main():
    # Grove - Temperature & Humidity Sensor connected to port D5
    sensor = DHT('11', 5)
    
    print("Bắt đầu gửi dữ liệu lên ThingSpeak qua MQTT...")
    print("Nhấn Ctrl+C để dừng chương trình")
    
    while True:
        temp_list = []
        humi_list = []
        
        # Thu thập dữ liệu trong 20 giây
        print("\n--- Thu thập dữ liệu trong 20 giây ---")
        collect_start = time()
        
        while time() - collect_start < 20:
            try:
                humi, temp = sensor.read()
                
                # Kiểm tra giá trị hợp lệ
                if temp is not None and humi is not None:
                    if 0 <= temp <= 50 and 0 <= humi <= 100:
                        temp_list.append(temp)
                        humi_list.append(humi)
                        print(f'Đọc: Nhiệt độ {temp}°C, Độ ẩm {humi}%')
                    else:
                        print(f'Giá trị không hợp lệ: Nhiệt độ {temp}°C, Độ ẩm {humi}%')
                else:
                    print('Lỗi đọc cảm biến')
                    
            except Exception as e:
                print(f'Lỗi: {e}')
            
            sleep(1)
        
        # Tính giá trị trung bình
        if len(temp_list) > 0 and len(humi_list) > 0:
            avg_temp = sum(temp_list) / len(temp_list)
            avg_humi = sum(humi_list) / len(humi_list)
            
            print(f'\n--- Giá trị trung bình ---')
            print(f'Nhiệt độ TB: {avg_temp:.2f}°C')
            print(f'Độ ẩm TB: {avg_humi:.2f}%')
            print(f'Số mẫu hợp lệ: {len(temp_list)}')
            
            # Gửi dữ liệu lên ThingSpeak
            print(f'Đang gửi qua MQTT: Temp={avg_temp:.2f}, Humi={avg_humi:.2f}')
            thingspeak_mqtt(avg_temp, avg_humi)
            print(f'Đã gửi dữ liệu qua MQTT')
        else:
            print('\nKhông có dữ liệu hợp lệ để gửi')

if __name__ == '__main__':
    main()
