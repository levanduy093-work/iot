import time
from grove.grove_mini_pir_motion_sensor import GroveMiniPIRMotionSensor
from grove.grove_relay import GroveRelay

# Grove - Mini PIR Motion Sensor connected to D5 pin
sensor = GroveMiniPIRMotionSensor(5)

# Grove - Relay connected to D16 pin
relay = GroveRelay(16)

def on_detect():
    print("Motion detected")
    
    relay.on()
    print("Relay on")

    time.sleep(1)

    relay.off()
    print("Relay off")

sensor.on_detect = on_detect

while True:
    time.sleep(1)

    