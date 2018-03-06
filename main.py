# Air Quality Sensing
#
# Main script
# todo: filter data, add temperature, check calibration of co2 co2_sensor,
#       develop a proper PSU for the sensors, use external ADC board
#       calibrate ADC: https://docs.pycom.io/chapter/tutorials/all/adc.html
#       use adcchannel.voltage() method instead:
#           https://docs.pycom.io/chapter/firmwareapi/pycom/machine/ADC.html
#       wifi enabled for OTA firmware update

import time
import socket
import binascii
import struct
import config
import cayenneLPP
import gc
from machine import ADC, Pin, UART, deepsleep
from network import LoRa

# enabling garbage collector
gc.enable()

# setting up the Analog/Digital Converter with 12 bits
adc = ADC(bits=12)
adc.vref(1155)

# create an analog pin on P10 for the co2 sensor
co2_sensor = adc.channel(pin='P20', attn=ADC.ATTN_2_5DB)

# init Lorawan
lora = LoRa(mode=LoRa.LORAWAN, adr=False, tx_retries=0, device_class=LoRa.CLASS_A)

# init uart
uart1 = UART(1, baudrate=9600, timeout_chars=7)


def join_lora(force_join = False):
    '''Joining The Things Network '''

    # restore previous state
    if not force_join:
        lora.nvram_restore()

    # remove default channels
    for i in range(16, 65):
        lora.remove_channel(i)
    for i in range(66, 72):
        lora.remove_channel(i)

    if not lora.has_joined() or force_join == True:

        # create an OTA authentication params
        app_eui = binascii.unhexlify(config.APP_EUI.replace(' ',''))
        app_key = binascii.unhexlify(config.APP_KEY.replace(' ',''))

        # join a network using OTAA if not previously done
        lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

        # wait until the module has joined the network
        attempt = 0
        while not lora.has_joined() and attempt < config.MAX_JOIN_ATTEMPT:
            time.sleep(2.5)
            attempt = attempt + 1

        # saving the state
        if not force_join:
            lora.nvram_save()

        # returning whether the join was successful
        if lora.has_joined():
            return True
        else:
            return False

    else:
        return True


def send_LPP_over_lora(pm1_0, pm2_5, pm10, co2):
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
   lpp.add_analog_input(co2,   channel = 14)

   # sending the payload
   lpp.send()

   # closing the socket and saving the LoRa state
   s.close()

def read_pm():
    '''Reading the pm using the sensor via serial port '''

    # wait 3 seconds to make sure that the buffer is filled
    time.sleep_ms(3000)
    raw_packet = uart1.readall()

    # finding the start/end of the packet and extracting it
    idx_begin = raw_packet.find(b'B')
    idx_end   = idx_begin + 31
    packet = raw_packet[idx_begin:idx_end]

    # pm concentrations
    pm1_0 = int.from_bytes(packet[4:6], 'high')
    pm2_5 = int.from_bytes(packet[6:8], 'high')
    pm10  = int.from_bytes(packet[8:10], 'high')

    # return the concentrations
    return (pm1_0, pm2_5, pm10)

def read_co2():

    volt = co2_sensor.voltage()
    for i in range(config.N_SAMPLES):
        volt = (co2_sensor.voltage() + volt) / 2

    #volt = (volt / 4096.0) * config.CALIB_CO2
    #print("volt = " + str(volt))

    if volt < 400:
        print('Pre-heating')
        return 0.0

    volt_diff = volt - 400.0
    co2 = volt_diff * 50.0 / 16.0

    return co2

'''
################################################################################
#
# Main script
#
# 1. Join Lorawan (if needed)
# 2. Read pm/co2 values
# 3. Transmit the data to Cayenne if join was successful
# 4. Sleep or deepsleep (see config)
#
################################################################################
'''

join_lora()

if config.USE_DEEPSLEEP:
    co2=0
    #co2 = read_co2() / 100.0
    (pm1_0, pm2_5, pm10) = read_pm()
    for i in range(config.N_TX):
        send_LPP_over_lora(pm1_0, pm2_5, pm10, co2)
    gc.collect()
    deepsleep(config.INT_SAMPLING)
else:
    while True:

        co2=0
        #co2 = read_co2() / 100.0
        #print(co2)

        (pm1_0, pm2_5, pm10) = read_pm()

        print('pm1  =' + str(pm1_0) + 'ug/m3')
        print('pm2.5=' + str(pm2_5) + 'ug/m3')
        print('pm10 =' + str(pm10) + 'ug/m3')

        for i in range(config.N_TX):
            send_LPP_over_lora(pm1_0, pm2_5, pm10, co2)

        time.sleep_ms(60000)
