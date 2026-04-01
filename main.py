# main.py

import time
import argparse

import json



def main(self_check=False):

    from services.serial_service import SerialService
    from services.control_service import ControlService

    from services.mavlink_service import MAVLinkService
    from services.mavlink_telemetry import MavlinkTelemetryService
    from services.telemetry_service import TelemetryService
    from services.vesc_service import VescService
    from services.avr_service import AVRService
    from services.mavlink_control import ArdupilotControl


    from core.health_manager import HealthManager
    from checks.gps import GPSCheck
    from checks.mavlink import MAVLinkCheck
    from checks.vesc import VescCheck
    from checks.avr import AvrCheck
    
    serial = SerialService()
    mavlink_control = ArdupilotControl()
    mavlink_telemetry = MavlinkTelemetryService()
    control = ControlService(serial, mavlink_control)

    mav = MAVLinkService()
    vesc = VescService()
    avr = AVRService()


    health = HealthManager([
        MAVLinkCheck(mav),
        GPSCheck(mav),
        VescCheck(vesc),
        AvrCheck(avr),
    ])
    health_last_print = 0.0
    health_print_interval_s = 2.0
    last_health_signature = None

    telemetry = TelemetryService(vesc, avr, mavlink_telemetry)

    serial.start()
    master = mav.connect()
    mavlink_control.set_master(master)
    mavlink_telemetry.set_master(master)

    print("System started")

    while True:
        try:
            current_master = mav.ensure_connection()
            if current_master is not mavlink_control.master:
                mavlink_control.set_master(current_master)
                mavlink_telemetry.set_master(current_master)
            control.tick()

            data = telemetry.tick()

            now = time.time()
            if now - health_last_print >= health_print_interval_s:
                results = health.run_checks()
                is_ready = health.is_system_ready(results)

                parts = []
                for name, result in results.items():
                    status = result.get("status", "unknown")
                    msg = result.get("message", "")
                    parts.append(f"{name}:{status}" + (f"({msg})" if msg else ""))

                line = " | ".join(parts)
                signature = (is_ready, line)
                if signature != last_health_signature:
                    level = "OK" if is_ready else "ALERT"
                    print(f"[HEALTH {level}] {line}")
                    last_health_signature = signature

                health_last_print = now

            # пишемо в порт
            with open("/tmp/momo_telem_out", "w") as f:
                f.write(json.dumps(data) + "\n")

            time.sleep(0.02)

        except Exception as e:
            print(f"MAIN ERROR: {e}")
            time.sleep(0.1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    raise SystemExit(main(self_check=args.self_check))
