# Hệ thống giám sát ánh sáng và khoảng cách với ThingSpeak MQTT

## 📋 Mô tả

Hệ thống IoT sử dụng Raspberry Pi để:
- Đọc giá trị từ cảm biến ánh sáng và cảm biến khoảng cách siêu âm
- Gửi dữ liệu lên ThingSpeak qua giao thức MQTT
- Hiển thị dữ liệu trên Terminal và LCD 16x2 mỗi 20 giây
- Điều khiển LED, buzzer và motor rung dựa trên giá trị cảm biến
- Hiển thị dữ liệu trên giao diện web Node-RED Dashboard với Gauge và Bar chart

## 🎯 Yêu cầu chức năng

### Điều khiển LED và Buzzer
- **Blue Light và Buzzer**: 
  - Bật khi cường độ ánh sáng > 500
  - Tắt khi cường độ ánh sáng < 200
  - Giữ nguyên trạng thái khi 200 ≤ ánh sáng ≤ 500

### Điều khiển LED vàng và Motor rung
- **LED vàng và Motor rung**:
  - Bật khi khoảng cách < 20 cm
  - Tắt khi khoảng cách > 40 cm
  - Giữ nguyên trạng thái khi 20 ≤ khoảng cách ≤ 40 cm

## 🛠️ Phần cứng yêu cầu

- **Raspberry Pi** (3B+, 4, hoặc Zero W)
- **Grove Base Hat** cho Raspberry Pi
- **Cảm biến ánh sáng Grove** (kết nối port A0)
- **Cảm biến khoảng cách siêu âm Grove** (kết nối port D5)
- **Blue Light Grove** (kết nối port D16)
- **LED vàng Grove** (kết nối port D18)
- **Buzzer Grove** (kết nối port D12)
- **Motor rung Grove** (kết nối port D22)
- **LCD 16x2 I2C Grove** (kết nối I2C port)

## 📦 Cài đặt phần mềm

### 1. Cài đặt thư viện Python

```bash
pip install paho-mqtt grove.py grove-display
```

### 2. Kích hoạt I2C (cho LCD)

```bash
sudo raspi-config
# Chọn: Interface Options > I2C > Enable
sudo reboot
```

### 3. Cấu hình ThingSpeak MQTT

1. Đăng nhập vào [ThingSpeak](https://thingspeak.com)
2. Tạo Channel mới với các field:
   - **Field 1 (L)**: Light Intensity (Cường độ ánh sáng)
   - **Field 2 (D)**: Distance (Khoảng cách)
3. Lấy **MQTT Device Credentials**:
   - **Write Credentials** (để publish): Lưu vào `send_data_mqtt_key.txt` ở thư mục gốc
   - **Read Credentials** (để subscribe): Lưu vào `receive_data_mqtt_key.txt` ở thư mục gốc
4. Format file key:
   ```
   username = YOUR_USERNAME
   clientId = YOUR_CLIENT_ID
   password = YOUR_PASSWORD
   ```
5. Chương trình Python sẽ tự động đọc từ `send_data_mqtt_key.txt`
6. Node-RED flow đã được cấu hình với credentials từ `receive_data_mqtt_key.txt`

## 🚀 Sử dụng

### Chạy chương trình Python

```bash
cd /home/duy/iot/kiemtra2
python send_data.py
```

**Chức năng**:
- Đọc cảm biến ánh sáng và khoảng cách mỗi 1 giây
- Điều khiển LED và buzzer/motor rung theo logic
- Hiển thị trên Terminal và LCD mỗi 20 giây
- Gửi dữ liệu lên ThingSpeak qua MQTT mỗi 20 giây

**Output Terminal**:
```
============================================================
HỆ THỐNG GIÁM SÁT ÁNH SÁNG VÀ KHOẢNG CÁCH
============================================================
Đọc cảm biến mỗi 1 giây
Hiển thị và gửi dữ liệu mỗi 20 giây
============================================================
✓ Đã kết nối MQTT thành công

============================================================
Thời gian: 2024-01-15 10:30:00
Cường độ ánh sáng: 650
Khoảng cách: 15.5 cm
Blue Light: BẬT
Buzzer: BẬT
LED vàng: BẬT
Motor rung: BẬT
============================================================
✓ Đã gửi dữ liệu lên ThingSpeak
```

### Thiết lập Node-RED Dashboard

#### Bước 1: Cài đặt Node-RED Dashboard

1. Mở Node-RED: `http://localhost:1880`
2. Click menu (☰) > **Manage palette**
3. Vào tab **Install**
4. Tìm và cài đặt: `node-red-dashboard`
5. Restart Node-RED nếu cần

#### Bước 2: Import Flow

1. Trong Node-RED, click menu (☰) > **Import**
2. Copy toàn bộ nội dung file `node_red_flow.json`
3. Paste vào ô import
4. Click **Import**
5. **Cập nhật MQTT Broker**:
   - Double-click vào node **ThingSpeak MQTT**
   - Cập nhật thông tin MQTT credentials của bạn
   - Click **Update**
6. Click **Deploy** để kích hoạt flow

#### Bước 3: Truy cập Dashboard

1. Sau khi deploy, click vào icon **🌐** ở góc trên bên phải
2. Hoặc truy cập trực tiếp: `http://localhost:1880/ui`
3. Bạn sẽ thấy giao diện web với:
   - **Gauge Cường độ ánh sáng** (0-1000)
   - **Gauge Khoảng cách** (0-200 cm)
   - **Bar Chart Cường độ ánh sáng**
   - **Bar Chart Khoảng cách**

## 📊 Cấu trúc Flow Node-RED

```
[MQTT Subscribe Light] ──> [Parse Light] ──> [Gauge Light]
                                      └─> [Bar Chart Light]
                                      └─> [Debug Light]

[MQTT Subscribe Distance] ──> [Parse Distance] ──> [Gauge Distance]
                                          └─> [Bar Chart Distance]
                                          └─> [Debug Distance]
```

### Các thành phần:

1. **MQTT Broker**: Kết nối với ThingSpeak MQTT server
2. **MQTT In Nodes**: Subscribe các topic:
   - `channels/3153408/subscribe/fields/field1` (Field 1 - L: Cường độ ánh sáng)
   - `channels/3153408/subscribe/fields/field2` (Field 2 - D: Khoảng cách)
3. **Function Nodes**: Parse và chuyển đổi dữ liệu
4. **UI Gauge**: Hiển thị giá trị dạng gauge
5. **UI Chart (Bar)**: Hiển thị biểu đồ cột
6. **Debug Nodes**: Hiển thị dữ liệu trong Debug panel

## 🔧 Cấu hình Pin

| Component | Port | GPIO Pin | Mô tả |
|-----------|------|----------|-------|
| Light Sensor | A0 | ADC Channel 0 | Cảm biến ánh sáng (0-1000) |
| Ultrasonic | D5 | GPIO5 | Cảm biến khoảng cách (cm) |
| Blue Light | D16 | GPIO16 | Điều khiển theo ánh sáng |
| LED Vàng | D18 | GPIO18 | Điều khiển theo khoảng cách |
| Buzzer | D12 | GPIO12 | Cảnh báo ánh sáng |
| Motor Rung | D22 | GPIO22 | Cảnh báo khoảng cách |
| LCD | I2C | I2C Bus | Hiển thị dữ liệu |

## 📝 Logic điều khiển

### Blue Light + Buzzer
```
if light_value > 500:
    Blue Light ON
    Buzzer ON
elif light_value < 200:
    Blue Light OFF
    Buzzer OFF
else:
    Giữ nguyên trạng thái
```

### LED Vàng + Motor Rung
```
if distance < 20 cm:
    LED vàng ON
    Motor rung ON
elif distance > 40 cm:
    LED vàng OFF
    Motor rung OFF
else:
    Giữ nguyên trạng thái
```

## 🔍 Troubleshooting

### Lỗi không đọc được cảm biến ánh sáng
- Kiểm tra kết nối port A0
- Kiểm tra Grove Base Hat đã được lắp đúng
- Kiểm tra ADC đã được khởi tạo đúng (address=0x08)

### Lỗi không đọc được cảm biến khoảng cách
- Kiểm tra kết nối port D5
- Đảm bảo không có vật cản trước cảm biến
- Kiểm tra nguồn điện đủ mạnh

### Lỗi kết nối MQTT
- Kiểm tra internet connection
- Kiểm tra MQTT credentials đúng chưa
- Kiểm tra Channel ID đúng chưa
- Kiểm tra firewall không chặn port 1883

### LCD không hiển thị
- Kiểm tra I2C đã được kích hoạt (`sudo raspi-config`)
- Kiểm tra kết nối I2C
- Kiểm tra địa chỉ I2C của LCD

### Node-RED không nhận được dữ liệu
- Kiểm tra MQTT Broker đã kết nối thành công
- Kiểm tra Topic subscribe đúng chưa
- Kiểm tra chương trình Python đang chạy và gửi dữ liệu
- Xem Debug panel để kiểm tra dữ liệu nhận được

## 📄 File trong dự án

- `send_data.py`: Chương trình Python chính
- `node_red_flow.json`: File cấu hình Node-RED flow
- `README.md`: Tài liệu hướng dẫn này

## 📞 Thông tin ThingSpeak

**Lưu ý**: Cần thay đổi các thông tin sau trong code theo Channel của bạn:
- Channel ID
- MQTT Username
- MQTT Client ID
- MQTT Password

## 🎓 Kiến thức cần thiết

- Python cơ bản
- Raspberry Pi GPIO
- MQTT protocol
- Node-RED cơ bản
- Grove sensors và actuators

---

**Tác giả**: Dự án IoT  
**Ngày tạo**: 2024  
**Phiên bản**: 1.0

