from grove.gpio import GPIO
import sys
import time

# Grove - Vibration Motor connected to D12 pin (có thể thay đổi pin tùy theo kết nối)
vibration_motor_pin = 12

class GroveVibrationMotor(GPIO):
    def __init__(self, pin):
        super(GroveVibrationMotor, self).__init__(pin, GPIO.OUT)

    def on(self):
        """Bật motor rung (Logic HIGH)"""
        self.write(1)

    def off(self):
        """Tắt motor rung (Logic LOW)"""
        self.write(0)

# Tạo instance của vibration motor
motor = GroveVibrationMotor(vibration_motor_pin)

print("Grove Vibration Motor Demo")
print("Nhấn Ctrl+C để dừng")

while True:
    try:
        # Bật motor rung
        motor.on()
        print("Motor rung: ON")
        time.sleep(1)
        
        # Tắt motor rung
        motor.off()
        print("Motor rung: OFF")
        time.sleep(1)
        
    except KeyboardInterrupt:
        motor.off()
        print("\nĐã dừng")
        exit(1)

