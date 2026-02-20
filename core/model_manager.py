import joblib
import os

class ModelManager:

    def __init__(self, model_path):
        self.model_path = model_path
        self.model = joblib.load(model_path)
        self.model_last_modified = os.path.getmtime(model_path)
        print("MODEL EXPECTS FEATURES:", self.model.feature_names_in_)


    def check_reload(self):
        current_modified = os.path.getmtime(self.model_path)

        if current_modified != self.model_last_modified:
            print("New model detected. Reloading...")
            self.model = joblib.load(self.model_path)
            self.model_last_modified = current_modified
            print("Model updated successfully.")

    def predict_proba(self, features):
        return self.model.predict_proba(features)
