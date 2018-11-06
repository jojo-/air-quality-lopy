# An Air Quality sensor over Lora
#
# Version 0.5
#
# Authors: J. Barthelemy and N. Verstaevel
#

import config
from SDS011 import SDS011

from EasyLoraConnect import EasyLoraConnect
import gc
import time
import struct
import machine

try:
    lora = EasyLoraConnect()
    #Init the SEN0177 Sensor
    sds011 = SDS011(PTX='P11',PRX='P10')

    while True:
            #Read sensor data
            error = False
            (pm2_5,pm10) = sds011._read_PM()
            if not sds011._isError():
                print('===============================')
                #print('pm1  =' + str(pm1) + ' ug/m3')
                print('pm2.5 =' + str(pm2_5) + ' ug/m3')
                print('pm10  =' + str(pm10) + ' ug/m3')
                #lora._send_LPP_over_lora([str(pm2_5),str(pm10)])
            else:
                print('Oups...something went wrong in the reading')
                error = True

            ttn_data = bytes()
            ttn_data = ttn_data + struct.pack('!l', pm2_5)
            ttn_data = ttn_data + struct.pack('!l', pm10)
            checksum = pm2_5+pm10
            ttn_data = ttn_data + struct.pack('!l', checksum)
            print("Sending : "+str(ttn_data))
            lora.send(ttn_data)
            
            gc.collect()
            pycom.rgbled(0x4B0082)
            time.sleep(config.INT_SAMPLING)
except:
    machine.reset()