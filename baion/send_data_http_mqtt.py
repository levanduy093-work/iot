# ========================================
# CHƯƠNG TRÌNH GỬI DỮ LIỆU DHT11 LÊN THINGSPEAK
# Sử dụng đồng thời cả HTTP và MQTT
# ========================================

from urllib import request, parse  # Thư viện để gửi HTTP request
import paho.mqtt.client as mqtt    # Thư viện MQTT để gửi dữ liệu qua MQTT
from time import sleep, time       # Hàm sleep để delay, time để tính thời gian
from seeed_dht import DHT          # Thư viện đọc cảm biến DHT11

# === THÔNG TIN KÊNH THINGSPEAK ===
# Channel ID: 3127848 (Test_Data_Server)
# Author: mwa0000039454674
# Gửi cả HTTP và MQTT vào cùng 1 channel:
# - HTTP: field1 (temperature_http), field2 (humidity_http)
# - MQTT: field3 (temperature_mqtt), field4 (humidity_mqtt)
# API Key (Write): AHHO5UL59ZCYUYCV
# API Key (Read): N251PNZ5EG0MWI2Y

# MQTT credentials
CLIENT_ID = "IQYGJxEjIxMmMxAzJSw1ISs"  # ID client MQTT
USERNAME  = "IQYGJxEjIxMmMxAzJSw1ISs"  # Username để xác thực MQTT
PASSWORD  = "aMJjEGryTWE/mhhIDZB7SKLD"  # Password để xác thực MQTT
CHANNEL_ID = "3127848"                   # ID kênh ThingSpeak

# Khởi tạo và cấu hình MQTT client
client = mqtt.Client(client_id=CLIENT_ID)                    # Tạo MQTT client với CLIENT_ID
client.username_pw_set(username=USERNAME, password=PASSWORD) # Đặt username và password
client.connect("mqtt3.thingspeak.com", 1883, 60)            # Kết nối đến ThingSpeak MQTT (port 1883, timeout 60s)

# ========================================
# HÀM TẠO THAM SỐ CHO HTTP REQUEST
# ========================================
def make_param_thingspeak(temp, humi):
    """
    Tạo tham số để gửi qua HTTP
    temp: Giá trị nhiệt độ trung bình
    humi: Giá trị độ ẩm trung bình
    Trả về: Dữ liệu đã encode sẵn để gửi (field1=temp, field2=humi)
    """
    params = parse.urlencode({'field1': temp, 'field2': humi}).encode()
    return params

# ========================================
# HÀM GỬI DỮ LIỆU QUA HTTP
# ========================================
def thingspeak_post_http(params):
    """
    Gửi dữ liệu lên ThingSpeak qua giao thức HTTP
    params: Tham số đã được encode (từ hàm make_param_thingspeak)
    Trả về: Response từ server ThingSpeak
    """
    api_key_write = "AHHO5UL59ZCYUYCV"  # API Key để xác thực ghi dữ liệu
    
    # Tạo HTTP POST request đến ThingSpeak
    req = request.Request('https://api.thingspeak.com/update', method="POST")
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')  # Định dạng dữ liệu gửi lên
    req.add_header('X-THINGSPEAKAPIKEY', api_key_write)                  # Header chứa API Key
    
    # Gửi request và nhận response
    r = request.urlopen(req, data=params)
    response_data = r.read()
    return response_data

# ========================================
# HÀM GỬI DỮ LIỆU QUA MQTT
# ========================================
def thingspeak_post_mqtt(temp, humi):
    """
    Gửi dữ liệu lên ThingSpeak qua giao thức MQTT
    temp: Giá trị nhiệt độ trung bình
    humi: Giá trị độ ẩm trung bình
    Gửi vào field3 và field4
    """
    # Publish dữ liệu lên topic của ThingSpeak
    # Format: field3=temp&field4=humi&status=MQTTPUBLISH
    client.publish(f"channels/{CHANNEL_ID}/publish", f"field3={temp}&field4={humi}&status=MQTTPUBLISH")

# ========================================
# HÀM CHÍNH - MAIN PROGRAM
# ========================================
def main():
    # Khởi tạo cảm biến DHT11 kết nối với cổng D5 của Grove Base Hat
    # '11' = DHT11, 5 = GPIO pin 5 (D5)
    sensor = DHT('11', 5)
    
    print("=" * 60)
    print("Bắt đầu gửi dữ liệu lên ThingSpeak qua HTTP và MQTT...")
    print("Nhấn Ctrl+C để dừng chương trình")
    print("=" * 60)
    
    # Vòng lặp vô hạn - chạy liên tục cho đến khi người dùng dừng (Ctrl+C)
    while True:
        # Khởi tạo 2 danh sách để lưu các giá trị đọc được trong 20 giây
        temp_list = []  # Danh sách lưu nhiệt độ
        humi_list = []  # Danh sách lưu độ ẩm
        
        # ========================================
        # BƯỚC 1: THU THẬP DỮ LIỆU TRONG 20 GIÂY
        # ========================================
        print("\n--- Thu thập dữ liệu trong 20 giây ---")
        collect_start = time()  # Lưu thời điểm bắt đầu thu thập
        
        # Đọc cảm biến mỗi 1 giây trong 20 giây
        while time() - collect_start < 20:
            try:
                # Đọc giá trị từ cảm biến DHT11
                humi, temp = sensor.read()  # humi = độ ẩm, temp = nhiệt độ
                
                # Kiểm tra xem giá trị có hợp lệ không
                if temp is not None and humi is not None:
                    # Kiểm tra giá trị trong phạm vi cho phép
                    # Nhiệt độ: 0-50°C, Độ ẩm: 0-100%
                    if 0 <= temp <= 50 and 0 <= humi <= 100:
                        # Giá trị hợp lệ -> Thêm vào danh sách
                        temp_list.append(temp)
                        humi_list.append(humi)
                        print(f'Đọc: Nhiệt độ {temp}°C, Độ ẩm {humi}%')
                    else:
                        # Giá trị ngoài phạm vi cho phép
                        print(f'Giá trị không hợp lệ: Nhiệt độ {temp}°C, Độ ẩm {humi}%')
                else:
                    # Giá trị None -> Lỗi đọc cảm biến
                    print('Lỗi đọc cảm biến')
                    
            except Exception as e:
                # Bắt các lỗi khác (nếu có)
                print(f'Lỗi: {e}')
            
            # Chờ 1 giây trước khi đọc tiếp
            sleep(1)
        
        # ========================================
        # BƯỚC 2: TÍNH TOÁN GIÁ TRỊ TRUNG BÌNH
        # ========================================
        # Kiểm tra xem có dữ liệu hợp lệ không
        if len(temp_list) > 0 and len(humi_list) > 0:
            # Tính trung bình cộng của nhiệt độ và độ ẩm
            avg_temp = sum(temp_list) / len(temp_list)
            avg_humi = sum(humi_list) / len(humi_list)
            
            print(f'\n--- Giá trị trung bình ---')
            print(f'Nhiệt độ TB: {avg_temp:.2f}°C')
            print(f'Độ ẩm TB: {avg_humi:.2f}%')
            print(f'Số mẫu hợp lệ: {len(temp_list)}')
            
            # ========================================
            # BƯỚC 3: GỬI DỮ LIỆU LÊN THINGSPEAK
            # ========================================
            
            # 3.1: Gửi qua HTTP (vào field1, field2 của Channel 3142608)
            params_thingspeak = make_param_thingspeak(avg_temp, avg_humi)
            response = thingspeak_post_http(params_thingspeak)
            print(f'✓ Đã gửi qua HTTP (field1, field2). Response: {response.decode()}')
            
            # 3.2: Gửi qua MQTT (vào field3, field4 của Channel 3127848)
            thingspeak_post_mqtt(avg_temp, avg_humi)
            print(f'✓ Đã gửi qua MQTT (field3, field4)')
        else:
            # Không có dữ liệu hợp lệ nào
            print('\nKhông có dữ liệu hợp lệ để gửi')
        
        # Sau khi gửi xong, vòng lặp sẽ bắt đầu lại chu kỳ 20 giây mới

# ========================================
# CHẠY CHƯƠNG TRÌNH
# ========================================
if __name__ == '__main__':
    main()
