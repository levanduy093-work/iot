# ========================================
# CHƯƠNG TRÌNH GỬI DỮ LIỆU DHT11 LÊN THINGSPEAK
# - HTTP: field1 (temperature_http), field2 (humidity_http)
# - MQTT: field3 (temperature_mqtt), field4 (humidity_mqtt)
# ========================================

from urllib import request, parse
import paho.mqtt.client as mqtt
from time import sleep, time
from seeed_dht import DHT

# ===== THÔNG TIN CHANNEL =====
CHANNEL_ID = "3127848"

# ===== API KEY (HTTP) =====
WRITE_API_KEY = "AHHO5UL59ZCYUYCV"   # dùng cho HTTP update

# ===== MQTT DEVICE (SENDER) – bạn cung cấp =====
CLIENT_ID = "Dg0MFSkPJAIJMgchHjw1BwY"
USERNAME  = "Dg0MFSkPJAIJMgchHjw1BwY"
PASSWORD  = "8p9YF6bT68Hxjny5ChF13Vrm"

MQTT_HOST = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

# ========================================
# MQTT callbacks
# ========================================
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✓ MQTT connected (sender)")
    else:
        print(f"✗ MQTT connect failed (rc={rc})")

def on_publish(client, userdata, mid):
    print(f"  → MQTT published MID={mid}")

# Khởi tạo MQTT client
client = mqtt.Client(client_id=CLIENT_ID)
client.username_pw_set(username=USERNAME, password=PASSWORD)
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)
client.loop_start()

# ========================================
# HTTP helpers
# ========================================
def make_param_thingspeak(temp, humi):
    """
    Tạo payload cho HTTP update:
      field1 = temp, field2 = humi
    """
    params = parse.urlencode({'field1': temp, 'field2': humi}).encode()
    return params

def thingspeak_post_http(params):
    """
    POST dữ liệu lên ThingSpeak bằng HTTP.
    """
    req = request.Request('https://api.thingspeak.com/update', method="POST")
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('X-THINGSPEAKAPIKEY', WRITE_API_KEY)
    with request.urlopen(req, data=params, timeout=10) as r:
        return r.read()

# ========================================
# MQTT publish (field3 & field4)
# ========================================
def thingspeak_post_mqtt(temp, humi):
    """
    Publish dữ liệu lên MQTT:
      field3 = temp, field4 = humi (cùng một message)
    """
    topic = f"channels/{CHANNEL_ID}/publish"
    payload = f"field3={temp}&field4={humi}&status=MQTTPUBLISH"
    # QoS=1 đảm bảo message được broker nhận ít nhất một lần
    return client.publish(topic, payload, qos=1)

# ========================================
# MAIN
# ========================================
def main():
    # Cảm biến DHT11 trên Grove Base Hat, cổng D5 → GPIO 5
    sensor = DHT('11', 5)

    print("=" * 60)
    print("Bắt đầu gửi dữ liệu lên ThingSpeak: HTTP(f1,f2) + MQTT(f3,f4)")
    print("Nhấn Ctrl+C để dừng chương trình")
    print("=" * 60)

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

            # ===== 1) Gửi qua HTTP (field1, field2)
            try:
                resp = thingspeak_post_http(make_param_thingspeak(avg_temp, avg_humi))
                print(f"✓ HTTP update (f1,f2): {resp.decode().strip()}")
            except Exception as e:
                print(f"✗ HTTP error: {e}")

            # ===== 2) Gửi qua MQTT (field3, field4)
            try:
                mqtt_result = thingspeak_post_mqtt(avg_temp, avg_humi)
                if mqtt_result.rc == mqtt.MQTT_ERR_SUCCESS:
                    print(f"✓ MQTT update (f3,f4) — MID: {mqtt_result.mid}")
                else:
                    print(f"✗ MQTT publish error — rc: {mqtt_result.rc}")
            except Exception as e:
                print(f"✗ MQTT error: {e}")

            # cho MQTT loop xử lý xong nếu còn queue
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
        client.loop_stop()
        client.disconnect()
        print("Đã ngắt kết nối MQTT")