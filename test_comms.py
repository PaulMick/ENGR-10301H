import logging
import time

from kaspersmicrobit import KaspersMicrobit

logging.basicConfig(level=logging.INFO)

with KaspersMicrobit.find_one_microbit() as microbit:

    i = 0
    while i < 100:
        microbit.uart.send_string(f"{i},p\n")
        i += 1
        time.sleep(0.25)

    time.sleep(1)

