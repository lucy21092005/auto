import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier


class ModelRetrainer:

    def retrain_model(self):

        print("Loading dataset...")

        data = pd.read_csv("training_dataset.csv")

        X = data[[
            "EAR",
            "BlinkCount",
            "ClosureDuration",
            "PhoneDetected",
            "DistractionDuration"
        ]]

        y = data["Label"]

        print("Training new model...")

        model = RandomForestClassifier(n_estimators=100)

        model.fit(X, y)

        joblib.dump(model, "driver_risk_model.pkl")

        print("Model retrained and saved successfully")
