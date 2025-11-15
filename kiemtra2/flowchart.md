# Lưu Đồ Giải Thuật - Hệ Thống Giám Sát Ánh Sáng và Khoảng Cách

## Flowchart Tổng Quan

```mermaid
flowchart TD
    Start([BẮT ĐẦU]) --> LoadCreds[Đọc MQTT credentials]
    LoadCreds --> InitMQTT[Kết nối ThingSpeak MQTT]
    InitMQTT --> InitSensors[Khởi tạo cảm biến và thiết bị]
    InitSensors --> InitVars[Khởi tạo biến trạng thái]
    InitVars --> MainLoop{Vòng lặp chính}
    
    MainLoop --> ReadLight[Đọc cảm biến ánh sáng]
    ReadLight --> CheckLightError{Lỗi?}
    CheckLightError -->|Có| SetLightZero[light_value = 0]
    CheckLightError -->|Không| ReadDistance[Đọc cảm biến khoảng cách]
    SetLightZero --> ReadDistance
    
    ReadDistance --> CheckDistError{Lỗi?}
    CheckDistError -->|Có| SetDistZero[distance = 0]
    CheckDistError -->|Không| ControlBlueLight[Điều khiển Blue Light & Buzzer]
    SetDistZero --> ControlBlueLight
    
    ControlBlueLight --> ControlLogic1{light_value > 500?}
    ControlLogic1 -->|Có| TurnOnBlue[Blue Light ON<br/>Buzzer ON]
    ControlLogic1 -->|Không| ControlLogic2{light_value < 200?}
    ControlLogic2 -->|Có| TurnOffBlue[Blue Light OFF<br/>Buzzer OFF]
    ControlLogic2 -->|Không| ControlYellowLED[Giữ nguyên]
    TurnOnBlue --> ControlYellowLED
    TurnOffBlue --> ControlYellowLED
    
    ControlYellowLED --> ControlLogic3{distance < 20cm?}
    ControlLogic3 -->|Có| TurnOnYellow[LED Vàng ON<br/>Motor Rung ON]
    ControlLogic3 -->|Không| ControlLogic4{distance > 40cm?}
    ControlLogic4 -->|Có| TurnOffYellow[LED Vàng OFF<br/>Motor Rung OFF]
    ControlLogic4 -->|Không| CheckDisplayTime[Giữ nguyên]
    TurnOnYellow --> CheckDisplayTime
    TurnOffYellow --> CheckDisplayTime
    
    CheckDisplayTime --> TimeCheck{Đã đủ 20 giây?}
    TimeCheck -->|Chưa| Sleep[Chờ 1 giây]
    TimeCheck -->|Đủ| DisplayTerminal[Hiển thị Terminal]
    DisplayTerminal --> DisplayLCD[Hiển thị LCD]
    DisplayLCD --> SendMQTT[Gửi MQTT lên ThingSpeak]
    SendMQTT --> UpdateTime[Cập nhật thời gian]
    UpdateTime --> Sleep
    
    Sleep --> CheckInterrupt{Ctrl+C?}
    CheckInterrupt -->|Không| MainLoop
    CheckInterrupt -->|Có| Cleanup[Tắt thiết bị]
    Cleanup --> StopMQTT[Ngắt kết nối MQTT]
    StopMQTT --> End([KẾT THÚC])
```

## Flowchart Chi Tiết - Điều Khiển Blue Light & Buzzer

```mermaid
flowchart TD
    Start([control_blue_light_buzzer]) --> Input[Input: light_value]
    Input --> Check1{light_value > 500?}
    Check1 -->|Có| CheckState1{blue_light_state == False?}
    CheckState1 -->|Có| TurnOn1[blue_light.on<br/>buzzer.on<br/>blue_light_state = True<br/>buzzer_state = True]
    CheckState1 -->|Không| End1[Giữ nguyên]
    TurnOn1 --> End1
    Check1 -->|Không| Check2{light_value < 200?}
    Check2 -->|Có| CheckState2{blue_light_state == True?}
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
    Check1 -->|Có| CheckState1{led_yellow_state == False?}
    CheckState1 -->|Có| TurnOn1[led_yellow.on<br/>vibration_motor.on<br/>led_yellow_state = True<br/>motor_state = True]
    CheckState1 -->|Không| End1[Giữ nguyên]
    TurnOn1 --> End1
    Check1 -->|Không| Check2{distance > 40cm?}
    Check2 -->|Có| CheckState2{led_yellow_state == True?}
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
    GetDist --> SetupPin[Thiết lập pin D5 OUTPUT]
    SetupPin --> SendPulse[Gửi xung trigger:<br/>LOW 2μs, HIGH 10μs, LOW]
    SendPulse --> SwitchInput[Chuyển pin sang INPUT]
    SwitchInput --> WaitEcho[Chờ tín hiệu ECHO]
    WaitEcho --> CheckEcho1{Có tín hiệu ECHO?}
    CheckEcho1 -->|Không| ReturnNone1[RETURN None]
    CheckEcho1 -->|Có| MeasureTime[Đo thời gian HIGH]
    MeasureTime --> CheckTimeout{Timeout?}
    CheckTimeout -->|Có| ReturnNone2[RETURN None]
    CheckTimeout -->|Không| CalcDist[Tính khoảng cách]
    CalcDist --> CheckValid{distance hợp lệ?}
    CheckValid -->|Không| ReturnNone3[RETURN None]
    CheckValid -->|Có| ReturnDist[RETURN distance]
    ReturnNone1 --> CheckRetry{dist == None?}
    ReturnNone2 --> CheckRetry
    ReturnNone3 --> CheckRetry
    ReturnDist --> End([RETURN distance])
    CheckRetry -->|Có| Loop
    CheckRetry -->|Không| End
```

## Ngưỡng Điều Khiển

| Thiết Bị | BẬT | TẮT |
|----------|-----|-----|
| Blue Light & Buzzer | Ánh sáng > 500 | Ánh sáng < 200 |
| LED Vàng & Motor Rung | Khoảng cách < 20cm | Khoảng cách > 40cm |

## Thời Gian

- **READ_INTERVAL**: 1 giây | **DISPLAY_INTERVAL**: 20 giây

---

# Sơ Đồ Nguyên Lý Kết Nối Dây

## Sơ Đồ Tổng Quan Hệ Thống

```mermaid
graph TB
    subgraph "Raspberry Pi"
        RPI[Raspberry Pi<br/>với Grove Base Hat]
    end
    
    subgraph "Cảm Biến"
        LS[Light Sensor<br/>Grove Light Sensor<br/>Port A0]
        US[Ultrasonic Ranger<br/>Grove Ultrasonic<br/>Port D5]
    end
    
    subgraph "Thiết Bị Điều Khiển"
        BL[Blue Light<br/>Grove LED<br/>Port D16]
        YL[LED Vàng<br/>Grove LED<br/>Port D18]
        BZ[Buzzer<br/>Grove Buzzer<br/>Port D12]
        VM[Vibration Motor<br/>Grove Motor<br/>Port D22]
    end
    
    subgraph "Hiển Thị"
        LCD[LCD Display<br/>JHD1802<br/>I2C]
    end
    
    subgraph "Kết Nối Mạng"
        NET[WiFi/Ethernet<br/>MQTT Connection<br/>ThingSpeak]
    end
    
    RPI -->|Analog Channel 0| LS
    RPI -->|Digital Pin 5| US
    RPI -->|Digital Pin 16| BL
    RPI -->|Digital Pin 18| YL
    RPI -->|Digital Pin 12| BZ
    RPI -->|Digital Pin 22| VM
    RPI -->|I2C SDA/SCL| LCD
    RPI -->|Internet| NET
```

## Sơ Đồ Chi Tiết Kết Nối Grove Base Hat

```
┌─────────────────────────────────────────────────────────────┐
│                    GROVE BASE HAT FOR RASPBERRY PI          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐       │
│  │ A0  │  │ A1  │  │ A2  │  │ A3  │  │ A4  │  │ A5  │       │
│  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘       │
│    │                                                          │
│    └─── Light Sensor (Analog)                                │
│                                                               │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐       │
│  │ D3  │  │ D4  │  │ D5  │  │ D6  │  │ D7  │  │ D8  │       │
│  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘       │
│              │                                                │
│              └─── Ultrasonic Ranger (Digital)                │
│                                                               │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐       │
│  │ D9  │  │ D10 │  │ D11 │  │ D12 │  │ D13 │  │ D14 │       │
│  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘       │
│                        │                                      │
│                        └─── Buzzer                            │
│                                                               │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐       │
│  │ D15 │  │ D16 │  │ D17 │  │ D18 │  │ D19 │  │ D20 │       │
│  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘       │
│              │                        │                        │
│              └─── Blue Light          └─── LED Vàng           │
│                                                               │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐       │
│  │ D21 │  │ D22 │  │ D23 │  │ D24 │  │ D25 │  │ D26 │       │
│  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘       │
│              │                                                │
│              └─── Vibration Motor                             │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              I2C CONNECTOR                           │    │
│  │  ┌────┐  ┌────┐  ┌────┐  ┌────┐                      │    │
│  │  │SDA │  │SCL │  │VCC │  │GND │                      │    │
│  │  └────┘  └────┘  └────┘  └────┘                      │    │
│  │                                                       │    │
│  │              └─── LCD Display JHD1802                │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Bảng Kết Nối Chi Tiết

| Thiết Bị | Port | GPIO | Chức Năng |
|----------|------|------|-----------|
| Light Sensor | A0 | ADC0 | Đọc ánh sáng (0-1000) |
| Ultrasonic Ranger | D5 | GPIO5 | Đọc khoảng cách |
| Blue Light | D16 | GPIO16 | Điều khiển LED xanh |
| LED Vàng | D18 | GPIO18 | Điều khiển LED vàng |
| Buzzer | D12 | GPIO12 | Điều khiển còi |
| Vibration Motor | D22 | GPIO22 | Điều khiển motor rung |
| LCD Display | I2C | SDA/SCL | Hiển thị dữ liệu |

## Sơ Đồ Kết Nối Grove Connector

**Analog Port (A0)**: VCC=5V, GND, Signal=ADC0  
**Digital Port (D5/D12/D16/D18/D22)**: VCC=5V, GND, Signal=GPIO  
**I2C Port**: VCC=5V, GND, SDA=GPIO2, SCL=GPIO3

## Sơ Đồ Nguyên Lý Điện

```mermaid
graph LR
    subgraph "Raspberry Pi GPIO"
        GPIO5[GPIO 5<br/>D5]
        GPIO12[GPIO 12<br/>D12]
        GPIO16[GPIO 16<br/>D16]
        GPIO18[GPIO 18<br/>D18]
        GPIO22[GPIO 22<br/>D22]
        ADC0[ADC Channel 0<br/>A0]
        I2C[I2C Bus<br/>SDA/SCL]
    end
    
    subgraph "Cảm Biến"
        LS[Light Sensor<br/>VCC: 5V<br/>GND: GND<br/>OUT: ADC0]
        US[Ultrasonic<br/>VCC: 5V<br/>GND: GND<br/>SIG: GPIO5]
    end
    
    subgraph "Thiết Bị Điều Khiển"
        BL[Blue LED<br/>VCC: 5V<br/>GND: GND<br/>IN: GPIO16]
        YL[Yellow LED<br/>VCC: 5V<br/>GND: GND<br/>IN: GPIO18]
        BZ[Buzzer<br/>VCC: 5V<br/>GND: GND<br/>IN: GPIO12]
        VM[Motor<br/>VCC: 5V<br/>GND: GND<br/>IN: GPIO22]
    end
    
    subgraph "Hiển Thị"
        LCD[LCD JHD1802<br/>VCC: 5V<br/>GND: GND<br/>SDA: I2C SDA<br/>SCL: I2C SCL]
    end
    
    ADC0 --> LS
    GPIO5 --> US
    GPIO16 --> BL
    GPIO18 --> YL
    GPIO12 --> BZ
    GPIO22 --> VM
    I2C --> LCD
```

## Hướng Dẫn Kết Nối

1. **Lắp Grove Base Hat** lên Raspberry Pi (tắt nguồn trước)
2. **Cảm biến**: Light Sensor → A0, Ultrasonic → D5
3. **Thiết bị**: Blue Light → D16, LED Vàng → D18, Buzzer → D12, Motor → D22
4. **LCD**: JHD1802 → I2C Port
5. **Kiểm tra**: Cắm chặt connector, kiểm tra nguồn 5V và GND

## Lưu Ý

⚠️ **An toàn**: Tắt nguồn trước khi kết nối/tháo, kiểm tra cực VCC/GND  
⚠️ **Tương thích**: Tất cả thiết bị phải là Grove modules, LCD hỗ trợ I2C  
⚠️ **Phần cứng**: Grove Base Hat phải tương thích với Raspberry Pi

