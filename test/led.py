import time
from time import mktime
import board
import digitalio

led = digitalio.DigitalInOut(board.D22)
led.direction = digitalio.Direction.OUTPUT

while 1:
    led.value = True
    time.sleep(1)
    led.value = False
    time.sleep(1)

blynk()
