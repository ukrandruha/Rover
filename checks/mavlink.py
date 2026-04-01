
from base import ComponentCheck

class MAVLinkCheck(ComponentCheck):
    name = "mavlink"

    def __init__(self, master):
        self.master = master

    def check(self):
        try:
            msg = self.master.recv_match(type='HEARTBEAT', blocking=True, timeout=2)
            if msg:
                return {"status": "ok", "critical": True}
            else:
                return {"status": "fail", "message": "No heartbeat", "critical": True}
        except Exception as e:
            return {"status": "fail", "message": str(e), "critical": True}