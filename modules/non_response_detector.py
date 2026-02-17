import time
from utils.constants import (
    NON_RESPONSE_EYE_CLOSURE_THRESHOLD,
    NON_RESPONSE_NO_BLINK_THRESHOLD,
    NON_RESPONSE_FACE_ABSENCE_THRESHOLD
)

class NonResponseDetector:
    """
    Detects prolonged non-responsive driver condition based on:
    - Eye closure duration
    - Blink absence duration
    - Face absence duration
    """

    def __init__(self):

        # Time when eyes first detected closed
        self.eye_closed_start_time = None

        # Last time blink detected
        self.last_blink_time = time.time()

        # Last time face detected
        self.face_last_detected_time = time.time()

        # Current non-response state
        self.non_responsive_state = False


    # Update eye state (called every frame)
    def update_eye_state(self, eyes_closed: bool):

        current_time = time.time()

        if eyes_closed:
            if self.eye_closed_start_time is None:
                self.eye_closed_start_time = current_time
        else:
            self.eye_closed_start_time = None


    # Update blink event (call when blink detected)
    def update_blink_event(self):

        self.last_blink_time = time.time()


    # Update face detection status (called every frame)
    def update_face_status(self, face_detected: bool):

        if face_detected:
            self.face_last_detected_time = time.time()


    # Check if driver is non-responsive
    def check_non_responsive(self) -> bool:

        current_time = time.time()

        eye_closure_duration = (
            current_time - self.eye_closed_start_time
            if self.eye_closed_start_time is not None
            else 0
        )

        no_blink_duration = current_time - self.last_blink_time

        face_absence_duration = current_time - self.face_last_detected_time


        # Condition check
        if (
            eye_closure_duration >= NON_RESPONSE_EYE_CLOSURE_THRESHOLD
            or no_blink_duration >= NON_RESPONSE_NO_BLINK_THRESHOLD
            or face_absence_duration >= NON_RESPONSE_FACE_ABSENCE_THRESHOLD
        ):
            self.non_responsive_state = True
        else:
            self.non_responsive_state = False


        return self.non_responsive_state


    # Optional: Get diagnostic info (useful for dashboard/debug)
    def get_status(self):

        current_time = time.time()

        return {
            "eye_closure_duration": (
                current_time - self.eye_closed_start_time
                if self.eye_closed_start_time else 0
            ),
            "no_blink_duration": current_time - self.last_blink_time,
            "face_absence_duration": current_time - self.face_last_detected_time,
            "non_responsive": self.non_responsive_state
        }
