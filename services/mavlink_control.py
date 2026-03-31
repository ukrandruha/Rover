# services/mavlink_control.py

from pymavlink import mavutil

class ArdupilotControl:

    def __init__(self):
        self.master = None
        self.armed = False

    def set_master(self, master):
        self.master = master

    def clamp(self, x, lo=1000, hi=2000):
        return max(lo, min(hi, int(x)))

    def rc_override(self, channels: dict):
        if not self.master:
            return

        rc = [65535] * 18

        for ch, val in channels.items():
            rc[ch - 1] = self.clamp(val)

        self.master.mav.rc_channels_override_send(
            self.master.target_system,
            self.master.target_component,
            *rc
        )

    def move_all(self, values):
        if not values or not self.master:
            return

        channels = {i+1: values[i] for i in range(len(values))}
        self.rc_override(channels)

    def arm(self):
        if not self.master:
            return

        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1, 0, 0, 0, 0, 0, 0
        )
        self.armed = True

    def disarm(self):
        if not self.master:
            return

        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            0, 0, 0, 0, 0, 0, 0
        )
        self.armed = False

    def motor_stop(self):
        self.move_all([1500] * 12)
