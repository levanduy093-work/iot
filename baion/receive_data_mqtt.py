# Channel ID: 3127848
# username    = "IRU6PSACOwQPHy4PKiczCiI"
# clientID    = "IRU6PSACOwQPHy4PKiczCiI"
# password    = "gHzqnX35vjOPS0jeNUVtBdfV"

# Biến lưu tạm để ghép cặp
current_temp = None
current_humi = None

def on_connect(client, userdata, flags, rc):
    print("Connected with Result code {}".format(rc))
    # Subscribe field3 & field4
    client.subscribe("channels/%s/subscribe/fields/field3" % (channel_ID))
    client.subscribe("channels/%s/subscribe/fields/field4" % (channel_ID))

def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")

def on_message(client, userdata, message):
    global current_temp, current_humi

    value = message.payload.decode().strip()
    topic = message.topic

    # Lưu giá trị đúng field
    if topic.endswith("field3"):
        current_temp = value
    elif topic.endswith("field4"):
        current_humi = value

    # In ra khi có đủ cả nhiệt độ & độ ẩm
    if current_temp is not None and current_humi is not None:
        print(f"Nhiệt độ: {current_temp} °C | Độ ẩm: {current_humi} %")

        # Reset để chờ cặp tiếp theo
        current_temp = None
        current_humi = None


import paho.mqtt.client as mqtt

channel_ID = "3127848"
client_id  = "IRU6PSACOwQPHy4PKiczCiI"

client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.username_pw_set(username = "IRU6PSACOwQPHy4PKiczCiI",
                       password = "gHzqnX35vjOPS0jeNUVtBdfV")

client.connect("mqtt3.thingspeak.com", 1883, 60)
client.loop_forever()