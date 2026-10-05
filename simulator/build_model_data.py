import pandas as pd

train = pd.read_csv("data/train_dataset.csv")
test = pd.read_csv("data/test_dataset.csv")

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
    "weight_7d_avg"
]

X_train = train[features]
y_train = train["future_deterioration"]

X_test = test[features]
y_test = test["future_deterioration"]

print("X_train:", X_train.shape)
print("y_train:", y_train.shape)

print("X_test:", X_test.shape)
print("y_test:", y_test.shape)

print("\nFeatures used:")
print(features)

print("\nTraining target:")
print(y_train.value_counts())