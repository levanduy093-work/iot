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
  - Cường độ ánh sáng: **0-1000** (giá trị ADC)
- **Sai số**: **±5%**
- **Cách sử dụng**: 
  - Kết nối vào **GPIO pin A0** (Analog Channel 0) trên **Grove Base Hat for Raspberry Pi**
  - Sử dụng thư viện `grove.adc` để đọc dữ liệu
  - Đọc dữ liệu: `light_value = light_sensor.value`
  - Giá trị trả về từ 0-1000, càng cao càng sáng

#### **Cảm biến khoảng cách dùng Grove - Ultrasonic Ranger**, có thông số:

- **Nguồn cung cấp**: 3.3V - 5V DC
- **Loại cảm biến**: Digital dùng chuẩn giao tiếp **GPIO Digital I/O**
- **Phạm vi đo**: 
  - Khoảng cách: **2-400 cm**
- **Sai số**: **±1 cm**
- **Cách sử dụng**: 
  - Kết nối vào **GPIO pin D5** (GPIO 5) trên **Grove Base Hat for Raspberry Pi**
  - Sử dụng thư viện `grove.grove_ultrasonic_ranger` để đọc dữ liệu
  - Đọc dữ liệu: `distance_value = ultrasonic_sensor.get_distance()`
  - Giá trị trả về đơn vị cm

#### **LCD Grove - LCD 16x2 I2C**

- **Loại**: Grove LCD 16x2 (White on Blue)
- **Giao tiếp**: I2C Protocol
- **Kích thước**: 16 cột x 2 dòng
- **Địa chỉ I2C**: 0x3E (mặc định)
- **Cách sử dụng**: 
  - Kết nối vào cổng I2C trên **Grove Base Hat for Raspberry Pi**
  - Sử dụng thư viện `grove.display.jhd1802`
  - Hiển thị cường độ ánh sáng ở dòng 1, khoảng cách ở dòng 2

#### **LED đỏ và vàng**

- **Loại**: Grove - LED Module
- **Điện áp hoạt động**: 3.3V - 5V
- **Giao tiếp**: Digital GPIO
- **Kết nối**:
  - **LED đỏ**: GPIO pin D16 (GPIO 16) trên **Grove Base Hat for Raspberry Pi**
  - **LED vàng**: GPIO pin D18 (GPIO 18) trên **Grove Base Hat for Raspberry Pi**
- **Điều khiển**: 
  - Logic HIGH (1) = LED sáng
  - Logic LOW (0) = LED tắt

#### **Buzzer (Chuông)**

- **Loại**: Grove - Buzzer Module
- **Điện áp hoạt động**: 3.3V - 5V
- **Giao tiếp**: Digital GPIO
- **Kết nối**: GPIO pin D12 (GPIO 12) trên **Grove Base Hat for Raspberry Pi**
- **Điều khiển**: 
  - Logic HIGH (1) = Buzzer kêu
  - Logic LOW (0) = Buzzer tắt

#### **Motor rung (Vibration Motor)**

- **Loại**: Grove - Vibration Motor Module
- **Điện áp hoạt động**: 3.3V - 5V
- **Giao tiếp**: Digital GPIO
- **Kết nối**: GPIO pin D13 (GPIO 13) trên **Grove Base Hat for Raspberry Pi**
- **Điều khiển**: 
  - Logic HIGH (1) = Motor rung
  - Logic LOW (0) = Motor tắt

#### **Protocol truyền thông dùng HTTP**

- **Giao thức**: HTTP/HTTPS
- **Phương thức**: POST (gửi dữ liệu lên server)
- **Endpoint**: `https://api.thingspeak.com/update`
- **Format dữ liệu**: `application/x-www-form-urlencoded`
- **Xác thực**: Sử dụng Write API Key trong header `X-THINGSPEAKAPIKEY`
- **Tần suất gửi**: Mỗi 10 giây (hoặc theo cấu hình)

#### **Sử dụng kết nối WiFi của Raspberry để truyền thông từ IoT Node với Server**

- **Kết nối**: WiFi 802.11 b/g/n
- **Cấu hình**: Qua file `/etc/wpa_supplicant/wpa_supplicant.conf`
- **Yêu cầu**: Raspberry Pi phải được kết nối Internet để gửi dữ liệu lên ThingSpeak

#### **Hiển thị giá trị cường độ ánh sáng và khoảng cách qua terminal (máy tính PC) và LCD sau mỗi 10 giây**

- **Terminal**: In giá trị ra console mỗi 10 giây
  - Format: `Cường độ ánh sáng: XXX | Khoảng cách: XX.X cm`
- **LCD**: Hiển thị trên màn hình LCD 16x2 mỗi 10 giây
  - Dòng 1: `Light: XXXX`
  - Dòng 2: `Dist: XX.Xcm`

#### **Xuất giá trị dữ liệu ra file Log dạng CSV để lưu trữ các sự kiện, thời gian, giá trị dữ liệu trung bình diễn ra trong quá trình hoạt động, mỗi sự kiện chiếm 1 dòng trong tập tin Log này**

- **Định dạng file**: CSV (Comma-Separated Values)
- **Tên file**: `iot_log.csv` hoặc `iot_log_YYYYMMDD.csv`
- **Cấu trúc file CSV**:
  ```csv
  Timestamp,Event,Light_Value,Distance,LED_Red,LED_Yellow,Buzzer,Vibration_Motor,Status
  2024-01-15 10:30:00,READ_SENSOR,450,35.5,0,0,0,0,NORMAL
  2024-01-15 10:30:10,LED_RED_ON,650,40.0,1,0,1,0,HIGH_LIGHT
  2024-01-15 10:30:20,LED_YELLOW_ON,500,15.0,0,1,0,1,CLOSE_DISTANCE
  ```
- **Các trường dữ liệu**:
  - `Timestamp`: Thời gian sự kiện (YYYY-MM-DD HH:MM:SS)
  - `Event`: Loại sự kiện (READ_SENSOR, LED_RED_ON, LED_RED_OFF, LED_YELLOW_ON, LED_YELLOW_OFF, BUZZER_ON, BUZZER_OFF, MOTOR_ON, MOTOR_OFF, SEND_DATA, ERROR)
  - `Light_Value`: Giá trị cường độ ánh sáng (0-1000)
  - `Distance`: Giá trị khoảng cách (cm)
  - `LED_Red`: Trạng thái LED đỏ (0 hoặc 1)
  - `LED_Yellow`: Trạng thái LED vàng (0 hoặc 1)
  - `Buzzer`: Trạng thái Buzzer (0 hoặc 1)
  - `Vibration_Motor`: Trạng thái Motor rung (0 hoặc 1)
  - `Status`: Trạng thái hệ thống (NORMAL, HIGH_LIGHT, CLOSE_DISTANCE, ALERT, ERROR)

#### **Điều khiển:**

- **LED đỏ sáng khi**: Cường độ ánh sáng > 600
- **LED đỏ tắt khi**: Cường độ ánh sáng < 400
- **Buzzer kêu khi**: Cường độ ánh sáng > 600 (hoạt động cùng LED đỏ)
- **Buzzer tắt khi**: Cường độ ánh sáng < 400
- **LED vàng sáng khi**: Khoảng cách < 20 cm
- **LED vàng tắt khi**: Khoảng cách > 40 cm
- **Motor rung khi**: Khoảng cách < 20 cm (hoạt động cùng LED vàng)
- **Motor rung tắt khi**: Khoảng cách > 40 cm

---

### b) Thông số của Server:

#### **Sử dụng platform ThingSpeak để thiết kế IoT server**

- **Platform**: ThingSpeak (MathWorks)
- **URL**: https://thingspeak.com
- **Giao thức**: HTTP REST API
- **Xác thực**: API Key (Write API Key và Read API Key)

#### **Cấu hình Server gồm:**

##### **Cơ sở dữ liệu:**

| Tên biến trạng thái | Kiểu dữ liệu | Phạm vi giá trị | Ghi chú |
|---------------------|--------------|-----------------|---------|
| L | int | 0-1000 | Dữ liệu cường độ ánh sáng |
| D | float | 2-400 | Dữ liệu khoảng cách (cm) |
| Led_R | int | [0,1] | Trạng thái LED đỏ (0=Tắt, 1=Bật) |
| Led_Y | int | [0,1] | Trạng thái LED vàng (0=Tắt, 1=Bật) |
| Buzzer | int | [0,1] | Trạng thái Buzzer (0=Tắt, 1=Bật) |
| Motor | int | [0,1] | Trạng thái Motor rung (0=Tắt, 1=Bật) |

**Mapping với ThingSpeak Fields:**
- **Field1**: L (Cường độ ánh sáng)
- **Field2**: D (Khoảng cách)
- **Field3**: Led_R (LED đỏ) - tùy chọn
- **Field4**: Led_Y (LED vàng) - tùy chọn
- **Field5**: Buzzer (Buzzer) - tùy chọn
- **Field6**: Motor (Motor rung) - tùy chọn

**Cấu trúc Channel ThingSpeak:**
- **Channel ID**: 3153408 (ví dụ)
- **Write API Key**: AHHO5UL59ZCYUYCV (ví dụ)
- **Read API Key**: N251PNZ5EG0MWI2Y (ví dụ)

##### **Thời gian gửi dữ liệu từ Cloud server xuống IoT node: 1s**

- **Lưu ý**: ThingSpeak không hỗ trợ gửi dữ liệu từ server xuống IoT node theo thời gian thực
- **Giải pháp**: Node-RED sẽ **polling** (lấy dữ liệu) từ ThingSpeak server mỗi 10 giây thông qua HTTP GET request để hiển thị trên Dashboard
- **Endpoint**: `https://api.thingspeak.com/channels/[CHANNEL_ID]/feeds.json?results=1&api_key=[READ_API_KEY]`
- **Format response**: JSON
- **Cấu trúc response**:
  ```json
  {
    "channel": {...},
    "feeds": [
      {
        "created_at": "2024-01-15T10:30:00Z",
        "entry_id": 12345,
        "field1": "650",
        "field2": "15.5"
      }
    ]
  }
  ```

---

## TÓM TẮT THÔNG SỐ KỸ THUẬT

### IoT Node (Raspberry Pi):

| Thành phần | Thông số |
|------------|----------|
| MCU | Raspberry Pi 4 |
| Cảm biến | Grove - Light Sensor (A0) + Grove - Ultrasonic Ranger (D5) |
| Hiển thị | Grove - LCD 16x2 I2C |
| Điều khiển | 2x Grove - LED (Đỏ D16, Vàng D18) + Grove - Buzzer (D12) + Grove - Vibration Motor (D13) |
| Giao tiếp | HTTP/HTTPS |
| Kết nối | WiFi |
| Logging | File CSV |

### Server (ThingSpeak):

| Thông số | Giá trị |
|----------|---------|
| Platform | ThingSpeak |
| Protocol | HTTP REST API |
| Fields | 2 fields chính (L: Ánh sáng, D: Khoảng cách) |
| Tần suất gửi | Mỗi 10 giây (từ IoT node lên server) |
| Tần suất nhận | Mỗi 10 giây (từ server về Node-RED Dashboard - polling) |

### Ngưỡng điều khiển:

| Thiết bị | Điều kiện BẬT | Điều kiện TẮT |
|----------|---------------|---------------|
| LED đỏ | Cường độ ánh sáng > 600 | Cường độ ánh sáng < 400 |
| Buzzer | Cường độ ánh sáng > 600 | Cường độ ánh sáng < 400 |
| LED vàng | Khoảng cách < 20 cm | Khoảng cách > 40 cm |
| Motor rung | Khoảng cách < 20 cm | Khoảng cách > 40 cm |

