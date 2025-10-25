import time, sys, math
from grove.adc import ADC

# //Channel = A0
sensor_pin = 0 

class GroveLightSensor():
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def light(self):
        value = self.adc.read(self.channel)
        return value

sensor = GroveLightSensor(sensor_pin)

print("Detecting light...")
while True:
    print(f"Light value: {0}".format(sensor.light))
    time.sleep(1)
