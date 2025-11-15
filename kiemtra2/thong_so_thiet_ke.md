# XÁC ĐỊNH CÁC THÔNG SỐ ĐẦU VÀO VÀ ĐẦU RA CỦA BÀI TOÁN THIẾT KẾ

## YÊU CẦU 1: XÁC ĐỊNH CÁC THÔNG SỐ ĐẦU VÀO VÀ ĐẦU RA CỦA BÀI TOÁN THIẾT KẾ

### a) Thông số của IoT Node:

#### **MCU sử dụng Raspberry Pi**
- **Model**: Raspberry Pi 4
- **Hệ điều hành**: Raspberry Pi OS (Linux)
- **Ngôn ngữ lập trình**: Python 3.x
- **Giao tiếp GPIO**: 40-pin GPIO header

#### **Cảm biến ánh sáng dùng Grove - Light Sensor**, có thông số:

- **Nguồn cung cấp**: 3.3V - 5V DC
- **Loại cảm biến**: Analog dùng chuẩn giao tiếp **ADC (Analog-to-Digital Converter)**
- **Phạm vi đo**: 
  - Giá trị ADC: **0-1000** (tỷ lệ 0.1%)
  - Điện áp tương ứng: **0-3.3V**
- **Sai số**: Phụ thuộc vào độ phân giải ADC (12-bit)
- **Cách sử dụng**: 
  - Kết nối vào **Port A0 (Analog)** trên **Grove Base Hat for Raspberry Pi**
  - Sử dụng thư viện `grove.adc.ADC` để đọc dữ liệu
  - Đọc dữ liệu: `light_value = light_sensor.value` (trả về 0-1000)
  - ADC address: 0x08 (mặc định)

#### **Cảm biến khoảng cách siêu âm dùng Grove - Ultrasonic Ranger**, có thông số:

- **Nguồn cung cấp**: 5V DC
- **Loại cảm biến**: Digital dùng chuẩn giao tiếp **Ultrasonic Pulse**
- **Phạm vi đo**: 
  - Khoảng cách: **2-400 cm**
  - Độ chính xác: **±3%**
- **Sai số**: Phụ thuộc vào điều kiện môi trường và vật cản
- **Cách sử dụng**: 
  - Kết nối vào **GPIO pin D5** (GPIO 5) trên **Grove Base Hat for Raspberry Pi**
  - Sử dụng class `GroveUltrasonicRanger` để đọc dữ liệu
  - Đọc dữ liệu: `distance = ultrasonic.get_distance()` (trả về khoảng cách cm)
  - Nguyên lý: Phát sóng siêu âm và đo thời gian phản hồi

#### **LCD Grove - LCD 16x2 I2C**

- **Loại**: Grove LCD 16x2 (White on Blue)
- **Giao tiếp**: I2C Protocol
- **Kích thước**: 16 cột x 2 dòng
- **Địa chỉ I2C**: 0x3E (mặc định)
- **Cách sử dụng**: 
  - Kết nối vào cổng I2C trên **Grove Base Hat for Raspberry Pi**
  - Sử dụng thư viện `grove.display.jhd1802`
  - Hiển thị cường độ ánh sáng ở dòng 1, khoảng cách ở dòng 2
  - Format: `Light: XXXX` và `Dist: XX.Xcm`

#### **Blue Light (LED xanh)**

- **Loại**: Grove - LED Module
- **Điện áp hoạt động**: 3.3V - 5V
- **Giao tiếp**: Digital GPIO
- **Kết nối**: GPIO pin D16 (GPIO 16) trên **Grove Base Hat for Raspberry Pi** - dùng để cảnh báo ánh sáng
- **Điều khiển**: 
  - Logic HIGH (1) = LED sáng
  - Logic LOW (0) = LED tắt

#### **LED vàng**

- **Loại**: Grove - LED Module
- **Điện áp hoạt động**: 3.3V - 5V
- **Giao tiếp**: Digital GPIO
- **Kết nối**: GPIO pin D18 (GPIO 18) trên **Grove Base Hat for Raspberry Pi** - dùng để cảnh báo khoảng cách
- **Điều khiển**: 
  - Logic HIGH (1) = LED sáng
  - Logic LOW (0) = LED tắt

#### **Buzzer (Chuông)**

- **Loại**: Grove - Buzzer Module
- **Điện áp hoạt động**: 3.3V - 5V
- **Giao tiếp**: Digital GPIO
- **Kết nối**: GPIO pin D12 (GPIO 12) trên **Grove Base Hat for Raspberry Pi**
- **Chức năng**: Cảnh báo âm thanh khi ánh sáng quá mạnh
- **Điều khiển**: 
  - Logic HIGH (1) = Buzzer kêu
  - Logic LOW (0) = Buzzer tắt

#### **Motor rung (Vibration Motor)**

- **Loại**: Grove - Vibration Motor Module
- **Điện áp hoạt động**: 3.3V - 5V
- **Giao tiếp**: Digital GPIO
- **Kết nối**: GPIO pin D22 (GPIO 22) trên **Grove Base Hat for Raspberry Pi**
- **Chức năng**: Cảnh báo rung khi vật cản quá gần
- **Điều khiển**: 
  - Logic HIGH (1) = Motor rung
  - Logic LOW (0) = Motor tắt

#### **Protocol truyền thông dùng MQTT**

- **Giao thức**: MQTT (Message Queuing Telemetry Transport)
- **Broker**: `mqtt3.thingspeak.com`
- **Port**: 1883 (non-TLS) hoặc 8883 (TLS)
- **Topic Publish**: `channels/[CHANNEL_ID]/publish`
- **Topic Subscribe**: `channels/[CHANNEL_ID]/subscribe/fields/field1` và `field2`
- **Xác thực**: Username và Password (MQTT Device Credentials từ ThingSpeak)
  - **Write Credentials**: Đọc từ file `send_data_mqtt_key.txt` (để publish)
  - **Read Credentials**: Đọc từ file `receive_data_mqtt_key.txt` (để subscribe)
- **QoS**: 1 (At least once delivery)
- **Tần suất gửi**: Mỗi 20 giây (hiển thị và gửi dữ liệu)

#### **Sử dụng kết nối WiFi của Raspberry để truyền thông từ IoT Node với Server**

- **Kết nối**: WiFi 802.11 b/g/n
- **Cấu hình**: Qua file `/etc/wpa_supplicant/wpa_supplicant.conf`
- **Yêu cầu**: Raspberry Pi phải được kết nối Internet để gửi dữ liệu lên ThingSpeak qua MQTT

#### **Hiển thị giá trị cường độ ánh sáng và khoảng cách qua terminal (máy tính PC) và LCD sau mỗi 20 giây**

- **Terminal**: In giá trị ra console mỗi 20 giây
  - Format: 
    ```
    ============================================================
    Thời gian: YYYY-MM-DD HH:MM:SS
    Cường độ ánh sáng: XXX
    Khoảng cách: XX.X cm
    Blue Light: BẬT/TẮT
    Buzzer: BẬT/TẮT
    LED vàng: BẬT/TẮT
    Motor rung: BẬT/TẮT
    ============================================================
    ```
  - Tần suất: Mỗi 20 giây
- **LCD**: Hiển thị trên màn hình LCD 16x2 mỗi 20 giây
  - Dòng 1: `Light: XXXX`
  - Dòng 2: `Dist: XX.Xcm`

#### **Điều khiển:**

- **Blue Light và Buzzer**:
  - **Bật khi**: Cường độ ánh sáng > 500
  - **Tắt khi**: Cường độ ánh sáng < 200
  - **Giữ nguyên trạng thái**: Khi 200 ≤ ánh sáng ≤ 500

- **LED vàng và Motor rung**:
  - **Bật khi**: Khoảng cách < 20 cm
  - **Tắt khi**: Khoảng cách > 40 cm
  - **Giữ nguyên trạng thái**: Khi 20 ≤ khoảng cách ≤ 40 cm

---

### b) Thông số của Server:

#### **Sử dụng platform ThingSpeak để thiết kế IoT server**

- **Platform**: ThingSpeak (MathWorks)
- **URL**: https://thingspeak.com
- **Giao thức**: MQTT Protocol
- **Broker**: `mqtt3.thingspeak.com:1883`
- **Xác thực**: MQTT Device Credentials (Username, Password, Client ID)

#### **Cấu hình Server gồm:**

##### **Cơ sở dữ liệu:**

| Tên biến trạng thái | Kiểu dữ liệu | Phạm vi giá trị | Ghi chú |
|---------------------|--------------|-----------------|---------|
| L | int | 0-1000 | Dữ liệu cường độ ánh sáng (Field 1) |
| D | float | 0-400 | Dữ liệu khoảng cách (cm) (Field 2) |

**Mapping với ThingSpeak Fields:**
- **Field 1 (L)**: Cường độ ánh sáng (0-1000)
- **Field 2 (D)**: Khoảng cách (cm)

**Cấu trúc Channel ThingSpeak:**
- **Channel ID**: 3153408
- **MQTT Write Username**: Đọc từ `send_data_mqtt_key.txt`
- **MQTT Write Client ID**: Đọc từ `send_data_mqtt_key.txt`
- **MQTT Write Password**: Đọc từ `send_data_mqtt_key.txt`
- **MQTT Read Username**: Đọc từ `receive_data_mqtt_key.txt`
- **MQTT Read Client ID**: Đọc từ `receive_data_mqtt_key.txt`
- **MQTT Read Password**: Đọc từ `receive_data_mqtt_key.txt`

**MQTT Topics:**
- **Publish Topic**: `channels/[CHANNEL_ID]/publish`
  - Payload format: `field1=XXX&field2=XX.X&status=MQTTPUBLISH`
- **Subscribe Topics**: 
  - `channels/[CHANNEL_ID]/subscribe/fields/field1` (Cường độ ánh sáng - L)
  - `channels/[CHANNEL_ID]/subscribe/fields/field2` (Khoảng cách - D)

##### **Thời gian gửi dữ liệu từ Cloud server xuống IoT node: Real-time**

- **Lưu ý**: ThingSpeak MQTT hỗ trợ real-time data streaming
- **Giải pháp**: Node-RED sẽ **subscribe** các MQTT topics để nhận dữ liệu real-time từ ThingSpeak
- **Cơ chế**: MQTT Subscribe với QoS=1 để đảm bảo nhận được dữ liệu
- **Tần suất**: Real-time (nhận ngay khi có dữ liệu mới được publish)
- **Format message**: 
  ```json
  {
    "payload": "650",
    "topic": "channels/3153408/subscribe/fields/field1",
    "timestamp": "2024-01-15T10:30:00Z"
  }
  ```

---

## TÓM TẮT THÔNG SỐ KỸ THUẬT

### IoT Node (Raspberry Pi):

| Thành phần | Thông số |
|------------|----------|
| MCU | Raspberry Pi 4 |
| Cảm biến ánh sáng | Grove - Light Sensor - Port A0 (Analog) |
| Cảm biến khoảng cách | Grove - Ultrasonic Ranger - GPIO D5 |
| Hiển thị | Grove - LCD 16x2 I2C |
| Điều khiển | Grove - Blue Light (D16) + Grove - Buzzer (D12) + Grove - LED vàng (D18) + Grove - Motor rung (D22) |
| Giao tiếp | MQTT Protocol |
| Broker | mqtt3.thingspeak.com:1883 |
| Kết nối | WiFi |
| Tần suất đọc cảm biến | Mỗi 1 giây |
| Tần suất hiển thị/gửi | Mỗi 20 giây |

### Server (ThingSpeak):

| Thông số | Giá trị |
|----------|---------|
| Platform | ThingSpeak |
| Protocol | MQTT |
| Broker | mqtt3.thingspeak.com:1883 |
| Fields | 2 fields (L: Cường độ ánh sáng, D: Khoảng cách) |
| Tần suất gửi | Mỗi 20 giây (từ IoT node lên server) |
| Tần suất nhận | Real-time (từ server về Node-RED Dashboard - MQTT Subscribe) |

### Ngưỡng điều khiển:

| Thiết bị | Điều kiện BẬT | Điều kiện TẮT | Giữ nguyên |
|----------|---------------|---------------|------------|
| Blue Light + Buzzer | Ánh sáng > 500 | Ánh sáng < 200 | 200 ≤ ánh sáng ≤ 500 |
| LED vàng + Motor rung | Khoảng cách < 20 cm | Khoảng cách > 40 cm | 20 ≤ khoảng cách ≤ 40 cm |

### Ưu điểm của MQTT so với HTTP:

| Đặc điểm | MQTT | HTTP |
|----------|------|------|
| Giao thức | Lightweight, binary | Text-based |
| Real-time | Có (push-based) | Không (polling) |
| Hiệu quả | Tiết kiệm băng thông | Tốn băng thông hơn |
| Kết nối | Persistent connection | Request/Response |
| QoS | Hỗ trợ (0, 1, 2) | Không hỗ trợ |
| Tần suất | Real-time | Phụ thuộc polling interval |

### Cấu trúc MQTT Message:

**Publish từ IoT Node:**
```
Topic: channels/3153408/publish
Payload: field1=650&field2=15.5&status=MQTTPUBLISH
```

**Subscribe trong Node-RED:**
```
Topic: channels/3153408/subscribe/fields/field1
Message: {"payload": "650", "topic": "..."}

Topic: channels/3153408/subscribe/fields/field2
Message: {"payload": "15.5", "topic": "..."}
```

### Node-RED Dashboard:

- **Gauge Cường độ ánh sáng**: Hiển thị giá trị 0-1000
- **Gauge Khoảng cách**: Hiển thị giá trị 0-200 cm
- **Bar Chart Cường độ ánh sáng**: Biểu đồ cột với Y-axis 0-1000
- **Bar Chart Khoảng cách**: Biểu đồ cột với Y-axis 0-200 cm
- **Cập nhật**: Real-time qua MQTT Subscribe
- **Truy cập**: `http://localhost:1880/ui`

### Mapping Pin Grove Base Hat:

| Component | Port | GPIO Pin | Loại | Mô tả |
|-----------|------|----------|------|-------|
| Light Sensor | A0 | ADC Channel 0 | Analog | Cảm biến ánh sáng (0-1000) |
| Ultrasonic | D5 | GPIO5 | Digital | Cảm biến khoảng cách (cm) |
| Blue Light | D16 | GPIO16 | Digital Output | Điều khiển theo ánh sáng |
| LED Vàng | D18 | GPIO18 | Digital Output | Điều khiển theo khoảng cách |
| Buzzer | D12 | GPIO12 | Digital Output | Cảnh báo ánh sáng |
| Motor Rung | D22 | GPIO22 | Digital Output | Cảnh báo khoảng cách |
| LCD | I2C | I2C Bus | I2C | Hiển thị dữ liệu |

