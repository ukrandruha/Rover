from .base import ComponentCheck

class AvrCheck(ComponentCheck):
    name = "Avr"

    def __init__(self, avr):
        self.avr = avr

    def check(self):
        try:
            data = self.avr.get_data()
            if data:
                return {"status": "ok", "message": "", "critical": False}
            return {"status": "warning", "message": "No AVR data", "critical": False}
        except Exception as e:
            return {"status": "warning", "message": str(e), "critical": False}
