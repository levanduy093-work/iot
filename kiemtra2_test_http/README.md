# Hệ thống Giám sát Ánh sáng và Khoảng cách với ThingSpeak HTTP

Dự án IoT sử dụng Raspberry Pi để đọc giá trị từ cảm biến ánh sáng và cảm biến khoảng cách, gửi dữ liệu lên ThingSpeak qua HTTP và điều khiển các thiết bị LED, buzzer, motor rung dựa trên ngưỡng giá trị.

## ✨ Tính năng

- **Đọc cảm biến ánh sáng**: Đọc giá trị từ Grove Light Sensor (A0)
- **Đọc cảm biến khoảng cách**: Đọc giá trị từ Grove Ultrasonic Ranger (D5)
- **Gửi dữ liệu lên ThingSpeak**: Gửi qua HTTP mỗi 10 giây
- **Hiển thị trên Terminal**: In giá trị cảm biến ra console
- **Hiển thị trên LCD 16x2**: Hiển thị ánh sáng và khoảng cách trên màn hình LCD
- **Điều khiển LED đỏ + Buzzer**: 
  - Bật khi cường độ ánh sáng > 600
  - Tắt khi cường độ ánh sáng < 400
- **Điều khiển LED vàng + Motor rung**:
  - Bật khi khoảng cách < 20 cm
  - Tắt khi khoảng cách > 40 cm
- **Dashboard Node-RED**: Hiển thị dữ liệu với Gauge và Bar chart

## 🛠️ Yêu cầu phần cứng

- **Raspberry Pi** (3B+, 4, hoặc Zero W)
- **Grove Base Hat** cho Raspberry Pi
- **Grove Light Sensor** (kết nối vào A0)
- **Grove Ultrasonic Ranger** (kết nối vào D5)
- **Grove LED đỏ** (kết nối vào D16)
- **Grove LED vàng** (kết nối vào D18)
- **Grove Buzzer** (kết nối vào D12)
- **Grove Vibration Motor** (kết nối vào D13)
- **Grove LCD 16x2 I2C** (kết nối vào I2C port)

## 📋 Yêu cầu phần mềm

- Python 3.x
- Thư viện Grove:
  - `grove.adc`
  - `grove.grove_ultrasonic_ranger`
  - `grove.display.jhd1802`
  - `grove.gpio`
- Node-RED với các node:
  - `node-red-dashboard`
  - `node-red-contrib-ui-chart` (cho Bar chart)

## 🔧 Cài đặt

### 1. Cài đặt thư viện Grove

```bash
# Cài đặt Grove Python libraries
git clone https://github.com/Seeed-Studio/grove.py
cd grove.py
sudo pip3 install .
```

### 2. Cấu hình ThingSpeak

1. Tạo tài khoản tại [ThingSpeak.com](https://thingspeak.com)
2. Tạo một Channel mới với 2 fields:
   - Field 1: Light (Ánh sáng)
   - Field 2: Distance (Khoảng cách)
3. Lấy **Write API Key** và **Read API Key**
4. Lấy **Channel ID**

### 3. Cấu hình chương trình Python

Mở file `send_data.py` và cập nhật thông tin ThingSpeak:

```python
# Tìm dòng này trong hàm main():
API_KEY_WRITE = "YOUR_WRITE_API_KEY_HERE"  # Thay bằng Write API Key của bạn
```

Thay `YOUR_WRITE_API_KEY_HERE` bằng Write API Key của bạn.

### 4. Cấu hình Node-RED Flow

1. Mở Node-RED: `http://localhost:1880`
2. Import file `node_red_flow.json`
3. Mở node "ThingSpeak API Request" và cập nhật:
   - `YOUR_CHANNEL_ID`: Thay bằng Channel ID của bạn
   - `YOUR_READ_API_KEY`: Thay bằng Read API Key của bạn
4. Deploy flow

## 🚀 Sử dụng

### Chạy chương trình Python

```bash
cd kiemtra2_test_http
python3 send_data.py
```

Chương trình sẽ:
- Đọc cảm biến mỗi 10 giây
- Hiển thị giá trị trên Terminal và LCD
- Gửi dữ liệu lên ThingSpeak mỗi 10 giây
- Điều khiển LED và buzzer/motor rung theo ngưỡng

### Xem Dashboard Node-RED

1. Mở trình duyệt: `http://localhost:1880/ui`
2. Dashboard sẽ hiển thị:
   - **Gauge**: Hiển thị giá trị ánh sáng và khoảng cách dạng đồng hồ
   - **Bar Chart**: Hiển thị biểu đồ cột cho ánh sáng và khoảng cách

## 📊 Cấu trúc dữ liệu ThingSpeak

- **Field 1**: Cường độ ánh sáng (0-1000)
- **Field 2**: Khoảng cách vật cản (cm)

## ⚙️ Ngưỡng điều khiển

### LED đỏ + Buzzer (theo ánh sáng)
- **Bật**: Khi ánh sáng > 600
- **Tắt**: Khi ánh sáng < 400
- **Trạng thái giữ nguyên**: Khi 400 ≤ ánh sáng ≤ 600

### LED vàng + Motor rung (theo khoảng cách)
- **Bật**: Khi khoảng cách < 20 cm
- **Tắt**: Khi khoảng cách > 40 cm
- **Trạng thái giữ nguyên**: Khi 20 cm ≤ khoảng cách ≤ 40 cm

## 🔌 Sơ đồ kết nối

```
Raspberry Pi + Grove Base Hat
├── A0  → Grove Light Sensor
├── D5  → Grove Ultrasonic Ranger
├── D12 → Grove Buzzer
├── D13 → Grove Vibration Motor
├── D16 → Grove LED đỏ
├── D18 → Grove LED vàng
└── I2C → Grove LCD 16x2
```

## 📝 Ghi chú

- ThingSpeak có giới hạn gửi dữ liệu: tối đa 1 lần mỗi 15 giây cho tài khoản miễn phí
- Nếu gặp lỗi khi đọc cảm biến, kiểm tra kết nối và đảm bảo Grove Base Hat được cài đặt đúng
- Để thay đổi pin kết nối, sửa các biến ở đầu file `send_data.py`

## 🐛 Xử lý lỗi

### Lỗi "Không thể đọc cảm biến"
- Kiểm tra kết nối Grove Base Hat
- Kiểm tra cảm biến có được cắm đúng port không
- Thử khởi động lại Raspberry Pi

### Lỗi "ThingSpeak update thất bại"
- Kiểm tra kết nối Internet
- Xác nhận API Key đúng
- Kiểm tra Channel ID đúng
- Đảm bảo đã đợi đủ 15 giây giữa các lần gửi (tài khoản miễn phí)

### LCD không hiển thị
- Kiểm tra kết nối I2C
- Chạy lệnh: `sudo i2cdetect -y 1` để kiểm tra địa chỉ I2C
- Đảm bảo Grove LCD được cấp nguồn đúng

## 📚 Tài liệu tham khảo

- [Grove Python Libraries](https://github.com/Seeed-Studio/grove.py)
- [ThingSpeak API Documentation](https://www.mathworks.com/help/thingspeak/)
- [Node-RED Dashboard](https://flows.nodered.org/node/node-red-dashboard)

