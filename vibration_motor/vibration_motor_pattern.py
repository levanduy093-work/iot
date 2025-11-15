from grove.gpio import GPIO
import sys
import time

# Grove - Vibration Motor connected to D12 pin
vibration_motor_pin = 12

class GroveVibrationMotor(GPIO):
    def __init__(self, pin):
        super(GroveVibrationMotor, self).__init__(pin, GPIO.OUT)

    def on(self):
        """Bật motor rung"""
        self.write(1)

    def off(self):
        """Tắt motor rung"""
        self.write(0)

motor = GroveVibrationMotor(vibration_motor_pin)

print("Grove Vibration Motor - Pattern Demo")
print("Tạo các pattern rung khác nhau")
print("Nhấn Ctrl+C để dừng")

def pattern_short_vibration():
    """Pattern: Rung ngắn (0.2 giây)"""
    motor.on()
    time.sleep(0.2)
    motor.off()
    time.sleep(0.3)

def pattern_long_vibration():
    """Pattern: Rung dài (1 giây)"""
    motor.on()
    time.sleep(1)
    motor.off()
    time.sleep(0.5)

def pattern_double_vibration():
    """Pattern: Rung đôi (2 lần ngắn)"""
    for _ in range(2):
        motor.on()
        time.sleep(0.15)
        motor.off()
        time.sleep(0.15)
    time.sleep(0.3)

def pattern_triple_vibration():
    """Pattern: Rung ba lần"""
    for _ in range(3):
        motor.on()
        time.sleep(0.1)
        motor.off()
        time.sleep(0.1)
    time.sleep(0.5)

def pattern_sos():
    """Pattern: SOS (3 ngắn, 3 dài, 3 ngắn)"""
    # 3 ngắn
    for _ in range(3):
        motor.on()
        time.sleep(0.2)
        motor.off()
        time.sleep(0.2)
    time.sleep(0.4)
    # 3 dài
    for _ in range(3):
        motor.on()
        time.sleep(0.6)
        motor.off()
        time.sleep(0.2)
    time.sleep(0.4)
    # 3 ngắn
    for _ in range(3):
        motor.on()
        time.sleep(0.2)
        motor.off()
        time.sleep(0.2)
    time.sleep(1)

patterns = [
    ("Rung ngắn", pattern_short_vibration),
    ("Rung dài", pattern_long_vibration),
    ("Rung đôi", pattern_double_vibration),
    ("Rung ba lần", pattern_triple_vibration),
    ("SOS", pattern_sos),
]

while True:
    try:
        for name, pattern_func in patterns:
            print(f"\nPattern: {name}")
            pattern_func()
            time.sleep(1)
            
    except KeyboardInterrupt:
        motor.off()
        print("\nĐã dừng")
        exit(1)

