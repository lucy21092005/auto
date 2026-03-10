import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import cv2
import time
import requests 
from core.model_manager import ModelManager
from core.risk_evaluator import RiskEvaluator
from core.perception_pipeline import PerceptionPipeline
from safety.alarm_controller import AlarmController
from modules.behavior_logger import BehaviorLogger
from ui.dashboard_renderer import DashboardRenderer


ANDROID_IP = "152.59.222.108"   # replace with phone IP
ANDROID_PORT = "8080"

def send_emergency_signal():

    try:

        url = f"http://{ANDROID_IP}:{ANDROID_PORT}/trigger"

        response = requests.post(url, json={"alert": "UNCONSCIOUS_DRIVER"})

        print("Emergency signal sent:", response.status_code)

    except Exception as e:

        print("Failed to send emergency signal:", e)


# Initialize systems
model_manager = ModelManager("driver_risk_model.pkl")
risk_evaluator = RiskEvaluator(model_manager)

perception_pipeline = PerceptionPipeline()

alarm_controller = AlarmController("alarm.wav")

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

frame_counter = 0

emergency_state="NORMAL"
emergency_sent = False
def capture_emergency_evidence(frame, telemetry_data):

    timestamp = int(time.time())

    image_path = os.path.join(EVIDENCE_FOLDER, f"driver_{timestamp}.jpg")
    json_path = os.path.join(EVIDENCE_FOLDER, f"telemetry_{timestamp}.json")

    try:
        cv2.imwrite(image_path, frame)

        with open(json_path, "w") as f:
            json.dump(telemetry_data, f, indent=4)

        print("Emergency evidence saved")

    except Exception as e:
        print("Evidence save error:", e)

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
        if risk_score < 40:
    emergency_state = "NORMAL"

elif risk_score < 70:
    emergency_state = "WARNING"

else:
    emergency_state = "CRITICAL"
        risk_level = risk_data["risk_level"]
        risk_color = risk_data["risk_color"]
        system_status = risk_data["system_status"]


        
        


       

       

        # STEP 3: Response Layer
        alarm_controller.update(risk_score)

        sos_triggered = False

        


        logger.log(
    ear,
    blink_count,
    closure_duration,
    int(phone_detected),
    distraction_duration,
    risk_score,
    None,
    None,
    None
)


        # STEP 5: Presentation Layer
        dashboard.render(
            frame,
            perception_data,
            risk_data,
           
        )


        

        telemetry_data = {

            "ear": float(ear),
            "blink_count": int(blink_count),
            "closure_duration": float(closure_duration),

            "phone_detected": bool(phone_detected),
            "distraction_duration": float(distraction_duration),

            "risk_score": float(risk_score),
            "risk_level": str(risk_level),
            "system_status": str(system_status),

            "sos_active": bool(
    risk_score >= 80 or
    non_responsive or
    closure_duration >= 3 or
    distraction_duration >= 5
),
     if telemetry_data["sos_active"] and not emergency_sent:

      print("CRITICAL DRIVER STATE DETECTED")

    send_emergency_signal()

    emergency_sent = True
            if emergency_state == "NORMAL":
            emergency_sent = FALSE

           

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




