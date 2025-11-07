# ========================================
# CHƯƠNG TRÌNH ĐỌC DỮ LIỆU TỪ THINGSPEAK QUA HTTP
# Đọc nhiệt độ và độ ẩm trung bình từ Channel 3127848
# Hiển thị ra Terminal và ghi Log vào file CSV
# ========================================

from urllib import request
from time import sleep
from datetime import datetime
import json
import csv
import os

# === THÔNG TIN KÊNH THINGSPEAK ===
# Channel ID: 3127848 (channel nhận dữ liệu từ chương trình 1)
# Author: mwa0000039454674
# API Key (Read): N251PNZ5EG0MWI2Y
API_KEY_READ = "N251PNZ5EG0MWI2Y"
CHANNEL_ID = "3127848"

# Tên file log
LOG_FILE = "receive_http_log.csv"

# ========================================
# HÀM ĐỌC DỮ LIỆU TỪ THINGSPEAK QUA HTTP
# ========================================
def thingspeak_get_latest():
    """
    Đọc dữ liệu mới nhất từ ThingSpeak qua HTTP
    Theo ThingSpeak channel 3127848:
    - field1: temperature_http (dữ liệu từ HTTP)
    - field2: humidity_http (dữ liệu từ HTTP)
    - field3: temperature_mqtt (dữ liệu từ MQTT)
    - field4: humidity_mqtt (dữ liệu từ MQTT)
    
    Chương trình này đọc field1, field2 (dữ liệu từ HTTP)
    Trả về: Dictionary chứa temperature (field1), humidity (field2), created_at
    """
    try:
        # Đọc từ Channel 3127848 - lấy 1 bản ghi mới nhất
        # API format: https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?results=1
        url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?results=1"
        
        # Channel này là public nên không cần API key
        
        req = request.Request(url, method="GET")
        with request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
        
        feeds = data.get("feeds", [])
        if not feeds:
            return None
        
        latest = feeds[0]
        created_at = latest.get("created_at")
        
        # Đọc field1 (temperature_http) và field2 (humidity_http)
        f1 = latest.get("field1")
        f2 = latest.get("field2")
        
        # Chuyển sang float
        def to_float(x):
            try:
                return float(x) if x is not None else None
            except Exception:
                return None
        
        temperature = to_float(f1)
        humidity = to_float(f2)
        
        return {
            "created_at": created_at,
            "temperature": temperature,
            "humidity": humidity,
        }
    except Exception as e:
        print(f'Lỗi khi đọc dữ liệu: {e}')
        return None

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
# HÀM CHÍNH - MAIN PROGRAM
# ========================================
def main():
    print("=" * 70)
    print("BẮT ĐẦU ĐỌC DỮ LIỆU TỪ THINGSPEAK QUA HTTP")
    print(f"Channel ID: {CHANNEL_ID}")
    print(f"File log: {LOG_FILE}")
    print("Nhấn Ctrl+C để dừng chương trình")
    print("=" * 70)
    
    # Ghi log khởi động chương trình
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_log(timestamp, None, None, "Khởi động chương trình đọc dữ liệu HTTP")
    
    # Vòng lặp vô hạn - đọc dữ liệu mỗi 1 giây
    try:
        while True:
            # Lấy thời gian hiện tại
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Đọc dữ liệu mới nhất
            latest = thingspeak_get_latest()
            
            if latest is None:
                print(f'[{timestamp}] Chưa có dữ liệu (feeds trống)')
                write_log(timestamp, None, None, "Chưa có dữ liệu")
            else:
                temp = latest["temperature"]
                humi = latest["humidity"]
                ts_utc = latest["created_at"]
                
                # Hiển thị ra Terminal
                if temp is not None and humi is not None:
                    print(f'[{timestamp}] Nhiệt độ: {temp:.2f}°C | Độ ẩm: {humi:.2f}%')
                    write_log(timestamp, temp, humi, "Đọc dữ liệu thành công")
                elif temp is not None:
                    print(f'[{timestamp}] Nhiệt độ: {temp:.2f}°C | Độ ẩm: N/A')
                    write_log(timestamp, temp, None, "Chỉ có nhiệt độ")
                elif humi is not None:
                    print(f'[{timestamp}] Nhiệt độ: N/A | Độ ẩm: {humi:.2f}%')
                    write_log(timestamp, None, humi, "Chỉ có độ ẩm")
                else:
                    print(f'[{timestamp}] Không có field hợp lệ')
                    write_log(timestamp, None, None, "Không có field hợp lệ")
            
            # Chờ 1 giây trước khi đọc tiếp
            sleep(1)
            
    except KeyboardInterrupt:
        # Khi người dùng nhấn Ctrl+C
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("\n" + "=" * 70)
        print("Đã dừng chương trình")
        print("=" * 70)
        
        # Ghi log dừng chương trình
        write_log(timestamp, None, None, "Dừng chương trình")

# ========================================
# CHẠY CHƯƠNG TRÌNH
# ========================================
if __name__ == '__main__':
    main()
