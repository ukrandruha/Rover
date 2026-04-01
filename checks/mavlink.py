from .base import ComponentCheck

class MAVLinkCheck(ComponentCheck):
    name = "mavlink"

    def __init__(self, mav_service):
        self.mav_service = mav_service

    def check(self):
        try:
            master = getattr(self.mav_service, "master", None)
            if not master:
                return {"status": "fail", "message": "No MAVLink connection", "critical": True}

            msg = master.recv_match(type='HEARTBEAT', blocking=False)
            if msg:
                return {"status": "ok", "message": "", "critical": True}
            else:
                return {"status": "fail", "message": "No heartbeat", "critical": True}
        except Exception as e:
            return {"status": "fail", "message": str(e), "critical": True}
