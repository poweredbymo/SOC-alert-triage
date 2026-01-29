from fastapi import FastAPI
import joblib
import json
import pandas as pd
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title='SOC Alert Triage API')

MODEL = joblib.load("models/alert_classifier.pkl")
with open("models/features.json", "r") as f:
    MODEL_FEATURES = json.load(f)

 # Define output format
class AlertInput(BaseModel):
    features: Dict[str, float]

@app.get("/")
def root():
    return {"message": "SOC Alert Triage API is live"}

@app.post("/predict")
def predict_alert(alert: AlertInput):
    df = pd.DataFrame([alert.features])

    df = df.reindex(columns=MODEL_FEATURES, fill_value=0)

    prediction = int(MODEL.predict(df)[0])
    probabilities = MODEL.predict_proba(df)[0].tolist()

    labels = {0:'FalsePositive', 1: 'BenignPositive', 2: 'TruePositive'}

    return {
        'prediction' : labels[prediction],
        'confidence' : round(max(probabilities), 2),
        'details' : {labels[i]: round(probabilities[i], 2) for i in range(3)}
    }   