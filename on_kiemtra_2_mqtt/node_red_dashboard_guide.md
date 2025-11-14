# Hướng dẫn tạo giao diện web Node-RED Dashboard hiển thị Nhiệt độ và Độ ẩm

## Yêu cầu

Tạo giao diện web dùng Node-RED Dashboard để hiển thị:
- **Nhiệt độ** từ ThingSpeak (Field 1) - hiển thị bằng Gauge
- **Độ ẩm** từ ThingSpeak (Field 2) - hiển thị bằng Gauge

## Thông tin kết nối ThingSpeak

- **Channel ID**: `3153408`
- **MQTT Server**: `mqtt3.thingspeak.com:1883`
- **Username**: `IRU6PSACOwQPHy4PKiczCiI`
- **Password**: `gHzqnX35vjOPS0jeNUVtBdfV`
- **Topic Nhiệt độ**: `channels/3153408/subscribe/fields/field1`
- **Topic Độ ẩm**: `channels/3153408/subscribe/fields/field2`

## Cài đặt

### Bước 1: Cài đặt Node-RED Dashboard

1. Mở Node-RED: `http://localhost:1880`
2. Click menu (☰) > **Manage palette**
3. Vào tab **Install**
4. Tìm và cài đặt: `node-red-dashboard`
5. Chờ cài đặt xong và restart Node-RED nếu cần

### Bước 2: Import Flow

1. Trong Node-RED, click menu (☰) > **Import**
2. Copy toàn bộ nội dung file `node_red_flow.json`
3. Paste vào ô import
4. Click **Import**
5. Click **Deploy** để kích hoạt flow

### Bước 3: Truy cập Dashboard

1. Sau khi deploy, click vào icon **🌐** ở góc trên bên phải
2. Hoặc truy cập trực tiếp: `http://localhost:1880/ui`
3. Bạn sẽ thấy giao diện web với 2 Gauge:
   - **Gauge Nhiệt độ** (0-100°C)
   - **Gauge Độ ẩm** (0-100%)

## Cấu trúc Flow

```
[MQTT In - Nhiệt độ] ──> [Parse] ──> [Gauge Nhiệt độ]
                        └─> [Debug]

[MQTT In - Độ ẩm] ──> [Parse] ──> [Gauge Độ ẩm]
                      └─> [Debug]
```

## Các thành phần trong Flow

### 1. MQTT Broker
- **Name**: ThingSpeak MQTT
- Đã cấu hình sẵn username/password

### 2. MQTT In Nodes
- **Nhận Nhiệt độ**: Subscribe topic `channels/3153408/subscribe/fields/field1`
- **Nhận Độ ẩm**: Subscribe topic `channels/3153408/subscribe/fields/field2`

### 3. Function Nodes
- **Parse Nhiệt độ**: Chuyển đổi string sang số
- **Parse Độ ẩm**: Chuyển đổi string sang số

### 4. UI Gauge Nodes
- **Gauge Nhiệt độ**: 
  - Min: 0, Max: 100
  - Label: °C
  - Hiển thị giá trị nhiệt độ
- **Gauge Độ ẩm**:
  - Min: 0, Max: 100
  - Label: %
  - Hiển thị giá trị độ ẩm

### 5. Debug Nodes
- Hiển thị dữ liệu trong Debug panel để kiểm tra

## Kiểm tra hoạt động

1. **Chạy chương trình Python gửi dữ liệu:**
   ```bash
   cd /home/duy/iot/on_kiemtra_2
   python send_data.py
   ```

2. **Mở Dashboard:**
   - Truy cập: `http://localhost:1880/ui`
   - Xem Gauge cập nhật giá trị theo thời gian thực

3. **Kiểm tra Debug:**
   - Mở tab Debug trong Node-RED
   - Xem dữ liệu nhận được từ ThingSpeak

## Tùy chỉnh Gauge

### Thay đổi phạm vi hiển thị

Double-click vào Gauge node và chỉnh sửa:
- **Min**: Giá trị nhỏ nhất (ví dụ: 0)
- **Max**: Giá trị lớn nhất (ví dụ: 100 cho nhiệt độ, 100 cho độ ẩm)

### Thay đổi màu sắc

Trong Gauge node, có thể thêm:
- **Colors**: Mảng màu cho các vùng giá trị
  ```json
  ["#00ff00", "#ffff00", "#ff0000"]
  ```

### Thay đổi kích thước

Trong UI Group node:
- **Width**: Độ rộng (1-12)
- **Height**: Chiều cao (số dòng)

## Troubleshooting

### Không thấy Dashboard

1. Kiểm tra đã cài đặt `node-red-dashboard` chưa
2. Restart Node-RED sau khi cài đặt
3. Kiểm tra có lỗi trong Deploy không

### Gauge không cập nhật

1. Kiểm tra MQTT Broker đã kết nối (status = connected)
2. Kiểm tra chương trình Python đang chạy và gửi dữ liệu
3. Mở Debug panel xem có nhận được dữ liệu không
4. Kiểm tra topic MQTT đúng chưa

### Giá trị hiển thị không đúng

1. Kiểm tra Function Parse có parse đúng không
2. Kiểm tra payload từ MQTT có đúng format không
3. Xem Debug panel để kiểm tra giá trị thực tế

## Mở rộng

### Thêm Text hiển thị giá trị số

1. Kéo node `ui_text` vào flow
2. Kết nối từ Function Parse đến ui_text
3. Cấu hình format hiển thị

### Thêm Chart để vẽ biểu đồ

1. Kéo node `ui_chart` vào flow
2. Kết nối từ Function Parse đến ui_chart
3. Cấu hình loại chart (line, bar, etc.)

### Thêm cảnh báo khi vượt ngưỡng

1. Thêm Function node kiểm tra giá trị
2. Nếu vượt ngưỡng, gửi notification hoặc đổi màu Gauge

## Tài liệu tham khảo

- [Node-RED Dashboard Documentation](https://github.com/node-red/node-red-dashboard)
- [ThingSpeak MQTT API](https://www.mathworks.com/help/thingspeak/mqtt-api.html)

