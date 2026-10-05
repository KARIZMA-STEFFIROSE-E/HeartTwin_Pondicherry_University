import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report
)

train_file = "data/train_dataset.csv"
test_file = "data/test_dataset.csv"

train = pd.read_csv(train_file)
test = pd.read_csv(test_file)

features = [
    "resting_hr",
    "hrv",
    "sleep_hours",
    "steps",
    "spo2",
    "weight_kg",

    "age",
    "bmi",
    "hypertension",
    "diabetes",
    "smoking",
    "previous_cardiac_event",
    "cholesterol",

    "hr_7d_avg",
    "hrv_7d_avg",
    "sleep_7d_avg",
    "steps_7d_avg",
    "spo2_7d_avg",
    "weight_7d_avg",

    "hr_deviation",
    "hrv_deviation",
    "sleep_deviation",
    "steps_deviation",
    "spo2_deviation",
    "weight_deviation",

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
    (
        "classifier",
        LogisticRegression(
            class_weight="balanced",
            max_iter=2000,
            random_state=42
        )
    )
])

model.fit(X_train, y_train)

probabilities = model.predict_proba(X_test)[:, 1]
predictions = (probabilities >= 0.5).astype(int)

roc_auc = roc_auc_score(y_test, probabilities)
pr_auc = average_precision_score(y_test, probabilities)

print("HeartTwin Prediction Model Evaluation")
print("======================================")

print(f"\nROC-AUC: {roc_auc:.3f}")
print(f"PR-AUC:  {pr_auc:.3f}")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

print("\nActual positive cases:")
print(y_test.sum())

print("Predicted positive cases:")
print(predictions.sum())