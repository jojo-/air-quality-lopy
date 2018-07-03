from machine import Pin, UART, RTC
import time


class SDS011(object):

    def __init__(self,PTX='P10',PRX='P11'):
        self._PTX = PTX
        self._PRX = PRX
        self._uart1 = UART(1, baudrate=9600, timeout_chars=7, pins=(PTX,PRX))
        self._pm2_5 = 0
        self._pm10 = 0
        self.error=0
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
        return self.error == 1

    def _read_PM(self):
        #Wait 3 seconds to make sure that the buffer is filled
        time.sleep_ms(3000)
        buffer = self._uart1.readall()
        if buffer is None:
            self.error = 1
            return (0,0)
        if (buffer[0] == 0xAA and buffer[1] == 0xC0 and buffer[9] == 0xAB):
            receiveSum = 0
            for i in range(2,8):
                receiveSum += buffer[i]
            if (receiveSum & 0xFF) == buffer[8]:
                self.error=0
                self._pm2_5= ((buffer[3]<<8) + buffer[2])
                self._pm10= ((buffer[5]<<8) + buffer[4])
                return (self._pm2_5, self._pm10)
            else:
                self.error = 1
                return (0,0)