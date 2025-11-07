from time import sleep
from grove.adc import ADC

adc = ADC()

while True:
    value = adc.read_voltage(0) # Đọc dạng điện áp (mV) (0-3299)
    # value = adc.read_raw(0) # Đọc dạng số ADC 12bit (0-4095)
    # value = adc.read(0) # Đọc dạng tỉ lệ điện áp đo chia 0.1% (0-999)
    print(value)
    sleep(2)
    