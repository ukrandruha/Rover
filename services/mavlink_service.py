# services/mavlink_service.py

import time
from pymavlink import mavutil

class MAVLinkService:
    def __init__(self, port="/dev/serial0", baud=57600):
        self.port = port
        self.baud = baud
        self.master = None
        self.last_heartbeat = 0

    def connect(self):
        while True:
            ok, error = self.try_connect_once(timeout=5)
            if ok:
                print("MAVLink connected")
                return self.master
            print(f"MAVLink retry: {error}")
            time.sleep(2)

    def try_connect_once(self, timeout=5):
        try:
            print("Connecting MAVLink...")
            self.master = mavutil.mavlink_connection(self.port, baud=self.baud)
            self.master.wait_heartbeat(timeout=timeout)
            self.last_heartbeat = time.time()
            return True, None
        except Exception as e:
            self.master = None
            return False, str(e)

    def ensure_connection(self):
        if self.master is None:
            return self.connect()

        try:
            msg = self.master.recv_match(type='HEARTBEAT', blocking=False)
            if msg:
                self.last_heartbeat = time.time()
        except Exception:
            self.master = None

        if self.master is None or time.time() - self.last_heartbeat > 3:
            print("MAVLink lost → reconnect")
            self.master = None
            return self.connect()

        return self.master
