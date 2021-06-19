import time
from time import mktime
import board
import digitalio

import adafruit_lis331
from adafruit_lis331 import H3LIS331Range 

from collections import deque
from math import sqrt
from datetime import datetime
import os

# Threshold for G
THRESHOLD = 4

deviceId = 3

# create a fixed size deque to store .5 seconds of samples @ 500 samples/second
dq = deque(maxlen=50)

led = digitalio.DigitalInOut(board.D11)
led.direction = digitalio.Direction.OUTPUT

i2c = board.I2C()  # uses board.SCL and board.SDA
lis = adafruit_lis331.H3LIS331(i2c, address=0x19)
lis.range = H3LIS331Range.RANGE_100G

dg=(0,0,0) # calibration values

def log(str):
    print(str)
#-----------------------------------------------------------
# get G calibrations
#-----------------------------------------------------------
def calibrateG():
    time.sleep(0.002)
    global dg
    dg = tuple(x/9.80665 for x in lis.acceleration)
    s = "Calibration: X:%.2f, Y: %.2f, Z: %.2f g"%(dg)+'\n'
    printToFile("log/tdi_accelerometer.log", s)
#-----------------------------------------------------------
# calculate G by 3 axises
#-----------------------------------------------------------
def getG():
    time.sleep(0.002)
    acc = tuple(x/9.80665 for x in lis.acceleration)
    #log("Acceleration: X:%.2f, Y: %.2f, Z: %.2f g"%(acc))
    return (round(acc[0]-dg[0],2), round(acc[1]-dg[1],2), round(acc[2]-dg[2],2))
#-----------------------------------------------------------
# print to to file
#-----------------------------------------------------------
def printToFile(fileName, str):
    log(str)
    f = open(fileName, "a")
    f.write(str)
    f.close()
#-----------------------------------------------------------
# write data to file
#-----------------------------------------------------------
def saveError(e):
    s = f'{datetime.now()} - {e}\n'
    printToFile("log/errors.txt", s)
#-----------------------------------------------------------
# write data to file
#-----------------------------------------------------------
def saveAll(dq):
    gx = [x[0] for x in dq]
    gy = [x[1] for x in dq]
    gz = [x[2] for x in dq]
    s = f'{{"date":"{datetime.now()}","deviceId":"{deviceId}","gx":{gx},"gy":{gy},"gz":{gz}}}\n'
    printToFile("data/data.txt", s)
#-----------------------------------------------------------
# make a blynk
#-----------------------------------------------------------
def blynk(delay=0.5):
    led.value = True
    time.sleep(delay)
    led.value = False
    time.sleep(delay)
#-----------------------------------------------------------
# main
#-----------------------------------------------------------
for _ in range(10): blynk(0.1)
os.makedirs("data", exist_ok=True)
os.makedirs("log", exist_ok=True)
os.makedirs("tmp", exist_ok=True)

printToFile("log/tdi_accelerometer.log", f'{datetime.now()} - Started\n')

calibrateG()

while 1:
    try:
        g=getG()
        dq.append(g)
        if g[0] > THRESHOLD or g[1] > THRESHOLD or g[2] > THRESHOLD:
            for _ in range(25):
                g=getG()
                dq.append(g)
            saveAll(dq)
            blynk()
         
    except Exception as e:
        try:
            saveError(e)
        except Exception as e2:
            log(e2)
