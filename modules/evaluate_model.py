import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# Load dataset
data = pd.read_csv("driver_behavior_log.csv")

# Load trained model
model = joblib.load("driver_risk_model.pkl")


# Features
X = data[[
    "ear",
    "blink_count",
    "eye_closure_duration",
    "phone_detected",
    "distraction_duration"
]]


# True labels (same logic used during training)
y_true = []

for index, row in data.iterrows():

    risk = 0

    if row["eye_closure_duration"] > 1.5:
        risk = 1

    if row["distraction_duration"] > 2.0:
        risk = 1

    if row["ear"] < 0.20:
        risk = 1

    y_true.append(risk)


# Predictions
y_pred = model.predict(X)


# Calculate metrics
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)


# Print results
print("\nMODEL PERFORMANCE RESULTS")
print("--------------------------")

print(f"Accuracy: {accuracy*100:.2f}%")
print(f"Precision: {precision*100:.2f}%")
print(f"Recall: {recall*100:.2f}%")
print(f"F1 Score: {f1*100:.2f}%")
