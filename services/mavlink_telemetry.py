# services/mavlink_telemetry.py

import time


class MavlinkTelemetryService:
    def __init__(self):
        self.master = None

    def set_master(self, master):
        self.master = master

    def safe_recv_match(self, *args, **kwargs):
        if not self.master:
            return None
        try:
            return self.master.recv_match(*args, **kwargs)
        except Exception:
            return None

    def get_gps_data(self, timeout=1.0):
        if not self.master:
            return {}

        deadline = time.time() + timeout
        lat = lon = hdop = sats = compass = None

        while time.time() < deadline:
            msg = self.safe_recv_match(
                type=["GLOBAL_POSITION_INT", "GPS_RAW_INT", "VFR_HUD"],
                blocking=True,
                timeout=0.2,
            )

            if not msg:
                continue

            msg_type = msg.get_type()
            if msg_type == "GLOBAL_POSITION_INT":
                lat = msg.lat / 1e7
                lon = msg.lon / 1e7
            elif msg_type == "GPS_RAW_INT":
                sats = msg.satellites_visible
                if msg.eph != 65535:
                    hdop = msg.eph / 100.0
            elif msg_type == "VFR_HUD":
                compass = msg.heading

        return {
            "lat": lat,
            "lon": lon,
            "satellites": sats,
            "hdop": hdop,
            "compass": compass,
        }
