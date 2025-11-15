# Lưu Đồ Giải Thuật - Hệ Thống Giám Sát Ánh Sáng và Khoảng Cách

## Flowchart Tổng Quan

```mermaid
flowchart TD
    Start([BẮT ĐẦU]) --> Init[Khởi tạo hệ thống:<br/>MQTT, Cảm biến, Thiết bị]
    Init --> MainLoop{Vòng lặp chính}
    
    MainLoop --> ReadSensors[Đọc cảm biến:<br/>Ánh sáng + Khoảng cách]
    ReadSensors --> Control[Điều khiển thiết bị:<br/>Blue Light/Buzzer theo ánh sáng<br/>LED Vàng/Motor theo khoảng cách]
    
    Control --> CheckTime{Đã đủ<br/>20 giây?}
    CheckTime -->|Chưa| Sleep[Chờ 1 giây]
    CheckTime -->|Đủ| Display[Hiển thị LCD + Terminal<br/>Gửi MQTT lên ThingSpeak]
    
    Display --> Sleep
    Sleep --> CheckExit{Ctrl+C?}
    CheckExit -->|Không| MainLoop
    CheckExit -->|Có| Cleanup[Tắt thiết bị<br/>Ngắt kết nối MQTT]
    Cleanup --> End([KẾT THÚC])
```

## Logic Điều Khiển Chi Tiết

### Điều Khiển Blue Light & Buzzer
- **BẬT**: Khi `light_value > 500`
- **TẮT**: Khi `light_value < 200`
- **Giữ nguyên**: Khi `200 ≤ light_value ≤ 500`

### Điều Khiển LED Vàng & Motor Rung
- **BẬT**: Khi `distance < 20cm`
- **TẮT**: Khi `distance > 40cm`
- **Giữ nguyên**: Khi `20cm ≤ distance ≤ 40cm`

## Mô Tả Các Bước Chính

1. **Khởi tạo**: Đọc MQTT credentials, kết nối ThingSpeak, khởi tạo cảm biến và thiết bị
2. **Vòng lặp chính**: Đọc cảm biến mỗi 1 giây → Điều khiển thiết bị → Kiểm tra thời gian hiển thị
3. **Hiển thị/Gửi dữ liệu**: Mỗi 20 giây hiển thị LCD/Terminal và gửi MQTT lên ThingSpeak
4. **Kết thúc**: Xử lý Ctrl+C, tắt thiết bị, ngắt kết nối MQTT

## Các Ngưỡng Điều Khiển

| Thiết Bị | Điều Kiện BẬT | Điều Kiện TẮT | Giữ Nguyên |
|----------|---------------|---------------|------------|
| Blue Light & Buzzer | Ánh sáng > 500 | Ánh sáng < 200 | 200 ≤ Ánh sáng ≤ 500 |
| LED Vàng & Motor Rung | Khoảng cách < 20cm | Khoảng cách > 40cm | 20cm ≤ Khoảng cách ≤ 40cm |

## Thời Gian

- **READ_INTERVAL**: 1 giây (đọc cảm biến)
- **DISPLAY_INTERVAL**: 20 giây (hiển thị và gửi dữ liệu)

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

| Thiết Bị | Loại Grove | Port | Chân GPIO | Chức Năng | Mô Tả |
|----------|------------|------|-----------|-----------|-------|
| **Light Sensor** | Analog | A0 | ADC Channel 0 | Đọc cường độ ánh sáng | Đo giá trị 0-1000 |
| **Ultrasonic Ranger** | Digital | D5 | GPIO 5 | Đọc khoảng cách | Đo khoảng cách 2-400cm |
| **Blue Light** | Digital | D16 | GPIO 16 | Điều khiển LED xanh | BẬT/TẮT theo ánh sáng |
| **LED Vàng** | Digital | D18 | GPIO 18 | Điều khiển LED vàng | BẬT/TẮT theo khoảng cách |
| **Buzzer** | Digital | D12 | GPIO 12 | Điều khiển còi | BẬT/TẮT theo ánh sáng |
| **Vibration Motor** | Digital | D22 | GPIO 22 | Điều khiển motor rung | BẬT/TẮT theo khoảng cách |
| **LCD Display** | I2C | I2C | SDA/SCL | Hiển thị dữ liệu | Hiển thị ánh sáng và khoảng cách |

## Sơ Đồ Kết Nối Grove Connector

### Analog Port (A0) - Light Sensor
```
┌─────────────────┐
│  GROVE CONNECTOR │
├─────────────────┤
│  Pin 1: VCC     │ ──── 5V
│  Pin 2: GND     │ ──── GND
│  Pin 3: Signal  │ ──── ADC Channel 0
│  Pin 4: NC      │
└─────────────────┘
```

### Digital Port (D5) - Ultrasonic Ranger
```
┌─────────────────┐
│  GROVE CONNECTOR │
├─────────────────┤
│  Pin 1: VCC     │ ──── 5V
│  Pin 2: GND     │ ──── GND
│  Pin 3: Signal  │ ──── GPIO 5 (Trigger/Echo)
│  Pin 4: NC      │
└─────────────────┘
```

### Digital Port (D12, D16, D18, D22) - LED, Buzzer, Motor
```
┌─────────────────┐
│  GROVE CONNECTOR │
├─────────────────┤
│  Pin 1: VCC     │ ──── 5V/3.3V
│  Pin 2: GND     │ ──── GND
│  Pin 3: Signal  │ ──── GPIO (12/16/18/22)
│  Pin 4: NC      │
└─────────────────┘
```

### I2C Port - LCD Display
```
┌─────────────────┐
│  GROVE CONNECTOR │
├─────────────────┤
│  Pin 1: VCC     │ ──── 5V
│  Pin 2: GND     │ ──── GND
│  Pin 3: SDA     │ ──── I2C SDA (GPIO 2)
│  Pin 4: SCL     │ ──── I2C SCL (GPIO 3)
└─────────────────┘
```

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

### Bước 1: Lắp Grove Base Hat
1. Tắt nguồn Raspberry Pi
2. Lắp Grove Base Hat lên Raspberry Pi (khớp với GPIO header)
3. Đảm bảo các chân GPIO được kết nối đúng

### Bước 2: Kết Nối Cảm Biến
1. **Light Sensor** → Cắm vào **Port A0** (Analog)
2. **Ultrasonic Ranger** → Cắm vào **Port D5** (Digital)

### Bước 3: Kết Nối Thiết Bị Điều Khiển
1. **Blue Light** → Cắm vào **Port D16**
2. **LED Vàng** → Cắm vào **Port D18**
3. **Buzzer** → Cắm vào **Port D12**
4. **Vibration Motor** → Cắm vào **Port D22**

### Bước 4: Kết Nối LCD Display
1. **LCD JHD1802** → Cắm vào **I2C Port** (bất kỳ I2C port nào trên Base Hat)

### Bước 5: Kiểm Tra Kết Nối
- Kiểm tra tất cả các connector đã được cắm chặt
- Kiểm tra nguồn điện (5V) cho các thiết bị
- Kiểm tra kết nối GND chung

## Lưu Ý Quan Trọng

⚠️ **An toàn điện:**
- Luôn tắt nguồn trước khi kết nối/tháo thiết bị
- Kiểm tra điện áp: Grove Base Hat cung cấp 5V cho các port
- Không kết nối sai cực (VCC/GND)

⚠️ **Tương thích:**
- Tất cả thiết bị phải là Grove modules
- LCD phải hỗ trợ I2C (JHD1802)
- Ultrasonic Ranger phải là loại single-pin (D5)

⚠️ **Phần cứng:**
- Raspberry Pi phải có Grove Base Hat được lắp đặt
- Đảm bảo Grove Base Hat tương thích với model Raspberry Pi
- Kiểm tra jumper I2C nếu cần thiết

