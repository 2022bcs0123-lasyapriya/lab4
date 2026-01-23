import os
import json
import joblib
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

# Load dataset
data = load_wine()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
f1 = f1_score(y_test, y_pred, average="weighted")

# Save model
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/model.pkl")

# Save metrics
metrics = {
    "f1": round(float(f1), 4)
}

with open("metrics.json", "w") as f:
    json.dump(metrics, f)

print("Training completed successfully")
print("F1 Score:", metrics["f1"])
