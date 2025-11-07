# ========================================
# CHƯƠNG TRÌNH ĐỌC DỮ LIỆU TỪ THINGSPEAK QUA HTTP
# Đọc nhiệt độ và độ ẩm trung bình từ Channel 3142608
# Hiển thị ra Terminal và ghi Log vào file CSV
# ========================================

from urllib import request
from time import sleep
from datetime import datetime
import json
import csv
import os

# === THÔNG TIN KÊNH THINGSPEAK ===
# Channel ID: 3142608
# Author: mwa0000039454674
# API Key (Read): N251PNZ5EG0MWI2Y
API_KEY_READ = "N251PNZ5EG0MWI2Y"
CHANNEL_ID = "3142608"

# Tên file log
LOG_FILE = "baion/receive_http_log.csv"

# ========================================
# HÀM ĐỌC DỮ LIỆU TỪ THINGSPEAK QUA HTTP
# ========================================
def thingspeak_get_http(field_number):
    """
    Đọc dữ liệu từ ThingSpeak qua HTTP
    field_number: Số thứ tự field cần đọc (1 hoặc 2)
    Trả về: Giá trị của field hoặc None nếu lỗi
    """
    try:
        # Tạo URL để lấy dữ liệu mới nhất từ field
        url = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/fields/{field_number}/last.json?api_key={API_KEY_READ}'
        
        # Gửi GET request
        req = request.Request(url, method="GET")
        r = request.urlopen(req)
        response_data = r.read().decode()
        
        # Parse JSON response
        data = json.loads(response_data)
        value = data[f'field{field_number}']
        
        return value
    except Exception as e:
        print(f'Lỗi khi đọc field{field_number}: {e}')
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
            
            # Đọc nhiệt độ từ field1
            temp = thingspeak_get_http(1)
            
            # Đọc độ ẩm từ field2
            humi = thingspeak_get_http(2)
            
            # Hiển thị ra Terminal
            if temp is not None and humi is not None:
                print(f'[{timestamp}] Nhiệt độ: {temp}°C | Độ ẩm: {humi}%')
                
                # Ghi log thành công
                write_log(timestamp, temp, humi, "Đọc dữ liệu thành công")
            else:
                print(f'[{timestamp}] Không thể đọc dữ liệu')
                
                # Ghi log lỗi
                write_log(timestamp, temp, humi, "Lỗi đọc dữ liệu")
            
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
