# services/telemetry_service.py

class TelemetryService:
    def __init__(self, vesc, avr, gps_provider):
        self.vesc = vesc
        self.avr = avr
        self.gps_provider = gps_provider

    def tick(self):
        payload = {}

        payload.update(self.vesc.get_data())
        payload.update(self.avr.get_data())

        try:
            payload["gps"] = self.gps_provider.get_gps_data(timeout=0.1)
        except:
            payload["gps"] = {}

        return payload
