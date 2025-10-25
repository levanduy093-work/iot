from grove.gpio import GPIO
import sys
import time

relay_pin = 12

class GroveRelay(GPIO):
    def __init__(self, pin):
        super(GroveRelay, self).__init__(pin, GPIO.OUT)

    def on(self):
        self.write(1)

    def off(self):
        self.write(0)


relay = GroveRelay(relay_pin)

while True:
    try:
        relay.on()
        time.sleep(1)
        relay.off()
        time.sleep(1)
    except KeyboardInterrupt:
        print("exit")
        exit(1)