from base import ComponentCheck

class VescCheck(ComponentCheck):
    name = "Vesc"

    def __init__(self, vesc):
        self.vesc = vesc

    def check(self):
        msg = self.vesc.get_measurements()
        if msg: 
            return {"status": "ok", "critical": True}
        return {"status": "fail", "message": "No control signal", "critical": True}

