# ========================================
# GỬI DỮ LIỆU DHT11 LÊN THINGSPEAK
# - HTTP (channel cũ):  field1 = temperature_http, field2 = humidity_http
# - MQTT (channel mới): field1 = temperature_mqtt, field2 = humidity_mqtt
# ========================================

from urllib import request, parse
import paho.mqtt.client as mqtt
from time import sleep, time
from seeed_dht import DHT

# ===== HTTP (giữ nguyên channel cũ) =====
CHANNEL_ID_HTTP     = "3127848"               # chỉ để log; HTTP xác định bằng WRITE_API_KEY
WRITE_API_KEY_HTTP  = "AHHO5UL59ZCYUYCV"      # API key channel cũ

# ===== MQTT (đưa sang channel MỚI) =====
CHANNEL_ID_MQTT = "3153408"  # MQTT_Data_Server (channel mới của bạn)

# --- Dùng MQTT Device Credentials (như CŨ) ---
CLIENT_ID_MQTT = "Dg0MFSkPJAIJMgchHjw1BwY"
USERNAME_MQTT  = "Dg0MFSkPJAIJMgchHjw1BwY"
PASSWORD_MQTT  = "8p9YF6bT68Hxjny5ChF13Vrm"

MQTT_HOST = "mqtt3.thingspeak.com"
MQTT_PORT = 1883           # dùng 8883 nếu muốn TLS
MQTT_KEEPALIVE = 60
MQTT_TOPIC = f"channels/{CHANNEL_ID_MQTT}/publish"  # dùng device credentials -> KHÔNG cần api_key

# ========================================
# MQTT callbacks
# ========================================
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✓ MQTT connected")
    else:
        print(f"✗ MQTT connect failed (rc={rc})")

def on_publish(client, userdata, mid):
    print(f"  → MQTT published MID={mid}")

# Khởi tạo MQTT client riêng cho channel MQTT mới
mqtt_client = mqtt.Client(client_id=CLIENT_ID_MQTT)
mqtt_client.username_pw_set(username=USERNAME_MQTT, password=PASSWORD_MQTT)
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish

# Nếu muốn TLS:
# mqtt_client.tls_set()        # bật TLS
# MQTT_PORT = 8883

mqtt_client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)
mqtt_client.loop_start()

# ========================================
# HTTP helpers (vẫn đẩy lên channel HTTP cũ)
# ========================================
def make_param_thingspeak_http(temp, humi):
    """
    Tạo payload cho HTTP update channel cũ:
      field1 = temp, field2 = humi
    """
    params = parse.urlencode({'field1': temp, 'field2': humi}).encode()
    return params

def thingspeak_post_http(params):
    """
    POST dữ liệu lên ThingSpeak bằng HTTP (channel cũ).
    """
    req = request.Request('https://api.thingspeak.com/update', method="POST")
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('X-THINGSPEAKAPIKEY', WRITE_API_KEY_HTTP)
    with request.urlopen(req, data=params, timeout=10) as r:
        return r.read()

# ========================================
# MQTT publish (đẩy lên channel MQTT mới, field1/field2)
# ========================================
def thingspeak_post_mqtt(temp, humi):
    """
    Publish dữ liệu lên channel MQTT mới:
      field1 = temp, field2 = humi (cùng một message)
    """
    payload = f"field1={temp}&field2={humi}&status=MQTTPUBLISH"
    # QoS=1 đảm bảo broker nhận ít nhất một lần
    return mqtt_client.publish(MQTT_TOPIC, payload, qos=1)

# ========================================
# MAIN
# ========================================
def main():
    # Cảm biến DHT11 trên Grove Base Hat, cổng D5 → GPIO 5
    sensor = DHT('11', 5)

    print("=" * 74)
    print("HTTP → Channel cũ (field1, field2)")
    print(f"  CHANNEL_ID_HTTP  = {CHANNEL_ID_HTTP}")
    print("MQTT → Channel MỚI (field1, field2)")
    print(f"  CHANNEL_ID_MQTT  = {CHANNEL_ID_MQTT}")
    print("Nhấn Ctrl+C để dừng chương trình")
    print("=" * 74)

    while True:
        temp_list, humi_list = [], []

        print("\n--- Thu thập dữ liệu trong 20 giây ---")
        t0 = time()
        while time() - t0 < 20:
            try:
                humi, temp = sensor.read()  # humi = %, temp = °C
                if temp is not None and humi is not None and 0 <= temp <= 50 and 0 <= humi <= 100:
                    temp_list.append(temp)
                    humi_list.append(humi)
                    print(f"Đọc: Temp {temp}°C | Humi {humi}%")
                else:
                    print("Giá trị không hợp lệ hoặc lỗi cảm biến")
            except Exception as e:
                print(f"Lỗi đọc cảm biến: {e}")
            sleep(1)

        if temp_list and humi_list:
            avg_temp = sum(temp_list) / len(temp_list)
            avg_humi = sum(humi_list) / len(humi_list)

            print("\n--- Giá trị trung bình ---")
            print(f"Nhiệt độ TB: {avg_temp:.2f}°C")
            print(f"Độ ẩm TB:   {avg_humi:.2f}%")
            print(f"Số mẫu hợp lệ: {len(temp_list)}")

            # ===== 1) Gửi qua HTTP (channel cũ: field1, field2)
            try:
                resp = thingspeak_post_http(make_param_thingspeak_http(avg_temp, avg_humi))
                print(f"✓ HTTP update (f1,f2) → channel {CHANNEL_ID_HTTP}: {resp.decode().strip()}")
            except Exception as e:
                print(f"✗ HTTP error: {e}")

            # ===== 2) Gửi qua MQTT (channel MỚI: field1, field2)
            try:
                mqtt_result = thingspeak_post_mqtt(avg_temp, avg_humi)
                if mqtt_result.rc == mqtt.MQTT_ERR_SUCCESS:
                    print(f"✓ MQTT update (f1,f2) → channel {CHANNEL_ID_MQTT} — MID: {mqtt_result.mid}")
                else:
                    print(f"✗ MQTT publish error — rc: {mqtt_result.rc}")
            except Exception as e:
                print(f"✗ MQTT error: {e}")

            # Cho MQTT loop xử lý xong nếu còn queue
            sleep(2)
        else:
            print("\nKhông có dữ liệu hợp lệ để gửi")

# ========================================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nChương trình đã dừng")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print("Đã ngắt kết nối MQTT")