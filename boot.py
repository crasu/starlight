# boot.py -- run on boot-up
import os
from network import WLAN
from machine import UART,  idle
import config

uart = UART(0, 115200)
os.dupterm(uart)

wlan = WLAN(mode=WLAN.STA)

if not wlan.isconnected():
    print("Connecting ...")
    wlan.connect(config.SSID, auth=(WLAN.WPA2, config.PASSWORD), timeout=5000)
    print("Waiting for wifi network:{}".format(config.SSID))
    while not wlan.isconnected():
        idle() # save power while waiting
    
    print("Connected to network:{}".format(config.SSID))

print(wlan.ifconfig())
