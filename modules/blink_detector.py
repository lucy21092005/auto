# modules/blink_detector.py

class BlinkDetector:

    def __init__(self, ear_threshold=0.20, min_frames_closed=2):
        """
        Blink detection using Eye Aspect Ratio (EAR)

        Parameters:
        ear_threshold: EAR value below which eye is considered closed
        min_frames_closed: minimum consecutive frames required to count as a blink
        """

        self.ear_threshold = ear_threshold
        self.min_frames_closed = min_frames_closed

        # Number of consecutive frames eye has been closed
        self.closed_frames = 0

        # Total blink count
        self.total_blinks = 0

        # Eye state tracking
        self.eye_closed = False

        # Blink event flag (used by NonResponseDetector)
        self.blink_detected = False


    def update(self, ear):
        """
        Update blink detection based on current EAR value

        Returns:
        total_blinks (int)
        """

        # Reset blink_detected flag every frame
        self.blink_detected = False

        # If EAR below threshold → eye closed
        if ear < self.ear_threshold:

            self.closed_frames += 1
            self.eye_closed = True

        else:

            # Eye reopened → check if blink occurred
            if self.eye_closed and self.closed_frames >= self.min_frames_closed:

                self.total_blinks += 1

                # Blink detected event
                self.blink_detected = True

            # Reset closed frame counter
            self.closed_frames = 0

            # Update eye state
            self.eye_closed = False


        return self.total_blinks


    def reset(self):
        """
        Reset blink detector state (optional utility)
        """

        self.closed_frames = 0
        self.total_blinks = 0
        self.eye_closed = False
        self.blink_detected = False


    def get_blink_count(self):
        """
        Returns total blink count
        """

        return self.total_blinks


    def is_eye_closed(self):
        """
        Returns True if eye currently closed
        """

        return self.eye_closed
