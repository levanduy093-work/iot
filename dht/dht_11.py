import time
from seeed_dht import DHT

def main():
    sensor = DHT('11', 5) # DHT11 on GPIO5, if Grove Hat find D2 pin
    while True:
        humidity, temperature = sensor.read()
        print("Temperature: {:.1f} C, Humidity: {:.1f} %".format(temperature, humidity))

        time.sleep(1)

if __name__ == "__main__":
    main()

