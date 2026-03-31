# services/avr_service.py

import serial

class AVRService:
    def __init__(self):
        try:
            self.avr = serial.Serial(
                "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A5069RR4-if00-port0",
                115200,
                timeout=0.5
            )
        except:
            self.avr = None

    def get_data(self):
        if not self.avr or not self.avr.is_open:
            return {}

        try:
            self.avr.write(b"GETSTATE\n")
            raw = self.avr.read_all().decode(errors="replace")

            data = {}
            for line in raw.splitlines():
                if line.startswith("STATE "):
                    parts = line.split()
                    if len(parts) >= 3:
                        data[parts[1]] = parts[2]

            return data

        except:
            return {}