## Test code for read date/time from gps and update RTC
import config
from SEN0177 import SEN0177
import time
import cayenneLPP

import socket
import binascii
# setup as a station
from network import LoRa
import gc

time.sleep(2)
gc.enable()
gc.collect()

# init Lorawan
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AU915, tx_retries=config.N_TX, device_class=LoRa.CLASS_A)

#Init the SEN0177 Sensor
sen0177 = SEN0177(PTX='P10',PRX='P11',PSLEEP='P9')

def join_lora(force_join= False):
    for i in range(16,65):
        try:
            lora.remove_channel(i)
        except:
            print("No range " + i)
    for i in range(66,72):
        try:
            lora.remove_channel(i)
        except:
            print("No range " + i)
    # create an OTA authentication params
    app_eui = binascii.unhexlify(config.APP_EUI.replace(' ',''))
    app_key = binascii.unhexlify(config.APP_KEY.replace(' ',''))

    pycom.rgbled(0xFF0000)
    # join a network using OTAA if not previously done
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
    print("Joining Lora")

    # wait until the module has joined the network
    attempt = 0
    while not lora.has_joined():
        time.sleep(2.5)
        print("Not joined yet")
    print("LoRa Joined")
    pycom.rgbled(0x000000)
def send_LPP_over_lora(pm1_0, pm2_5, pm10):
   '''Sending data over LoraWan using Cayenne LPP format'''

   # create a LoRa socket
   s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

   # set the LoRaWAN data rate
   s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.DATA_RATE)

   # make the socket blocking
   s.setblocking(True)

   # creating the lpp object
   lpp = cayenneLPP.CayenneLPP(size = 150, sock = s)

   # adding the payload
   lpp.add_analog_input(pm1_0, channel = 11)
   lpp.add_analog_input(pm2_5, channel = 12)
   lpp.add_analog_input(pm10,  channel = 13)

   # sending the payload
   lpp.send()

   # closing the socket and saving the LoRa state
   s.close()

join_lora()

while True:
    #Read sensor data
    (pm1_0,pm2_5,pm10)= sen0177._read_PM()
    print('===============================')
    print('pm1   =' + str(pm1_0) + ' ug/m3')
    print('pm2.5 =' + str(pm2_5) + ' ug/m3')
    print('pm10  =' + str(pm10) + ' ug/m3')

    send_LPP_over_lora(pm1_0,pm2_5,pm10)

    gc.collect()
    time.sleep(config.INT_SAMPLING)
