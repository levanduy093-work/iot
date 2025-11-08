# ========================================
# MQTT SUBSCRIBER — IN & LOG MỖI 1 GIÂY (LẶP LẠI GIÁ TRỊ CŨ NẾU CHƯA CÓ DỮ LIỆU MỚI)
# ========================================

import paho.mqtt.client as mqtt
from datetime import datetime
from time import sleep
import csv, os

# ===== CẤU HÌNH KÊNH & THIẾT BỊ =====
CHANNEL_ID = "3153408"

USERNAME   = "IRU6PSACOwQPHy4PKiczCiI"
CLIENT_ID  = "IRU6PSACOwQPHy4PKiczCiI"
PASSWORD   = "gHzqnX35vjOPS0jeNUVtBdfV"

MQTT_HOST  = "mqtt3.thingspeak.com"
MQTT_PORT  = 1883
KEEPALIVE  = 60

LOG_FILE = "receive_mqtt_log.csv"

# Giá trị lưu trữ mới nhất
latest_temp = None
latest_humi = None

# Đánh dấu xem có dữ liệu mới hay không
new_data = False

def now_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def to_float(x):
    try:
        return float(x) if x is not None else None
    except:
        return None

def write_log(ts, temp, humi, event):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['Thời gian', 'Nhiệt độ (°C)', 'Độ ẩm (%)', 'Sự kiện']
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            w.writeheader()
        w.writerow({
            'Thời gian': ts,
            'Nhiệt độ (°C)': f"{temp:.2f}" if isinstance(temp, (int, float)) else 'N/A',
            'Độ ẩm (%)': f"{humi:.2f}" if isinstance(humi, (int, float)) else 'N/A',
            'Sự kiện': event
        })

# ===== MQTT callbacks =====
def on_connect(client, userdata, flags, rc):
    print("Connected with result code:", rc)
    client.subscribe(f"channels/{CHANNEL_ID}/subscribe/fields/field1", qos=1)
    client.subscribe(f"channels/{CHANNEL_ID}/subscribe/fields/field2", qos=1)

def on_message(client, userdata, message):
    global latest_temp, latest_humi, new_data

    val = message.payload.decode().strip()
    if message.topic.endswith("field1"):
        latest_temp = to_float(val)
        new_data = True
    elif message.topic.endswith("field2"):
        latest_humi = to_float(val)
        new_data = True

def main():
    global new_data

    print("=" * 78)
    print("ĐỌC DỮ LIỆU TỪ THINGSPEAK QUA MQTT — MỖI 1 GIÂY")
    print("Nếu không có dữ liệu mới ⇒ hiển thị lại dữ liệu cũ")
    print(f"Channel ID: {CHANNEL_ID}")
    print(f"File log: {LOG_FILE}")
    print("=" * 78)

    write_log(now_str(), None, None, "Khởi động chương trình MQTT")

    client = mqtt.Client(client_id=CLIENT_ID)
    client.username_pw_set(username=USERNAME, password=PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_HOST, MQTT_PORT, KEEPALIVE)
    client.loop_start()

    try:
        while True:
            ts = now_str()

            if latest_temp is None and latest_humi is None:
                # chưa từng có dữ liệu để hiển thị
                print(f"[{ts}] Chưa có dữ liệu")
                write_log(ts, None, None, "Chưa có dữ liệu")
            else:
                # có dữ liệu (mới hoặc cũ)
                temp = latest_temp
                humi = latest_humi

                print(f"[{ts}] Nhiệt độ: {temp:.2f}°C | Độ ẩm: {humi:.2f}%"
                      if temp is not None and humi is not None else
                      f"[{ts}] Nhiệt độ: {temp:.2f}°C | Độ ẩm: N/A"
                      if temp is not None else
                      f"[{ts}] Nhiệt độ: N/A | Độ ẩm: {humi:.2f}%")

                # log event: mới hay lặp lại
                if new_data:
                    write_log(ts, temp, humi, "Dữ liệu MỚI")
                    new_data = False
                else:
                    write_log(ts, temp, humi, "Lặp lại dữ liệu CŨ")

            sleep(1)

    except KeyboardInterrupt:
        print("\n" + "=" * 78)
        print("Đã dừng chương trình")
        print("=" * 78)
        write_log(now_str(), None, None, "Dừng chương trình")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()