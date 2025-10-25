import time
from grove.grove_relay import GroveRelay
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger

# Grove - Relay connected to D16 pin
relay = GroveRelay(16)

# Grove - Ultrasonic Ranger connected to D5 pin
sensor = GroveUltrasonicRanger(5)

while True:
    print("Detecting distance ...")
    distance = sensor.get_distance()
    print("{}".format(distance))

    if distance < 20:
        relay.on()
        print("Relay on")
    else:
        relay.off()
        print("Relay off")

    time.sleep(1)

