# services/control_service.py

import time
import queue


class ControlService:
    def __init__(self, serial_service,pilot):
        self.serial = serial_service
        self.pilot = pilot
        self.last_packet_time = time.time()
        self.connected = False
        self.last_tick = 0
        self.disconnect_timeout_s = 1

    def tick(self):
        now = time.time()

        # 50 Hz
        if now - self.last_tick < 0.02:
            return

        self.last_tick = now

        try:
            vals = self.serial.queue.get_nowait()
            self.connected = True
            self.last_packet_time = now

            self.pilot.move_all(vals)

        except queue.Empty:
            pass

        if self.connected and now - self.last_packet_time > self.disconnect_timeout_s:
            self.connected = False
            self.pilot.motor_stop()
