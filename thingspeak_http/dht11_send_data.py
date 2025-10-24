import time
from seeed_dht import DHT
from urllib import request, parse
from time import sleep

# Channel ID: 3127848
# Author: toltalbiuh
# API Key (Write): AHHO5UL59ZCYUYCV
# API Key (Read): N251PNZ5EG0MWI2Y

def make_param_thingspeak(temperature, humidity):
    # Map: field1 = temperature (°C), field2 = humidity (%)
    params = parse.urlencode({
        'field1': f"{temperature:.1f}",
        'field2': f"{humidity:.1f}"
    }).encode()
    return params

def thingspeak_post(params):
    api_key_write = "AHHO5UL59ZCYUYCV"
    req = request.Request('https://api.thingspeak.com/update', method="POST")
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('X-THINGSPEAKAPIKEY', api_key_write)
    with request.urlopen(req, data=params, timeout=10) as r:
        response_data = r.read().decode().strip()
    return response_data

def main():
    # Grove - DHT11 on GPIO5 (Grove Base Hat: port D2)
    sensor = DHT('11', 5)
    READ_INTERVAL = 10  # seconds
    SEND_INTERVAL = 20  # seconds
    last_sent_ts = 0.0
    print(
        "Đang đọc DHT11 mỗi 10 giây và gửi dữ liệu lên ThingSpeak mỗi 20 giây (field1=temp, field2=hum)…"
    )

    while True:
        try:
            humidity, temperature = sensor.read()
        except Exception as e:
            print(f"Lỗi khi đọc cảm biến: {e}")
            sleep(5)
            continue

        if humidity is None or temperature is None:
            print("Đọc cảm biến thất bại (None); thử lại sau 5s…")
            sleep(5)
            continue

        print("Temperature: {:.1f} C, Humidity: {:.1f} %".format(temperature, humidity))

        # Gửi lên ThingSpeak mỗi 20 giây
        now = time.time()
        if now - last_sent_ts >= SEND_INTERVAL:
            try:
                params = make_param_thingspeak(temperature, humidity)
                resp = thingspeak_post(params)
                if resp == '0':
                    print("ThingSpeak update thất bại (response 0)")
                else:
                    print(f"Đã gửi lên ThingSpeak, entry id: {resp}")
            except Exception as e:
                print(f"Lỗi HTTP khi gửi lên ThingSpeak: {e}")
            else:
                last_sent_ts = now

        # Đọc/hiển thị mỗi 10 giây
        sleep(READ_INTERVAL)

if __name__ == "__main__":
    main()