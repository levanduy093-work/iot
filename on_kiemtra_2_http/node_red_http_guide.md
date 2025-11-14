# Hướng dẫn tạo giao diện web Node-RED Dashboard nhận dữ liệu từ ThingSpeak qua HTTP

## Yêu cầu

Tạo giao diện web dùng Node-RED Dashboard để hiển thị:
- **Nhiệt độ** từ ThingSpeak (Field 1) - hiển thị bằng Gauge
- **Độ ẩm** từ ThingSpeak (Field 2) - hiển thị bằng Gauge

**Sử dụng HTTP API** thay vì MQTT để lấy dữ liệu từ ThingSpeak.

## Thông tin kết nối ThingSpeak

- **Channel ID**: `3153408`
- **Read API Key**: `N251PNZ5EG0MWI2Y`
- **Write API Key**: `AHHO5UL59ZCYUYCV`
- **API Endpoint**: `https://api.thingspeak.com/channels/3153408/feeds.json?results=1&api_key=N251PNZ5EG0MWI2Y`

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
[Inject Timer] ──> [HTTP Request] ──> [Function Parse] ──> [Gauge Nhiệt độ]
                                              └─> [Gauge Độ ẩm]
                                              └─> [Debug nodes]
```

## Các thành phần trong Flow

### 1. Inject Node (Timer)
- **Name**: Timer 15 giây
- **Repeat**: Mỗi 15 giây
- **Chức năng**: Kích hoạt HTTP request để lấy dữ liệu mới

### 2. HTTP Request Node
- **Name**: ThingSpeak API Request
- **Method**: GET
- **URL**: `https://api.thingspeak.com/channels/3153408/feeds.json?results=1&api_key=N251PNZ5EG0MWI2Y`
- **Return**: JSON object
- **Chức năng**: Lấy dữ liệu mới nhất từ ThingSpeak

### 3. Function Node (Parse dữ liệu)
- **Name**: Parse dữ liệu ThingSpeak
- **Chức năng**: 
  - Parse JSON response từ ThingSpeak
  - Lấy field1 (nhiệt độ) và field2 (độ ẩm)
  - Tạo 2 message riêng cho nhiệt độ và độ ẩm
  - Output 2 luồng dữ liệu

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

## So sánh HTTP vs MQTT

### HTTP (Polling):
- ✅ Đơn giản, không cần broker
- ✅ Dễ debug và kiểm tra
- ❌ Phải poll định kỳ (không real-time như MQTT)
- ❌ Tốn tài nguyên hơn (phải gửi request liên tục)

### MQTT (Subscribe):
- ✅ Real-time, nhận dữ liệu ngay khi có
- ✅ Hiệu quả hơn (push-based)
- ❌ Cần cấu hình broker phức tạp hơn
- ❌ Cần username/password

## Kiểm tra hoạt động

1. **Chạy chương trình Python gửi dữ liệu:**
   ```bash
   cd /home/duy/iot/on_kiemtra_2_http
   python send_data.py
   ```

2. **Mở Dashboard:**
   - Truy cập: `http://localhost:1880/ui`
   - Xem Gauge cập nhật giá trị mỗi 15 giây

3. **Kiểm tra Debug:**
   - Mở tab Debug trong Node-RED
   - Xem dữ liệu nhận được từ ThingSpeak API

## Tùy chỉnh Flow

### Thay đổi tần suất cập nhật

Double-click vào **Inject Timer** node:
- **Repeat**: Thay đổi số giây (ví dụ: `10` cho 10 giây)
- **Lưu ý**: ThingSpeak có rate limit 15 giây/lần, không nên poll quá nhanh

### Thay đổi phạm vi Gauge

Double-click vào Gauge node:
- **Min**: Giá trị nhỏ nhất
- **Max**: Giá trị lớn nhất

### Thêm xử lý lỗi

Thêm **Catch** node để bắt lỗi từ HTTP request:
```
[HTTP Request] ──> [Function Parse]
     └─> [Catch] ──> [Debug Error]
```

## Troubleshooting

### Không thấy Dashboard

1. Kiểm tra đã cài đặt `node-red-dashboard` chưa
2. Restart Node-RED sau khi cài đặt
3. Kiểm tra có lỗi trong Deploy không

### Gauge không cập nhật

1. Kiểm tra Inject Timer có chạy không (xem status node)
2. Kiểm tra HTTP Request có trả về dữ liệu không (xem Debug)
3. Kiểm tra Function Parse có parse đúng không
4. Kiểm tra chương trình Python đang chạy và gửi dữ liệu

### Lỗi HTTP Request

1. Kiểm tra API Key đúng chưa
2. Kiểm tra Channel ID đúng chưa
3. Kiểm tra kết nối internet
4. Kiểm tra ThingSpeak có rate limit không (phải chờ 15 giây giữa các request)

### Giá trị hiển thị không đúng

1. Kiểm tra Function Parse có parse đúng field không
2. Kiểm tra payload từ HTTP response có đúng format không
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

- [ThingSpeak HTTP API](https://www.mathworks.com/help/thingspeak/readdata.html)
- [Node-RED Dashboard Documentation](https://github.com/node-red/node-red-dashboard)
- [Node-RED HTTP Request Node](https://nodered.org/docs/user-guide/nodes/http-request)

