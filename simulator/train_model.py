import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

train = pd.read_csv("data/train_dataset.csv")
test = pd.read_csv("data/test_dataset.csv")

features = [
    # Current wearable state
    "resting_hr",
    "hrv",
    "sleep_hours",
    "steps",
    "spo2",
    "weight_kg",

    # Historical/EHR information
    "age",
    "bmi",
    "hypertension",
    "diabetes",
    "smoking",
    "previous_cardiac_event",
    "cholesterol",

    # 7-day trends
    "hr_7d_avg",
    "hrv_7d_avg",
    "sleep_7d_avg",
    "steps_7d_avg",
    "spo2_7d_avg",
    "weight_7d_avg",

    # Personalized Digital Twin deviations
    "hr_deviation",
    "hrv_deviation",
    "sleep_deviation",
    "steps_deviation",
    "spo2_deviation",
    "weight_deviation",

    # Personalized percentage changes
    "hr_percent_change",
    "hrv_percent_change",
    "sleep_percent_change",
    "steps_percent_change",
    "spo2_percent_change",
    "weight_percent_change"
]

X_train = train[features]
y_train = train["future_deterioration"]

X_test = test[features]
y_test = test["future_deterioration"]

model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(
        class_weight="balanced",
        max_iter=2000,
        random_state=42
    ))
])

model.fit(X_train, y_train)

print("Personalized Logistic Regression trained successfully!")
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))
print("Features used:", len(features))

predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

print("\nProbability range:")
print("Minimum:", round(probabilities.min(), 3))
print("Maximum:", round(probabilities.max(), 3))

accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, zero_division=0)
recall = recall_score(y_test, predictions, zero_division=0)
f1 = f1_score(y_test, predictions, zero_division=0)

print("\nModel Evaluation:")
print("Accuracy :", round(accuracy, 3))
print("Precision:", round(precision, 3))
print("Recall   :", round(recall, 3))
print("F1 Score :", round(f1, 3))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))