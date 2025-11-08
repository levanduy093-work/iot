# Channel ID: 3127848
# username    = "IRU6PSACOwQPHy4PKiczCiI"
# clientID    = "IRU6PSACOwQPHy4PKiczCiI"
# password    = "gHzqnX35vjOPS0jeNUVtBdfV"

def on_connect(client, userdata, flags, rc):
    print("Connected with Result code {}".format(rc))
    # subscribes to updates to channel fields (Field3 & Field4)
    client.subscribe("channels/%s/subscribe/fields/field3" % (channel_ID))
    client.subscribe("channels/%s/subscribe/fields/field4" % (channel_ID))

def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")

def on_message(client, userdata, message):
    print(message.payload.decode())
    #print(message.topic)

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