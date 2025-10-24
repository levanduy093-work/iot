# IoT Project - Hệ thống giám sát IoT với Raspberry Pi

Dự án IoT sử dụng Raspberry Pi để thu thập dữ liệu cảm biến và truyền lên nền tảng ThingSpeak để theo dõi và phân tích.

## ✨ Tính năng

- **Điều khiển LED với nút nhấn**: Sử dụng gpiozero để điều khiển LED thông qua nút nhấn
- **Cảm biến nhiệt độ độ ẩm DHT11**: Đọc dữ liệu từ cảm biến DHT11 với thư viện seeed_dht
- **Hiển thị LCD**: Hiển thị dữ liệu cảm biến trên màn hình LCD 16x2 (tùy chọn)
- **Tích hợp ThingSpeak HTTP**: Gửi dữ liệu cảm biến lên ThingSpeak qua HTTP API
- **Tích hợp ThingSpeak MQTT**: Gửi dữ liệu qua giao thức MQTT với xác thực
- **Grove Sensors**: Hỗ trợ các cảm biến Grove thông qua Grove Base Hat

## 🛠️ Yêu cầu hệ thống

### Phần cứng
- **Raspberry Pi** (3B+, 4, hoặc Zero W)
- **Grove Base Hat** (tùy chọn, để dễ dàng kết nối các cảm biến)
- **Cảm biến DHT11** (kết nối vào GPIO5/D2)
- **LED và nút nhấn** (kết nối vào GPIO5 và GPIO6)
- **Màn hình LCD 16x2** (tùy chọn, kết nối I2C)

### Phần mềm
- **Python 3.7+**
- **gpiozero** - Thư viện điều khiển GPIO
- **seeed-dht** - Thư viện đọc cảm biến DHT11
- **paho-mqtt** - Thư viện MQTT client
- **grove.py** - Thư viện Grove sensors

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
pip install gpiozero seeed-dht paho-mqtt grove.py

# Nếu sử dụng Grove Base Hat, cài đặt thêm
pip install grove-display
```

### 3. Cài đặt thư viện hệ thống (cho RPi.GPIO)

```bash
sudo apt update
sudo apt install python3-gpiozero python3-pip
```

### 4. Kích hoạt I2C (cho LCD)

```bash
sudo raspi-config
# Chọn: Interface Options > I2C > Enable
sudo reboot
```

## 🚀 Cách sử dụng

### LED Control với Button

```bash
cd button_led
python led_botton.py
```

**Chức năng**: Nhấn nút để bật LED, thả nút để tắt LED

### Đọc cảm biến DHT11

```bash
cd dht
python dht_11.py
```

**Chức năng**: Đọc và hiển thị nhiệt độ và độ ẩm mỗi giây

### Gửi dữ liệu lên ThingSpeak qua HTTP

```bash
cd thingspeak_http
python dht11_send_data.py
```

**Chức năng**:
- Đọc dữ liệu DHT11 mỗi 10 giây
- Gửi dữ liệu lên ThingSpeak mỗi 20 giây
- Field1: Nhiệt độ (°C)
- Field2: Độ ẩm (%)

### Gửi dữ liệu lên ThingSpeak qua MQTT

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
├── button_led/                 # Điều khiển LED với nút nhấn
│   ├── led_botton.py          # LED toggle với button
│   ├── grove_led.py           # Grove LED control
│   └── led_on_off_5_times.py  # LED blink 5 lần
├── dht/                       # Cảm biến nhiệt độ độ ẩm
│   └── dht_11.py             # Đọc DHT11 và hiển thị LCD
├── light_sensor/              # Cảm biến ánh sáng (chưa implement)
├── thingspeak_http/           # ThingSpeak HTTP integration
│   ├── dht11_send_data.py    # Gửi DHT11 data qua HTTP
│   ├── dht11_receive_data.py # Nhận data từ ThingSpeak
│   ├── send_data.py          # Gửi data generic
│   └── receive_data.py       # Nhận data generic
└── thingspeak_mqtt/           # ThingSpeak MQTT integration
    ├── send_data.py          # Gửi data qua MQTT
    └── receive_data.py       # Nhận data qua MQTT
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
# Cập nhật API Key của bạn
api_key_write = "YOUR_WRITE_API_KEY_HERE"
```

**File: `thingspeak_mqtt/send_data.py`**
```python
# Cập nhật thông tin MQTT
CHANNEL_ID = "YOUR_CHANNEL_ID"
CLIENT_ID = "YOUR_CLIENT_ID"
USERNAME = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"
```

## 🔧 Troubleshooting

### Lỗi không tìm thấy module
```bash
# Cài đặt lại thư viện
pip install --upgrade gpiozero seeed-dht paho-mqtt grove.py
```

### Lỗi GPIO permission
```bash
# Chạy với quyền root hoặc thêm user vào gpio group
sudo usermod -a -G gpio $USER
sudo reboot
```

### Lỗi DHT11 không đọc được
- Kiểm tra kết nối GPIO5/D2
- Đảm bảo DHT11 được kết nối đúng cách
- Thử thay đổi thời gian sleep giữa các lần đọc

### Lỗi ThingSpeak connection
- Kiểm tra API key và Channel ID
- Đảm bảo internet connection
- Kiểm tra ThingSpeak rate limits (mỗi 15 giây)

## 📊 Monitoring và Visualization

Dữ liệu được gửi lên ThingSpeak có thể được xem và phân tích:

1. **Dashboard**: Xem dữ liệu real-time
2. **Charts**: Biểu đồ nhiệt độ và độ ẩm
3. **Apps**: Tạo ứng dụng mobile để theo dõi
4. **Alerts**: Thiết lập cảnh báo khi vượt ngưỡng

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

**Lưu ý**: Thay đổi các thông tin cấu hình (API keys, Channel ID) theo thông tin ThingSpeak của bạn trước khi chạy các script.
