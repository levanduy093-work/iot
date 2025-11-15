# Lưu đồ giải thuật - Hệ thống giám sát ánh sáng và khoảng cách với ThingSpeak HTTP

## 1. Lưu đồ tổng quan hệ thống

```mermaid
flowchart TB
    subgraph RaspberryPi["RASPBERRY PI"]
        A1[Đọc cảm biến ánh sáng A0] --> A2[Đọc cảm biến khoảng cách D5]
        A2 --> A3[Xử lý dữ liệu]
        A3 --> A4[Điều khiển LED & Buzzer/Motor]
        A4 --> A5[Hiển thị Terminal & LCD]
        A5 --> A6[Gửi lên ThingSpeak HTTP API]
    end
    
    subgraph ThingSpeak["THINGSPEAK SERVER"]
        B1[Nhận dữ liệu HTTP POST] --> B2[Lưu trữ dữ liệu<br/>Field1: Ánh sáng<br/>Field2: Khoảng cách]
        B2 --> B3[API Endpoint sẵn sàng]
    end
    
    subgraph NodeRED["NODE-RED DASHBOARD"]
        C1[Timer mỗi 10 giây] --> C2[HTTP GET Request]
        C2 --> C3[Parse dữ liệu JSON]
        C3 --> C4[Hiển thị Gauge & Bar Chart]
    end
    
    A6 -->|HTTP POST| B1
    B3 -->|HTTP GET| C2
    C4 -->|Web UI| User[Người dùng xem Dashboard]
    
    style RaspberryPi fill:#E8F5E9
    style ThingSpeak fill:#E3F2FD
    style NodeRED fill:#FFF3E0
    style User fill:#FCE4EC
```

## 2. Lưu đồ chương trình Python (Raspberry Pi) - Chương trình chính

```mermaid
flowchart TD
    Start([BẮT ĐẦU]) --> Init[Khởi tạo:<br/>- Light Sensor A0<br/>- Ultrasonic Sensor D5<br/>- LED đỏ D16, LED vàng D18<br/>- Buzzer D12<br/>- Vibration Motor D13<br/>- LCD I2C]
    Init --> PrintStart[In thông báo khởi động<br/>Hiển thị ngưỡng điều khiển]
    PrintStart --> InitLCD[Khởi tạo LCD<br/>Hiển thị 'Initializing...']
    InitLCD --> SetVars[Khởi tạo biến:<br/>READ_INTERVAL = 10s<br/>last_sent_ts = 0<br/>API_KEY_WRITE]
    SetVars --> Loop{Vòng lặp chính<br/>While True}
    
    Loop --> ReadLight[Đọc cảm biến ánh sáng<br/>light_value = light_sensor.value]
    ReadLight --> CheckLightError{Lỗi đọc<br/>ánh sáng?}
    
    CheckLightError -->|Có| SetLightZero[light_value = 0<br/>In lỗi]
    CheckLightError -->|Không| ReadDistance[Đọc cảm biến khoảng cách<br/>distance_value = ultrasonic_sensor.get_distance]
    
    SetLightZero --> ReadDistance
    ReadDistance --> CheckDistError{Lỗi đọc<br/>khoảng cách?}
    
    CheckDistError -->|Có| SetDistZero[distance_value = 0<br/>In lỗi]
    CheckDistError -->|Không| DisplayTerminal[Hiển thị Terminal:<br/>- Cường độ ánh sáng<br/>- Khoảng cách]
    
    SetDistZero --> DisplayTerminal
    DisplayTerminal --> DisplayLCD[Gọi display_on_lcd<br/>Hiển thị trên LCD 16x2]
    
    DisplayLCD --> ControlRedBuzzer[Gọi control_led_red_buzzer<br/>Điều khiển LED đỏ + Buzzer]
    ControlRedBuzzer --> ControlYellowVib[Gọi control_led_yellow_vibration<br/>Điều khiển LED vàng + Motor rung]
    
    ControlYellowVib --> CheckTime{Đã qua<br/>10 giây?<br/>now - last_sent_ts >= 10}
    
    CheckTime -->|Chưa| Sleep10[Chờ 10 giây<br/>sleep READ_INTERVAL]
    CheckTime -->|Có| CheckAPIKey{API_KEY_WRITE<br/>đã cấu hình?}
    
    CheckAPIKey -->|Chưa| PrintWarning[In cảnh báo:<br/>Chưa cấu hình API Key]
    CheckAPIKey -->|Có| PrepareParams[Tạo params HTTP<br/>make_param_thingspeak<br/>field1=light_value<br/>field2=distance_value]
    
    PrintWarning --> UpdateTime[last_sent_ts = now]
    PrepareParams --> SendHTTP[Gửi HTTP POST<br/>thingspeak_post_http]
    
    SendHTTP --> CheckResp{Response<br/>thành công?<br/>resp != '0'}
    
    CheckResp -->|Có| PrintSuccess[In: Đã gửi dữ liệu<br/>entry id: resp]
    CheckResp -->|Không| PrintFail[In: Update thất bại]
    
    PrintSuccess --> UpdateTime
    PrintFail --> UpdateTime
    UpdateTime --> Sleep10
    Sleep10 --> Loop
    
    Loop -.->|Ctrl+C| Interrupt[Nhận KeyboardInterrupt]
    Interrupt --> Cleanup[Tắt tất cả thiết bị:<br/>- LED đỏ OFF<br/>- LED vàng OFF<br/>- Buzzer OFF<br/>- Motor rung OFF<br/>- LCD: 'System OFF']
    Cleanup --> End([KẾT THÚC])
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style Loop fill:#87CEEB
    style CheckTime fill:#FFD700
    style CheckAPIKey fill:#FFD700
    style CheckResp fill:#FFD700
```

## 3. Lưu đồ điều khiển LED đỏ và Buzzer

```mermaid
flowchart TD
    Start([BẮT ĐẦU control_led_red_buzzer]) --> Input[Input: light_value]
    Input --> CheckHigh{light_value<br/>> 600?}
    
    CheckHigh -->|Có| CheckRedOn{LED đỏ<br/>đang BẬT?}
    CheckHigh -->|Không| CheckLow{light_value<br/>< 400?}
    
    CheckRedOn -->|Chưa| TurnOnRed[Bật LED đỏ<br/>led_red.on<br/>led_red_state = True<br/>In: LED ĐỎ BẬT]
    CheckRedOn -->|Rồi| CheckBuzzerOn{Buzzer<br/>đang BẬT?}
    
    TurnOnRed --> CheckBuzzerOn
    CheckBuzzerOn -->|Chưa| TurnOnBuzzer[Bật Buzzer<br/>buzzer.on<br/>buzzer_state = True<br/>In: BUZZER BẬT]
    CheckBuzzerOn -->|Rồi| End([KẾT THÚC])
    TurnOnBuzzer --> End
    
    CheckLow -->|Có| CheckRedOff{LED đỏ<br/>đang BẬT?}
    CheckLow -->|Không| End
    
    CheckRedOff -->|Có| TurnOffRed[Tắt LED đỏ<br/>led_red.off<br/>led_red_state = False<br/>In: LED ĐỎ TẮT]
    CheckRedOff -->|Không| CheckBuzzerOff{Buzzer<br/>đang BẬT?}
    
    TurnOffRed --> CheckBuzzerOff
    CheckBuzzerOff -->|Có| TurnOffBuzzer[Tắt Buzzer<br/>buzzer.off<br/>buzzer_state = False<br/>In: BUZZER TẮT]
    CheckBuzzerOff -->|Không| End
    TurnOffBuzzer --> End
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style CheckHigh fill:#FFD700
    style CheckLow fill:#FFD700
```

## 4. Lưu đồ điều khiển LED vàng và Motor rung

```mermaid
flowchart TD
    Start([BẮT ĐẦU control_led_yellow_vibration]) --> Input[Input: distance_value]
    Input --> CheckClose{distance_value<br/>< 20cm?}
    
    CheckClose -->|Có| CheckYellowOn{LED vàng<br/>đang BẬT?}
    CheckClose -->|Không| CheckFar{distance_value<br/>> 40cm?}
    
    CheckYellowOn -->|Chưa| TurnOnYellow[Bật LED vàng<br/>led_yellow.on<br/>led_yellow_state = True<br/>In: LED VÀNG BẬT]
    CheckYellowOn -->|Rồi| CheckMotorOn{Motor rung<br/>đang BẬT?}
    
    TurnOnYellow --> CheckMotorOn
    CheckMotorOn -->|Chưa| TurnOnMotor[Bật Motor rung<br/>vibration_motor.on<br/>vibration_motor_state = True<br/>In: MOTOR RUNG BẬT]
    CheckMotorOn -->|Rồi| End([KẾT THÚC])
    TurnOnMotor --> End
    
    CheckFar -->|Có| CheckYellowOff{LED vàng<br/>đang BẬT?}
    CheckFar -->|Không| End
    
    CheckYellowOff -->|Có| TurnOffYellow[Tắt LED vàng<br/>led_yellow.off<br/>led_yellow_state = False<br/>In: LED VÀNG TẮT]
    CheckYellowOff -->|Không| CheckMotorOff{Motor rung<br/>đang BẬT?}
    
    TurnOffYellow --> CheckMotorOff
    CheckMotorOff -->|Có| TurnOffMotor[Tắt Motor rung<br/>vibration_motor.off<br/>vibration_motor_state = False<br/>In: MOTOR RUNG TẮT]
    CheckMotorOff -->|Không| End
    TurnOffMotor --> End
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style CheckClose fill:#FFD700
    style CheckFar fill:#FFD700
```

## 5. Lưu đồ gửi dữ liệu lên ThingSpeak (HTTP POST)

```mermaid
flowchart TD
    Start([BẮT ĐẦU thingspeak_post_http]) --> Input[Input: params, api_key_write]
    Input --> CreateRequest[Tạo HTTP Request<br/>URL: api.thingspeak.com/update<br/>Method: POST]
    CreateRequest --> AddHeaders[Thêm Headers:<br/>Content-Type: application/x-www-form-urlencoded<br/>X-THINGSPEAKAPIKEY: api_key_write]
    AddHeaders --> SendRequest[Gửi HTTP Request<br/>với timeout 10s<br/>request.urlopen]
    SendRequest --> CheckSuccess{Request<br/>thành công?}
    
    CheckSuccess -->|Có| ReadResponse[Đọc response<br/>r.read.decode.strip]
    CheckSuccess -->|Không| PrintError[In: Lỗi HTTP<br/>Return None]
    
    ReadResponse --> ReturnID[Return entry ID<br/>response_data]
    PrintError --> End([KẾT THÚC])
    ReturnID --> End
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style CheckSuccess fill:#FFD700
```

## 6. Lưu đồ Node-RED nhận và hiển thị dữ liệu (HTTP)

```mermaid
flowchart TD
    Start([BẮT ĐẦU Node-RED Flow]) --> InitTimer[Inject Timer<br/>Repeat: 10 giây]
    InitTimer --> Trigger[Kích hoạt mỗi 10 giây]
    
    Trigger --> HTTPRequest[HTTP Request Node<br/>GET: api.thingspeak.com/channels/CHANNEL_ID/feeds.json<br/>results=1&api_key=READ_API_KEY]
    
    HTTPRequest --> CheckResponse{Response<br/>thành công?}
    
    CheckResponse -->|Không| Error[Debug Error]
    Error --> Wait[Chờ lần trigger tiếp theo]
    
    CheckResponse -->|Có| ParseJSON[Function: Parse JSON<br/>Lấy feeds[0]]
    ParseJSON --> CheckFeeds{feeds<br/>có dữ liệu?}
    
    CheckFeeds -->|Không| ReturnNull[Return null]
    CheckFeeds -->|Có| ExtractData[Lấy field1 và field2<br/>Parse sang float<br/>lightValue = parseFloat field1<br/>distanceValue = parseFloat field2]
    
    ExtractData --> CheckValid{Giá trị<br/>hợp lệ?<br/>!isNaN}
    
    CheckValid -->|Không| ReturnNull
    CheckValid -->|Có| CreateMessages[Tạo 2 messages:<br/>msgLight: payload=lightValue, topic='light'<br/>msgDistance: payload=distanceValue, topic='distance']
    
    CreateMessages --> OutputLight[Output 1: Ánh sáng]
    CreateMessages --> OutputDistance[Output 2: Khoảng cách]
    
    OutputLight --> UpdateGaugeLight[Cập nhật Gauge Ánh sáng<br/>0-1000]
    OutputLight --> UpdateBarLight[Cập nhật Bar Chart Ánh sáng]
    OutputLight --> DebugLight[Debug: Ánh sáng]
    
    OutputDistance --> UpdateGaugeDist[Cập nhật Gauge Khoảng cách<br/>0-200cm]
    OutputDistance --> UpdateBarDist[Cập nhật Bar Chart Khoảng cách]
    OutputDistance --> DebugDist[Debug: Khoảng cách]
    
    UpdateGaugeLight --> Wait
    UpdateBarLight --> Wait
    UpdateGaugeDist --> Wait
    UpdateBarDist --> Wait
    DebugLight --> Wait
    DebugDist --> Wait
    ReturnNull --> Wait
    Wait --> Trigger
    
    style Start fill:#90EE90
    style CheckResponse fill:#FFD700
    style CheckFeeds fill:#FFD700
    style CheckValid fill:#FFD700
    style UpdateGaugeLight fill:#4ECDC4
    style UpdateGaugeDist fill:#4ECDC4
    style UpdateBarLight fill:#95E1D3
    style UpdateBarDist fill:#95E1D3
```

## 7. Lưu đồ chi tiết Node-RED Flow

```mermaid
flowchart LR
    subgraph Timer["TIMER"]
        A1[Inject<br/>10 giây] --> A2[Trigger]
    end
    
    subgraph HTTP["HTTP REQUEST"]
        B1[HTTP Request<br/>GET ThingSpeak API] --> B2[Response JSON]
    end
    
    subgraph Parse["PARSE DATA"]
        C1[Function Parse<br/>Extract field1, field2] --> C2[Create 2 messages<br/>Light & Distance]
    end
    
    subgraph Display["DISPLAY"]
        D1[Gauge Ánh sáng<br/>0-1000] --> D2[Gauge Khoảng cách<br/>0-200cm]
        E1[Bar Chart Ánh sáng] --> E2[Bar Chart Khoảng cách]
        F1[Debug Ánh sáng] --> F2[Debug Khoảng cách]
    end
    
    A2 --> B1
    B2 --> C1
    C2 -->|Output 1| D1
    C2 -->|Output 1| E1
    C2 -->|Output 1| F1
    C2 -->|Output 2| D2
    C2 -->|Output 2| E2
    C2 -->|Output 2| F2
    
    D1 -->|Web UI| User[User Dashboard]
    D2 -->|Web UI| User
    E1 -->|Web UI| User
    E2 -->|Web UI| User
    
    style Timer fill:#E3F2FD
    style HTTP fill:#FFF3E0
    style Parse fill:#E8F5E9
    style Display fill:#FCE4EC
```

## 8. Lưu đồ luồng dữ liệu tổng thể (HTTP)

```mermaid
sequenceDiagram
    participant RPi as Raspberry Pi
    participant TS as ThingSpeak Server
    participant NR as Node-RED
    participant UI as Web Dashboard
    
    RPi->>RPi: Đọc cảm biến ánh sáng (A0)
    RPi->>RPi: Đọc cảm biến khoảng cách (D5)
    RPi->>RPi: Điều khiển LED đỏ + Buzzer<br/>(ánh sáng > 600 hoặc < 400)
    RPi->>RPi: Điều khiển LED vàng + Motor rung<br/>(khoảng cách < 20cm hoặc > 40cm)
    RPi->>RPi: Hiển thị Terminal & LCD
    RPi->>TS: HTTP POST (field1=light, field2=distance)
    TS->>TS: Lưu trữ dữ liệu
    
    Note over NR: Mỗi 10 giây
    NR->>TS: HTTP GET Request (feeds.json?results=1)
    TS->>NR: JSON Response (field1, field2)
    NR->>NR: Parse JSON
    NR->>NR: Cập nhật Gauge & Bar Chart
    NR->>UI: Hiển thị trên Dashboard
    UI->>UI: User xem ánh sáng & khoảng cách
```

## 9. Lưu đồ logic điều khiển thiết bị

```mermaid
flowchart TD
    Start([Đọc giá trị cảm biến]) --> ReadLight[light_value<br/>distance_value]
    
    ReadLight --> CheckLight{Ánh sáng<br/>> 600?}
    ReadLight --> CheckDist{Khoảng cách<br/>< 20cm?}
    
    CheckLight -->|Có| TurnOnRedBuzzer[Bật LED đỏ + Buzzer]
    CheckLight -->|Không| CheckLightLow{Ánh sáng<br/>< 400?}
    
    CheckLightLow -->|Có| TurnOffRedBuzzer[Tắt LED đỏ + Buzzer]
    CheckLightLow -->|Không| KeepRedState[Giữ nguyên trạng thái]
    
    CheckDist -->|Có| TurnOnYellowVib[Bật LED vàng + Motor rung]
    CheckDist -->|Không| CheckDistFar{Khoảng cách<br/>> 40cm?}
    
    CheckDistFar -->|Có| TurnOffYellowVib[Tắt LED vàng + Motor rung]
    CheckDistFar -->|Không| KeepYellowState[Giữ nguyên trạng thái]
    
    TurnOnRedBuzzer --> End([KẾT THÚC])
    TurnOffRedBuzzer --> End
    KeepRedState --> End
    TurnOnYellowVib --> End
    TurnOffYellowVib --> End
    KeepYellowState --> End
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style CheckLight fill:#FFD700
    style CheckDist fill:#FFD700
    style TurnOnRedBuzzer fill:#FF6B6B
    style TurnOnYellowVib fill:#FFE66D
```

## Mô tả các thành phần:

### Raspberry Pi (Python):
- **Cảm biến ánh sáng**: Grove Light Sensor (A0) - giá trị 0-1000
- **Cảm biến khoảng cách**: Grove Ultrasonic Ranger (D5) - đơn vị cm
- **LED đỏ**: Grove LED (D16) - bật khi ánh sáng > 600, tắt khi < 400
- **LED vàng**: Grove LED (D18) - bật khi khoảng cách < 20cm, tắt khi > 40cm
- **Buzzer**: Grove Buzzer (D12) - hoạt động cùng LED đỏ
- **Motor rung**: Grove Vibration Motor (D13) - hoạt động cùng LED vàng
- **LCD**: Grove LCD 16x2 I2C - hiển thị ánh sáng và khoảng cách
- **Gửi dữ liệu**: HTTP POST lên ThingSpeak mỗi 10 giây
- **Đọc cảm biến**: Mỗi 10 giây

### ThingSpeak Server:
- **Nhận dữ liệu**: Qua HTTP POST từ Raspberry Pi
- **Lưu trữ**: 
  - Field1: Cường độ ánh sáng (0-1000)
  - Field2: Khoảng cách vật cản (cm)
- **API Endpoint**: `https://api.thingspeak.com/channels/[CHANNEL_ID]/feeds.json`

### Node-RED Dashboard (HTTP):
- **Timer**: Inject node kích hoạt mỗi 10 giây
- **HTTP Request**: GET dữ liệu từ ThingSpeak API
- **Parse**: Chuyển đổi JSON sang số (lightValue, distanceValue)
- **Hiển thị**: 
  - Gauge cho ánh sáng (0-1000)
  - Gauge cho khoảng cách (0-200cm)
  - Bar Chart cho ánh sáng
  - Bar Chart cho khoảng cách
- **Truy cập**: `http://localhost:1880/ui` hoặc `http://[IP]:1880/ui`

### Logic điều khiển:
- **LED đỏ + Buzzer**: 
  - Bật khi ánh sáng > 600
  - Tắt khi ánh sáng < 400
  - Giữ nguyên khi 400 ≤ ánh sáng ≤ 600
- **LED vàng + Motor rung**: 
  - Bật khi khoảng cách < 20 cm
  - Tắt khi khoảng cách > 40 cm
  - Giữ nguyên khi 20 cm ≤ khoảng cách ≤ 40 cm

### Ngưỡng điều khiển:
- **LIGHT_THRESHOLD_HIGH**: 600 (bật LED đỏ + buzzer)
- **LIGHT_THRESHOLD_LOW**: 400 (tắt LED đỏ + buzzer)
- **DISTANCE_THRESHOLD_CLOSE**: 20 cm (bật LED vàng + motor rung)
- **DISTANCE_THRESHOLD_FAR**: 40 cm (tắt LED vàng + motor rung)

### Rate Limits:
- **ThingSpeak HTTP**: Tối đa 1 request mỗi 15 giây (tài khoản miễn phí)
- **Python**: Gửi mỗi 10 giây, đọc cảm biến mỗi 10 giây
- **Node-RED**: Lấy dữ liệu mỗi 10 giây

### Xử lý lỗi:
- **Lỗi đọc cảm biến**: Gán giá trị mặc định (0) và tiếp tục
- **Lỗi HTTP**: In thông báo lỗi và tiếp tục vòng lặp
- **Lỗi LCD**: In cảnh báo và tiếp tục
- **KeyboardInterrupt**: Tắt tất cả thiết bị và thoát an toàn

