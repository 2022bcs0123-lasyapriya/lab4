from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

model = joblib.load("model/model.pkl")

FEATURE_ORDER = [
    "fixed acidity", "volatile acidity", "citric acid",
    "residual sugar", "chlorides", "free sulfur dioxide",
    "total sulfur dioxide", "density", "pH",
    "sulphates", "alcohol"
]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: dict):
    try:
        features = [data[f] for f in FEATURE_ORDER]
        features = np.array(features).reshape(1, -1)
        prediction = model.predict(features)[0]

        return {
            "name": "Bagadi Lasya Priya",
            "roll_no": "2022BCS0123",
            "wine_quality": int(prediction)
        }
    except KeyError as e:
        return {"error": f"Missing feature: {str(e)}"}
