from machine import Pin, UART, RTC
import time


class SEN0177(object):

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

    def _read_PM(self):
        #Wait 3 seconds to make sure that the buffer is filled
        time.sleep_ms(3000)
        raw_packet = self._uart1.readall()
        # finding the start/end of the packet and extracting it
        idx_begin = raw_packet.find(b'B')
        idx_end   = idx_begin + 31
        packet = raw_packet[idx_begin:idx_end]

        print(raw_packet)
        print(len(raw_packet))
        print(raw_packet[0])
        print(raw_packet[1])
        print(packet[3:4])

        # pm concentrations
        self._pm1_0 = int.from_bytes(packet[4:6], 'high')
        self._pm2_5 = int.from_bytes(packet[6:8], 'high')
        self._pm10  = int.from_bytes(packet[8:10], 'high')
        # return the concentrations
        return (self._pm1_0, self._pm2_5, self._pm10)
