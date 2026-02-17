import time


class ClosureDetector:

    def __init__(self, ear_threshold=0.20):

        self.ear_threshold = ear_threshold

        self.eye_closed = False
        self.start_time = 0

        self.closure_duration = 0


    def update(self, ear):

        current_time = time.time()

        # Eye closed
        if ear < self.ear_threshold:

            if not self.eye_closed:

                self.eye_closed = True
                self.start_time = current_time

            self.closure_duration = current_time - self.start_time

        else:

            # Eye reopened
            self.eye_closed = False
            self.closure_duration = 0


        return self.closure_duration
