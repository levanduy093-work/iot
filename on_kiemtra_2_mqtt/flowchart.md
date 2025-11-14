# Lưu đồ giải thuật - Hệ thống giám sát nhiệt độ và độ ẩm với Node-RED Dashboard

## 1. Lưu đồ tổng quan hệ thống

```mermaid
flowchart TB
    subgraph RaspberryPi["RASPBERRY PI"]
        A1[Đọc cảm biến DHT11] --> A2[Xử lý dữ liệu]
        A2 --> A3[Điều khiển LED & Buzzer]
        A3 --> A4[Gửi lên ThingSpeak MQTT]
    end
    
    subgraph ThingSpeak["THINGSPEAK SERVER"]
        B1[Nhận dữ liệu MQTT] --> B2[Lưu trữ dữ liệu]
        B2 --> B3[Publish dữ liệu qua MQTT]
    end
    
    subgraph NodeRED["NODE-RED DASHBOARD"]
        C1[Subscribe MQTT] --> C2[Parse dữ liệu]
        C2 --> C3[Hiển thị trên Gauge]
    end
    
    A4 -->|MQTT Publish| B1
    B3 -->|MQTT Subscribe| C1
    C3 -->|Web UI| User[Người dùng xem Dashboard]
    
    style RaspberryPi fill:#E8F5E9
    style ThingSpeak fill:#E3F2FD
    style NodeRED fill:#FFF3E0
    style User fill:#FCE4EC
```

## 2. Lưu đồ chương trình Python (Raspberry Pi)

```mermaid
flowchart TD
    Start([BẮT ĐẦU]) --> Init[Khởi tạo:<br/>- MQTT Client<br/>- DHT11 Sensor<br/>- LED đỏ, LED vàng<br/>- Buzzer]
    Init --> PrintStart[In thông báo khởi động]
    PrintStart --> Loop{Vòng lặp chính}
    
    Loop --> ReadSensor[Đọc cảm biến DHT11<br/>humi, temp = sensor.read]
    ReadSensor --> Display[Hiển thị lên Terminal<br/>Nhiệt độ và Độ ẩm]
    Display --> ControlLED[Gọi hàm control_leds]
    ControlLED --> ControlBuzzer[Gọi hàm control_buzzer]
    ControlBuzzer --> SendMQTT[Gửi dữ liệu lên ThingSpeak<br/>qua MQTT]
    SendMQTT --> PrintSuccess[In: Đã gửi dữ liệu]
    PrintSuccess --> CheckBuzzer{Buzzer đang<br/>hoạt động?}
    
    CheckBuzzer -->|Có| Sleep1[Chờ 1 giây]
    CheckBuzzer -->|Không| Sleep10[Chờ 10 giây]
    
    Sleep1 --> Loop
    Sleep10 --> Loop
    
    Loop -.->|Ctrl+C| Interrupt[Nhận KeyboardInterrupt]
    Interrupt --> Cleanup[Tắt LED và Buzzer<br/>Ngắt kết nối MQTT]
    Cleanup --> End([KẾT THÚC])
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style Loop fill:#87CEEB
    style CheckBuzzer fill:#FFD700
```

## 3. Lưu đồ điều khiển LED (control_leds)

```mermaid
flowchart TD
    Start([BẮT ĐẦU control_leds]) --> CheckTemp1{Nhiệt độ<br/>> 40°C?}
    
    CheckTemp1 -->|Có| CheckRedState1{LED đỏ<br/>đã bật?}
    CheckTemp1 -->|Không| CheckTemp2{Nhiệt độ<br/>< 30°C?}
    
    CheckRedState1 -->|Chưa| TurnOnRed[Bật LED đỏ<br/>led_red_state = True<br/>In thông báo]
    CheckRedState1 -->|Đã bật| CheckTemp2
    
    CheckTemp2 -->|Có| CheckRedState2{LED đỏ<br/>đang bật?}
    CheckTemp2 -->|Không| CheckHumi1
    
    CheckRedState2 -->|Có| TurnOffRed[Tắt LED đỏ<br/>led_red_state = False<br/>In thông báo]
    CheckRedState2 -->|Không| CheckHumi1
    
    TurnOnRed --> CheckHumi1{Độ ẩm<br/>> 70%?}
    TurnOffRed --> CheckHumi1
    
    CheckHumi1 -->|Có| CheckYellowState1{LED vàng<br/>đã bật?}
    CheckHumi1 -->|Không| CheckHumi2{Độ ẩm<br/>< 40%?}
    
    CheckYellowState1 -->|Chưa| TurnOnYellow[Bật LED vàng<br/>led_yellow_state = True<br/>In thông báo]
    CheckYellowState1 -->|Đã bật| End
    
    CheckHumi2 -->|Có| CheckYellowState2{LED vàng<br/>đang bật?}
    CheckHumi2 -->|Không| End
    
    CheckYellowState2 -->|Có| TurnOffYellow[Tắt LED vàng<br/>led_yellow_state = False<br/>In thông báo]
    CheckYellowState2 -->|Không| End
    
    TurnOnYellow --> End([KẾT THÚC])
    TurnOffYellow --> End
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style CheckTemp1 fill:#FFD700
    style CheckTemp2 fill:#FFD700
    style CheckHumi1 fill:#FFD700
    style CheckHumi2 fill:#FFD700
    style TurnOnRed fill:#FF6B6B
    style TurnOffRed fill:#4ECDC4
    style TurnOnYellow fill:#FFE66D
    style TurnOffYellow fill:#4ECDC4
```

## 4. Lưu đồ điều khiển Buzzer (control_buzzer)

```mermaid
flowchart TD
    Start([BẮT ĐẦU control_buzzer]) --> GetTime[Lấy thời gian hiện tại<br/>current_time = time]
    GetTime --> CheckTemp{Nhiệt độ<br/>> 50°C?}
    
    CheckTemp -->|Có| CheckBuzzerState{Buzzer đã<br/>được kích hoạt?}
    CheckTemp -->|Không| CheckBuzzerOff{Buzzer đang<br/>hoạt động?}
    
    CheckBuzzerState -->|Chưa| InitBuzzer[Khởi tạo buzzer<br/>buzzer_state = True<br/>buzzer_is_on = True<br/>buzzer_last_toggle_time = current_time<br/>Bật buzzer<br/>In thông báo]
    CheckBuzzerState -->|Đã kích hoạt| CheckTime{Đã qua<br/>1 giây?<br/>current_time - buzzer_last_toggle_time >= 1.0}
    
    CheckTime -->|Có| ToggleBuzzer[Toggle trạng thái buzzer<br/>buzzer_is_on = not buzzer_is_on<br/>Cập nhật buzzer_last_toggle_time]
    CheckTime -->|Chưa| End
    
    ToggleBuzzer --> CheckBuzzerOn{buzzer_is_on<br/>= True?}
    CheckBuzzerOn -->|Có| TurnOnBuzzer[Bật buzzer]
    CheckBuzzerOn -->|Không| TurnOffBuzzer[Tắt buzzer]
    
    CheckBuzzerOff -->|Có| TurnOffBuzzer2[Tắt buzzer<br/>buzzer_state = False<br/>buzzer_is_on = False<br/>In thông báo]
    CheckBuzzerOff -->|Không| End
    
    InitBuzzer --> End([KẾT THÚC])
    TurnOnBuzzer --> End
    TurnOffBuzzer --> End
    TurnOffBuzzer2 --> End
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style CheckTemp fill:#FFD700
    style CheckBuzzerState fill:#FFD700
    style CheckTime fill:#FFD700
    style InitBuzzer fill:#FF6B6B
    style TurnOnBuzzer fill:#FF6B6B
    style TurnOffBuzzer fill:#4ECDC4
    style TurnOffBuzzer2 fill:#4ECDC4
```

## 5. Lưu đồ gửi dữ liệu lên ThingSpeak (thingspeak_mqtt)

```mermaid
flowchart TD
    Start([BẮT ĐẦU thingspeak_mqtt]) --> PrepareData[Chuẩn bị dữ liệu<br/>Channel_ID = '3153408'<br/>Tạo chuỗi dữ liệu:<br/>field1=temp<br/>field2=humi<br/>field3=led_yellow_status<br/>field4=led_red_status]
    PrepareData --> Publish[Gửi dữ liệu qua MQTT<br/>client.publish<br/>channels/Channel_ID/publish]
    Publish --> End([KẾT THÚC])
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style Publish fill:#87CEEB
```

## 6. Lưu đồ Node-RED nhận và hiển thị dữ liệu

```mermaid
flowchart TD
    Start([BẮT ĐẦU Node-RED Flow]) --> InitMQTT[Khởi tạo MQTT Broker<br/>Kết nối ThingSpeak]
    InitMQTT --> Connect{Đã kết nối<br/>MQTT?}
    
    Connect -->|Chưa| WaitConnect[Chờ kết nối]
    WaitConnect --> Connect
    Connect -->|Đã kết nối| Subscribe[Subscribe các topic:<br/>- channels/3153408/subscribe/fields/field1<br/>- channels/3153408/subscribe/fields/field2]
    
    Subscribe --> Listen[Lắng nghe dữ liệu]
    
    Listen --> ReceiveTemp{Nhận dữ liệu<br/>Nhiệt độ?}
    Listen --> ReceiveHumi{Nhận dữ liệu<br/>Độ ẩm?}
    
    ReceiveTemp -->|Có| ParseTemp[Parse Nhiệt độ<br/>parseFloat payload]
    ReceiveHumi -->|Có| ParseHumi[Parse Độ ẩm<br/>parseFloat payload]
    
    ParseTemp --> CheckValidTemp{Giá trị<br/>hợp lệ?}
    ParseHumi --> CheckValidHumi{Giá trị<br/>hợp lệ?}
    
    CheckValidTemp -->|Có| UpdateGaugeTemp[Cập nhật Gauge Nhiệt độ<br/>Hiển thị trên Dashboard]
    CheckValidTemp -->|Không| DebugTemp[Debug: Giá trị không hợp lệ]
    
    CheckValidHumi -->|Có| UpdateGaugeHumi[Cập nhật Gauge Độ ẩm<br/>Hiển thị trên Dashboard]
    CheckValidHumi -->|Không| DebugHumi[Debug: Giá trị không hợp lệ]
    
    UpdateGaugeTemp --> Listen
    UpdateGaugeHumi --> Listen
    DebugTemp --> Listen
    DebugHumi --> Listen
    
    style Start fill:#90EE90
    style Connect fill:#FFD700
    style ReceiveTemp fill:#87CEEB
    style ReceiveHumi fill:#87CEEB
    style UpdateGaugeTemp fill:#4ECDC4
    style UpdateGaugeHumi fill:#4ECDC4
```

## 7. Lưu đồ chi tiết Node-RED Flow

```mermaid
flowchart LR
    subgraph MQTT["MQTT INPUT"]
        A1[MQTT In - Nhiệt độ<br/>Topic: field1] --> A2[MQTT In - Độ ẩm<br/>Topic: field2]
    end
    
    subgraph Parse["PARSE DATA"]
        B1[Function Parse<br/>Nhiệt độ] --> B2[Function Parse<br/>Độ ẩm]
    end
    
    subgraph Display["DISPLAY"]
        C1[Gauge Nhiệt độ<br/>0-100°C] --> C2[Gauge Độ ẩm<br/>0-100%]
        D1[Debug Nhiệt độ] --> D2[Debug Độ ẩm]
    end
    
    A1 -->|Payload| B1
    A1 -->|Payload| C1
    A2 -->|Payload| B2
    A2 -->|Payload| C2
    
    B1 --> D1
    B2 --> D2
    
    C1 -->|Web UI| User[User Dashboard]
    C2 -->|Web UI| User
    
    style MQTT fill:#E3F2FD
    style Parse fill:#FFF3E0
    style Display fill:#E8F5E9
    style User fill:#FCE4EC
```

## 8. Lưu đồ luồng dữ liệu tổng thể

```mermaid
sequenceDiagram
    participant RPi as Raspberry Pi
    participant TS as ThingSpeak Server
    participant NR as Node-RED
    participant UI as Web Dashboard
    
    RPi->>RPi: Đọc cảm biến DHT11
    RPi->>RPi: Điều khiển LED & Buzzer
    RPi->>TS: MQTT Publish (temp, humi, LED status)
    TS->>TS: Lưu trữ dữ liệu
    TS->>NR: MQTT Publish (field1, field2)
    NR->>NR: Parse dữ liệu
    NR->>NR: Cập nhật Gauge
    NR->>UI: Hiển thị trên Dashboard
    UI->>UI: User xem nhiệt độ & độ ẩm
```

## Mô tả các thành phần:

### Raspberry Pi (Python):
- **Cảm biến**: DHT11 đọc nhiệt độ và độ ẩm
- **Điều khiển**: LED đỏ (nhiệt độ), LED vàng (độ ẩm), Buzzer (cảnh báo)
- **Gửi dữ liệu**: MQTT Publish lên ThingSpeak mỗi 10 giây (hoặc 1 giây nếu buzzer hoạt động)

### ThingSpeak Server:
- **Nhận dữ liệu**: Qua MQTT từ Raspberry Pi
- **Lưu trữ**: Field1 (nhiệt độ), Field2 (độ ẩm), Field3 (LED vàng), Field4 (LED đỏ)
- **Publish**: Gửi lại dữ liệu qua MQTT cho các subscriber

### Node-RED Dashboard:
- **Subscribe**: Nhận dữ liệu từ ThingSpeak qua MQTT
- **Parse**: Chuyển đổi string sang số
- **Hiển thị**: Gauge trên giao diện web
- **Truy cập**: `http://localhost:1880/ui` hoặc `http://[IP]:1880/ui`

### Logic điều khiển:
- **LED đỏ**: Bật khi temp > 40°C, tắt khi temp < 30°C
- **LED vàng**: Bật khi humi > 70%, tắt khi humi < 40%
- **Buzzer**: Bật/tắt mỗi 1 giây khi temp > 50°C
