from gpiozero import LED
import time

relay = LED(12)

while True:
    relay.on()
    time.sleep(1)
    relay.off()
    time.sleep(1)