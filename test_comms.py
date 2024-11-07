import logging
import time

from kaspersmicrobit import KaspersMicrobit

logging.basicConfig(level=logging.INFO)

with KaspersMicrobit.find_one_microbit() as microbit:

    microbit.uart.send_string("1234\n")

    time.sleep(1)

