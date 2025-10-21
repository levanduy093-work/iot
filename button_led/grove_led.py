from grove.gpio import GPIO
import sys, time

led_pin = 5

class GroveLED(GPIO):
    def __init__(self, pin):
        super(GroveLED, self).__init__(pin, GPIO.OUT)

    def on(self):
        self.write(1)

    def off(self):
        self.write(0)

led = GroveLED(led_pin)

while True:
    try:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)

    except KeyboardInterrupt:
        led.off()
        print("exit")
        exit(1)