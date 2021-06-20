import board
import digitalio
import time

import requests
import os
from time import sleep
from datetime import datetime

import socket
#-----------------------------------------------------------
# global variables
#-----------------------------------------------------------
deviceId=3

tdi_url="https://tdiwebapp2.azurewebsites.net"
FILE_NAME="data.txt"
DATA_FOLDER="data"
TMP_FOLDER="tmp"

ledGreen = digitalio.DigitalInOut(board.D22)
ledGreen.direction = digitalio.Direction.OUTPUT
ledRed = digitalio.DigitalInOut(board.D27)
ledRed.direction = digitalio.Direction.OUTPUT
#ledBlue = digitalio.DigitalInOut(board.PA6)
#ledBlue.direction = digitalio.Direction.OUTPUT

#-----------------------------------------------------------
# log to console
#-----------------------------------------------------------
def log(str):
    print(str)
#-----------------------------------------------------------
# get mac address ("wlan0", eth0, tun2, lo)
#-----------------------------------------------------------
def getmac(interface):
  try:
    mac = open('/sys/class/net/'+interface+'/address').readline()
  except:
    mac = "00:00:00:00:00:00"

  return mac[0:17]
#-----------------------------------------------------------
# get private IP on the local network
#-----------------------------------------------------------
def get_my_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Google Public DNS
        s.connect(('8.8.8.8', 1)) 
        IP = s.getsockname()[0]
    except Exception:
        IP = 'IP not found'
    finally:
        s.close()
    return IP
#-----------------------------------------------------------
# make a blynk
#-----------------------------------------------------------
def ledInfoBlynk(delay=0.5):
    ledGreen.value = True
    time.sleep(delay)
    ledGreen.value = False
#-----------------------------------------------------------
# make a blynk
#-----------------------------------------------------------
def ledAlarmBlynk(delay=0.5):
    ledRed.value = True
    time.sleep(delay)
    ledRed.value = False
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
    try:
        s = f'{datetime.now()} - {e}\n'
        printToFile("log/http-server-errors.txt",s)
    except Exception as e:
        log(e) 
#-----------------------------------------------------------
# Send data
#-----------------------------------------------------------
def send_data(txt):
    r=requests.post(tdi_url+'/home/setdata', data={'row':txt}, timeout=20)
    log(r.text)
    ledAlarmBlynk(0.1)
    return r.status_code
 
def read_file(file_name):
    if not os.path.isfile(file_name):
        return False
    
    log('send file: '+file_name)
    with open(file_name) as f:
        for line in f:
            send_data(line)
    
    os.remove(file_name)
            
    
def is_ready_to_send():
    try:
        ip=get_my_private_ip()
        mac=getmac("wlan0")
        r=requests.post(tdi_url+'/home/ping', data={'deviceId':deviceId, 'ip':ip, 'mac':mac}, timeout=20)
        ledInfoBlynk(0.1)
        return r.status_code == 200
    except:
        ledInfoBlynk(5)
        return False
#-----------------------------------------------------------
# main
#-----------------------------------------------------------
for _ in range(3): #app started indicator
    ledInfoBlynk(0.1)
    time.sleep(0.1)

os.makedirs("data", exist_ok=True)
os.makedirs("log", exist_ok=True)
os.makedirs("tmp", exist_ok=True)

printToFile("log/http-server.log", f'{datetime.now()} - Started\n')

while 1:
    try:
        sleep(10) #delay in sec
        if is_ready_to_send():
            log('ready to send')
            read_file(TMP_FOLDER+"/"+FILE_NAME)
            #move
            sourceFN = DATA_FOLDER+"/"+FILE_NAME
            if os.path.isfile(sourceFN):
                os.replace(sourceFN, TMP_FOLDER+"/"+FILE_NAME)
                read_file(TMP_FOLDER+"/"+FILE_NAME)
    except Exception as e:
        saveError(e)
