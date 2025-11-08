import paho.mqtt.client as mqtt
from time import sleep
from random import randint

# Channel ID: 3127848
# username  = 'Dg0MFSkPJAIJMgchHjw1BwY'
# client_ID = 'Dg0MFSkPJAIJMgchHjw1BwY'
# password  = '8p9YF6bT68Hxjny5ChF13Vrm'

client = mqtt.Client(client_id="Dg0MFSkPJAIJMgchHjw1BwY")
client.username_pw_set("Dg0MFSkPJAIJMgchHjw1BwY",
                       password="8p9YF6bT68Hxjny5ChF13Vrm")
client.connect("mqtt3.thingspeak.com", 1883, 60)

def thingspeak_mqtt(data):
    Channel_ID = "3127848"
    client.publish("channels/%s/publish" % (Channel_ID),
                   "field3=%s&status=MQTTPUBLISH" % (data))

while True:
    data_random = randint(0, 50)
    print(data_random)

    thingspeak_mqtt(data_random)
    sleep(20)