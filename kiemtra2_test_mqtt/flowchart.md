# Lưu đồ giải thuật - Hệ thống giám sát nhiệt độ và độ ẩm với ThingSpeak MQTT

## 1. Lưu đồ tổng quan hệ thống

```mermaid
flowchart TB
    subgraph RaspberryPi["RASPBERRY PI"]
        A1[Đọc cảm biến DHT11] --> A2[Xử lý dữ liệu]
        A2 --> A3[Điều khiển LED & Buzzer]
        A3 --> A4[Gửi lên ThingSpeak MQTT]
    end
    
    subgraph ThingSpeak["THINGSPEAK SERVER"]
        B1[Nhận dữ liệu MQTT Publish] --> B2[Lưu trữ dữ liệu<br/>Field1: Nhiệt độ<br/>Field2: Độ ẩm]
        B2 --> B3[MQTT Broker sẵn sàng]
    end
    
    subgraph NodeRED["NODE-RED DASHBOARD"]
        C1[MQTT Subscribe] --> C2[Nhận dữ liệu real-time]
        C2 --> C3[Parse dữ liệu]
        C3 --> C4[Hiển thị trên Gauge]
    end
    
    A4 -->|MQTT Publish| B1
    B3 -->|MQTT Subscribe| C1
    C4 -->|Web UI| User[Người dùng xem Dashboard]
    
    style RaspberryPi fill:#E8F5E9
    style ThingSpeak fill:#E3F2FD
    style NodeRED fill:#FFF3E0
    style User fill:#FCE4EC
```

## 2. Lưu đồ chương trình Python (Raspberry Pi) - Chương trình chính

```mermaid
flowchart TD
    Start([BẮT ĐẦU]) --> Init[Khởi tạo:<br/>- DHT11 Sensor D5<br/>- LED đỏ D16<br/>- LED vàng D18<br/>- Buzzer D12]
    Init --> InitMQTT[Khởi tạo MQTT Client:<br/>- Client ID<br/>- Username/Password<br/>- Connect mqtt3.thingspeak.com:1883]
    InitMQTT --> PrintStart[In thông báo khởi động<br/>Hiển thị ngưỡng điều khiển]
    PrintStart --> Loop{Vòng lặp chính<br/>While True}
    
    Loop --> ReadSensor[Đọc cảm biến DHT11<br/>humi, temp = sensor.read]
    ReadSensor --> CheckValid{Dữ liệu<br/>hợp lệ?<br/>humi != None<br/>temp != None}
    
    CheckValid -->|Không| SleepRetry[Chờ 5 giây<br/>Thử lại]
    SleepRetry --> Loop
    CheckValid -->|Có| Display[Hiển thị Terminal:<br/>Nhiệt độ và Độ ẩm]
    
    Display --> ControlLED[Gọi hàm control_leds<br/>Điều khiển LED đỏ và vàng]
    ControlLED --> ControlBuzzer[Gọi hàm control_buzzer<br/>Điều khiển buzzer]
    ControlBuzzer --> SendMQTT[Gọi hàm thingspeak_mqtt<br/>Gửi dữ liệu lên ThingSpeak]
    
    SendMQTT --> CheckBuzzer{Buzzer đang<br/>hoạt động?}
    
    CheckBuzzer -->|Có| Sleep1[Chờ 1 giây<br/>Để toggle buzzer]
    CheckBuzzer -->|Không| Sleep10[Chờ 10 giây]
    
    Sleep1 --> Loop
    Sleep10 --> Loop
    
    Loop -.->|Ctrl+C| Interrupt[Nhận KeyboardInterrupt]
    Interrupt --> Cleanup[Tắt LED và Buzzer<br/>Disconnect MQTT]
    Cleanup --> End([KẾT THÚC])
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style Loop fill:#87CEEB
    style CheckValid fill:#FFD700
    style CheckBuzzer fill:#FFD700
```

## 3. Lưu đồ điều khiển LED đỏ (theo nhiệt độ)

```mermaid
flowchart TD
    Start([BẮT ĐẦU control_leds]) --> Input[Input: temp, humi]
    Input --> CheckTempHigh{temp<br/>> 40°C?}
    
    CheckTempHigh -->|Có| CheckRedOn{LED đỏ<br/>đang BẬT?}
    CheckTempHigh -->|Không| CheckTempLow{temp<br/>< 30°C?}
    
    CheckRedOn -->|Chưa| TurnOnRed[Bật LED đỏ<br/>led_red.on<br/>led_red_state = True<br/>In: LED ĐỎ BẬT]
    CheckRedOn -->|Rồi| CheckHumi{Điều khiển<br/>LED vàng}
    TurnOnRed --> CheckHumi
    
    CheckTempLow -->|Có| CheckRedOff{LED đỏ<br/>đang BẬT?}
    CheckTempLow -->|Không| CheckHumi
    
    CheckRedOff -->|Có| TurnOffRed[Tắt LED đỏ<br/>led_red.off<br/>led_red_state = False<br/>In: LED ĐỎ TẮT]
    CheckRedOff -->|Không| CheckHumi
    TurnOffRed --> CheckHumi
    
    CheckHumi --> End([KẾT THÚC])
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style CheckTempHigh fill:#FFD700
    style CheckTempLow fill:#FFD700
```

## 4. Lưu đồ điều khiển LED vàng (theo độ ẩm)

```mermaid
flowchart TD
    Start([Điều khiển LED vàng]) --> CheckHumiHigh{humi<br/>> 70%?}
    
    CheckHumiHigh -->|Có| CheckYellowOn{LED vàng<br/>đang BẬT?}
    CheckHumiHigh -->|Không| CheckHumiLow{humi<br/>< 40%?}
    
    CheckYellowOn -->|Chưa| TurnOnYellow[Bật LED vàng<br/>led_yellow.on<br/>led_yellow_state = True<br/>In: LED VÀNG BẬT]
    CheckYellowOn -->|Rồi| End([KẾT THÚC])
    TurnOnYellow --> End
    
    CheckHumiLow -->|Có| CheckYellowOff{LED vàng<br/>đang BẬT?}
    CheckHumiLow -->|Không| End
    
    CheckYellowOff -->|Có| TurnOffYellow[Tắt LED vàng<br/>led_yellow.off<br/>led_yellow_state = False<br/>In: LED VÀNG TẮT]
    CheckYellowOff -->|Không| End
    TurnOffYellow --> End
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style CheckHumiHigh fill:#FFD700
    style CheckHumiLow fill:#FFD700
```

## 5. Lưu đồ điều khiển Buzzer (theo nhiệt độ)

```mermaid
flowchart TD
    Start([BẮT ĐẦU control_buzzer]) --> Input[Input: temp]
    Input --> CheckTemp{temp<br/>> 50°C?}
    
    CheckTemp -->|Có| CheckBuzzerState{Buzzer đang<br/>hoạt động?}
    CheckTemp -->|Không| CheckBuzzerOff{Buzzer đang<br/>BẬT?}
    
    CheckBuzzerState -->|Chưa| InitBuzzer[Khởi tạo buzzer:<br/>buzzer_state = True<br/>buzzer_last_toggle_time = now<br/>buzzer_is_on = True<br/>buzzer.on<br/>In: CHUÔNG BẬT]
    CheckBuzzerState -->|Rồi| CheckTime{Đã qua<br/>1 giây?<br/>now - last_toggle >= 1.0}
    
    InitBuzzer --> End([KẾT THÚC])
    
    CheckTime -->|Có| ToggleBuzzer[Toggle buzzer:<br/>buzzer_is_on = !buzzer_is_on<br/>buzzer_last_toggle_time = now<br/>Nếu buzzer_is_on: buzzer.on<br/>Nếu không: buzzer.off]
    CheckTime -->|Chưa| End
    ToggleBuzzer --> End
    
    CheckBuzzerOff -->|Có| TurnOffBuzzer[Tắt buzzer:<br/>buzzer.off<br/>buzzer_state = False<br/>buzzer_is_on = False<br/>In: CHUÔNG TẮT]
    CheckBuzzerOff -->|Không| End
    TurnOffBuzzer --> End
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style CheckTemp fill:#FFD700
    style CheckTime fill:#FFD700
```

## 6. Lưu đồ gửi dữ liệu lên ThingSpeak (MQTT Publish)

```mermaid
flowchart TD
    Start([BẮT ĐẦU thingspeak_mqtt]) --> Input[Input: temp, humi]
    Input --> CheckChannel{CHANNEL_ID<br/>đã cấu hình?}
    
    CheckChannel -->|Chưa| PrintWarning[In cảnh báo:<br/>Chưa cấu hình Channel ID<br/>Return]
    CheckChannel -->|Có| CreateTopic[Tạo MQTT Topic:<br/>channels/CHANNEL_ID/publish]
    
    PrintWarning --> End([KẾT THÚC])
    
    CreateTopic --> CreatePayload[Tạo Payload:<br/>field1=temp&field2=humi<br/>&status=MQTTPUBLISH]
    CreatePayload --> Publish[Gửi MQTT Publish:<br/>client.publish topic, payload]
    Publish --> End
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style CheckChannel fill:#FFD700
```

## 7. Lưu đồ Node-RED nhận và hiển thị dữ liệu (MQTT)

```mermaid
flowchart TD
    Start([BẮT ĐẦU Node-RED Flow]) --> InitMQTT[Khởi tạo MQTT Broker:<br/>mqtt3.thingspeak.com:1883<br/>Username/Password]
    InitMQTT --> ConnectMQTT{Kết nối<br/>MQTT thành công?}
    
    ConnectMQTT -->|Không| Error[Debug Error]
    Error --> Wait[Chờ kết nối lại]
    Wait --> ConnectMQTT
    
    ConnectMQTT -->|Có| SubscribeTemp[MQTT Subscribe:<br/>Topic: channels/CHANNEL_ID/<br/>subscribe/fields/field1]
    ConnectMQTT -->|Có| SubscribeHumi[MQTT Subscribe:<br/>Topic: channels/CHANNEL_ID/<br/>subscribe/fields/field2]
    
    SubscribeTemp --> ReceiveTemp[Nhận message<br/>nhiệt độ]
    SubscribeHumi --> ReceiveHumi[Nhận message<br/>độ ẩm]
    
    ReceiveTemp --> ParseTemp[Function: Parse Nhiệt độ<br/>parseFloat payload]
    ReceiveHumi --> ParseHumi[Function: Parse Độ ẩm<br/>parseFloat payload]
    
    ParseTemp --> CheckValidTemp{Giá trị<br/>hợp lệ?<br/>!isNaN}
    ParseHumi --> CheckValidHumi{Giá trị<br/>hợp lệ?<br/>!isNaN}
    
    CheckValidTemp -->|Không| ReturnNullTemp[Return null]
    CheckValidTemp -->|Có| UpdateGaugeTemp[Cập nhật Gauge Nhiệt độ<br/>Hiển thị trên Dashboard]
    CheckValidTemp -->|Có| DebugTemp[Debug: Nhiệt độ]
    
    CheckValidHumi -->|Không| ReturnNullHumi[Return null]
    CheckValidHumi -->|Có| UpdateGaugeHumi[Cập nhật Gauge Độ ẩm<br/>Hiển thị trên Dashboard]
    CheckValidHumi -->|Có| DebugHumi[Debug: Độ ẩm]
    
    UpdateGaugeTemp --> Wait
    UpdateGaugeHumi --> Wait
    DebugTemp --> Wait
    DebugHumi --> Wait
    ReturnNullTemp --> Wait
    ReturnNullHumi --> Wait
    Wait --> ReceiveTemp
    Wait --> ReceiveHumi
    
    style Start fill:#90EE90
    style ConnectMQTT fill:#FFD700
    style CheckValidTemp fill:#FFD700
    style CheckValidHumi fill:#FFD700
    style UpdateGaugeTemp fill:#4ECDC4
    style UpdateGaugeHumi fill:#4ECDC4
```

## 8. Lưu đồ chi tiết Node-RED Flow

```mermaid
flowchart LR
    subgraph MQTT["MQTT BROKER"]
        A1[ThingSpeak MQTT<br/>mqtt3.thingspeak.com] --> A2[Connected]
    end
    
    subgraph Subscribe["MQTT SUBSCRIBE"]
        B1[MQTT In: Nhiệt độ<br/>Topic: field1] --> B2[MQTT In: Độ ẩm<br/>Topic: field2]
    end
    
    subgraph Parse["PARSE DATA"]
        C1[Function Parse<br/>Nhiệt độ] --> C2[Function Parse<br/>Độ ẩm]
    end
    
    subgraph Display["DISPLAY"]
        D1[Gauge Nhiệt độ<br/>0-100°C] --> D2[Gauge Độ ẩm<br/>0-100%]
        E1[Debug Nhiệt độ] --> E2[Debug Độ ẩm]
    end
    
    A2 --> B1
    A2 --> B2
    B1 --> C1
    B2 --> C2
    C1 --> D1
    C1 --> E1
    C2 --> D2
    C2 --> E2
    
    D1 -->|Web UI| User[User Dashboard]
    D2 -->|Web UI| User
    
    style MQTT fill:#E3F2FD
    style Subscribe fill:#FFF3E0
    style Parse fill:#E8F5E9
    style Display fill:#FCE4EC
```

## 9. Lưu đồ luồng dữ liệu tổng thể (MQTT)

```mermaid
sequenceDiagram
    participant RPi as Raspberry Pi
    participant TS as ThingSpeak MQTT Broker
    participant NR as Node-RED
    participant UI as Web Dashboard
    
    RPi->>RPi: Đọc cảm biến DHT11
    RPi->>RPi: Điều khiển LED đỏ (temp > 40°C)
    RPi->>RPi: Điều khiển LED vàng (humi > 70%)
    RPi->>RPi: Điều khiển Buzzer (temp > 50°C)
    RPi->>TS: MQTT Publish (field1=temp, field2=humi)
    TS->>TS: Lưu trữ dữ liệu
    
    Note over NR: MQTT Subscribe (real-time)
    TS->>NR: MQTT Message (field1: nhiệt độ)
    TS->>NR: MQTT Message (field2: độ ẩm)
    NR->>NR: Parse JSON
    NR->>NR: Cập nhật Gauge
    NR->>UI: Hiển thị trên Dashboard
    UI->>UI: User xem nhiệt độ & độ ẩm
```

## 10. Lưu đồ logic điều khiển thiết bị

```mermaid
flowchart TD
    Start([Đọc giá trị cảm biến]) --> ReadSensor[temp, humi]
    
    ReadSensor --> CheckTempHigh{temp > 40°C?}
    ReadSensor --> CheckTempBuzzer{temp > 50°C?}
    ReadSensor --> CheckHumiHigh{humi > 70%?}
    ReadSensor --> CheckTempLow{temp < 30°C?}
    ReadSensor --> CheckHumiLow{humi < 40%?}
    
    CheckTempHigh -->|Có| TurnOnRed[Bật LED đỏ]
    CheckTempHigh -->|Không| CheckTempLow
    
    CheckTempLow -->|Có| TurnOffRed[Tắt LED đỏ]
    CheckTempLow -->|Không| KeepRedState[Giữ nguyên LED đỏ]
    
    CheckTempBuzzer -->|Có| ToggleBuzzer[Buzzer: 1s ON, 1s OFF<br/>Lặp lại]
    CheckTempBuzzer -->|Không| TurnOffBuzzer[Tắt Buzzer]
    
    CheckHumiHigh -->|Có| TurnOnYellow[Bật LED vàng]
    CheckHumiHigh -->|Không| CheckHumiLow
    
    CheckHumiLow -->|Có| TurnOffYellow[Tắt LED vàng]
    CheckHumiLow -->|Không| KeepYellowState[Giữ nguyên LED vàng]
    
    TurnOnRed --> End([KẾT THÚC])
    TurnOffRed --> End
    KeepRedState --> End
    TurnOnYellow --> End
    TurnOffYellow --> End
    KeepYellowState --> End
    ToggleBuzzer --> End
    TurnOffBuzzer --> End
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style CheckTempHigh fill:#FFD700
    style CheckTempBuzzer fill:#FFD700
    style CheckHumiHigh fill:#FFD700
    style TurnOnRed fill:#FF6B6B
    style TurnOnYellow fill:#FFE66D
```

## Mô tả các thành phần:

### Raspberry Pi (Python):
- **Cảm biến**: DHT11 đọc nhiệt độ và độ ẩm (D5)
- **LED đỏ**: Grove LED (D16) - bật khi nhiệt độ > 40°C, tắt khi < 30°C
- **LED vàng**: Grove LED (D18) - bật khi độ ẩm > 70%, tắt khi < 40%
- **Buzzer**: Grove Buzzer (D12) - 1s bip, 1s không, lặp lại khi nhiệt độ > 50°C
- **Gửi dữ liệu**: MQTT Publish lên ThingSpeak (real-time)
- **Đọc cảm biến**: Mỗi 10 giây (hoặc 1 giây nếu buzzer hoạt động)

### ThingSpeak MQTT Broker:
- **Nhận dữ liệu**: Qua MQTT Publish từ Raspberry Pi
- **Lưu trữ**: 
  - Field1: Nhiệt độ (°C)
  - Field2: Độ ẩm (%)
- **MQTT Broker**: `mqtt3.thingspeak.com:1883`
- **Topic Publish**: `channels/[CHANNEL_ID]/publish`
- **Topic Subscribe**: `channels/[CHANNEL_ID]/subscribe/fields/field1` và `field2`

### Node-RED Dashboard (MQTT):
- **MQTT Broker**: Kết nối với ThingSpeak MQTT
- **MQTT Subscribe**: Subscribe các topic field1 và field2
- **Parse**: Chuyển đổi payload sang số (parseFloat)
- **Hiển thị**: 
  - Gauge cho nhiệt độ (0-100°C)
  - Gauge cho độ ẩm (0-100%)
- **Truy cập**: `http://localhost:1880/ui` hoặc `http://[IP]:1880/ui`

### Logic điều khiển:
- **LED đỏ**: 
  - Bật khi nhiệt độ > 40°C
  - Tắt khi nhiệt độ < 30°C
  - Giữ nguyên khi 30°C ≤ nhiệt độ ≤ 40°C
- **LED vàng**: 
  - Bật khi độ ẩm > 70%
  - Tắt khi độ ẩm < 40%
  - Giữ nguyên khi 40% ≤ độ ẩm ≤ 70%
- **Buzzer**: 
  - Bật khi nhiệt độ > 50°C
  - Chế độ: 1 giây ON, 1 giây OFF, lặp lại
  - Tắt khi nhiệt độ ≤ 50°C

### Ngưỡng điều khiển:
- **TEMP_THRESHOLD_HIGH**: 40°C (bật LED đỏ)
- **TEMP_THRESHOLD_LOW**: 30°C (tắt LED đỏ)
- **TEMP_BUZZER_THRESHOLD**: 50°C (bật buzzer)
- **HUMI_THRESHOLD_HIGH**: 70% (bật LED vàng)
- **HUMI_THRESHOLD_LOW**: 40% (tắt LED vàng)

### Ưu điểm MQTT:
- **Real-time**: Dữ liệu được gửi và nhận ngay lập tức
- **Hiệu quả**: Giao thức nhẹ, tiết kiệm băng thông
- **Đáng tin cậy**: QoS đảm bảo gửi nhận dữ liệu
- **Không cần polling**: Không cần gửi request liên tục như HTTP

### Xử lý lỗi:
- **Lỗi đọc cảm biến**: Gán giá trị None và thử lại sau 5 giây
- **Lỗi MQTT**: In thông báo lỗi và tiếp tục vòng lặp
- **KeyboardInterrupt**: Tắt tất cả thiết bị, disconnect MQTT và thoát an toàn

