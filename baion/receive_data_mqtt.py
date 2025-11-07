# ========================================
# CHƯƠNG TRÌNH ĐỌC DỮ LIỆU TỪ THINGSPEAK QUA MQTT
# Đọc nhiệt độ và độ ẩm trung bình từ Channel 3127848
# Hiển thị ra Terminal và ghi Log vào file CSV
# ========================================

import paho.mqtt.client as mqtt
from time import sleep
from datetime import datetime
import csv
import os

# === THÔNG TIN KÊNH THINGSPEAK ===
# Channel ID: 3127848
CLIENT_ID = "Dg0MFSkPJAIJMgchHjw1BwY"
USERNAME  = "Dg0MFSkPJAIJMgchHjw1BwY"
PASSWORD  = "8p9YF6bT68Hxjny5ChF13Vrm"
CHANNEL_ID = "3127848"
READ_API_KEY = "N251PNZ5EG0MWI2Y"

# Tên file log
LOG_FILE = "receive_mqtt_log.csv"

# Biến toàn cục để lưu giá trị nhiệt độ và độ ẩm
current_temp = None
current_humi = None
last_log_time = 0  # Để tránh ghi log quá nhiều

# ========================================
# HÀM GHI LOG VÀO FILE CSV
# ========================================
def write_log(timestamp, temp, humi, event):
    """
    Ghi log vào file CSV
    timestamp: Thời gian sự kiện
    temp: Nhiệt độ
    humi: Độ ẩm
    event: Mô tả sự kiện
    """
    # Kiểm tra xem file đã tồn tại chưa
    file_exists = os.path.isfile(LOG_FILE)
    
    # Mở file ở chế độ append (thêm vào cuối file)
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Thời gian', 'Nhiệt độ (°C)', 'Độ ẩm (%)', 'Sự kiện']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Nếu file chưa tồn tại, ghi header
        if not file_exists:
            writer.writeheader()
        
        # Ghi dữ liệu
        writer.writerow({
            'Thời gian': timestamp,
            'Nhiệt độ (°C)': temp if temp else 'N/A',
            'Độ ẩm (%)': humi if humi else 'N/A',
            'Sự kiện': event
        })

# ========================================
# HÀM CALLBACK KHI KẾT NỐI THÀNH CÔNG
# ========================================
def on_connect(client, userdata, flags, rc):
    """
    Callback được gọi khi kết nối đến MQTT broker
    rc: Return code (0 = thành công)
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if rc == 0:
        print(f"[{timestamp}] Đã kết nối đến ThingSpeak MQTT broker")
        write_log(timestamp, None, None, f"Kết nối MQTT thành công (code: {rc})")
        
        # Subscribe (đăng ký) nhận dữ liệu từ field3 và field4
        # Format: channels/<channelID>/subscribe/fields/field<N>/<READ_API_KEY>
        # Field3 = Nhiệt độ
        client.subscribe(f"channels/{CHANNEL_ID}/subscribe/fields/field3/{READ_API_KEY}")
        print(f"[{timestamp}] Đã subscribe field3 (Nhiệt độ)")
        
        # Field4 = Độ ẩm
        client.subscribe(f"channels/{CHANNEL_ID}/subscribe/fields/field4/{READ_API_KEY}")
        print(f"[{timestamp}] Đã subscribe field4 (Độ ẩm)")
    else:
        print(f"[{timestamp}] Kết nối thất bại với code: {rc}")
        write_log(timestamp, None, None, f"Kết nối MQTT thất bại (code: {rc})")

# ========================================
# HÀM CALLBACK KHI MẤT KẾT NỐI
# ========================================
def on_disconnect(client, userdata, rc):
    """
    Callback được gọi khi mất kết nối với MQTT broker
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] Mất kết nối với MQTT broker")
    write_log(timestamp, None, None, f"Mất kết nối MQTT (code: {rc})")

# ========================================
# HÀM CALLBACK KHI NHẬN ĐƯỢC MESSAGE
# ========================================
def on_message(client, userdata, message):
    """
    Callback được gọi khi nhận được message từ topic đã subscribe
    message: Chứa payload (dữ liệu) và topic
    """
    global current_temp, current_humi, last_log_time
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Lấy giá trị từ message
    value = message.payload.decode()
    topic = message.topic
    
    # Xác định xem message từ field nào
    if 'field3' in topic:
        # Field3 = Nhiệt độ
        current_temp = value
        print(f"[{timestamp}] Nhận Nhiệt độ: {value}°C")
    elif 'field4' in topic:
        # Field4 = Độ ẩm
        current_humi = value
        print(f"[{timestamp}] Nhận Độ ẩm: {value}%")
    
    # Ghi log mỗi khi nhận dữ liệu (không cần chờ cả 2 field)
    import time
    current_time = time.time()
    if current_time - last_log_time >= 1:  # Ghi log mỗi giây một lần
        write_log(timestamp, current_temp, current_humi, "Nhận dữ liệu MQTT")
        last_log_time = current_time

# ========================================
# HÀM CHÍNH - MAIN PROGRAM
# ========================================
def main():
    global last_log_time
    import time
    last_log_time = time.time()
    
    print("=" * 70)
    print("BẮT ĐẦU ĐỌC DỮ LIỆU TỪ THINGSPEAK QUA MQTT")
    print(f"Channel ID: {CHANNEL_ID}")
    print(f"File log: {LOG_FILE}")
    print("Nhấn Ctrl+C để dừng chương trình")
    print("=" * 70)
    
    # Ghi log khởi động chương trình
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_log(timestamp, None, None, "Khởi động chương trình đọc dữ liệu MQTT")
    
    # Tạo MQTT client
    client = mqtt.Client(client_id=CLIENT_ID)
    
    # Đăng ký các callback functions
    client.on_connect = on_connect       # Được gọi khi kết nối thành công
    client.on_disconnect = on_disconnect # Được gọi khi mất kết nối
    client.on_message = on_message       # Được gọi khi nhận message
    
    # Đặt username và password
    client.username_pw_set(username=USERNAME, password=PASSWORD)
    
    try:
        # Kết nối đến ThingSpeak MQTT broker
        client.connect("mqtt3.thingspeak.com", 1883, 60)
        
        # Chạy vòng lặp để nhận message liên tục
        # loop_forever() sẽ chặn chương trình và tự động xử lý kết nối
        client.loop_forever()
        
    except KeyboardInterrupt:
        # Khi người dùng nhấn Ctrl+C
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("\n" + "=" * 70)
        print("Đang ngắt kết nối...")
        
        # Ngắt kết nối MQTT
        client.disconnect()
        
        print("Đã dừng chương trình")
        print("=" * 70)
        
        # Ghi log dừng chương trình
        write_log(timestamp, None, None, "Dừng chương trình")
    
    except Exception as e:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] Lỗi: {e}")
        write_log(timestamp, None, None, f"Lỗi: {e}")

# ========================================
# CHẠY CHƯƠNG TRÌNH
# ========================================
if __name__ == '__main__':
    main()
