import time
from seeed_dht import DHT
from grove.display.jhd1802 import JHD1802

def main():
    # Grove - 16x2 LCD (White on Blue) connected to I2C port
    lcd = JHD1802()
    
    # Grove - Temperature & Humidity Sensor connected to D2 pin
    sensor = DHT('11', 5) # DHT11 on GPIO5, if Grove Hat find D2 pin
    while True:
        humidity, temperature = sensor.read()
        print("Temperature: {:.1f} C, Humidity: {:.1f} %".format(temperature, humidity))

        lcd.setCursor(0, 0)
        lcd.write("Temperature: {:.1f} C".format(temperature))

        lcd.setCursor(1, 0)
        lcd.write("Humidity: {:.1f} %".format(humidity))

        time.sleep(1)

if __name__ == "__main__":
    main()

