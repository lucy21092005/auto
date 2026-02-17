# modules/sos_alert.py

import time
import os


class SOSAlertSystem:
    """
    SOS Alert System using connected Android phone via ADB.
    Sends real SMS using user's SIM card.
    Includes cooldown protection to prevent repeated alerts.
    """

    def __init__(self, cooldown=60, emergency_number="+916282143385"):

        # Cooldown time (seconds)
        self.cooldown = cooldown

        # Last SOS trigger timestamp
        self.last_trigger_time = 0

        # SOS state
        self.sos_active = False

        # Emergency contact number (CHANGE IF NEEDED)
        self.emergency_number = emergency_number

        # Emergency message
        self.message = "🚨 AUTO-GUARDIAN-X ALERT: Driver is non-responsive. Immediate attention required."


    def can_trigger(self):

        current_time = time.time()

        return (current_time - self.last_trigger_time) >= self.cooldown


    def trigger(self):

        if self.can_trigger():

            self.last_trigger_time = time.time()
            self.sos_active = True

            print("🚨 SOS ALERT TRIGGERED")

            # Send SMS via Android phone
            self.send_sms_alert()

            return True

        return False


    def send_sms_alert(self):

        try:

            print("Sending SMS via connected Android phone...")

            command = (
                f'adb shell service call isms 7 i32 0 '
                f's16 "com.android.mms.service" '
                f's16 "{self.emergency_number}" '
                f's16 "null" '
                f's16 "{self.message}" '
                f's16 "null" '
                f's16 "null"'
            )

            os.system(command)

            print("✅ SMS sent successfully via Android phone")

        except Exception as e:

            print("❌ SMS sending failed:", e)


    def reset(self):

        self.sos_active = False


    def is_active(self):

        return self.sos_active
