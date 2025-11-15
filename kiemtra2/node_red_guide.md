# Hướng dẫn thiết lập Node-RED Dashboard

## Yêu cầu

Tạo giao diện web dùng Node-RED để hiển thị:
- **Cường độ ánh sáng** từ ThingSpeak (Field 1) - hiển thị bằng Gauge và Bar chart
- **Khoảng cách** từ ThingSpeak (Field 2) - hiển thị bằng Gauge và Bar chart

**Sử dụng MQTT** để nhận dữ liệu real-time từ ThingSpeak.

## Thông tin kết nối ThingSpeak MQTT

**Lưu ý**: Node-RED sử dụng credentials từ file `receive_data_mqtt_key.txt` để subscribe dữ liệu từ ThingSpeak.

- **Channel ID**: `3153408` (thay đổi theo Channel của bạn)
- **MQTT Server**: `mqtt3.thingspeak.com`
- **Port**: `1883`
- **Username**: `IRU6PSACOwQPHy4PKiczCiI` (từ receive_data_mqtt_key.txt)
- **Client ID**: `IRU6PSACOwQPHy4PKiczCiI` (từ receive_data_mqtt_key.txt)
- **Password**: `gHzqnX35vjOPS0jeNUVtBdfV` (từ receive_data_mqtt_key.txt)

## Topic MQTT để Subscribe

ThingSpeak publish dữ liệu qua các topic sau:
- `channels/3153408/subscribe/fields/field1` - Field 1 (L): Cường độ ánh sáng
- `channels/3153408/subscribe/fields/field2` - Field 2 (D): Khoảng cách

## Cài đặt

### Bước 1: Cài đặt Node-RED (nếu chưa có)

```bash
# Cài đặt Node.js và npm (nếu chưa có)
sudo apt update
sudo apt install nodejs npm

# Cài đặt Node-RED
sudo npm install -g --unsafe-perm node-red

# Chạy Node-RED
node-red
```

Truy cập: `http://localhost:1880`

### Bước 2: Cài đặt Node-RED Dashboard

1. Trong Node-RED, click menu (☰) > **Manage palette**
2. Vào tab **Install**
3. Tìm và cài đặt: `node-red-dashboard`
4. Chờ cài đặt xong và restart Node-RED nếu cần

### Bước 3: Import Flow

1. Trong Node-RED, click menu (☰) > **Import**
2. Copy toàn bộ nội dung file `node_red_flow.json`
3. Paste vào ô import
4. Click **Import**
5. **Quan trọng**: Cập nhật MQTT Broker credentials từ file `receive_data_mqtt_key.txt`:
   - Double-click vào node **ThingSpeak MQTT** (màu xanh)
   - Cập nhật với credentials từ `receive_data_mqtt_key.txt`:
     - **Server**: `mqtt3.thingspeak.com`
     - **Port**: `1883`
     - **Client ID**: `IRU6PSACOwQPHy4PKiczCiI` (hoặc từ file receive_data_mqtt_key.txt)
     - **Username**: `IRU6PSACOwQPHy4PKiczCiI` (hoặc từ file receive_data_mqtt_key.txt)
     - **Password**: `gHzqnX35vjOPS0jeNUVtBdfV` (hoặc từ file receive_data_mqtt_key.txt)
   - Click **Update**
6. Click **Deploy** để kích hoạt flow

### Bước 4: Truy cập Dashboard

1. Sau khi deploy, click vào icon **🌐** ở góc trên bên phải
2. Hoặc truy cập trực tiếp: `http://localhost:1880/ui`
3. Bạn sẽ thấy giao diện web với:
   - **Gauge Cường độ ánh sáng** (0-1000)
   - **Gauge Khoảng cách** (0-200 cm)
   - **Bar Chart Cường độ ánh sáng**
   - **Bar Chart Khoảng cách**

## Cấu trúc Flow

```
[MQTT Subscribe Light] ──> [Parse Light] ──> [Gauge Light]
                                      └─> [Bar Chart Light]
                                      └─> [Debug Light]

[MQTT Subscribe Distance] ──> [Parse Distance] ──> [Gauge Distance]
                                          └─> [Bar Chart Distance]
                                          └─> [Debug Distance]
```

## Các thành phần trong Flow

### 1. MQTT Broker Node
- **Name**: ThingSpeak MQTT
- **Server**: mqtt3.thingspeak.com
- **Port**: 1883
- **Chức năng**: Kết nối với ThingSpeak MQTT server

### 2. MQTT In Nodes (2 nodes)
- **Nhận Cường độ ánh sáng**:
  - Topic: `channels/3153408/subscribe/fields/field1`
  - Field: Field 1 (L) - Cường độ ánh sáng
  - QoS: 1
- **Nhận Khoảng cách**:
  - Topic: `channels/3153408/subscribe/fields/field2`
  - Field: Field 2 (D) - Khoảng cách
  - QoS: 1

### 3. Function Nodes (2 nodes)
- **Parse Cường độ ánh sáng**: 
  - Parse string sang float
  - Kiểm tra giá trị hợp lệ
- **Parse Khoảng cách**:
  - Parse string sang float
  - Kiểm tra giá trị hợp lệ

### 4. UI Gauge Nodes (2 nodes)
- **Gauge Cường độ ánh sáng**:
  - Min: 0, Max: 1000
  - Hiển thị giá trị ánh sáng
- **Gauge Khoảng cách**:
  - Min: 0, Max: 200
  - Label: cm
  - Hiển thị giá trị khoảng cách

### 5. UI Chart Nodes (Bar Chart) (2 nodes)
- **Bar Chart Cường độ ánh sáng**:
  - Chart Type: Bar
  - Y-axis: 0-1000
  - Hiển thị lịch sử giá trị
- **Bar Chart Khoảng cách**:
  - Chart Type: Bar
  - Y-axis: 0-200
  - Hiển thị lịch sử giá trị

### 6. Debug Nodes (2 nodes)
- Hiển thị dữ liệu trong Debug panel để kiểm tra

## Kiểm tra hoạt động

1. **Chạy chương trình Python gửi dữ liệu:**
   ```bash
   cd /home/duy/iot/kiemtra2
   python send_data.py
   ```

2. **Mở Dashboard:**
   - Truy cập: `http://localhost:1880/ui`
   - Xem Gauge và Bar chart cập nhật giá trị real-time

3. **Kiểm tra Debug:**
   - Mở tab Debug trong Node-RED
   - Xem dữ liệu nhận được từ ThingSpeak MQTT

## Tùy chỉnh Flow

### Thay đổi phạm vi Gauge

Double-click vào Gauge node:
- **Min**: Giá trị nhỏ nhất
- **Max**: Giá trị lớn nhất

### Thay đổi phạm vi Bar Chart

Double-click vào Chart node:
- **Y Min**: Giá trị nhỏ nhất trục Y
- **Y Max**: Giá trị lớn nhất trục Y

### Thêm xử lý lỗi

Thêm **Catch** node để bắt lỗi từ MQTT:
```
[MQTT In] ──> [Function Parse]
     └─> [Catch] ──> [Debug Error]
```

## Troubleshooting

### Không thấy Dashboard

1. Kiểm tra đã cài đặt `node-red-dashboard` chưa
2. Restart Node-RED sau khi cài đặt
3. Kiểm tra có lỗi trong Deploy không

### Gauge/Chart không cập nhật

1. Kiểm tra MQTT Broker có kết nối thành công không (xem status node)
2. Kiểm tra MQTT In nodes có nhận được dữ liệu không (xem Debug)
3. Kiểm tra Function Parse có parse đúng không
4. Kiểm tra chương trình Python đang chạy và gửi dữ liệu

### Lỗi MQTT Connection

1. Kiểm tra MQTT credentials đúng chưa
2. Kiểm tra Channel ID đúng chưa
3. Kiểm tra kết nối internet
4. Kiểm tra ThingSpeak MQTT server có hoạt động không

### Giá trị hiển thị không đúng

1. Kiểm tra Function Parse có parse đúng field không
2. Kiểm tra payload từ MQTT có đúng format không
3. Xem Debug panel để kiểm tra giá trị thực tế

## Mở rộng

### Thêm Text hiển thị giá trị số

1. Kéo node `ui_text` vào flow
2. Kết nối từ Function Parse đến ui_text
3. Cấu hình format hiển thị

### Thêm Line Chart để vẽ biểu đồ đường

1. Kéo node `ui_chart` vào flow
2. Cấu hình Chart Type: `line`
3. Kết nối từ Function Parse đến ui_chart

### Thêm cảnh báo khi vượt ngưỡng

1. Thêm Function node kiểm tra giá trị
2. Nếu vượt ngưỡng, gửi notification hoặc đổi màu Gauge

## Tài liệu tham khảo

- [ThingSpeak MQTT API](https://www.mathworks.com/help/thingspeak/mqtt-basics.html)
- [Node-RED Dashboard Documentation](https://github.com/node-red/node-red-dashboard)
- [Node-RED MQTT Node](https://nodered.org/docs/user-guide/nodes/mqtt)

