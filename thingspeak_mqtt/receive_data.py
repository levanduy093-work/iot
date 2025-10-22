import paho.mqtt.client as mqtt
from time import sleep
from random import randint

CLIENT_ID = "AxYcMR0HLBEmFB8qATYiEjk"
USERNAME  = "AxYcMR0HLBEmFB8qATYiEjk"
PASSWORD  = "Y8+GZ1Dnp8QRpb1+MftJDKgI"
CHANNEL_ID = "3125997"

def on_connect(client, userdata, flags, rc):
    print("Connected with Result code {}".format(rc))

    # Subscribe to upadates to a channel field from a private channel
    # channels/<channelID>/subscribe/fields/field<fieldnumber>
    client.subscribe(f"channels/{CHANNEL_ID}/subscribe/fields/field3")

def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")

def on_message(client, userdata, message):
    print("Message received: " + message.payload.decode())
    print("Topic: " + message.topic)

client = mqtt.Client(CLIENT_ID)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set(username=USERNAME, password=PASSWORD)

client.connect("mqtt3.thingspeak.com", 1883, 60)
client.loop_forever()