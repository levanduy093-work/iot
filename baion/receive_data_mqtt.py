import json
from datetime import datetime
import paho.mqtt.client as mqtt

USERNAME   = "IRU6PSACOwQPHy4PKiczCiI"
CLIENT_ID  = "IRU6PSACOwQPHy4PKiczCiI"
PASSWORD   = "gHzqnX35vjOPS0jeNUVtBdfV"
CHANNEL_ID = "3127848"

MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE = "mqtt3.thingspeak.com", 1883, 60

current_temp = None
current_humi = None

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def try_float(x):
    try:
        return float(str(x).strip())
    except Exception:
        return None

def maybe_print_pair():
    if current_temp is not None and current_humi is not None:
        print(f"[{now()}] ⇄ CURRENT → field3={current_temp}°C, field4={current_humi}%")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[{now()}] MQTT connected (rc={rc})")
        t3 = f"channels/{CHANNEL_ID}/subscribe/fields/field3"
        t4 = f"channels/{CHANNEL_ID}/subscribe/fields/field4"
        tj = f"channels/{CHANNEL_ID}/subscribe/json"
        client.subscribe(t3, qos=0)
        client.subscribe(t4, qos=0)
        client.subscribe(tj, qos=0)
        print(f"[{now()}] Subscribed:\n  • {t3}\n  • {t4}\n  • {tj}")
    else:
        print(f"[{now()}] MQTT connect failed (rc={rc})")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"[{now()}] Disconnected unexpectedly (rc={rc})")
    else:
        print(f"[{now()}] Disconnected")

def on_message(client, userdata, message):
    global current_temp, current_humi
    topic = message.topic
    payload = message.payload.decode(errors="ignore").strip()
    print(f"[{now()}] {topic}: {payload}")

    try:
        if topic.endswith("/field3"):
            v = try_float(payload)
            if v is not None:
                current_temp = v
                print(f"[{now()}] → field3(temp) = {current_temp}°C")
                maybe_print_pair()

        elif topic.endswith("/field4"):
            v = try_float(payload)
            if v is not None:
                current_humi = v
                print(f"[{now()}] → field4(humi) = {current_humi}%")
                maybe_print_pair()

        elif topic.endswith("/json"):
            data = json.loads(payload)
            f3 = try_float(data.get("field3"))
            f4 = try_float(data.get("field4"))
            updated = False
            if f3 is not None:
                current_temp = f3
                print(f"[{now()}] → field3(temp) = {current_temp}°C")
                updated = True
            if f4 is not None:
                current_humi = f4
                print(f"[{now()}] → field4(humi) = {current_humi}%")
                updated = True
            if updated:
                maybe_print_pair()
    except Exception as e:
        print(f"[{now()}] Parse error: {e}")

def main():
    print("="*66)
    print("RECEIVER (MQTT-only) – field3 & field4 from ThingSpeak (PUBLIC)")
    print(f"Channel: {CHANNEL_ID}")
    print("="*66)

    client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)
    client.username_pw_set(USERNAME, PASSWORD)

    # Last-Will: thông báo nếu client chết bất thường
    client.will_set(f"clients/{CLIENT_ID}/status", payload="offline", qos=0, retain=False)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    try:
        client.reconnect_delay_set(min_delay=1, max_delay=30)
    except AttributeError:
        pass

    client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)
    client.loop_forever()

if __name__ == "__main__":
    main()