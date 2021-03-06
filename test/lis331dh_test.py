# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_lis331
from adafruit_lis331 import H3LIS331Range 

i2c = board.I2C()  # uses board.SCL and board.SDA
lis = adafruit_lis331.H3LIS331(i2c)
lis.range = H3LIS331Range.RANGE_400G

while True:
    print("Acceleration : X: %.2f, Y:%.2f, Z:%.2f ms^2" % lis.acceleration)
    time.sleep(0.1)
