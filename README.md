# IoT Project - Hệ thống giám sát IoT với Raspberry Pi

Dự án IoT sử dụng Raspberry Pi để thu thập dữ liệu từ nhiều loại cảm biến khác nhau và truyền lên nền tảng ThingSpeak để theo dõi và phân tích. Hỗ trợ đầy đủ các cảm biến Grove thông qua Grove Base Hat.

## ✨ Tính năng

- **Điều khiển LED**: Bật/tắt và nhấp nháy LED với Grove Base Hat
- **Cảm biến ánh sáng**: Đọc dữ liệu từ cảm biến ánh sáng Grove
- **Cảm biến nhiệt độ độ ẩm DHT11**: Đọc và hiển thị dữ liệu DHT11 với LCD
- **Cảm biến khoảng cách siêu âm**: Đo khoảng cách với cảm biến siêu âm Grove
- **Cảm biến độ ẩm đất**: Theo dõi độ ẩm đất với cảnh báo buzzer
- **Cảm biến PIR (Motion)**: Phát hiện chuyển động và điều khiển relay
- **Hiển thị LCD**: Hiển thị dữ liệu cảm biến trên màn hình LCD 16x2 I2C
- **Điều khiển Relay**: Bật/tắt thiết bị điện thông qua relay
- **Điều khiển Servo**: Điều khiển động cơ servo 180 độ
- **Tích hợp ThingSpeak HTTP**: Gửi dữ liệu cảm biến lên ThingSpeak qua HTTP API
- **Tích hợp ThingSpeak MQTT**: Gửi dữ liệu qua giao thức MQTT với xác thực
- **ADC Analog Reading**: Đọc dữ liệu analog từ các cảm biến

## 🛠️ Yêu cầu hệ thống

### Phần cứng
- **Raspberry Pi** (3B+, 4, hoặc Zero W)
- **Grove Base Hat** (khuyến nghị, để dễ dàng kết nối các cảm biến Grove)
- **Cảm biến DHT11** (kết nối vào GPIO5/D2)
- **LED Grove** (kết nối vào D5)
- **Cảm biến ánh sáng Grove** (kết nối vào A0)
- **Cảm biến siêu âm Grove** (kết nối vào D5)
- **Cảm biến độ ẩm đất Grove** (kết nối vào A0)
- **Cảm biến PIR Motion Grove** (kết nối vào D5)
- **Màn hình LCD 16x2 I2C** (kết nối I2C)
- **Relay Grove** (kết nối vào D16)
- **Buzzer Grove** (kết nối vào D12)
- **Servo Motor** (kết nối vào D12)
- **Nút nhấn** (tùy chọn)

### Phần mềm
- **Python 3.7+**
- **gpiozero** - Thư viện điều khiển GPIO
- **seeed-dht** - Thư viện đọc cảm biến DHT11
- **paho-mqtt** - Thư viện MQTT client
- **grove.py** - Thư viện Grove sensors
- **numpy** - Thư viện tính toán số học (cho servo)
- **RPi.GPIO** - Thư viện GPIO cho Raspberry Pi

## 📦 Cài đặt

### 1. Cài đặt Python và môi trường

```bash
# Tạo môi trường conda (khuyến nghị)
conda create -n iot python=3.9
conda activate iot

# Hoặc sử dụng môi trường Python mặc định
pip install --upgrade pip
```

### 2. Cài đặt thư viện cần thiết

```bash
# Cài đặt các thư viện Python
pip install gpiozero seeed-dht paho-mqtt grove.py numpy

# Cài đặt thư viện Grove Display cho LCD
pip install grove-display
```

### 3. Cài đặt thư viện hệ thống (cho RPi.GPIO)

```bash
sudo apt update
sudo apt install python3-gpiozero python3-pip python3-numpy
```

### 4. Kích hoạt I2C (cho LCD và các cảm biến I2C)

```bash
sudo raspi-config
# Chọn: Interface Options > I2C > Enable
sudo reboot
```

### 5. Thêm user vào gpio group (cho quyền truy cập GPIO)

```bash
sudo usermod -a -G gpio $USER
sudo reboot
```

## 🚀 Cách sử dụng

### 1. Điều khiển LED Grove

```bash
cd button_led
python grove_led.py
```

**Chức năng**: Nhấp nháy LED Grove (bật 1 giây, tắt 1 giây)

### 2. Cảm biến ánh sáng

```bash
cd light_sensor
python light_sensor.py
```

**Chức năng**: Đọc giá trị ánh sáng từ cảm biến Grove (0-4095)

### 3. Cảm biến nhiệt độ độ ẩm DHT11

```bash
cd dht_lcd
python dht_11_lcd.py
```

**Chức năng**:
- Đọc nhiệt độ và độ ẩm từ DHT11
- Hiển thị dữ liệu trên LCD 16x2 I2C
- Cập nhật mỗi giây

### 4. Cảm biến khoảng cách siêu âm

```bash
cd ultrasonic_relay
python ultrasonic.py
```

**Chức năng**: Đo khoảng cách bằng cảm biến siêu âm Grove (cm)

### 5. Hệ thống giám sát độ ẩm đất

```bash
cd moisture_lcd_buzzer
python moisture_lcd_buzzer.py
```

**Chức năng**:
- Đọc độ ẩm đất từ cảm biến Grove
- Hiển thị trên LCD 16x2
- Kích hoạt buzzer khi đất quá ẩm (moisture > 600)
- Phân loại: dry (< 300), moist (300-600), wet (> 600)

### 6. Cảm biến PIR Motion

```bash
cd pir_mini_motion
python pir_mini_motion.py
```

**Chức năng**:
- Phát hiện chuyển động bằng PIR sensor
- Tự động bật relay trong 1 giây khi có chuyển động
- Hiển thị trạng thái trên console

### 7. Hiển thị LCD

```bash
cd lcd
python lcd.py
```

**Chức năng**: Hiển thị "Hello, World!" trên LCD 16x2 I2C

### 8. Điều khiển Relay

```bash
cd relay
python relay.py
```

**Chức năng**: Bật/tắt relay mỗi giây (tương tự LED)

### 9. Điều khiển Servo Motor

```bash
cd servo
python servo.py
```

**Chức năng**: Quét servo từ 0° đến 180° và ngược lại

### 10. Đọc ADC Analog

```bash
cd adc
python adc.py
```

**Chức năng**: Đọc giá trị analog từ Grove ADC (0-3299mV)

### 11. Gửi dữ liệu lên ThingSpeak qua HTTP

```bash
cd thingspeak_http
python dht11_send_data.py
```

**Chức năng**:
- Đọc dữ liệu DHT11 mỗi 10 giây
- Gửi dữ liệu lên ThingSpeak mỗi 20 giây
- Field1: Nhiệt độ (°C)
- Field2: Độ ẩm (%)

### 12. Gửi dữ liệu lên ThingSpeak qua MQTT

```bash
cd thingspeak_mqtt
python send_data.py
```

**Chức năng**:
- Gửi dữ liệu ngẫu nhiên lên ThingSpeak qua MQTT
- Field3: Giá trị ngẫu nhiên
- Tự động xác thực với ThingSpeak

## 📁 Cấu trúc dự án

```
iot/
├── adc/                       # Đọc dữ liệu analog
│   └── adc.py                # Đọc ADC Grove (0-3299mV)
├── button_led/                # Điều khiển LED
│   ├── grove_led.py          # LED Grove nhấp nháy
│   ├── led_button.py         # LED với nút nhấn
│   └── led_on_off_5_times.py # LED blink 5 lần
├── dht_lcd/                   # DHT11 với LCD display
│   └── dht_11_lcd.py         # DHT11 đọc và hiển thị LCD
├── lcd/                       # LCD display
│   └── lcd.py                # LCD Hello World
├── light_sensor/              # Cảm biến ánh sáng
│   └── light_sensor.py       # Grove light sensor
├── moisture_lcd_buzzer/       # Hệ thống giám sát độ ẩm
│   └── moisture_lcd_buzzer.py # Moisture sensor với LCD và buzzer
├── pir_mini_motion/           # Cảm biến PIR motion
│   └── pir_mini_motion.py    # PIR sensor điều khiển relay
├── relay/                     # Điều khiển relay
│   └── relay.py              # Relay bật/tắt
├── servo/                     # Điều khiển servo motor
│   └── servo.py              # Servo quét 0-180°
├── thingspeak_http/           # ThingSpeak HTTP integration
│   ├── dht11_send_data.py    # Gửi DHT11 data qua HTTP
│   ├── dht11_receive_data.py # Nhận data từ ThingSpeak
│   ├── send_data.py          # Gửi data generic
│   └── receive_data.py       # Nhận data generic
├── thingspeak_mqtt/           # ThingSpeak MQTT integration
│   ├── send_data.py          # Gửi data qua MQTT
│   └── receive_data.py       # Nhận data qua MQTT
└── ultrasonic_relay/          # Cảm biến khoảng cách
    ├── ultrasonic.py         # Grove ultrasonic sensor
    └── ultrasonic_relay.py   # Ultrasonic với relay
```

## ⚙️ Cấu hình ThingSpeak

### Tạo kênh ThingSpeak

1. Đăng nhập vào [ThingSpeak](https://thingspeak.com)
2. Tạo kênh mới với các field:
   - **Field 1**: Temperature (°C)
   - **Field 2**: Humidity (%)
   - **Field 3**: Other data
3. Lấy **Channel ID** và **API Keys**

### Cập nhật thông tin trong code

**File: `thingspeak_http/dht11_send_data.py`**
```python
# API Key đã được cấu hình sẵn
api_key_write = "AHHO5UL59ZCYUYCV"  # Thay đổi theo API key của bạn
```

**File: `thingspeak_mqtt/send_data.py`**
```python
# Cập nhật thông tin MQTT của bạn
CHANNEL_ID = "YOUR_CHANNEL_ID"
CLIENT_ID = "YOUR_CLIENT_ID"
USERNAME = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"
```

### Thông tin kênh demo
- **Channel ID**: 3127848
- **Write API Key**: AHHO5UL59ZCYUYCV
- **Read API Key**: N251PNZ5EG0MWI2Y
- **Link**: [ThingSpeak Channel 3127848](https://thingspeak.com/channels/3127848)

## 🔧 Troubleshooting

### Lỗi không tìm thấy module
```bash
# Cài đặt lại tất cả thư viện cần thiết
pip install --upgrade gpiozero seeed-dht paho-mqtt grove.py numpy grove-display

# Hoặc cài đặt với quyền sudo nếu cần
sudo pip install gpiozero seeed-dht paho-mqtt grove.py numpy grove-display
```

### Lỗi GPIO permission
```bash
# Thêm user vào gpio group
sudo usermod -a -G gpio $USER
sudo reboot

# Hoặc chạy script với quyền root
sudo python script.py
```

### Lỗi I2C không hoạt động (LCD, ADC)
```bash
# Kiểm tra I2C đã được kích hoạt
ls /dev/i2c*

# Nếu không có /dev/i2c-1, kích hoạt lại I2C
sudo raspi-config
# Chọn: Interface Options > I2C > Enable
sudo reboot
```

### Lỗi DHT11 không đọc được
- Kiểm tra kết nối GPIO5/D2 (nếu dùng Grove Base Hat)
- Đảm bảo DHT11 được kết nối đúng cách (VCC, GND, Data)
- Thử thay đổi thời gian sleep giữa các lần đọc
- Kiểm tra nguồn điện 3.3V/5V phù hợp

### Lỗi Grove sensors không hoạt động
- Kiểm tra kết nối với Grove Base Hat
- Đảm bảo Base Hat được lắp đúng vào GPIO pins
- Kiểm tra điện áp nguồn (3.3V hoặc 5V tùy cảm biến)

### Lỗi cảm biến ánh sáng/độ ẩm
- Kiểm tra kết nối analog (A0, A1, v.v.)
- Đảm bảo cảm biến được cắm đúng port analog
- Kiểm tra giá trị ADC có thay đổi khi có tác động

### Lỗi servo motor
- Kiểm tra kết nối PWM pin (thường là D12)
- Đảm bảo nguồn điện đủ mạnh (servo cần dòng lớn)
- Kiểm tra góc servo không vượt quá 0-180°

### Lỗi ThingSpeak connection
- Kiểm tra API key và Channel ID
- Đảm bảo internet connection
- Kiểm tra ThingSpeak rate limits (mỗi 15 giây)
- Kiểm tra firewall không chặn HTTP/MQTT requests

### Lỗi import grove modules
```bash
# Cài đặt grove.py từ source
git clone https://github.com/Seeed-Studio/grove.py.git
cd grove.py
sudo pip install .

# Hoặc cài đặt bản mới nhất
pip install --upgrade grove.py
```

## 📊 Monitoring và Visualization

Dữ liệu được gửi lên ThingSpeak có thể được xem và phân tích:

1. **Dashboard**: Xem dữ liệu real-time từ tất cả cảm biến
2. **Charts**: Biểu đồ nhiệt độ, độ ẩm, ánh sáng, khoảng cách
3. **Apps**: Tạo ứng dụng mobile để theo dõi
4. **Alerts**: Thiết lập cảnh báo khi vượt ngưỡng
5. **Data Export**: Xuất dữ liệu để phân tích

### Các loại dữ liệu được theo dõi:
- **Field 1**: Nhiệt độ (°C) từ DHT11
- **Field 2**: Độ ẩm (%) từ DHT11
- **Field 3**: Dữ liệu khác (ánh sáng, khoảng cách, độ ẩm đất)

## 🤝 Đóng góp

1. Fork dự án
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📄 Giấy phép

Dự án này được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.

## 📞 Liên hệ

- **Author**: toltalbiuh
- **ThingSpeak Channel**: [3127848](https://thingspeak.com/channels/3127848)
- **Email**: [your-email@example.com]

---

## 📝 Ghi chú

- **Chạy lần đầu**: Đảm bảo đã kích hoạt I2C và thêm user vào gpio group
- **Grove Base Hat**: Khuyến nghị sử dụng để dễ dàng kết nối các cảm biến
- **API Keys**: Thay đổi API keys trong code theo thông tin ThingSpeak của bạn
- **Rate Limits**: ThingSpeak có giới hạn 15 giây/lần gửi dữ liệu
- **Power Supply**: Một số cảm biến (servo, relay) cần nguồn điện riêng
- **Pin Mapping**: Kiểm tra kỹ pin mapping khi kết nối trực tiếp với GPIO
