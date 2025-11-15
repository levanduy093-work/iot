# XÁC ĐỊNH CÁC THÔNG SỐ ĐẦU VÀO VÀ ĐẦU RA CỦA BÀI TOÁN THIẾT KẾ

## YÊU CẦU 1: XÁC ĐỊNH CÁC THÔNG SỐ ĐẦU VÀO VÀ ĐẦU RA CỦA BÀI TOÁN THIẾT KẾ

### a) Thông số của IoT Node:

#### **MCU sử dụng Raspberry Pi**
- **Model**: Raspberry Pi 4
- **Hệ điều hành**: Raspberry Pi OS (Linux)
- **Ngôn ngữ lập trình**: Python 3.x
- **Giao tiếp GPIO**: 40-pin GPIO header

#### **Cảm biến nhiệt độ và độ ẩm dùng Grove - Temperature & Humidity Sensor (DHT11)**, có thông số:

- **Nguồn cung cấp**: 5V DC
- **Loại cảm biến**: Digital dùng chuẩn giao tiếp **1-Wire Protocol**
- **Phạm vi đo**: 
  - Nhiệt độ: **0-50°C**
  - Độ ẩm: **0-100%RH**
- **Sai số**: 
  - Nhiệt độ: **±2°C**
  - Độ ẩm: **±5%RH**
- **Cách sử dụng**: 
  - Kết nối vào **GPIO pin D5** (GPIO 5) trên **Grove Base Hat for Raspberry Pi**
  - Sử dụng thư viện `seeed_dht` để đọc dữ liệu
  - Đọc dữ liệu: `humi, temp = sensor.read()`
  - Cảm biến tự động đo cả nhiệt độ và độ ẩm

#### **LCD Grove - LCD 16x2 I2C**

- **Loại**: Grove LCD 16x2 (White on Blue)
- **Giao tiếp**: I2C Protocol
- **Kích thước**: 16 cột x 2 dòng
- **Địa chỉ I2C**: 0x3E (mặc định)
- **Cách sử dụng**: 
  - Kết nối vào cổng I2C trên **Grove Base Hat for Raspberry Pi**
  - Sử dụng thư viện `grove.display.jhd1802`
  - Hiển thị nhiệt độ ở dòng 1, độ ẩm ở dòng 2 (tùy chọn - không bắt buộc trong đề bài)

#### **LED đỏ và vàng**

- **Loại**: Grove - LED Module
- **Điện áp hoạt động**: 3.3V - 5V
- **Giao tiếp**: Digital GPIO
- **Kết nối**:
  - **LED đỏ**: GPIO pin D16 (GPIO 16) trên **Grove Base Hat for Raspberry Pi** - dùng để cảnh báo nhiệt độ
  - **LED vàng**: GPIO pin D18 (GPIO 18) trên **Grove Base Hat for Raspberry Pi** - dùng để cảnh báo độ ẩm
- **Điều khiển**: 
  - Logic HIGH (1) = LED sáng
  - Logic LOW (0) = LED tắt

#### **Buzzer (Chuông)**

- **Loại**: Grove - Buzzer Module
- **Điện áp hoạt động**: 3.3V - 5V
- **Giao tiếp**: Digital GPIO
- **Kết nối**: GPIO pin D12 (GPIO 12) trên **Grove Base Hat for Raspberry Pi**
- **Chức năng**: Cảnh báo âm thanh
- **Điều khiển**: 
  - Logic HIGH (1) = Buzzer kêu
  - Logic LOW (0) = Buzzer tắt
- **Chế độ hoạt động**: 1 giây bip, 1 giây không và lặp lại khi nhiệt độ > 50°C

#### **Protocol truyền thông dùng MQTT**

- **Giao thức**: MQTT (Message Queuing Telemetry Transport)
- **Broker**: `mqtt3.thingspeak.com`
- **Port**: 1883 (non-TLS) hoặc 8883 (TLS)
- **Topic Publish**: `channels/[CHANNEL_ID]/publish`
- **Topic Subscribe**: `channels/[CHANNEL_ID]/subscribe/fields/field1` và `field2`
- **Xác thực**: Username và Password (MQTT Device Credentials từ ThingSpeak)
- **QoS**: 1 (At least once delivery)
- **Tần suất gửi**: Real-time (gửi ngay khi đọc được dữ liệu)

#### **Sử dụng kết nối WiFi của Raspberry để truyền thông từ IoT Node với Server**

- **Kết nối**: WiFi 802.11 b/g/n
- **Cấu hình**: Qua file `/etc/wpa_supplicant/wpa_supplicant.conf`
- **Yêu cầu**: Raspberry Pi phải được kết nối Internet để gửi dữ liệu lên ThingSpeak qua MQTT

#### **Hiển thị giá trị nhiệt độ và độ ẩm qua terminal (máy tính PC) và LCD sau mỗi giây**

- **Terminal**: In giá trị ra console mỗi khi đọc cảm biến
  - Format: `Nhiệt độ: XX°C | Độ ẩm: XX%`
  - Tần suất: Mỗi 10 giây (hoặc 1 giây nếu buzzer hoạt động)
- **LCD**: Hiển thị trên màn hình LCD 16x2 (tùy chọn)
  - Dòng 1: `temperature: XX C`
  - Dòng 2: `humidity: XX%`

#### **Xuất giá trị dữ liệu ra file Log dạng CSV để lưu trữ các sự kiện, thời gian, giá trị dữ liệu trung bình diễn ra trong quá trình hoạt động, mỗi sự kiện chiếm 1 dòng trong tập tin Log này**

- **Định dạng file**: CSV (Comma-Separated Values)
- **Tên file**: `iot_log.csv` hoặc `iot_log_YYYYMMDD.csv`
- **Cấu trúc file CSV**:
  ```csv
  Timestamp,Event,Temperature,Humidity,LED_Red,LED_Yellow,Buzzer,Status
  2024-01-15 10:30:00,READ_SENSOR,25.5,65.0,0,0,0,NORMAL
  2024-01-15 10:30:10,LED_RED_ON,42.0,60.0,1,0,0,HIGH_TEMP
  2024-01-15 10:30:20,LED_YELLOW_ON,35.0,75.0,1,1,0,HIGH_HUMI
  2024-01-15 10:30:30,BUZZER_ON,52.0,70.0,1,1,1,ALERT
  ```
- **Các trường dữ liệu**:
  - `Timestamp`: Thời gian sự kiện (YYYY-MM-DD HH:MM:SS)
  - `Event`: Loại sự kiện (READ_SENSOR, LED_RED_ON, LED_RED_OFF, LED_YELLOW_ON, LED_YELLOW_OFF, BUZZER_ON, BUZZER_OFF, SEND_DATA, ERROR)
  - `Temperature`: Giá trị nhiệt độ (°C)
  - `Humidity`: Giá trị độ ẩm (%)
  - `LED_Red`: Trạng thái LED đỏ (0 hoặc 1)
  - `LED_Yellow`: Trạng thái LED vàng (0 hoặc 1)
  - `Buzzer`: Trạng thái Buzzer (0 hoặc 1)
  - `Status`: Trạng thái hệ thống (NORMAL, HIGH_TEMP, HIGH_HUMI, ALERT, ERROR)

#### **Điều khiển:**

- **LED đỏ sáng khi**: Nhiệt độ > 40°C
- **LED đỏ tắt khi**: Nhiệt độ < 30°C
- **LED vàng sáng khi**: Độ ẩm > 70%
- **LED vàng tắt khi**: Độ ẩm < 40%
- **Chuông (Buzzer) kêu khi**: Nhiệt độ > 50°C
  - Chế độ: 1 giây bip, 1 giây không và lặp lại
  - Tự động tắt khi nhiệt độ ≤ 50°C

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
| T | float | 0-50 | Dữ liệu nhiệt độ (°C) |
| H | float | 0-100 | Dữ liệu độ ẩm (%RH) |
| Led_R | int | [0,1] | Trạng thái LED đỏ (0=Tắt, 1=Bật) |
| Led_Y | int | [0,1] | Trạng thái LED vàng (0=Tắt, 1=Bật) |
| Buzzer | int | [0,1] | Trạng thái Buzzer (0=Tắt, 1=Bật) |

**Mapping với ThingSpeak Fields:**
- **Field1**: T (Nhiệt độ)
- **Field2**: H (Độ ẩm)
- **Field3**: Led_R (LED đỏ) - tùy chọn
- **Field4**: Led_Y (LED vàng) - tùy chọn
- **Field5**: Buzzer (Buzzer) - tùy chọn

**Cấu trúc Channel ThingSpeak:**
- **Channel ID**: 3153408 (ví dụ)
- **MQTT Username**: Dg0MFSkPJAIJMgchHjw1BwY (ví dụ)
- **MQTT Client ID**: Dg0MFSkPJAIJMgchHjw1BwY (ví dụ)
- **MQTT Password**: 8p9YF6bT68Hxjny5ChF13Vrm (ví dụ)

**MQTT Topics:**
- **Publish Topic**: `channels/[CHANNEL_ID]/publish`
  - Payload format: `field1=XX&field2=XX&status=MQTTPUBLISH`
- **Subscribe Topics**: 
  - `channels/[CHANNEL_ID]/subscribe/fields/field1` (Nhiệt độ)
  - `channels/[CHANNEL_ID]/subscribe/fields/field2` (Độ ẩm)

##### **Thời gian gửi dữ liệu từ Cloud server xuống IoT node: 1s**

- **Lưu ý**: ThingSpeak MQTT hỗ trợ real-time data streaming
- **Giải pháp**: Node-RED sẽ **subscribe** các MQTT topics để nhận dữ liệu real-time từ ThingSpeak
- **Cơ chế**: MQTT Subscribe với QoS=1 để đảm bảo nhận được dữ liệu
- **Tần suất**: Real-time (nhận ngay khi có dữ liệu mới được publish)
- **Format message**: 
  ```json
  {
    "payload": "25.5",
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
| Cảm biến | Grove - Temperature & Humidity Sensor (DHT11) - GPIO D5 |
| Hiển thị | Grove - LCD 16x2 I2C (tùy chọn) |
| Điều khiển | 2x Grove - LED (Đỏ D16, Vàng D18) + Grove - Buzzer (D12) |
| Giao tiếp | MQTT Protocol |
| Broker | mqtt3.thingspeak.com:1883 |
| Kết nối | WiFi |
| Logging | File CSV |

### Server (ThingSpeak):

| Thông số | Giá trị |
|----------|---------|
| Platform | ThingSpeak |
| Protocol | MQTT |
| Broker | mqtt3.thingspeak.com:1883 |
| Fields | 2 fields chính (T: Nhiệt độ, H: Độ ẩm) |
| Tần suất gửi | Real-time (từ IoT node lên server) |
| Tần suất nhận | Real-time (từ server về Node-RED Dashboard - MQTT Subscribe) |

### Ngưỡng điều khiển:

| Thiết bị | Điều kiện BẬT | Điều kiện TẮT |
|----------|---------------|---------------|
| LED đỏ | Nhiệt độ > 40°C | Nhiệt độ < 30°C |
| LED vàng | Độ ẩm > 70% | Độ ẩm < 40% |
| Buzzer | Nhiệt độ > 50°C | Nhiệt độ ≤ 50°C |
| Buzzer Pattern | 1s ON, 1s OFF (lặp lại) | Tự động tắt khi nhiệt độ ≤ 50°C |

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
Payload: field1=25.5&field2=65.0&status=MQTTPUBLISH
```

**Subscribe trong Node-RED:**
```
Topic: channels/3153408/subscribe/fields/field1
Message: {"payload": "25.5", "topic": "..."}
```

### Node-RED Dashboard:

- **Gauge Nhiệt độ**: Hiển thị giá trị 0-100°C
- **Gauge Độ ẩm**: Hiển thị giá trị 0-100%
- **Cập nhật**: Real-time qua MQTT Subscribe
- **Truy cập**: `http://localhost:1880/ui`

