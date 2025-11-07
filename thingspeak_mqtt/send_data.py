# ---- Thingspeak MQTT (paho-mqtt 2.x) ----
import paho.mqtt.client as mqtt
from time import sleep
from random import randint

CLIENT_ID = "BAwPPDYtETwNHRsKFD0yHwE"
USERNAME  = "BAwPPDYtETwNHRsKFD0yHwE"
PASSWORD  = "cK3C/mWbHLRUFkbak1DY+31U"
CHANNEL_ID = "3142608"

# Quan trọng: dùng keyword client_id=... (không truyền positional)
client = mqtt.Client(CLIENT_ID)
client.username_pw_set(username=USERNAME, password=PASSWORD)

# Thingspeak MQTT3 (TCP 1883). Nếu dùng TLS: port 8883 + client.tls_set()
client.connect("mqtt3.thingspeak.com", 1883, 60)

def thingspeak_mqtt(data):
    client.publish(f"channels/{CHANNEL_ID}/publish", f"field3={data}&status=MQTTPUBLISH")

while True:
    random_value = randint(0, 50)
    print(f"Publishing value: {random_value}")
    thingspeak_mqtt(random_value)
    sleep(20)  # ThingSpeak yêu cầu tối thiểu 15 giây giữa các lần gửi dữ liệu