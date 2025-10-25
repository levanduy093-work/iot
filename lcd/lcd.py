import time
from grove.display.jhd1802 import JHD1802

# Grove - 16x2 LCD(White on Blue) connected to I2C port
lcd = JHD1802()

lcd.setCursor(0, 0)
lcd.write("Hello, World!")

time.sleep(1)

lcd.setCursor(1, 0)
lcd.write("Hello, World!")

time.sleep(1)