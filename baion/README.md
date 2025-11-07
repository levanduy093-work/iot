# HƯỚNG DẪN SỬ DỤNG - CHƯƠNG TRÌNH IOT THINGSPEAK

## 📋 Tổng quan

Dự án gồm 2 chương trình chính:
- **Chương trình 1**: Gửi dữ liệu DHT11 lên ThingSpeak
- **Chương trình 2**: Nhận dữ liệu từ ThingSpeak và ghi log

---

## 📤 CHƯƠNG TRÌNH 1: GỬI DỮ LIỆU

### File: `send_data_http_mqtt.py`

**Chức năng:**
- Đọc cảm biến DHT11 mỗi 1 giây trong 20 giây
- Loại bỏ giá trị không hợp lệ
- Tính trung bình nhiệt độ và độ ẩm
- Gửi lên ThingSpeak mỗi 20 giây qua **CẢ HTTP và MQTT**

**Dữ liệu gửi:**
- **HTTP**: field1 (temperature), field2 (humidity)
- **MQTT**: field3 (temperature), field4 (humidity)
- **Channel**: 3127848 (Test_Data_Server)

**Cách chạy:**
```bash
cd /home/duy/iot/baion
python3 send_data_http_mqtt.py
```

**Lưu ý:** 
- Chương trình chạy liên tục, nhấn Ctrl+C để dừng
- Cần kết nối cảm biến DHT11 vào cổng D5

---

## 📥 CHƯƠNG TRÌNH 2: NHẬN DỮ LIỆU

### File 1: `receive_data_http.py` - Nhận qua HTTP

**Chức năng:**
- Đọc dữ liệu từ ThingSpeak qua HTTP mỗi 1 giây
- Hiển thị ra Terminal
- Ghi log vào file `receive_http_log.csv`

**Dữ liệu đọc:**
- **field1**: Nhiệt độ (từ HTTP)
- **field2**: Độ ẩm (từ HTTP)
- **Channel**: 3127848

**Cách chạy:**
```bash
cd /home/duy/iot/baion
python3 receive_data_http.py
```

**File log:** `receive_http_log.csv`
```csv
Thời gian,Nhiệt độ (°C),Độ ẩm (%),Sự kiện
2025-11-08 00:13:14,30.0,70.06,Đọc dữ liệu thành công
```

---

### File 2: `receive_data_mqtt.py` - Nhận qua MQTT

**Chức năng:**
- Subscribe (đăng ký) nhận dữ liệu từ ThingSpeak qua MQTT
- Tự động hiển thị khi có dữ liệu mới
- Ghi log vào file `receive_mqtt_log.csv`

**Dữ liệu đọc:**
- **field3**: Nhiệt độ (từ MQTT)
- **field4**: Độ ẩm (từ MQTT)
- **Channel**: 3127848

**Cách chạy:**
```bash
cd /home/duy/iot/baion
python3 receive_data_mqtt.py
```

**File log:** `receive_mqtt_log.csv`

---

## 🚀 CÁCH SỬ DỤNG TOÀN BỘ HỆ THỐNG

### Bước 1: Chạy chương trình GỬI dữ liệu
```bash
# Terminal 1
cd /home/duy/iot/baion
python3 send_data_http_mqtt.py
```

### Bước 2: Chạy chương trình NHẬN dữ liệu qua HTTP
```bash
# Terminal 2
cd /home/duy/iot/baion
python3 receive_data_http.py
```

### Bước 3: Chạy chương trình NHẬN dữ liệu qua MQTT
```bash
# Terminal 3
cd /home/duy/iot/baion
python3 receive_data_mqtt.py
```

---

## 📊 THÔNG TIN THINGSPEAK

**Channel:** Test_Data_Server
- **Channel ID**: 3127848
- **Author**: mwa0000039454674
- **Write API Key**: AHHO5UL59ZCYUYCV
- **Read API Key**: N251PNZ5EG0MWI2Y

**Cấu trúc Field:**
- **field1**: temperature_http (Nhiệt độ từ HTTP)
- **field2**: humidity_http (Độ ẩm từ HTTP)
- **field3**: temperature_mqtt (Nhiệt độ từ MQTT)
- **field4**: humidity_mqtt (Độ ẩm từ MQTT)

**Xem dữ liệu trực tuyến:**
https://thingspeak.mathworks.com/channels/3127848

---

## 📝 FILE LOG

Mỗi chương trình tạo file log riêng với format CSV:

| Thời gian | Nhiệt độ (°C) | Độ ẩm (%) | Sự kiện |
|-----------|---------------|-----------|---------|
| 2025-11-08 10:30:15 | 25.5 | 60.2 | Đọc dữ liệu thành công |

**Các sự kiện được ghi:**
- Khởi động chương trình
- Kết nối MQTT thành công/thất bại
- Đọc dữ liệu thành công
- Lỗi đọc dữ liệu
- Dừng chương trình

---

## ⚠️ LƯU Ý

1. **ThingSpeak giới hạn**: Tối đa 1 request mỗi 15 giây cho free account
2. **Chương trình gửi phải chạy trước** để có dữ liệu nhận về
3. **Cảm biến DHT11** phải kết nối đúng cổng D5
4. **File log** được tạo tự động trong thư mục `baion/`
5. Nhấn **Ctrl+C** để dừng bất kỳ chương trình nào

---

## 🐛 TROUBLESHOOTING

**Lỗi: GPIO not allocated**
- Chỉ chạy 1 chương trình sử dụng DHT11 tại 1 thời điểm

**Lỗi: No data received (MQTT)**
- Đảm bảo chương trình gửi đang chạy
- Kiểm tra field3, field4 trên ThingSpeak có dữ liệu chưa

**Lỗi: File not found (log file)**
- File log được tạo tự động lần chạy đầu tiên
- Đảm bảo quyền ghi trong thư mục baion/

---

## 📞 THÔNG TIN

- **Author**: mwa0000039454674
- **Project**: IoT Data Logger with ThingSpeak
- **Date**: November 2025
