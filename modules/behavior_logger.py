import csv
import os
import time


class BehaviorLogger:

    def __init__(self, filename="driver_behavior_log.csv"):

        self.filename = filename

        # Always ensure header exists
        if not os.path.exists(self.filename) or os.stat(self.filename).st_size == 0:

            with open(self.filename, mode="w", newline="") as file:

                writer = csv.writer(file)

                writer.writerow([
                    "timestamp",
                    "ear",
                    "blink_count",
                    "eye_closure_duration",
                    "phone_detected",
                    "distraction_duration",
                    "risk_score"
                ])


    def log(self, ear, blink_count, closure_duration, phone_detected, distraction_duration, risk_score, latitude=None, longitude=None, map_link=None):

        timestamp = time.time()

        with open(self.filename, mode="a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
    timestamp,
    ear,
    blink_count,
    closure_duration,
    phone_detected,
    distraction_duration,
    risk_score,
    latitude,
    longitude,
    map_link
])
