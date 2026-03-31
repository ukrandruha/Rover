# services/serial_service.py

import serial
import threading
import queue
import time
import logging

PACKET_SIZE = 15

def unpack7(payload: bytes):
    vals, acc, acc_bits = [], 0, 0
    for b in payload:
        acc |= b << acc_bits
        acc_bits += 8
        while acc_bits >= 10 and len(vals) < 12:
            x10 = acc & 0x3FF
            acc >>= 10
            acc_bits -= 10
            vals.append(x10 + 1000)
    return vals


class SerialService:
    def __init__(self, port="/tmp/momo_out", baud=115200):
        self.port = serial.Serial(port, baudrate=baud, timeout=0.1)
        self.queue = queue.Queue(maxsize=50)
        self.running = True

    def start(self):
        threading.Thread(target=self.read_loop, daemon=True).start()

    def read_loop(self):
        buffer = b""

        while self.running:
            try:
                data = self.port.read(64)
                if not data:
                    continue

                buffer += data

                while len(buffer) >= PACKET_SIZE:
                    packet = buffer[:PACKET_SIZE]
                    buffer = buffer[PACKET_SIZE:]

                    vals = unpack7(packet)
                    if not self.queue.full():
                        self.queue.put(vals)

            except Exception:
                logging.error("Serial error", exc_info=True)
                time.sleep(0.1)