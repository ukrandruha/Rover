# services/vesc_service.py

from pyvesc import VESC

class VescService:
    def __init__(self):
        try:
            self.vesc = VESC('/dev/ttyACM0', baudrate=115200)
        except:
            self.vesc = None

    def get_data(self):
        if not self.vesc:
            return {}

        try:
            data = self.vesc.get_measurements()
            return {"avg_input_current": getattr(data, "avg_input_current", None)}
        except:
            return {}
