from kaspersmicrobit import KaspersMicrobit
import time

class MicrobitCommunicator:
    def __init__(self) -> None:
        with KaspersMicrobit.find_one_microbit() as mb:
            self.microbit = mb

    def send_data(self, pose: list[float]) -> None:
        self.microbit.uart.send_string(str(pose).replace(" ", "") + "\n")