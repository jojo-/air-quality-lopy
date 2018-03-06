# Air Quality Sensing
#
# Configuration for The Things Network

# credentials
APP_EUI = '70 B3 D5 7E D0 00 8D 7D'
#APP_KEY = 'AD E1 13 FF 0E EC BE B7 F5 AB A1 33 DA EF A6 A6' # Proto 2
APP_KEY = '84 B4 56 AA 9A 16 74 FE F3 9A FA BA EC 4C C2 BC' # Proto 1

# max number of connection attemps to TTN
MAX_JOIN_ATTEMPT = const(50)

# number of packets to be transmit with the same data  (retries)
# default is 3
N_TX = const(3)

# data rate used to send message via LoRaWAN:
# 1 (slowest - longest range) to 4 (fastest - smallest range)
DATA_RATE = const(4)

N_SAMPLES = 5000
#CALIB_CO2 = 1476

# Set flag to true if you want to force the join to The Things Network
# and have access to the REPL interface
FORCE_JOIN = False

USE_DEEPSLEEP = False
