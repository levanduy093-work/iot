# Lưu đồ giải thuật - Hệ thống giám sát nhiệt độ và độ ẩm

## 1. Lưu đồ chương trình chính (main)

```mermaid
flowchart TD
    Start([BẮT ĐẦU]) --> Init[Khởi tạo MQTT Client<br/>Khởi tạo DHT11 Sensor<br/>Khởi tạo LED và Buzzer]
    Init --> PrintStart[In thông báo khởi động]
    PrintStart --> Loop{Vòng lặp chính}
    
    Loop --> ReadSensor[Đọc dữ liệu từ DHT11<br/>humi, temp = sensor.read]
    ReadSensor --> Display[Hiển thị nhiệt độ và độ ẩm<br/>lên Terminal]
    Display --> ControlLED[Gọi hàm control_leds]
    ControlLED --> ControlBuzzer[Gọi hàm control_buzzer]
    ControlBuzzer --> SendMQTT[Gửi dữ liệu lên ThingSpeak<br/>qua MQTT]
    SendMQTT --> CheckBuzzer{Buzzer đang<br/>hoạt động?}
    
    CheckBuzzer -->|Có| Sleep1[Chờ 1 giây]
    CheckBuzzer -->|Không| Sleep10[Chờ 10 giây]
    
    Sleep1 --> Loop
    Sleep10 --> Loop
    
    Loop -.->|Ctrl+C| Interrupt[Nhận KeyboardInterrupt]
    Interrupt --> Cleanup[Tắt tất cả LED và Buzzer<br/>Ngắt kết nối MQTT]
    Cleanup --> End([KẾT THÚC])
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style Loop fill:#87CEEB
    style CheckBuzzer fill:#FFD700
```

## 2. Lưu đồ điều khiển LED (control_leds)

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

## 3. Lưu đồ điều khiển Buzzer (control_buzzer)

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

## 4. Lưu đồ gửi dữ liệu lên ThingSpeak (thingspeak_mqtt)

```mermaid
flowchart TD
    Start([BẮT ĐẦU thingspeak_mqtt]) --> PrepareData[Chuẩn bị dữ liệu<br/>Channel_ID = '3153408'<br/>Tạo chuỗi dữ liệu:<br/>field1=temp<br/>field2=humi<br/>field3=led_yellow_status<br/>field4=led_red_status]
    PrepareData --> Publish[Gửi dữ liệu qua MQTT<br/>client.publish<br/>channels/Channel_ID/publish]
    Publish --> End([KẾT THÚC])
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style Publish fill:#87CEEB
```

## 5. Lưu đồ tổng quan hệ thống

```mermaid
flowchart TB
    subgraph Init["KHỞI TẠO"]
        A1[Khởi tạo MQTT Client] --> A2[Khởi tạo DHT11 Sensor]
        A2 --> A3[Khởi tạo LED đỏ, LED vàng]
        A3 --> A4[Khởi tạo Buzzer]
    end
    
    subgraph MainLoop["VÒNG LẶP CHÍNH"]
        B1[Đọc cảm biến DHT11] --> B2[Hiển thị dữ liệu]
        B2 --> B3[Điều khiển LED]
        B3 --> B4[Điều khiển Buzzer]
        B4 --> B5[Gửi lên ThingSpeak]
        B5 --> B6{Chờ thời gian}
        B6 -->|Buzzer hoạt động| B7[Chờ 1 giây]
        B6 -->|Buzzer không hoạt động| B8[Chờ 10 giây]
        B7 --> B1
        B8 --> B1
    end
    
    subgraph LEDControl["ĐIỀU KHIỂN LED"]
        C1{Nhiệt độ > 40°C?} -->|Có| C2[Bật LED đỏ]
        C1 -->|Không| C3{Nhiệt độ < 30°C?}
        C3 -->|Có| C4[Tắt LED đỏ]
        C3 -->|Không| C5{Độ ẩm > 70%?}
        C5 -->|Có| C6[Bật LED vàng]
        C5 -->|Không| C7{Độ ẩm < 40%?}
        C7 -->|Có| C8[Tắt LED vàng]
    end
    
    subgraph BuzzerControl["ĐIỀU KHIỂN BUZZER"]
        D1{Nhiệt độ > 50°C?} -->|Có| D2{Buzzer đã kích hoạt?}
        D2 -->|Chưa| D3[Khởi tạo và bật buzzer]
        D2 -->|Đã kích hoạt| D4{Đã qua 1 giây?}
        D4 -->|Có| D5[Toggle buzzer on/off]
        D1 -->|Không| D6{Tắt buzzer nếu đang bật}
    end
    
    Init --> MainLoop
    B3 --> LEDControl
    B4 --> BuzzerControl
    
    style Init fill:#E8F5E9
    style MainLoop fill:#E3F2FD
    style LEDControl fill:#FFF3E0
    style BuzzerControl fill:#FCE4EC
```

## Mô tả các thành phần:

### Khởi tạo:
- **MQTT Client**: Kết nối với ThingSpeak qua MQTT
- **DHT11 Sensor**: Cảm biến nhiệt độ và độ ẩm (port D5)
- **LED đỏ**: Pin 16, cảnh báo nhiệt độ
- **LED vàng**: Pin 18, cảnh báo độ ẩm
- **Buzzer**: Pin 12, cảnh báo âm thanh

### Logic điều khiển:
- **LED đỏ**: Bật khi temp > 40°C, tắt khi temp < 30°C
- **LED vàng**: Bật khi humi > 70%, tắt khi humi < 40%
- **Buzzer**: Bật/tắt mỗi 1 giây khi temp > 50°C

### Gửi dữ liệu:
- Gửi nhiệt độ, độ ẩm và trạng thái LED lên ThingSpeak mỗi chu kỳ

