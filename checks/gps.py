from base import ComponentCheck
class GPSCheck(ComponentCheck):
    name = "gps"

    def __init__(self, master):
        self.master = master

    def check(self):
        msg = self.master.recv_match(type='GPS_RAW_INT', blocking=False)
        if msg:
            return {"status": "ok", "critical": False}
        return {"status": "warning", "message": "No GPS", "critical": False}