import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

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

print("HeartTwin Future-Risk Prediction Model")
print("======================================")

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")
print(f"Features used: {len(features)}")

print("\nPrediction probabilities:")
print(
    pd.DataFrame({
        "patient_id": test["patient_id"],
        "date": test["date"],
        "actual_future_deterioration": y_test,
        "future_risk_probability": probabilities.round(3)
    })
    .sort_values("future_risk_probability", ascending=False)
    .head(15)
    .to_string(index=False)
)

print("\nProbability range:")
print(f"Minimum: {probabilities.min():.3f}")
print(f"Maximum: {probabilities.max():.3f}")
print(f"Mean: {probabilities.mean():.3f}")