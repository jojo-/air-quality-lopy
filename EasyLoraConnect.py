import cayenneLPP
import config
import binascii
import struct
import pycom
import time
import socket
from network import LoRa

class EasyLoraConnect(object): 

    def __init__(self):
        self.lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AS923, tx_retries=config.N_TX, device_class=LoRa.CLASS_A)
        self._join_lora()

    def _join_lora(self,force_join= True):
    
        # create an OTA authentication params
        app_eui = binascii.unhexlify(config.APP_EUI.replace(' ',''))
        app_key = binascii.unhexlify(config.APP_KEY.replace(' ',''))
        #nwk_swkey = binascii.unhexlify(config.NWK_KEY)
        #app_swkey = binascii.unhexlify(config.APP_SWKEY)
        #dev_addr = struct.unpack(">l", binascii.unhexlify(config.DEV_ADDR))[0]
        # Switch the red led on
        pycom.rgbled(0xFF0000)

        # join a network using OTAA if not previously done
        self.lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
        #self.lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

        print(binascii.hexlify(self.lora.mac()).upper().decode('utf-8'))
        print("Joining Lora")

        # wait until the module has joined the network
        attempt = 0
        while not self.lora.has_joined():
            time.sleep(2.5)
            print("Not joined yet")
        print("LoRa Joined")
        # Switch the red led off
        pycom.rgbled(0x006400)

    def _send_LPP_over_lora(self,split):
        '''Sending data over LoraWan using Cayenne LPP format'''
        pycom.rgbled(0xFF8C00)
        # create a LoRa socket
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        # set the LoRaWAN data rate
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.DATA_RATE)

        # make the socket blocking
        s.setblocking(True)

        # creating the lpp object
        lpp = cayenneLPP.CayenneLPP(size = 150, sock = s)

        # adding the payload
        i=0
        for val in split: 
            lpp.add_digital_input(int(val), channel = i)
            i=i+1

        # sending the payload
        lpp.send()
        
        pycom.rgbled(0x006400)
        # closing the socket and saving the LoRa state
        s.close()
