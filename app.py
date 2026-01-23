from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

model = joblib.load("model/model.pkl")

@app.post("/predict")
def predict(data: dict):
    features = np.array(list(data.values())).reshape(1, -1)
    prediction = model.predict(features)[0]

    return {
        "name": "Bagadi Lasya Priya",
        "roll_no": "2022BCS0123",
        "wine_quality": int(prediction)
    }
