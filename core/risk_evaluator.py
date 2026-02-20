import numpy as np


class RiskEvaluator:

    def __init__(self, model_manager):
        self.model_manager = model_manager

    def evaluate(self, perception_data):

        # Extract features from perception_data
        ear = perception_data["ear"]
        blink_count = perception_data["blink_count"]
        closure_duration = perception_data["closure_duration"]
        phone_detected = perception_data["phone_detected"]
        distraction_duration = perception_data["distraction_duration"]

        # Create feature array
        features = np.array([[
            ear,
            blink_count,
            closure_duration,
            int(phone_detected),
            distraction_duration
        ]])

        # Predict probabilities
        probabilities = self.model_manager.predict_proba(features)[0]

        # Calculate risk score
        risk_score = probabilities[1] * 100

        # ALWAYS define risk_level
        if risk_score >= 70:
            risk_level = "HIGH"
            risk_color = (0, 0, 255)
            system_status = "HIGH RISK"

        elif risk_score >= 40:
            risk_level = "MEDIUM"
            risk_color = (0, 255, 255)
            system_status = "MEDIUM RISK"

        else:
            risk_level = "LOW"
            risk_color = (0, 255, 0)
            system_status = "SAFE"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_color": risk_color,
            "system_status": system_status
        }
