# ---- Thingspeak MQTT (paho-mqtt 2.x) ----
import paho.mqtt.client as mqtt
from time import sleep
from random import randint

CLIENT_ID = "KAwYFzoPHwIFPToMJiEADAc"
USERNAME  = "KAwYFzoPHwIFPToMJiEADAc"
PASSWORD  = "9EyhBPHUdp6QAkhBAzFQY/fW"
CHANNEL_ID = "3125997"

# Quan trọng: dùng keyword client_id=... (không truyền positional)
client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)
client.username_pw_set(username=USERNAME, password=PASSWORD)

# Thingspeak MQTT3 (TCP 1883). Nếu dùng TLS: port 8883 + client.tls_set()
client.connect("mqtt3.thingspeak.com", 1883, 60)

# Chạy vòng lặp mạng trong thread nền
client.loop_start()

def thingspeak_mqtt(value):
    topic = f"channels/{CHANNEL_ID}/publish"
    payload = f"field3={value}&status=MQTTPUBLISH"
    # QoS 0 là đủ cho ThingSpeak
    client.publish(topic, payload, qos=0)

try:
    while True:
        v = randint(0, 50)
        print(v)
        thingspeak_mqtt(v)
        sleep(20)

except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()