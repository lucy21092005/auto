import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import cv2
import time
from modules.gps_tracker import get_location
from core.model_manager import ModelManager
from core.risk_evaluator import RiskEvaluator
from core.perception_pipeline import PerceptionPipeline
from safety.alarm_controller import AlarmController
from modules.sos_alert import SOSAlertSystem
from modules.behavior_logger import BehaviorLogger
from ui.dashboard_renderer import DashboardRenderer


# Initialize systems
model_manager = ModelManager("driver_risk_model.pkl")
risk_evaluator = RiskEvaluator(model_manager)

perception_pipeline = PerceptionPipeline()

alarm_controller = AlarmController("alarm.wav")
sos_system = SOSAlertSystem()
logger = BehaviorLogger()

dashboard = DashboardRenderer()
# Telemetry file path
TELEMETRY_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "shared",
    "dashboard_data.json"
)
# Ensure shared directory exists
os.makedirs(os.path.dirname(TELEMETRY_FILE), exist_ok=True)




# Camera
cap = cv2.VideoCapture(1, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


if not cap.isOpened():
    print("Camera failed to open")
    exit()

# GPS state
last_lat = None
last_lon = None
last_map_link = None

GPS_COOLDOWN = 10  # seconds
last_gps_time = 0
frame_counter = 0
try:

    while True:

        # Reload model if updated
        model_manager.check_reload()

        ret, frame = cap.read()

        # Export frame for dashboard
        frame_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "shared",
            "frame.jpg"
        )

        # Make sure shared folder exists
        os.makedirs(os.path.dirname(frame_path), exist_ok=True)

        frame_counter += 1

        if frame_counter % 10 == 0:
            cv2.imwrite(frame_path, frame)


        if not ret:
            break


        # STEP 1: Perception Layer
        perception_data = perception_pipeline.process(frame)

        ear = perception_data["ear"]
        blink_count = perception_data["blink_count"]
        closure_duration = perception_data["closure_duration"]
        phone_detected = perception_data["phone_detected"]
        distraction_duration = perception_data["distraction_duration"]
        non_responsive = perception_data["non_responsive"]
        drowsiness_status = perception_data["drowsiness_status"]
        phone_status = perception_data["phone_status"]


        # STEP 2: Risk Evaluation Layer
        risk_data = risk_evaluator.evaluate(perception_data)

        risk_score = risk_data["risk_score"]
        risk_level = risk_data["risk_level"]
        risk_color = risk_data["risk_color"]
        system_status = risk_data["system_status"]


        # GPS acquisition during HIGH risk
        lat = None
        lon = None
        map_link = None

        current_time = time.time()

        if risk_level == "HIGH":

            if current_time - last_gps_time >= GPS_COOLDOWN:

                lat, lon = get_location()

                if lat is not None and lon is not None:

                    map_link = f"https://maps.google.com/?q={lat},{lon}"

                    last_lat = lat
                    last_lon = lon
                    last_map_link = map_link
                    last_gps_time = current_time

                    print(f"GPS Location: {lat}, {lon}")


        # STEP 3: Response Layer
        alarm_controller.update(risk_score)

        sos_triggered = False

        if (
            risk_score >= 80 or
            non_responsive or
            closure_duration >= 3 or
            distraction_duration >= 5
        ):
            if sos_system.trigger():
                sos_triggered = True


        logger.log(
            ear,
            blink_count,
            closure_duration,
            int(phone_detected),
            distraction_duration,
            risk_score,
            last_lat,
            last_lon,
            last_map_link
        )


        # STEP 5: Presentation Layer
        dashboard.render(
            frame,
            perception_data,
            risk_data,
            sos_system.is_active()
        )


        # GPS telemetry export
        lat, lon = get_location()

        map_link = None

        if lat is not None and lon is not None:
            map_link = f"https://maps.google.com/?q={lat},{lon}"


        telemetry_data = {

            "ear": float(ear),
            "blink_count": int(blink_count),
            "closure_duration": float(closure_duration),

            "phone_detected": bool(phone_detected),
            "distraction_duration": float(distraction_duration),

            "risk_score": float(risk_score),
            "risk_level": str(risk_level),
            "system_status": str(system_status),

            "sos_active": bool(sos_system.is_active()),

            # GPS data
            "latitude": lat,
            "longitude": lon,
            "map_link": map_link,

            "timestamp": time.time()
        }


        # Write telemetry data to shared file
        try:

            if frame_counter % 10 == 0:
                with open(TELEMETRY_FILE, "w") as f:
                    json.dump(telemetry_data, f, indent=4)

        except Exception as e:

            print("Telemetry write error:", e)


        # Show frame
        cv2.imshow("AUTO-GUARDIAN-X", frame)


        # Exit on ESC
        if cv2.waitKey(1) & 0xFF == 27:
            break


except KeyboardInterrupt:

    print("\nCTRL+C detected. Shutting down safely...")

finally:

    cap.release()
    cv2.destroyAllWindows()

    try:
        import pygame
        pygame.mixer.quit()
    except:
        pass

    print("System stopped.")




