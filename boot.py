# Air Quality Sensing
#
# Boot script

from machine import UART
from network import WLAN
import pycom
import os

# deactivate wifi
if pycom.wifi_on_boot:
    wlan = WLAN()
    wlan.deinit()
    pycom.wifi_on_boot(False)

# disabling the heartbeat
pycom.heartbeat(False)

# setting up the communication interface
uart = UART(0, 115200)
os.dupterm(uart)
