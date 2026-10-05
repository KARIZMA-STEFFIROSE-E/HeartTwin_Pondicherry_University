import pandas as pd

input_file = "data/merged_dataset.csv"
output_file = "data/features_dataset.csv"

df = pd.read_csv(input_file)

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(["patient_id", "date"])


# ============================================================
# 1. Rolling 7-day averages
# ============================================================

for column, feature_name in [
    ("resting_hr", "hr_7d_avg"),
    ("hrv", "hrv_7d_avg"),
    ("sleep_hours", "sleep_7d_avg"),
    ("steps", "steps_7d_avg"),
    ("spo2", "spo2_7d_avg"),
    ("weight_kg", "weight_7d_avg")
]:
    df[feature_name] = (
        df.groupby("patient_id")[column]
        .transform(lambda x: x.rolling(7, min_periods=1).mean())
    )


# ============================================================
# 2. Patient-specific baseline
# ============================================================

baseline_columns = [
    "resting_hr",
    "hrv",
    "sleep_hours",
    "steps",
    "spo2",
    "weight_kg"
]

for column in baseline_columns:

    baseline_name = column + "_baseline"

    df[baseline_name] = (
        df.groupby("patient_id")[column]
        .transform("mean")
    )


# ============================================================
# 3. Deviation from personal baseline
# ============================================================

df["hr_deviation"] = (
    df["resting_hr"] - df["resting_hr_baseline"]
)

df["hrv_deviation"] = (
    df["hrv"] - df["hrv_baseline"]
)

df["sleep_deviation"] = (
    df["sleep_hours"] - df["sleep_hours_baseline"]
)

df["steps_deviation"] = (
    df["steps"] - df["steps_baseline"]
)

df["spo2_deviation"] = (
    df["spo2"] - df["spo2_baseline"]
)

df["weight_deviation"] = (
    df["weight_kg"] - df["weight_kg_baseline"]
)


# ============================================================
# 4. Percentage deviation
# ============================================================

df["hr_percent_change"] = (
    df["hr_deviation"] / df["resting_hr_baseline"] * 100
)

df["hrv_percent_change"] = (
    df["hrv_deviation"] / df["hrv_baseline"] * 100
)

df["sleep_percent_change"] = (
    df["sleep_deviation"] / df["sleep_hours_baseline"] * 100
)

df["steps_percent_change"] = (
    df["steps_deviation"] / df["steps_baseline"] * 100
)

df["spo2_percent_change"] = (
    df["spo2_deviation"] / df["spo2_baseline"] * 100
)

df["weight_percent_change"] = (
    df["weight_deviation"] / df["weight_kg_baseline"] * 100
)


# ============================================================
# Save
# ============================================================

df.to_csv(output_file, index=False)

print("Personalized feature dataset created!")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nNew personalized features:")
print([
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
])

print("\nOutput:")
print(output_file)