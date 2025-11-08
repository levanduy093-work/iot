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

def thingspeak_mqtt(temp, humi):
    Channel_ID = "3127848"
    # Gửi dữ liệu lên cả Field3 và Field4
    client.publish("channels/%s/publish" % (Channel_ID),
                   "field3=%s&field4=%s&status=MQTTPUBLISH" % (temp, humi))

while True:
    temp_random = randint(20, 40)  # giả lập nhiệt độ
    humi_random = randint(40, 80)  # giả lập độ ẩm

    print("Temp:", temp_random, "°C   |   Humi:", humi_random, "%")

    thingspeak_mqtt(temp_random, humi_random)
    sleep(20)