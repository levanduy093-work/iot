# ========================================
# THINGSPEAK MQTT SUBSCRIBER (LOG CSV + IN TERMINAL)
# - Channel: 3153408 (field1: temperature, field2: humidity)
# - Credentials: IRU6PSACOwQPHy4PKiczCiI / gHzqnX35vjOPS0jeNUVtBdfV
# ========================================

import paho.mqtt.client as mqtt
from datetime import datetime
from time import sleep
import csv
import os

# ===== CẤU HÌNH KÊNH & THIẾT BỊ =====
CHANNEL_ID = "3153408"  # Đổi thành "3127848" nếu muốn nghe channel cũ

USERNAME   = "IRU6PSACOwQPHy4PKiczCiI"
CLIENT_ID  = "IRU6PSACOwQPHy4PKiczCiI"
PASSWORD   = "gHzqnX35vjOPS0jeNUVtBdfV"

MQTT_HOST  = "mqtt3.thingspeak.com"
MQTT_PORT  = 1883           # Dùng 8883 + client.tls_set() nếu muốn TLS
KEEPALIVE  = 60

# ===== FILE LOG =====
LOG_FILE = "receive_mqtt_log.csv"

# ===== Biến ghép cặp =====
current_temp = None   # field1
current_humi = None   # field2
last_pair_time = None

# ========================================
# GHI LOG CSV
# ========================================
def write_log(timestamp, temp, humi, event):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['Thời gian', 'Nhiệt độ (°C)', 'Độ ẩm (%)', 'Sự kiện']
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            w.writeheader()
        w.writerow({
            'Thời gian': timestamp,
            'Nhiệt độ (°C)': f"{temp:.2f}" if isinstance(temp, (int, float)) else (temp if temp else 'N/A'),
            'Độ ẩm (%)': f"{humi:.2f}" if isinstance(humi, (int, float)) else (humi if humi else 'N/A'),
            'Sự kiện': event
        })

def now_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def to_float(x):
    try:
        return float(x) if x is not None else None
    except Exception:
        return None

# ========================================
# MQTT CALLBACKS
# ========================================
def on_connect(client, userdata, flags, rc):
    print("Connected with result code:", rc)
    # Đăng ký field1 & field2 của CHANNEL_ID
    client.subscribe(f"channels/{CHANNEL_ID}/subscribe/fields/field1", qos=1)
    client.subscribe(f"channels/{CHANNEL_ID}/subscribe/fields/field2", qos=1)

def on_disconnect(client, userdata, rc):
    print("Disconnected from broker")

def on_message(client, userdata, message):
    """
    Gom cặp field1/field2. Khi đủ -> in terminal + ghi CSV, rồi reset.
    """
    global current_temp, current_humi, last_pair_time

    value = message.payload.decode().strip()
    topic = message.topic

    if topic.endswith("field1"):
        current_temp = value
    elif topic.endswith("field2"):
        current_humi = value

    if current_temp is not None and current_humi is not None:
        ts = now_str()
        temp_f = to_float(current_temp)
        humi_f = to_float(current_humi)

        if temp_f is not None and humi_f is not None:
            print(f'[{ts}] Nhiệt độ: {temp_f:.2f}°C | Độ ẩm: {humi_f:.2f}%')
            write_log(ts, temp_f, humi_f, "Nhận cặp dữ liệu MQTT")
        elif temp_f is not None:
            print(f'[{ts}] Nhiệt độ: {temp_f:.2f}°C | Độ ẩm: N/A')
            write_log(ts, temp_f, None, "Chỉ có nhiệt độ (MQTT)")
        elif humi_f is not None:
            print(f'[{ts}] Nhiệt độ: N/A | Độ ẩm: {humi_f:.2f}%')
            write_log(ts, None, humi_f, "Chỉ có độ ẩm (MQTT)")
        else:
            print(f'[{ts}] Không có field hợp lệ (MQTT)')
            write_log(ts, None, None, "Không có field hợp lệ (MQTT)")

        current_temp = None
        current_humi = None
        last_pair_time = datetime.now()

# ========================================
# MAIN
# ========================================
def main():
    print("=" * 78)
    print("BẮT ĐẦU ĐỌC DỮ LIỆU TỪ THINGSPEAK QUA MQTT")
    print(f"Channel ID: {CHANNEL_ID}")
    print(f"File log: {LOG_FILE}")
    print("Nhấn Ctrl+C để dừng chương trình")
    print("=" * 78)

    write_log(now_str(), None, None, "Khởi động chương trình đọc dữ liệu MQTT")

    client = mqtt.Client(client_id=CLIENT_ID)
    client.username_pw_set(username=USERNAME, password=PASSWORD)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Bật TLS nếu cần:
    # client.tls_set()
    # MQTT_PORT = 8883

    client.connect(MQTT_HOST, MQTT_PORT, KEEPALIVE)

    client.loop_start()
    try:
        while True:
            # Mỗi giây, nếu chưa từng nhận cặp nào, in & log "Chưa có dữ liệu" (giống HTTP)
            if last_pair_time is None:
                ts = now_str()
                print(f'[{ts}] Chưa có dữ liệu (MQTT)')
                write_log(ts, None, None, "Chưa có dữ liệu")
            sleep(1)
    except KeyboardInterrupt:
        print("\n" + "=" * 78)
        print("Đã dừng chương trình")
        print("=" * 78)
        write_log(now_str(), None, None, "Dừng chương trình")
    finally:
        client.loop_stop()
        client.disconnect()

# ========================================
# RUN
# ========================================
if __name__ == "__main__":
    main()