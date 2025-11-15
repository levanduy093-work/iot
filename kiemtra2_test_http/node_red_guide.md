# Hướng dẫn cấu hình Node-RED Dashboard

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

Sau khi import, bạn cần cấu hình các thông tin ThingSpeak:

### 1. Cấu hình HTTP Request Node

1. Double-click vào node **"ThingSpeak API Request"**
2. Tìm dòng URL và thay thế:
   ```
   https://api.thingspeak.com/channels/YOUR_CHANNEL_ID/feeds.json?results=1&api_key=YOUR_READ_API_KEY
   ```
   
   Thay:
   - `YOUR_CHANNEL_ID` → Channel ID của bạn (ví dụ: 3153408)
   - `YOUR_READ_API_KEY` → Read API Key của bạn (ví dụ: N251PNZ5EG0MWI2Y)

3. Click **Done**

### 2. Kiểm tra Timer

Node **"Timer 10 giây"** đã được cấu hình để gửi request mỗi 10 giây. Bạn có thể điều chỉnh nếu cần:
- Double-click vào node
- Thay đổi giá trị **Repeat** (đơn vị: giây)

## 🎨 Cấu hình Dashboard UI

### 1. Kiểm tra UI Tab và Group

Flow đã bao gồm:
- **UI Tab**: "Dashboard" 
- **UI Group**: "Giám sát Ánh sáng & Khoảng cách"

Bạn có thể tùy chỉnh:
- Double-click vào **UI Tab** để đổi tên, icon
- Double-click vào **UI Group** để đổi layout, kích thước

### 2. Cấu hình Gauge

Có 2 Gauge nodes:
- **Gauge Ánh sáng**: Hiển thị giá trị 0-1000
- **Gauge Khoảng cách**: Hiển thị giá trị 0-200 cm

Để tùy chỉnh:
1. Double-click vào Gauge node
2. Thay đổi:
   - **Title**: Tiêu đề hiển thị
   - **Min/Max**: Giá trị min/max
   - **Label**: Đơn vị (ví dụ: "cm", "lux")
   - **Format**: Định dạng số (ví dụ: "{{value}}")

### 3. Cấu hình Bar Chart

Có 2 Bar Chart nodes:
- **Bar Chart Ánh sáng**: Biểu đồ cột cho ánh sáng
- **Bar Chart Khoảng cách**: Biểu đồ cột cho khoảng cách

Để tùy chỉnh:
1. Double-click vào Chart node
2. Thay đổi:
   - **Label**: Nhãn hiển thị
   - **Chart Type**: Đảm bảo là "bar"
   - **Y-axis Min/Max**: Giá trị trục Y
   - **Colors**: Màu sắc của biểu đồ

## 🚀 Deploy và Sử dụng

### 1. Deploy Flow

1. Sau khi cấu hình xong, click nút **Deploy** (góc trên bên phải)
2. Đợi thông báo "Successfully deployed"

### 2. Truy cập Dashboard

1. Mở trình duyệt
2. Truy cập: `http://localhost:1880/ui`
   - Hoặc `http://[IP_RASPBERRY_PI]:1880/ui` nếu truy cập từ máy khác
3. Dashboard sẽ hiển thị:
   - **Gauge Ánh sáng**: Đồng hồ đo cường độ ánh sáng
   - **Gauge Khoảng cách**: Đồng hồ đo khoảng cách
   - **Bar Chart Ánh sáng**: Biểu đồ cột ánh sáng theo thời gian
   - **Bar Chart Khoảng cách**: Biểu đồ cột khoảng cách theo thời gian

## 🔍 Debug

### Kiểm tra dữ liệu trong Debug Panel

1. Mở **Debug panel** (tab bên phải trong Node-RED)
2. Bạn sẽ thấy:
   - **Debug Ánh sáng**: Giá trị ánh sáng nhận được
   - **Debug Khoảng cách**: Giá trị khoảng cách nhận được

### Kiểm tra HTTP Request

1. Double-click vào node **"ThingSpeak API Request"**
2. Click tab **Test** để xem response
3. Hoặc kiểm tra trong Debug panel

## 🐛 Xử lý lỗi

### Dashboard không hiển thị

- Kiểm tra đã Deploy flow chưa
- Kiểm tra URL: `http://localhost:1880/ui` (có `/ui` ở cuối)
- Kiểm tra console của trình duyệt (F12) để xem lỗi

### Không nhận được dữ liệu

- Kiểm tra ThingSpeak Channel ID và API Key đúng chưa
- Kiểm tra chương trình Python đã gửi dữ liệu lên ThingSpeak chưa
- Kiểm tra Debug panel để xem có lỗi không
- Kiểm tra kết nối Internet

### Gauge/Chart không cập nhật

- Kiểm tra Timer node có chạy không (có dấu chấm xanh)
- Kiểm tra HTTP Request có trả về dữ liệu không
- Kiểm tra Parse function có parse đúng không

## 📊 Cấu trúc Flow

```
[Timer 10s] 
    ↓
[HTTP Request ThingSpeak]
    ↓
[Parse dữ liệu]
    ├─→ [Gauge Ánh sáng]
    ├─→ [Bar Chart Ánh sáng]
    ├─→ [Debug Ánh sáng]
    ├─→ [Gauge Khoảng cách]
    ├─→ [Bar Chart Khoảng cách]
    └─→ [Debug Khoảng cách]
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

## 📚 Tài liệu tham khảo

- [Node-RED Dashboard Documentation](https://github.com/node-red/node-red-dashboard)
- [Node-RED Documentation](https://nodered.org/docs/)
- [ThingSpeak API Documentation](https://www.mathworks.com/help/thingspeak/)

