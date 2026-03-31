# main.py

import time
import argparse

import json

def run_self_check():
    print("=== SELF-CHECK START ===")
    ok = True

    try:
        from services.serial_service import SerialService
        from services.mavlink_service import MAVLinkService
        from services.vesc_service import VescService
        from services.avr_service import AVRService
    except ModuleNotFoundError as e:
        print(f"imports: FAIL ({e})")
        print("=== SELF-CHECK FAILED ===")
        return 1

    serial = None
    try:
        serial = SerialService()
        print("serial_in: OK")
    except Exception as e:
        ok = False
        print(f"serial_in: FAIL ({e})")

    vesc = VescService()
    print(f"vesc: {'OK' if vesc.vesc else 'UNAVAILABLE'}")

    avr = AVRService()
    print(f"avr: {'OK' if avr.avr else 'UNAVAILABLE'}")

    mav = MAVLinkService()
    mav_ok, mav_err = mav.try_connect_once(timeout=3)
    if mav_ok:
        print("mavlink: OK")
    else:
        ok = False
        print(f"mavlink: FAIL ({mav_err})")

    if serial and hasattr(serial, "port"):
        try:
            serial.port.close()
        except Exception:
            pass
    if avr and avr.avr:
        try:
            avr.avr.close()
        except Exception:
            pass
    if mav.master and hasattr(mav.master, "close"):
        try:
            mav.master.close()
        except Exception:
            pass

    print(f"=== SELF-CHECK {'PASSED' if ok else 'FAILED'} ===")
    return 0 if ok else 1


def main(self_check=False):
    if self_check:
        return run_self_check()

    from services.serial_service import SerialService
    from services.control_service import ControlService
    from services.mavlink_service import MAVLinkService
    from services.mavlink_telemetry import MavlinkTelemetryService
    from services.telemetry_service import TelemetryService
    from services.vesc_service import VescService
    from services.avr_service import AVRService
    from services.mavlink_control import ArdupilotControl

    serial = SerialService()
    mavlink_control = ArdupilotControl()
    mavlink_telemetry = MavlinkTelemetryService()
    control = ControlService(serial, mavlink_control)

    mav = MAVLinkService()
    vesc = VescService()
    avr = AVRService()

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
