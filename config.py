# Air Quality Sensing

# credentials
APP_EUI = 'xxx'
APP_KEY = 'xxx' # Proto 1
NWK_KEY = 'xxx'
DEV_ADR = 'xxx'

# max number of connection attemps to TTN
MAX_JOIN_ATTEMPT = const(50)
INT_SAMPLING = 30    # number of sec between each reading
# number of packets to be transmit with the same data  (retries)
# default is 3
N_TX = const(3)

# data rate used to send message via LoRaWAN:
# 1 (slowest - longest range) to 4 (fastest - smallest range)
DATA_RATE = const(4)
