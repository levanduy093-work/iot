# ========================================
# CHƯƠNG TRÌNH ĐỌC DỮ LIỆU TỪ THINGSPEAK QUA HTTP
# Đọc nhiệt độ và độ ẩm trung bình từ Channel 3127848
# Hiển thị ra Terminal và ghi Log vào file CSV
# - In mỗi 1 giây (nếu chưa có bản ghi mới thì in lại giá trị cũ)
# - Căn thời gian để đúng chu kỳ 1.0s
# ========================================

from urllib import request
from time import sleep, time
from datetime import datetime
import json
import csv
import os

# === THÔNG TIN KÊNH THINGSPEAK ===
API_KEY_READ = "N251PNZ5EG0MWI2Y"   # channel này public nên có thể không cần
CHANNEL_ID = "3127848"

# Tên file log
LOG_FILE = "receive_http_log.csv"

# Lưu giá trị gần nhất (để lặp lại khi chưa có bản ghi mới)
last_temp = None
last_humi = None
last_entry_id = None  # dùng để phát hiện bản ghi mới

# ========================================
# HÀM ĐỌC DỮ LIỆU TỪ THINGSPEAK QUA HTTP
# ========================================
def thingspeak_get_latest():
    """
    Đọc 1 bản ghi mới nhất từ ThingSpeak qua HTTP
    - field1: temperature_http
    - field2: humidity_http
    Trả về: dict {entry_id, created_at, temperature, humidity} hoặc None
    """
    try:
        # public: không cần api_key; nếu private: thêm ?api_key=...
        url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?results=1"
        # url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={API_KEY_READ}&results=1"

        with request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read().decode())

        feeds = data.get("feeds", [])
        if not feeds:
            return None

        latest = feeds[0]
        created_at = latest.get("created_at")
        entry_id = latest.get("entry_id")

        def to_float(x):
            try:
                return float(x) if x is not None else None
            except Exception:
                return None

        temperature = to_float(latest.get("field1"))
        humidity    = to_float(latest.get("field2"))

        return {
            "entry_id": entry_id,
            "created_at": created_at,
            "temperature": temperature,
            "humidity": humidity,
        }
    except Exception as e:
        # Có thể log lỗi nếu muốn
        # print(f'Lỗi khi đọc dữ liệu: {e}')
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
    file_exists = os.path.isfile(LOG_FILE)

    def fmt(x):
        try:
            return f"{float(x):.2f}"
        except Exception:
            return 'N/A' if x is None else str(x)

    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Thời gian', 'Nhiệt độ (°C)', 'Độ ẩm (%)', 'Sự kiện']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'Thời gian': timestamp,
            'Nhiệt độ (°C)': fmt(temp),
            'Độ ẩm (%)': fmt(humi),
            'Sự kiện': event
        })

# ========================================
# HÀM CHÍNH - MAIN PROGRAM
# ========================================
def main():
    global last_temp, last_humi, last_entry_id

    print("=" * 70)
    print("BẮT ĐẦU ĐỌC DỮ LIỆU TỪ THINGSPEAK QUA HTTP")
    print(f"Channel ID: {CHANNEL_ID}")
    print(f"File log: {LOG_FILE}")
    print("Nhấn Ctrl+C để dừng chương trình")
    print("=" * 70)

    # Ghi log khởi động chương trình
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_log(timestamp, None, None, "Khởi động chương trình đọc dữ liệu HTTP")

    # Vòng lặp vô hạn - đọc dữ liệu mỗi 1 giây (đúng chu kỳ)
    try:
        while True:
            loop_start = time()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            latest = thingspeak_get_latest()

            if latest is not None and latest.get("entry_id") is not None:
                # Nếu có bản ghi mới, cập nhật bộ nhớ
                if latest["entry_id"] != last_entry_id:
                    last_entry_id = latest["entry_id"]
                    last_temp = latest["temperature"]
                    last_humi = latest["humidity"]

            # In ra (luôn, mỗi 1 giây) — dùng giá trị cũ nếu chưa có bản mới
            if last_temp is not None and last_humi is not None:
                print(f'[{timestamp}] Nhiệt độ: {last_temp:.2f}°C | Độ ẩm: {last_humi:.2f}%')
                write_log(timestamp, last_temp, last_humi, "Hiển thị mỗi 1 giây")
            elif last_temp is not None:
                print(f'[{timestamp}] Nhiệt độ: {last_temp:.2f}°C | Độ ẩm: N/A')
                write_log(timestamp, last_temp, None, "Hiển thị mỗi 1 giây")
            elif last_humi is not None:
                print(f'[{timestamp}] Nhiệt độ: N/A | Độ ẩm: {last_humi:.2f}%')
                write_log(timestamp, None, last_humi, "Hiển thị mỗi 1 giây")
            else:
                print(f'[{timestamp}] Chưa có dữ liệu')
                write_log(timestamp, None, None, "Chưa có dữ liệu")

            # Căn thời gian để đúng 1.0 giây mỗi vòng
            elapsed = time() - loop_start
            if elapsed < 1.0:
                sleep(1.0 - elapsed)

    except KeyboardInterrupt:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("\n" + "=" * 70)
        print("Đã dừng chương trình")
        print("=" * 70)
        write_log(timestamp, None, None, "Dừng chương trình")

# ========================================
# CHẠY CHƯƠNG TRÌNH
# ========================================
if __name__ == '__main__':
    main()