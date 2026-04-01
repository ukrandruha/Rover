from .base import ComponentCheck

class VescCheck(ComponentCheck):
    name = "Vesc"

    def __init__(self, vesc):
        self.vesc = vesc

    def check(self):
        try:
            data = self.vesc.get_data()
            if "avg_input_current" in data:
                return {"status": "ok", "message": "", "critical": True}
            return {"status": "fail", "message": "No VESC data", "critical": True}
        except Exception as e:
            return {"status": "fail", "message": str(e), "critical": True}
