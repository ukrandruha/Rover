from base import ComponentCheck

class AvrCheck(ComponentCheck):
    name = "Avr"

    def __init__(self, avr):
        self.avr = avr

    def check(self):
        msg = self.avr.get_measurements()
        if msg: 
            return {"status": "ok", "critical": True}
        return {"status": "fail", "message": "No control signal", "critical": True}