import time
from grove.gpio import GPIO
from grove.display.jhd1802 import JHD1802
from grove.grove_moisture_sensor import GroveMoistureSensor

buzzer_pin = 12
MoistureSensor_pin = 0

class GroveBuzzer(GPIO):
    def __init__(self, pin):
        super(GroveBuzzer, self).__init__(pin, GPIO.OUT)

    def on(self):
        self.write(1)

    def off(self):
        self.write(0)

def main():
    # Grove - LCD connected to I2C port
    lcd = JHD1802()

    # Grove - Moisture Sensor connected to port A0 pin
    sensor = GroveMoistureSensor(MoistureSensor_pin)

    # Grove - Buzzer connected to port PWM
    buzzer = GroveBuzzer(buzzer_pin)

    while True:
        mois = sensor.moisture
        if 0 <= mois < 300:
            level = 'dry'
            buzzer.off()
        elif 300 <= mois < 600:
            level = 'moist'
            buzzer.off()
        else:
            level = 'wet'
            buzzer.on()
        
        print("Moisture: {}, Level: {}".format(mois, level))

        lcd.setCursor(0, 0)
        lcd.write("Moisture: {0:>6}".format(mois))

        lcd.setCursor(1, 0)
        lcd.write("Level: {0:>6}".format(level))

        time.sleep(1)

if __name__ == "__main__":
    main()