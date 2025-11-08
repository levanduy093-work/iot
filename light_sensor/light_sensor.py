import time
from grove.adc import ADC

sensor_pin = 0      # Channel = A0

class GroveLightSensor:
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC(address=0x08)

    @property
    def value(self):
        return self.adc.read(self.channel)   # trả về 0–1000

def value_to_voltage(value, vref=3.3):
    """
    Chuyển đổi giá trị 0–1000 sang điện áp (Volt)
    """
    return (value / 1000.0) * vref

sensor = GroveLightSensor(sensor_pin)

print("Detecting Light (Voltage Only)...")
while True:
    value = sensor.value
    voltage = value_to_voltage(value)

    print(f"Voltage: {voltage:.3f} V")
    time.sleep(1)