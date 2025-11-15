# Hệ thống Giám sát Nhiệt độ và Độ ẩm với ThingSpeak MQTT

Dự án IoT sử dụng Raspberry Pi để đọc giá trị từ cảm biến nhiệt độ và độ ẩm DHT11, gửi dữ liệu lên ThingSpeak qua MQTT và điều khiển các thiết bị LED, buzzer dựa trên ngưỡng giá trị.

## ✨ Tính năng

- **Đọc cảm biến DHT11**: Đọc nhiệt độ và độ ẩm từ Grove DHT11 Sensor (D5)
- **Gửi dữ liệu lên ThingSpeak**: Gửi qua MQTT protocol
- **Hiển thị trên Terminal**: In giá trị cảm biến ra console
- **Điều khiển LED đỏ**: 
  - Bật khi nhiệt độ > 40°C
  - Tắt khi nhiệt độ < 30°C
- **Điều khiển LED vàng**: 
  - Bật khi độ ẩm > 70%
  - Tắt khi độ ẩm < 40%
- **Điều khiển Buzzer**: 
  - 1 giây bip, 1 giây không và lặp lại khi nhiệt độ > 50°C
- **Dashboard Node-RED**: Hiển thị dữ liệu với Gauge

## 🛠️ Yêu cầu phần cứng

- **Raspberry Pi** (3B+, 4, hoặc Zero W)
- **Grove Base Hat** cho Raspberry Pi
- **Grove DHT11 Sensor** (kết nối vào D5)
- **Grove LED đỏ** (kết nối vào D16)
- **Grove LED vàng** (kết nối vào D18)
- **Grove Buzzer** (kết nối vào D12)

## 📋 Yêu cầu phần mềm

- Python 3.x
- Thư viện Grove:
  - `seeed_dht`
  - `grove.gpio`
- Thư viện MQTT:
  - `paho-mqtt`
- Node-RED với các node:
  - `node-red-dashboard`
  - `node-red-contrib-mqtt-broker` (hoặc node MQTT built-in)

## 🔧 Cài đặt

### 1. Cài đặt thư viện Grove

```bash
# Cài đặt Grove Python libraries
git clone https://github.com/Seeed-Studio/grove.py
cd grove.py
sudo pip3 install .
```

### 2. Cài đặt thư viện MQTT

```bash
sudo pip3 install paho-mqtt
```

### 3. Cài đặt thư viện DHT11

```bash
sudo pip3 install seeed-python-dht
```

### 4. Cấu hình ThingSpeak MQTT

1. Tạo tài khoản tại [ThingSpeak.com](https://thingspeak.com)
2. Tạo một Channel mới với 2 fields:
   - Field 1: Temperature (Nhiệt độ)
   - Field 2: Humidity (Độ ẩm)
3. Vào **Device Credentials** để lấy:
   - **Channel ID**
   - **Username** (MQTT Username)
   - **Client ID** (MQTT Client ID)
   - **Password** (MQTT Password)

### 5. Cấu hình chương trình Python

Mở file `send_data.py` và cập nhật thông tin MQTT:

```python
# Tìm các dòng này và thay thế:
CHANNEL_ID = "YOUR_CHANNEL_ID_HERE"
CLIENT_ID = "YOUR_CLIENT_ID_HERE"
USERNAME = "YOUR_USERNAME_HERE"
PASSWORD = "YOUR_PASSWORD_HERE"
```

Thay các giá trị `YOUR_*_HERE` bằng thông tin từ ThingSpeak Device Credentials.

### 6. Cấu hình Node-RED Flow

1. Mở Node-RED: `http://localhost:1880`
2. Import file `node_red_flow.json`
3. Mở node **"ThingSpeak MQTT"** (MQTT broker) và cập nhật:
   - `YOUR_CLIENT_ID_HERE`: Thay bằng Client ID của bạn
   - `YOUR_USERNAME_HERE`: Thay bằng Username của bạn
   - `YOUR_PASSWORD_HERE`: Thay bằng Password của bạn
4. Mở các node **"Nhận Nhiệt độ"** và **"Nhận Độ ẩm"** và cập nhật:
   - `YOUR_CHANNEL_ID`: Thay bằng Channel ID của bạn
5. Deploy flow

## 🚀 Sử dụng

### Chạy chương trình Python

```bash
cd kiemtra2_test_mqtt
python3 send_data.py
```

Chương trình sẽ:
- Đọc cảm biến DHT11 mỗi 10 giây (hoặc 1 giây nếu buzzer hoạt động)
- Hiển thị giá trị trên Terminal
- Gửi dữ liệu lên ThingSpeak qua MQTT
- Điều khiển LED và buzzer theo ngưỡng

### Xem Dashboard Node-RED

1. Mở trình duyệt: `http://localhost:1880/ui`
2. Dashboard sẽ hiển thị:
   - **Gauge Nhiệt độ**: Hiển thị giá trị nhiệt độ (0-100°C)
   - **Gauge Độ ẩm**: Hiển thị giá trị độ ẩm (0-100%)

## 📊 Cấu trúc dữ liệu ThingSpeak

- **Field 1**: Nhiệt độ (°C)
- **Field 2**: Độ ẩm (%)

## ⚙️ Ngưỡng điều khiển

### LED đỏ (Cảnh báo nhiệt độ)
- **Bật**: Khi nhiệt độ > 40°C
- **Tắt**: Khi nhiệt độ < 30°C
- **Trạng thái giữ nguyên**: Khi 30°C ≤ nhiệt độ ≤ 40°C

### LED vàng (Cảnh báo độ ẩm)
- **Bật**: Khi độ ẩm > 70%
- **Tắt**: Khi độ ẩm < 40%
- **Trạng thái giữ nguyên**: Khi 40% ≤ độ ẩm ≤ 70%

### Buzzer (Cảnh báo âm thanh)
- **Bật**: Khi nhiệt độ > 50°C
- **Chế độ**: 1 giây bip, 1 giây không, lặp lại
- **Tắt**: Khi nhiệt độ ≤ 50°C

## 🔌 Sơ đồ kết nối

```
Raspberry Pi + Grove Base Hat
├── D5  → Grove DHT11 Sensor (Nhiệt độ & Độ ẩm)
├── D12 → Grove Buzzer
├── D16 → Grove LED đỏ
└── D18 → Grove LED vàng
```

## 📝 Ghi chú

- MQTT là giao thức real-time, dữ liệu được gửi ngay khi đọc được từ cảm biến
- Nếu buzzer đang hoạt động, chương trình sẽ kiểm tra và toggle buzzer mỗi 1 giây
- Nếu buzzer không hoạt động, chương trình đọc cảm biến mỗi 10 giây
- Để thay đổi pin kết nối, sửa các biến ở đầu file `send_data.py`

## 🐛 Xử lý lỗi

### Lỗi "Không thể đọc cảm biến"
- Kiểm tra kết nối Grove Base Hat
- Kiểm tra cảm biến DHT11 có được cắm đúng port D5 không
- Thử khởi động lại Raspberry Pi
- Đảm bảo cảm biến DHT11 được cấp nguồn đúng

### Lỗi "MQTT connect failed"
- Kiểm tra kết nối Internet
- Xác nhận Username, Password, Client ID đúng
- Kiểm tra Channel ID đúng
- Đảm bảo ThingSpeak MQTT broker đang hoạt động

### Lỗi "ModuleNotFoundError: No module named 'paho'"
- Cài đặt lại: `sudo pip3 install paho-mqtt`

### Lỗi "ModuleNotFoundError: No module named 'seeed_dht'"
- Cài đặt lại: `sudo pip3 install seeed-python-dht`

### Node-RED không nhận được dữ liệu
- Kiểm tra MQTT broker đã được cấu hình đúng chưa
- Kiểm tra Topic subscription đúng chưa (Channel ID)
- Kiểm tra Debug panel trong Node-RED để xem có lỗi không
- Đảm bảo chương trình Python đang chạy và gửi dữ liệu

## 📚 Tài liệu tham khảo

- [Grove Python Libraries](https://github.com/Seeed-Studio/grove.py)
- [ThingSpeak MQTT API Documentation](https://www.mathworks.com/help/thingspeak/mqtt-api.html)
- [Node-RED Dashboard](https://flows.nodered.org/node/node-red-dashboard)
- [Paho MQTT Python Client](https://www.eclipse.org/paho/clients/python/)

