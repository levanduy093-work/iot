# Hướng dẫn cấu hình Node-RED Dashboard với MQTT

## 📋 Yêu cầu

Trước khi bắt đầu, đảm bảo bạn đã cài đặt:
- Node-RED
- Node-RED Dashboard (`node-red-dashboard`)

## 🔧 Cài đặt Node-RED Dashboard

Nếu chưa cài đặt, chạy lệnh sau trong Node-RED:

1. Mở Node-RED: `http://localhost:1880`
2. Vào **Menu** → **Manage palette**
3. Tìm và cài đặt: `node-red-dashboard`

Hoặc cài đặt qua terminal:
```bash
cd ~/.node-red
npm install node-red-dashboard
```

## 📥 Import Flow vào Node-RED

### Cách 1: Import từ file JSON

1. Mở Node-RED: `http://localhost:1880`
2. Click vào **Menu** (góc trên bên phải) → **Import**
3. Click **Select a file to import** hoặc **Browse**
4. Chọn file `node_red_flow.json`
5. Click **Import**

### Cách 2: Copy-paste JSON

1. Mở file `node_red_flow.json` bằng text editor
2. Copy toàn bộ nội dung
3. Mở Node-RED → **Menu** → **Import**
4. Paste vào ô **Import nodes**
5. Click **Import**

## ⚙️ Cấu hình Flow

Sau khi import, bạn cần cấu hình các thông tin MQTT:

### 1. Cấu hình MQTT Broker

1. Double-click vào node **"ThingSpeak MQTT"** (mqtt-broker)
2. Cập nhật các thông tin:
   - **Broker**: `mqtt3.thingspeak.com` (giữ nguyên)
   - **Port**: `1883` (giữ nguyên)
   - **Client ID**: Thay `YOUR_CLIENT_ID_HERE` bằng Client ID của bạn
   - **Username**: Thay `YOUR_USERNAME_HERE` bằng Username của bạn
   - **Password**: Thay `YOUR_PASSWORD_HERE` bằng Password của bạn
3. Click **Update** và **Done**

### 2. Cấu hình MQTT Input Nodes

#### Node "Nhận Nhiệt độ":
1. Double-click vào node **"Nhận Nhiệt độ"**
2. Tìm dòng **Topic** và thay thế:
   ```
   channels/YOUR_CHANNEL_ID/subscribe/fields/field1
   ```
   Thay `YOUR_CHANNEL_ID` bằng Channel ID của bạn
3. Đảm bảo **Broker** đã chọn **"ThingSpeak MQTT"**
4. Click **Done**

#### Node "Nhận Độ ẩm":
1. Double-click vào node **"Nhận Độ ẩm"**
2. Tìm dòng **Topic** và thay thế:
   ```
   channels/YOUR_CHANNEL_ID/subscribe/fields/field2
   ```
   Thay `YOUR_CHANNEL_ID` bằng Channel ID của bạn
3. Đảm bảo **Broker** đã chọn **"ThingSpeak MQTT"**
4. Click **Done**

### 3. Kiểm tra Parse Functions

Các node **"Parse Nhiệt độ"** và **"Parse Độ ẩm"** đã được cấu hình sẵn. Bạn có thể kiểm tra:
- Double-click vào node để xem code
- Code sẽ parse giá trị từ string sang float

### 4. Kiểm tra Gauge Nodes

Các node Gauge đã được cấu hình:
- **Gauge Nhiệt độ**: Min=0, Max=100, Label="°C"
- **Gauge Độ ẩm**: Min=0, Max=100, Label="%"

Bạn có thể tùy chỉnh:
1. Double-click vào Gauge node
2. Thay đổi:
   - **Title**: Tiêu đề hiển thị
   - **Min/Max**: Giá trị min/max
   - **Label**: Đơn vị
   - **Format**: Định dạng số

## 🚀 Deploy và Sử dụng

### 1. Deploy Flow

1. Sau khi cấu hình xong, click nút **Deploy** (góc trên bên phải)
2. Đợi thông báo "Successfully deployed"

### 2. Kiểm tra kết nối MQTT

1. Kiểm tra các node MQTT có dấu chấm xanh không:
   - Dấu chấm xanh = Đã kết nối thành công
   - Dấu chấm đỏ = Lỗi kết nối
2. Nếu có lỗi, kiểm tra lại thông tin MQTT broker

### 3. Truy cập Dashboard

1. Mở trình duyệt
2. Truy cập: `http://localhost:1880/ui`
   - Hoặc `http://[IP_RASPBERRY_PI]:1880/ui` nếu truy cập từ máy khác
3. Dashboard sẽ hiển thị:
   - **Gauge Nhiệt độ**: Đồng hồ đo nhiệt độ (0-100°C)
   - **Gauge Độ ẩm**: Đồng hồ đo độ ẩm (0-100%)

## 🔍 Debug

### Kiểm tra dữ liệu trong Debug Panel

1. Mở **Debug panel** (tab bên phải trong Node-RED)
2. Bạn sẽ thấy:
   - **Debug Nhiệt độ**: Giá trị nhiệt độ nhận được
   - **Debug Độ ẩm**: Giá trị độ ẩm nhận được

### Kiểm tra MQTT Connection

1. Double-click vào node **"ThingSpeak MQTT"**
2. Kiểm tra trạng thái kết nối:
   - **Connected**: Kết nối thành công
   - **Disconnected**: Chưa kết nối hoặc lỗi

### Kiểm tra MQTT Topics

1. Kiểm tra các node **"Nhận Nhiệt độ"** và **"Nhận Độ ẩm"**
2. Đảm bảo Topic đúng format:
   - `channels/[CHANNEL_ID]/subscribe/fields/field1` (nhiệt độ)
   - `channels/[CHANNEL_ID]/subscribe/fields/field2` (độ ẩm)

## 🐛 Xử lý lỗi

### Dashboard không hiển thị

- Kiểm tra đã Deploy flow chưa
- Kiểm tra URL: `http://localhost:1880/ui` (có `/ui` ở cuối)
- Kiểm tra console của trình duyệt (F12) để xem lỗi

### Không nhận được dữ liệu từ MQTT

- Kiểm tra MQTT broker đã được cấu hình đúng chưa
- Kiểm tra Username, Password, Client ID đúng chưa
- Kiểm tra Topic subscription đúng chưa (Channel ID)
- Kiểm tra chương trình Python đang chạy và gửi dữ liệu
- Kiểm tra Debug panel trong Node-RED để xem có lỗi không
- Kiểm tra kết nối Internet

### Gauge không cập nhật

- Kiểm tra MQTT input nodes có nhận được dữ liệu không (Debug panel)
- Kiểm tra Parse function có parse đúng không
- Kiểm tra Gauge node có được kết nối đúng không
- Thử refresh trang dashboard

### Lỗi "Connection refused" hoặc "Connection timeout"

- Kiểm tra kết nối Internet
- Kiểm tra ThingSpeak MQTT broker đang hoạt động: `mqtt3.thingspeak.com:1883`
- Kiểm tra firewall có chặn port 1883 không
- Kiểm tra Username và Password đúng chưa

## 📊 Cấu trúc Flow

```
[MQTT Broker: ThingSpeak]
    ↓
[MQTT In: Nhận Nhiệt độ] → [Parse Nhiệt độ] → [Gauge Nhiệt độ] → [Dashboard]
    ↓                                              ↓
[MQTT In: Nhận Độ ẩm]   → [Parse Độ ẩm]   → [Gauge Độ ẩm]   → [Dashboard]
```

## 💡 Tùy chỉnh nâng cao

### Thêm Chart Line

Nếu muốn thêm biểu đồ đường (line chart):
1. Thêm node **ui_chart** mới
2. Cấu hình **Chart Type** = "line"
3. Kết nối với output của Parse function

### Thêm Text Display

Để hiển thị giá trị dạng text:
1. Thêm node **ui_text**
2. Kết nối với output của Parse function
3. Cấu hình format: `{{payload}}`

### Thêm Notification

Để cảnh báo khi giá trị vượt ngưỡng:
1. Thêm node **ui_notification**
2. Thêm function node để kiểm tra ngưỡng
3. Kết nối với notification node

### Thêm Multiple Gauges

Để hiển thị nhiều Gauge trên cùng một dashboard:
1. Thêm các node **ui_gauge** mới
2. Kết nối với cùng một **ui_group**
3. Điều chỉnh **order** để sắp xếp vị trí

## 📚 Tài liệu tham khảo

- [Node-RED Dashboard Documentation](https://github.com/node-red/node-red-dashboard)
- [Node-RED MQTT Documentation](https://nodered.org/docs/user-guide/nodes/mqtt)
- [ThingSpeak MQTT API Documentation](https://www.mathworks.com/help/thingspeak/mqtt-api.html)

