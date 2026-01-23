from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

# Load trained model
model = joblib.load("model/model.pkl")

# Wine dataset has 13 features — fixed order
FEATURE_ORDER = [
    "alcohol",
    "malic_acid",
    "ash",
    "alcalinity_of_ash",
    "magnesium",
    "total_phenols",
    "flavanoids",
    "nonflavanoid_phenols",
    "proanthocyanins",
    "color_intensity",
    "hue",
    "od280/od315_of_diluted_wines",
    "proline"
]

@app.post("/predict")
def predict(data: dict):
    try:
        # Convert input dict to ordered feature list
        features = [data[f] for f in FEATURE_ORDER]
        features = np.array(features).reshape(1, -1)

        prediction = model.predict(features)[0]

        return {
            "name": "Bagadi Lasya Priya",
            "roll_no": "2022BCS0123",
            "wine_quality": int(prediction)
        }

    except KeyError as e:
        return {
            "error": f"Missing feature: {str(e)}"
        }
