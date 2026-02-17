import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
data = pd.read_csv("driver_behavior_log.csv")

# Select features
X = data[[
    "ear",
    "blink_count",
    "eye_closure_duration",
    "phone_detected",
    "distraction_duration"
]]

# Create labels (simple rule-based for initial training)
# 0 = SAFE, 1 = RISK

y = []

for index, row in data.iterrows():

    risk = 0

    if row["eye_closure_duration"] > 1.5:
        risk = 1

    if row["distraction_duration"] > 2.0:
        risk = 1

    if row["ear"] < 0.20:
        risk = 1

    y.append(risk)

# Train model
model = RandomForestClassifier(n_estimators=100)

model.fit(X, y)

# Save model
joblib.dump(model, "driver_risk_model.pkl")

print("Model trained and saved as driver_risk_model.pkl")
