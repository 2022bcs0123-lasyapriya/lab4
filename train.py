# train.py - Lab 5 version

import os
import json
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

# Load dataset
df = pd.read_csv("winequality.csv", sep=";")

X = df.drop("quality", axis=1)
y = df["quality"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average="weighted")

# Ensure directories exist
os.makedirs("model", exist_ok=True)
os.makedirs("artifacts", exist_ok=True)

# Save model
joblib.dump(model, "model/model.pkl")

# Save metrics for Jenkins
metrics = {
    "accuracy": float(accuracy),
    "f1": float(f1)
}

os.makedirs("artifacts", exist_ok=True)
with open("artifacts/metrics.json", "w") as f:
    json.dump(metrics, f)

with open("metrics.json", "w") as f:
    json.dump(metrics, f)

# Lab requirement print
print("Name: Bagadi Lasya Priya")
print("Roll No: 2022BCS0123")
print("Accuracy:", accuracy)
