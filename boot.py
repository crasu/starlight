# boot.py -- run on boot-up
import os
from network import WLAN
import machine
import config

uart = machine.UART(0, 115200)
os.dupterm(uart)

wlan = WLAN(mode=WLAN.STA)

if not wlan.isconnected():
    print("Connecting ...")
    wlan.connect(config.SSID, auth=(WLAN.WPA2, config.PASSWORD), timeout=5000)
    print("Waiting for wifi network:{}".format(config.SSID))
    while not wlan.isconnected():
        machine.idle() # save power while waiting
    
    print("Connected to network:{}".format(config.SSID))
    wlan.ifconfig(config=(config.IP, '255.255.255.0', config.GATEWAY, '8.8.8.8'))

print(wlan.ifconfig())
