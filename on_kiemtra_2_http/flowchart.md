# Lưu đồ giải thuật - Hệ thống giám sát nhiệt độ và độ ẩm với Node-RED Dashboard (HTTP)

## 1. Lưu đồ tổng quan hệ thống

```mermaid
flowchart TB
    subgraph RaspberryPi["RASPBERRY PI"]
        A1[Đọc cảm biến DHT11] --> A2[Xử lý dữ liệu]
        A2 --> A3[Điều khiển LED & Buzzer]
        A3 --> A4[Gửi lên ThingSpeak HTTP API]
    end
    
    subgraph ThingSpeak["THINGSPEAK SERVER"]
        B1[Nhận dữ liệu HTTP POST] --> B2[Lưu trữ dữ liệu]
        B2 --> B3[API Endpoint sẵn sàng]
    end
    
    subgraph NodeRED["NODE-RED DASHBOARD"]
        C1[Timer mỗi 15 giây] --> C2[HTTP GET Request]
        C2 --> C3[Parse dữ liệu JSON]
        C3 --> C4[Hiển thị trên Gauge]
    end
    
    A4 -->|HTTP POST| B1
    B3 -->|HTTP GET| C2
    C4 -->|Web UI| User[Người dùng xem Dashboard]
    
    style RaspberryPi fill:#E8F5E9
    style ThingSpeak fill:#E3F2FD
    style NodeRED fill:#FFF3E0
    style User fill:#FCE4EC
```

## 2. Lưu đồ chương trình Python (Raspberry Pi)

```mermaid
flowchart TD
    Start([BẮT ĐẦU]) --> Init[Khởi tạo:<br/>- DHT11 Sensor<br/>- LED đỏ, LED vàng<br/>- Buzzer]
    Init --> PrintStart[In thông báo khởi động]
    PrintStart --> SetVars[Khởi tạo biến:<br/>READ_INTERVAL = 10s<br/>SEND_INTERVAL = 15s<br/>last_sent_ts = 0]
    SetVars --> Loop{Vòng lặp chính}
    
    Loop --> ReadSensor[Đọc cảm biến DHT11<br/>humi, temp = sensor.read]
    ReadSensor --> CheckValid{Dữ liệu<br/>hợp lệ?}
    
    CheckValid -->|Không| SleepRetry[Chờ 5 giây<br/>Thử lại]
    SleepRetry --> Loop
    CheckValid -->|Có| Display[Hiển thị lên Terminal<br/>Nhiệt độ và Độ ẩm]
    
    Display --> ControlLED[Gọi hàm control_leds]
    ControlLED --> ControlBuzzer[Gọi hàm control_buzzer]
    ControlBuzzer --> CheckTime{Đã qua<br/>15 giây?<br/>now - last_sent_ts >= 15}
    
    CheckTime -->|Chưa| CheckBuzzer{Buzzer đang<br/>hoạt động?}
    CheckTime -->|Có| PrepareParams[Tạo params HTTP<br/>field1=temp<br/>field2=humi<br/>field3=led_yellow<br/>field4=led_red]
    
    PrepareParams --> SendHTTP[Gửi HTTP POST<br/>thingspeak_post_http]
    SendHTTP --> CheckResp{Response<br/>thành công?}
    
    CheckResp -->|Có| UpdateTime[Cập nhật last_sent_ts<br/>In: Đã gửi dữ liệu]
    CheckResp -->|Không| PrintError[In: Update thất bại]
    
    UpdateTime --> CheckBuzzer
    PrintError --> CheckBuzzer
    
    CheckBuzzer -->|Có| Sleep1[Chờ 1 giây]
    CheckBuzzer -->|Không| Sleep10[Chờ 10 giây]
    
    Sleep1 --> Loop
    Sleep10 --> Loop
    
    Loop -.->|Ctrl+C| Interrupt[Nhận KeyboardInterrupt]
    Interrupt --> Cleanup[Tắt LED và Buzzer]
    Cleanup --> End([KẾT THÚC])
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style Loop fill:#87CEEB
    style CheckTime fill:#FFD700
    style CheckBuzzer fill:#FFD700
```

## 3. Lưu đồ gửi dữ liệu lên ThingSpeak (HTTP POST)

```mermaid
flowchart TD
    Start([BẮT ĐẦU thingspeak_post_http]) --> CreateParams[Tạo URL encoded params<br/>field1=temp<br/>field2=humi<br/>field3=led_yellow<br/>field4=led_red]
    CreateParams --> CreateRequest[Tạo HTTP Request<br/>URL: api.thingspeak.com/update<br/>Method: POST]
    CreateRequest --> AddHeaders[Thêm Headers:<br/>Content-Type: application/x-www-form-urlencoded<br/>X-THINGSPEAKAPIKEY: API_KEY]
    AddHeaders --> SendRequest[Gửi HTTP Request<br/>với timeout 10s]
    SendRequest --> CheckSuccess{Request<br/>thành công?}
    
    CheckSuccess -->|Có| ReadResponse[Đọc response<br/>Decode string]
    CheckSuccess -->|Không| ReturnError[Return None]
    
    ReadResponse --> ReturnID[Return entry ID]
    ReturnError --> End([KẾT THÚC])
    ReturnID --> End
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style CheckSuccess fill:#FFD700
```

## 4. Lưu đồ Node-RED nhận và hiển thị dữ liệu (HTTP)

```mermaid
flowchart TD
    Start([BẮT ĐẦU Node-RED Flow]) --> InitTimer[Inject Timer<br/>Repeat: 15 giây]
    InitTimer --> Trigger[Kích hoạt mỗi 15 giây]
    
    Trigger --> HTTPRequest[HTTP Request Node<br/>GET: api.thingspeak.com/channels/3153408/feeds.json<br/>results=1&api_key=READ_API_KEY]
    
    HTTPRequest --> CheckResponse{Response<br/>thành công?}
    
    CheckResponse -->|Không| Error[Debug Error]
    Error --> Wait[Chờ lần trigger tiếp theo]
    
    CheckResponse -->|Có| ParseJSON[Function: Parse JSON<br/>Lấy feeds[0]]
    ParseJSON --> CheckFeeds{feeds<br/>có dữ liệu?}
    
    CheckFeeds -->|Không| ReturnNull[Return null]
    CheckFeeds -->|Có| ExtractData[Lấy field1 và field2<br/>Parse sang float]
    
    ExtractData --> CheckValid{Giá trị<br/>hợp lệ?}
    
    CheckValid -->|Không| ReturnNull
    CheckValid -->|Có| CreateMessages[Tạo 2 messages:<br/>msgTemp: payload=temp<br/>msgHumi: payload=humi]
    
    CreateMessages --> OutputTemp[Output 1: Nhiệt độ]
    CreateMessages --> OutputHumi[Output 2: Độ ẩm]
    
    OutputTemp --> UpdateGaugeTemp[Cập nhật Gauge Nhiệt độ<br/>Hiển thị trên Dashboard]
    OutputTemp --> DebugTemp[Debug: Nhiệt độ]
    
    OutputHumi --> UpdateGaugeHumi[Cập nhật Gauge Độ ẩm<br/>Hiển thị trên Dashboard]
    OutputHumi --> DebugHumi[Debug: Độ ẩm]
    
    UpdateGaugeTemp --> Wait
    UpdateGaugeHumi --> Wait
    DebugTemp --> Wait
    DebugHumi --> Wait
    ReturnNull --> Wait
    Wait --> Trigger
    
    style Start fill:#90EE90
    style CheckResponse fill:#FFD700
    style CheckFeeds fill:#FFD700
    style CheckValid fill:#FFD700
    style UpdateGaugeTemp fill:#4ECDC4
    style UpdateGaugeHumi fill:#4ECDC4
```

## 5. Lưu đồ chi tiết Node-RED Flow

```mermaid
flowchart LR
    subgraph Timer["TIMER"]
        A1[Inject<br/>15 giây] --> A2[Trigger]
    end
    
    subgraph HTTP["HTTP REQUEST"]
        B1[HTTP Request<br/>GET ThingSpeak API] --> B2[Response JSON]
    end
    
    subgraph Parse["PARSE DATA"]
        C1[Function Parse<br/>Extract field1, field2] --> C2[Create 2 messages]
    end
    
    subgraph Display["DISPLAY"]
        D1[Gauge Nhiệt độ<br/>0-100°C] --> D2[Gauge Độ ẩm<br/>0-100%]
        E1[Debug Nhiệt độ] --> E2[Debug Độ ẩm]
    end
    
    A2 --> B1
    B2 --> C1
    C2 -->|Output 1| D1
    C2 -->|Output 1| E1
    C2 -->|Output 2| D2
    C2 -->|Output 2| E2
    
    D1 -->|Web UI| User[User Dashboard]
    D2 -->|Web UI| User
    
    style Timer fill:#E3F2FD
    style HTTP fill:#FFF3E0
    style Parse fill:#E8F5E9
    style Display fill:#FCE4EC
```

## 6. Lưu đồ luồng dữ liệu tổng thể (HTTP)

```mermaid
sequenceDiagram
    participant RPi as Raspberry Pi
    participant TS as ThingSpeak Server
    participant NR as Node-RED
    participant UI as Web Dashboard
    
    RPi->>RPi: Đọc cảm biến DHT11
    RPi->>RPi: Điều khiển LED & Buzzer
    RPi->>TS: HTTP POST (temp, humi, LED status)
    TS->>TS: Lưu trữ dữ liệu
    
    Note over NR: Mỗi 15 giây
    NR->>TS: HTTP GET Request (feeds.json)
    TS->>NR: JSON Response (field1, field2)
    NR->>NR: Parse JSON
    NR->>NR: Cập nhật Gauge
    NR->>UI: Hiển thị trên Dashboard
    UI->>UI: User xem nhiệt độ & độ ẩm
```

## 7. So sánh HTTP vs MQTT

```mermaid
flowchart TD
    subgraph HTTP["HTTP METHOD"]
        H1[Polling mỗi 15 giây] --> H2[HTTP GET Request]
        H2 --> H3[Nhận JSON Response]
        H3 --> H4[Parse và hiển thị]
        H5[Ưu điểm:<br/>- Đơn giản<br/>- Dễ debug] --> H6[Nhược điểm:<br/>- Không real-time<br/>- Tốn tài nguyên]
    end
    
    subgraph MQTT["MQTT METHOD"]
        M1[Subscribe topic] --> M2[Nhận dữ liệu push]
        M2 --> M3[Parse và hiển thị]
        M4[Ưu điểm:<br/>- Real-time<br/>- Hiệu quả] --> M5[Nhược điểm:<br/>- Phức tạp hơn<br/>- Cần broker]
    end
    
    style HTTP fill:#E3F2FD
    style MQTT fill:#FFF3E0
```

## Mô tả các thành phần:

### Raspberry Pi (Python - HTTP):
- **Cảm biến**: DHT11 đọc nhiệt độ và độ ẩm
- **Điều khiển**: LED đỏ (nhiệt độ), LED vàng (độ ẩm), Buzzer (cảnh báo)
- **Gửi dữ liệu**: HTTP POST lên ThingSpeak mỗi 15 giây (rate limit)
- **Đọc cảm biến**: Mỗi 10 giây (hoặc 1 giây nếu buzzer hoạt động)

### ThingSpeak Server:
- **Nhận dữ liệu**: Qua HTTP POST từ Raspberry Pi
- **Lưu trữ**: Field1 (nhiệt độ), Field2 (độ ẩm), Field3 (LED vàng), Field4 (LED đỏ)
- **API Endpoint**: `https://api.thingspeak.com/channels/3153408/feeds.json`

### Node-RED Dashboard (HTTP):
- **Timer**: Inject node kích hoạt mỗi 15 giây
- **HTTP Request**: GET dữ liệu từ ThingSpeak API
- **Parse**: Chuyển đổi JSON sang số
- **Hiển thị**: Gauge trên giao diện web
- **Truy cập**: `http://localhost:1880/ui` hoặc `http://[IP]:1880/ui`

### Logic điều khiển:
- **LED đỏ**: Bật khi temp > 40°C, tắt khi temp < 30°C
- **LED vàng**: Bật khi humi > 70%, tắt khi humi < 40%
- **Buzzer**: Bật/tắt mỗi 1 giây khi temp > 50°C

### Rate Limits:
- **ThingSpeak HTTP**: Tối đa 1 request mỗi 15 giây
- **Python**: Gửi mỗi 15 giây, đọc cảm biến mỗi 10 giây

