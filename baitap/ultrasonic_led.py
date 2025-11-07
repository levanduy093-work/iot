import time
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.display.jhd1802 import JHD1802
from grove.gpio import GPIO

led_pin = 16

class GroveLED(GPIO):
    def __init__(self, pin):
        super(GroveLED, self).__init__(pin, GPIO.OUT)

    def on(self):
        self.write(1)

    def off(self):
        self.write(0)

led = GroveLED(led_pin)

led_status = "OFF"
ultrasonic_sensor = GroveUltrasonicRanger(5)
lcd = JHD1802()

while True:
    distance = ultrasonic_sensor.get_distance()
    print("Distance: {:.1f} cm".format(distance))
    
    if distance < 10:
        led.on()
        led_status = "ON"
        print("LED ON")
    else:
        led.off()
        led_status = "OFF"
        print("LED OFF")

    lcd.setCursor(0, 0)
    lcd.write("Distance: {:.f}cm".format(distance))

    lcd.setCursor(1, 0)
    lcd.write("LED: {}".format(led_status))
    time.sleep(1)