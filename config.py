# Air Quality Sensing
#
# Configuration for The Things Network

# credentials
APP_EUI = 'XX XX XX XX XX XX XX XX'
APP_KEY = 'YY YY YY YY YY YY YY YY YY YY YY YY YY YY YY YY' # Proto 1

# max number of connection attemps to TTN
MAX_JOIN_ATTEMPT = const(50)

# number of packets to be transmit with the same data  (retries)
# default is 3
N_TX = const(0)

# data rate used to send message via LoRaWAN:
# 1 (slowest - longest range) to 4 (fastest - smallest range)
DATA_RATE = const(4)

N_SAMPLES = 5000
#CALIB_CO2 = 1476

# Set flag to true if you want to force the join to The Things Network
# and have access to the REPL interface
FORCE_JOIN = False

# Set flag to True if you want to use the deepsleep between the readings (save power)
USE_DEEPSLEEP = False
