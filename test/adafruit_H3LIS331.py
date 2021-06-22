import time
import board
import adafruit_lis331

i2c = board.I2C()
# uncomment this line and comment out the one after if using the H3LIS331
# lis = adafruit_lis331.H3LIS331(i2c)
lis = adafruit_lis331.LIS331HH(i2c)