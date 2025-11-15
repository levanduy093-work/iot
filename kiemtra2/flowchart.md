# Lưu Đồ Giải Thuật - Hệ Thống Giám Sát Ánh Sáng và Khoảng Cách

## Flowchart Tổng Quan

```mermaid
flowchart TD
    Start([BẮT ĐẦU]) --> LoadCreds[Đọc MQTT credentials<br/>từ file send_data_mqtt_key.txt]
    LoadCreds --> InitMQTT[Khởi tạo MQTT Client<br/>và kết nối đến ThingSpeak]
    InitMQTT --> InitSensors[Khởi tạo các cảm biến:<br/>- Light Sensor A0<br/>- Ultrasonic D5<br/>- Blue Light D16<br/>- LED Vàng D18<br/>- Buzzer D12<br/>- Motor Rung D22<br/>- LCD Display]
    InitSensors --> InitVars[Khởi tạo biến trạng thái:<br/>blue_light_state = False<br/>led_yellow_state = False<br/>buzzer_state = False<br/>motor_state = False<br/>last_display_time = now]
    InitVars --> PrintHeader[In thông tin hệ thống<br/>ra màn hình]
    PrintHeader --> MainLoop{Vòng lặp chính}
    
    MainLoop --> ReadLight[Đọc cảm biến ánh sáng<br/>light_sensor.value]
    ReadLight --> CheckLightError{Lỗi đọc<br/>ánh sáng?}
    CheckLightError -->|Có| SetLightZero[light_value = 0]
    CheckLightError -->|Không| ReadDistance[Đọc cảm biến khoảng cách<br/>ultrasonic.get_distance]
    SetLightZero --> ReadDistance
    
    ReadDistance --> CheckDistError{Lỗi đọc<br/>khoảng cách?}
    CheckDistError -->|Có| SetDistZero[distance = 0]
    CheckDistError -->|Không| ControlBlueLight[Điều khiển Blue Light & Buzzer]
    SetDistZero --> ControlBlueLight
    
    ControlBlueLight --> ControlLogic1{light_value > 500?}
    ControlLogic1 -->|Có| TurnOnBlue[Blue Light ON<br/>Buzzer ON]
    ControlLogic1 -->|Không| ControlLogic2{light_value < 200?}
    ControlLogic2 -->|Có| TurnOffBlue[Blue Light OFF<br/>Buzzer OFF]
    ControlLogic2 -->|Không| ControlYellowLED[Giữ nguyên trạng thái]
    TurnOnBlue --> ControlYellowLED
    TurnOffBlue --> ControlYellowLED
    
    ControlYellowLED --> ControlLogic3{distance < 20cm?}
    ControlLogic3 -->|Có| TurnOnYellow[LED Vàng ON<br/>Motor Rung ON]
    ControlLogic3 -->|Không| ControlLogic4{distance > 40cm?}
    ControlLogic4 -->|Có| TurnOffYellow[LED Vàng OFF<br/>Motor Rung OFF]
    ControlLogic4 -->|Không| CheckDisplayTime[Giữ nguyên trạng thái]
    TurnOnYellow --> CheckDisplayTime
    TurnOffYellow --> CheckDisplayTime
    
    CheckDisplayTime --> TimeCheck{Đã đủ<br/>20 giây?}
    TimeCheck -->|Chưa| Sleep[Chờ 1 giây<br/>time.sleep READ_INTERVAL]
    TimeCheck -->|Đã đủ| DisplayTerminal[Hiển thị dữ liệu<br/>ra Terminal:<br/>- Thời gian<br/>- Ánh sáng<br/>- Khoảng cách<br/>- Trạng thái các thiết bị]
    
    DisplayTerminal --> DisplayLCD[Hiển thị trên LCD:<br/>Dòng 1: Light: XXXX<br/>Dòng 2: Dist: XX.Xcm]
    DisplayLCD --> SendMQTT[Gửi dữ liệu lên ThingSpeak<br/>qua MQTT:<br/>field1=light_value<br/>field2=distance]
    SendMQTT --> CheckMQTTError{Lỗi gửi<br/>MQTT?}
    CheckMQTTError -->|Có| PrintError[In thông báo lỗi]
    CheckMQTTError -->|Không| UpdateTime[last_display_time = current_time]
    PrintError --> UpdateTime
    UpdateTime --> Sleep
    
    Sleep --> CheckInterrupt{Có tín hiệu<br/>Ctrl+C?}
    CheckInterrupt -->|Không| MainLoop
    CheckInterrupt -->|Có| Cleanup[Tắt tất cả thiết bị:<br/>- Blue Light OFF<br/>- LED Vàng OFF<br/>- Buzzer OFF<br/>- Motor Rung OFF]
    Cleanup --> StopMQTT[Dừng MQTT loop<br/>và ngắt kết nối]
    StopMQTT --> End([KẾT THÚC])
```

## Flowchart Chi Tiết - Điều Khiển Blue Light & Buzzer

```mermaid
flowchart TD
    Start([control_blue_light_buzzer]) --> Input[Input: light_value]
    Input --> Check1{light_value > 500?}
    Check1 -->|Có| CheckState1{blue_light_state<br/>== False?}
    CheckState1 -->|Có| TurnOn1[blue_light.on<br/>buzzer.on<br/>blue_light_state = True<br/>buzzer_state = True]
    CheckState1 -->|Không| End1[Giữ nguyên]
    TurnOn1 --> End1
    Check1 -->|Không| Check2{light_value < 200?}
    Check2 -->|Có| CheckState2{blue_light_state<br/>== True?}
    CheckState2 -->|Có| TurnOff1[blue_light.off<br/>buzzer.off<br/>blue_light_state = False<br/>buzzer_state = False]
    CheckState2 -->|Không| End2[Giữ nguyên]
    TurnOff1 --> End2
    Check2 -->|Không| End3[Giữ nguyên<br/>200 <= light_value <= 500]
    End1 --> Return([RETURN])
    End2 --> Return
    End3 --> Return
```

## Flowchart Chi Tiết - Điều Khiển LED Vàng & Motor Rung

```mermaid
flowchart TD
    Start([control_led_yellow_motor]) --> Input[Input: distance]
    Input --> Check1{distance < 20cm?}
    Check1 -->|Có| CheckState1{led_yellow_state<br/>== False?}
    CheckState1 -->|Có| TurnOn1[led_yellow.on<br/>vibration_motor.on<br/>led_yellow_state = True<br/>motor_state = True]
    CheckState1 -->|Không| End1[Giữ nguyên]
    TurnOn1 --> End1
    Check1 -->|Không| Check2{distance > 40cm?}
    Check2 -->|Có| CheckState2{led_yellow_state<br/>== True?}
    CheckState2 -->|Có| TurnOff1[led_yellow.off<br/>vibration_motor.off<br/>led_yellow_state = False<br/>motor_state = False]
    CheckState2 -->|Không| End2[Giữ nguyên]
    TurnOff1 --> End2
    Check2 -->|Không| End3[Giữ nguyên<br/>20cm <= distance <= 40cm]
    End1 --> Return([RETURN])
    End2 --> Return
    End3 --> Return
```

## Flowchart Chi Tiết - Đọc Cảm Biến Khoảng Cách

```mermaid
flowchart TD
    Start([ultrasonic.get_distance]) --> Loop[Vòng lặp while True]
    Loop --> GetDist[Gọi _get_distance]
    GetDist --> SetupPin[Thiết lập pin D5<br/>OUTPUT mode]
    SetupPin --> SendPulse[Gửi xung trigger:<br/>LOW 2μs<br/>HIGH 10μs<br/>LOW]
    SendPulse --> SwitchInput[Chuyển pin sang<br/>INPUT mode]
    SwitchInput --> WaitEcho[Chờ tín hiệu ECHO<br/>với timeout 1000]
    WaitEcho --> CheckEcho1{Có tín hiệu<br/>ECHO?}
    CheckEcho1 -->|Không| ReturnNone1[RETURN None]
    CheckEcho1 -->|Có| MeasureTime[Đo thời gian<br/>tín hiệu HIGH]
    MeasureTime --> CheckTimeout{Timeout<br/>10000?}
    CheckTimeout -->|Có| ReturnNone2[RETURN None]
    CheckTimeout -->|Không| CalcDist[Tính khoảng cách:<br/>distance = time * 1000000 / 29 / 2]
    CalcDist --> CheckValid{distance > 530<br/>hoặc None?}
    CheckValid -->|Có| ReturnNone3[RETURN None]
    CheckValid -->|Không| ReturnDist[RETURN distance]
    ReturnNone1 --> CheckRetry{dist == None?}
    ReturnNone2 --> CheckRetry
    ReturnNone3 --> CheckRetry
    ReturnDist --> End([RETURN distance])
    CheckRetry -->|Có| Loop
    CheckRetry -->|Không| End
```

## Mô Tả Các Bước Chính

### 1. Khởi Tạo Hệ Thống
- Đọc thông tin xác thực MQTT từ file `send_data_mqtt_key.txt`
- Kết nối đến ThingSpeak MQTT broker
- Khởi tạo tất cả cảm biến và thiết bị điều khiển
- Thiết lập các biến trạng thái ban đầu

### 2. Vòng Lặp Chính
- **Đọc cảm biến mỗi 1 giây (READ_INTERVAL)**
  - Đọc cảm biến ánh sáng (0-1000)
  - Đọc cảm biến khoảng cách (cm)
  
- **Điều khiển thiết bị theo logic:**
  - Blue Light & Buzzer: BẬT khi ánh sáng > 500, TẮT khi < 200
  - LED Vàng & Motor Rung: BẬT khi khoảng cách < 20cm, TẮT khi > 40cm
  
- **Hiển thị và gửi dữ liệu mỗi 20 giây (DISPLAY_INTERVAL)**
  - Hiển thị trên Terminal
  - Hiển thị trên LCD
  - Gửi lên ThingSpeak qua MQTT

### 3. Xử Lý Lỗi
- Xử lý lỗi đọc cảm biến (gán giá trị mặc định)
- Xử lý lỗi hiển thị LCD
- Xử lý lỗi gửi MQTT

### 4. Kết Thúc
- Xử lý tín hiệu Ctrl+C
- Tắt tất cả thiết bị
- Ngắt kết nối MQTT
- Thoát chương trình

## Các Ngưỡng Điều Khiển

| Thiết Bị | Điều Kiện BẬT | Điều Kiện TẮT | Giữ Nguyên |
|----------|---------------|---------------|------------|
| Blue Light & Buzzer | Ánh sáng > 500 | Ánh sáng < 200 | 200 ≤ Ánh sáng ≤ 500 |
| LED Vàng & Motor Rung | Khoảng cách < 20cm | Khoảng cách > 40cm | 20cm ≤ Khoảng cách ≤ 40cm |

## Thời Gian

- **READ_INTERVAL**: 1 giây (đọc cảm biến)
- **DISPLAY_INTERVAL**: 20 giây (hiển thị và gửi dữ liệu)

