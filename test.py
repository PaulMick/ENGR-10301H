import logging
import time

from kaspersmicrobit import KaspersMicrobit

logging.basicConfig(level=logging.INFO)

with KaspersMicrobit.find_one_microbit() as microbit:

    microbit.uart.send_string("1234\n")

    time.sleep(1)

# from microbit_comms import MicrobitCommunicator
# import time

# mb_comms = MicrobitCommunicator()

# mb_comms.send_data([0, -1.1, -2, 3.3, 4, 5])

# time.sleep(20)