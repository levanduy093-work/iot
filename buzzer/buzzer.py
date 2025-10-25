from gpiozero import Buzzer
from signal import pause

bz = Buzzer(12)

bz.beep(0.1, 1)   # ton = 0.1s, toff = 1s

pause()