from .base import ComponentCheck
class GPSCheck(ComponentCheck):
    name = "gps"

    def __init__(self, mav_service):
        self.mav_service = mav_service

    def check(self):
        try:
            master = getattr(self.mav_service, "master", None)
            if not master:
                return {"status": "warning", "message": "MAVLink disconnected", "critical": False}

            msg = master.recv_match(type='GPS_RAW_INT', blocking=False)
            if msg:
                return {"status": "ok", "message": "", "critical": False}
            return {"status": "warning", "message": "No GPS", "critical": False}
        except Exception as e:
            return {"status": "warning", "message": str(e), "critical": False}
