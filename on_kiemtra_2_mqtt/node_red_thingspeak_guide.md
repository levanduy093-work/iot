# Hướng dẫn sử dụng Node-RED nhận dữ liệu từ ThingSpeak qua MQTT

## Thông tin kênh ThingSpeak

- **Channel ID**: `3153408`
- **MQTT Server**: `mqtt3.thingspeak.com`
- **Port**: `1883`
- **Username**: `IRU6PSACOwQPHy4PKiczCiI`
- **Client ID**: `IRU6PSACOwQPHy4PKiczCiI`
- **Password**: `gHzqnX35vjOPS0jeNUVtBdfV`

## Các Field trong Channel

- **Field 1**: Nhiệt độ (°C)
- **Field 2**: Độ ẩm (%)
- **Field 3**: LED vàng (1=BẬT, 0=TẮT)
- **Field 4**: LED đỏ (1=BẬT, 0=TẮT)

## Topic MQTT để Subscribe

ThingSpeak publish dữ liệu qua các topic sau:
- `channels/3153408/subscribe/fields/field1` - Nhiệt độ
- `channels/3153408/subscribe/fields/field2` - Độ ẩm
- `channels/3153408/subscribe/fields/field3` - LED vàng
- `channels/3153408/subscribe/fields/field4` - LED đỏ

## Cách thiết lập Node-RED

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

### Bước 2: Cài đặt node MQTT (nếu chưa có)

Trong Node-RED:
1. Click vào menu (☰) > **Manage palette**
2. Vào tab **Install**
3. Tìm và cài đặt: `node-red-node-mqtt`

### Bước 3: Tạo Flow nhận dữ liệu

#### Cách 1: Tạo thủ công

1. **Kéo thả các node sau vào flow:**
   - `mqtt in` (4 node - mỗi node cho 1 field)
   - `function` (để xử lý dữ liệu)
   - `debug` (để hiển thị dữ liệu)
   - `gauge` hoặc `chart` (để hiển thị trực quan)

2. **Cấu hình MQTT Broker:**
   - Double-click vào node `mqtt in` đầu tiên
   - Click **Add new mqtt-broker** > **Add**
   - Điền thông tin:
     - **Server**: `mqtt3.thingspeak.com`
     - **Port**: `1883`
     - **Client ID**: `IRU6PSACOwQPHy4PKiczCiI`
     - **Username**: `IRU6PSACOwQPHy4PKiczCiI`
     - **Password**: `gHzqnX35vjOPS0jeNUVtBdfV`
   - Click **Update** > **Done**

3. **Cấu hình từng MQTT In node:**

   **Node 1 - Nhiệt độ:**
   - **Topic**: `channels/3153408/subscribe/fields/field1`
   - **Name**: `ThingSpeak - Nhiệt độ`
   - **Output**: `auto-detect` hoặc `string`

   **Node 2 - Độ ẩm:**
   - **Topic**: `channels/3153408/subscribe/fields/field2`
   - **Name**: `ThingSpeak - Độ ẩm`
   - **Output**: `auto-detect` hoặc `string`

   **Node 3 - LED vàng:**
   - **Topic**: `channels/3153408/subscribe/fields/field3`
   - **Name**: `ThingSpeak - LED vàng`
   - **Output**: `auto-detect` hoặc `string`

   **Node 4 - LED đỏ:**
   - **Topic**: `channels/3153408/subscribe/fields/field4`
   - **Name**: `ThingSpeak - LED đỏ`
   - **Output**: `auto-detect` hoặc `string`

4. **Tạo Function node để xử lý dữ liệu:**

   Kéo node `function` vào và cấu hình:
   ```javascript
   // Lưu trữ dữ liệu mới nhất
   var field = msg.topic.split('/').pop(); // Lấy field1, field2, ...
   var value = parseFloat(msg.payload) || 0;
   
   // Lưu vào context để sử dụng sau
   context.set(field, value);
   
   // Tạo object chứa tất cả dữ liệu
   var data = {
       timestamp: new Date().toISOString(),
       temperature: context.get('field1') || null,
       humidity: context.get('field2') || null,
       led_yellow: context.get('field3') || null,
       led_red: context.get('field4') || null,
       [field]: value
   };
   
   msg.payload = data;
   msg.topic = field;
   
   return msg;
   ```

5. **Kết nối các node:**
   ```
   [MQTT In - field1] ──┐
   [MQTT In - field2] ──┤
   [MQTT In - field3] ──┼──> [Function] ──> [Debug]
   [MQTT In - field4] ──┘
   ```

#### Cách 2: Import Flow có sẵn

1. Copy nội dung file `node_red_flow.json`
2. Trong Node-RED: Menu (☰) > **Import**
3. Paste nội dung JSON
4. Click **Import**
5. Click **Deploy** để kích hoạt flow

### Bước 4: Kiểm tra dữ liệu

1. Mở tab **Debug** ở bên phải
2. Chạy chương trình Python gửi dữ liệu (`send_data.py`)
3. Xem dữ liệu hiển thị trong Debug panel

## Flow mẫu chi tiết

### Flow 1: Hiển thị dữ liệu trong Debug

```
[MQTT In - field1] ──> [Function Parse] ──> [Debug]
[MQTT In - field2] ──> [Function Parse] ──> [Debug]
[MQTT In - field3] ──> [Function Parse] ──> [Debug]
[MQTT In - field4] ──> [Function Parse] ──> [Debug]
```

### Flow 2: Hiển thị trên Dashboard

```
[MQTT In - field1] ──> [Gauge - Nhiệt độ]
[MQTT In - field2] ──> [Gauge - Độ ẩm]
[MQTT In - field3] ──> [Switch - LED vàng]
[MQTT In - field4] ──> [Switch - LED đỏ]
```

### Flow 3: Lưu vào Database

```
[MQTT In - all fields] ──> [Function Combine] ──> [MongoDB] hoặc [MySQL]
```

## Function Node mẫu - Xử lý và kết hợp dữ liệu

```javascript
// Function: Combine All Fields
var field = msg.topic.split('/').pop();
var value = parseFloat(msg.payload) || 0;

// Lưu vào context
context.set(field, value);

// Lấy tất cả giá trị hiện tại
var temp = context.get('field1') || null;
var humi = context.get('field2') || null;
var led_y = context.get('field3') || null;
var led_r = context.get('field4') || null;

// Tạo message mới
msg.payload = {
    timestamp: new Date().toISOString(),
    temperature: temp,
    humidity: humi,
    led_yellow: led_y === 1 ? "BẬT" : "TẮT",
    led_red: led_r === 1 ? "BẬT" : "TẮT"
};

msg.topic = "thingspeak_data";
return msg;
```

## Function Node - Format hiển thị

```javascript
// Function: Format Display
var data = msg.payload;
var output = `\n=== DỮ LIỆU THINGSPEAK ===\n`;
output += `Thời gian: ${new Date(data.timestamp).toLocaleString('vi-VN')}\n`;
output += `Nhiệt độ: ${data.temperature}°C\n`;
output += `Độ ẩm: ${data.humidity}%\n`;
output += `LED Vàng: ${data.led_yellow}\n`;
output += `LED Đỏ: ${data.led_red}\n`;
output += `========================\n`;

msg.payload = output;
return msg;
```

## Troubleshooting

### Không nhận được dữ liệu

1. **Kiểm tra kết nối MQTT:**
   - Xem status của mqtt-broker node (phải là "connected")
   - Kiểm tra username/password đúng chưa

2. **Kiểm tra Topic:**
   - Đảm bảo topic đúng format: `channels/3153408/subscribe/fields/field1`
   - Không có khoảng trắng thừa

3. **Kiểm tra chương trình gửi:**
   - Đảm bảo `send_data.py` đang chạy
   - Kiểm tra có gửi dữ liệu thành công không

4. **Kiểm tra Debug panel:**
   - Mở tab Debug
   - Xem có message nào không
   - Kiểm tra format của payload

### Dữ liệu hiển thị không đúng

1. **Parse dữ liệu:**
   - ThingSpeak gửi dữ liệu dạng string
   - Cần parse sang số: `parseFloat(msg.payload)`

2. **Xử lý giá trị null:**
   - Kiểm tra giá trị trước khi sử dụng
   - Dùng toán tử `||` để gán giá trị mặc định

## Tài liệu tham khảo

- [ThingSpeak MQTT API](https://www.mathworks.com/help/thingspeak/mqtt-api.html)
- [Node-RED MQTT Documentation](https://nodered.org/docs/user-guide/nodes/mqtt)
- [Node-RED Dashboard](https://github.com/node-red/node-red-dashboard)

