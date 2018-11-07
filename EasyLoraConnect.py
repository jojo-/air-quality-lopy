import config
import binascii
import struct
import pycom
import time
import socket
from network import LoRa
import machine

class EasyLoraConnect(object): 

    def __init__(self, resetOnFailure=True):
        self.lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AS923, tx_retries=config.N_TX, device_class=LoRa.CLASS_A)
        self.resetOnFailure = resetOnFailure
        self._join_lora()

    def _join_lora(self,force_join= True):
    
        # create an OTA authentication params
        app_eui = binascii.unhexlify(config.APP_EUI.replace(' ',''))
        app_key = binascii.unhexlify(config.APP_KEY.replace(' ',''))

        # Switch the red led on
        pycom.rgbled(0xFF0000)

        # join a network using OTAA if not previously done
        self.lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

        print(binascii.hexlify(self.lora.mac()).upper().decode('utf-8'))
        print("Joining Lora")

        # wait until the module has joined the network
        nb_try = 0
        while not self.lora.has_joined():
            time.sleep(2.5)
            print("Not joined yet in try "+ str(nb_try))
            if self.resetOnFailure and nb_try > config.MAX_TRY:
                print("Cannot join so rebooting")
                machine.reset()
            nb_try = nb_try + 1
        print("LoRa Joined")
        # Switch the red led off
        pycom.rgbled(0x006400)

    def send(self,payload):
        '''Sending data over LoraWan '''
        pycom.rgbled(0xFF8C00)
        # create a LoRa socket
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        # set the LoRaWAN data rate
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.DATA_RATE)

        # make the socket blocking
        s.setblocking(True)

        s.send(payload)
        
        pycom.rgbled(0x006400)
        # closing the socket and saving the LoRa state
        s.close()

        self.lora.nvram_save()
