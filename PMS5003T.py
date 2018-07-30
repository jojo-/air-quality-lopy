from machine import Pin, UART, RTC
import time


class PMS5003T(object):

    def __init__(self,PTX='P10',PRX='P11',PSLEEP=None):
        self._PTX = PTX
        self._PRX = PRX
        self._PSLEEP = PSLEEP
        self._uart1 = UART(1, baudrate=9600, timeout_chars=7, pins=(PTX,PRX))
        if self._PSLEEP is not None:
            self._set_pin = Pin(PSLEEP, mode=Pin.OUT, pull=Pin.PULL_DOWN)
        self._pm1_0 = 0
        self._pm2_5 = 0
        self._pm10 = 0
        self.error = False
        self._sleep()

    def _sleep(self):
        if self._PSLEEP is not None:
            self._set_pin.value(0)

    def _awake(self):
        if self._PSLEEP is not None:
            self._set_pin.value(1)

    def _get_pm1_0(self):
        return self._pm1_0

    def _get_pm2_5(self):
        return self._pm2_5

    def _get_pm10(self):
        return self._pm10

    def _isError(self):
        return self.error

    def _read_PM(self):
        raw_packet = None
        while raw_packet is None:
            raw_packet = self._uart1.readall()

        # finding the start/end of the packet and extracting it
        idx_begin = raw_packet.find(b'B')
 
        idx_end   = idx_begin + 32
        packet = raw_packet[idx_begin+1:idx_end]
   
        if(packet[0] == 0x4d):
            receiveflag=0
            receiveSum=0
            for i in range(0,28):
                receiveSum = receiveSum + packet[i]
            receiveSum = receiveSum + 0x42
            if (receiveSum == ((packet[29]<<8)+packet[30])):
                self.error = False
            else:
                self.error = True
            # pm concentrations
            self._pm1_0 = ((packet[3]<<8) + packet[4])
            self._pm2_5 = ((packet[5]<<8) + packet[6])
            self._pm10  = ((packet[7]<<8) + packet[8])
        # return the concentrations
        return (self._pm1_0, self._pm2_5, self._pm10)
