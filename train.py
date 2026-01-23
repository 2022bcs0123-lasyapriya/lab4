# train.py - corrected version
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier  # or Regressor
from sklearn.metrics import f1_score, accuracy_score

# Option 1: use local file
df = pd.read_csv("winequality-red.csv", sep=";")   # or winequality-white.csv
# or Option 2: download from UCI
# url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
# df = pd.read_csv(url, sep=";")

X = df.drop("quality", axis=1)
y = df["quality"]

# Optional: make it binary classification (common in tutorials)
# y = (y >= 6).astype(int)   # good vs bad

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
# or print("F1:", f1_score(y_test, y_pred, average="weighted"))

joblib.dump(model, "model/model.pkl")
