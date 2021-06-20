import spidev # To communicate with SPI devices
from numpy import interp    # To scale values
from time import sleep      # To add delay
from collections import deque
from math import sqrt
from datetime import datetime

import RPi.GPIO as GPIO      # To use GPIO pins

# Initializing LED pin as OUTPUT pin
led_pin = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

while 1:
    GPIO.output(led_pin,GPIO.HIGH)
    sleep(1)
    GPIO.output(led_pin,GPIO.LOW)
    sleep(1)
