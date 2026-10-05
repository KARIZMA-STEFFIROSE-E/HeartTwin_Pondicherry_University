import pandas as pd

input_file = "data/features_dataset.csv"
output_file = "data/personal_deviation.csv"

df = pd.read_csv(input_file)

df["date"] = pd.to_datetime(df["date"])

# Percentage deviation from each patient's own baseline
df["hr_change_pct"] = df["hr_percent_change"]
df["hrv_change_pct"] = df["hrv_percent_change"]
df["sleep_change_pct"] = df["sleep_percent_change"]
df["steps_change_pct"] = df["steps_percent_change"]
df["spo2_change_pct"] = df["spo2_percent_change"]
df["weight_change_pct"] = df["weight_percent_change"]

# Select useful personalized fields
deviation = df[
    [
        "patient_id",
        "date",

        "resting_hr",
        "resting_hr_baseline",
        "hr_change_pct",

        "hrv",
        "hrv_baseline",
        "hrv_change_pct",

        "sleep_hours",
        "sleep_hours_baseline",
        "sleep_change_pct",

        "steps",
        "steps_baseline",
        "steps_change_pct",

        "spo2",
        "spo2_baseline",
        "spo2_change_pct",

        "weight_kg",
        "weight_kg_baseline",
        "weight_change_pct",

        "deterioration"
    ]
].copy()

deviation.to_csv(output_file, index=False)

print("Personal deviation dataset created.")
print(f"Rows: {len(deviation)}")
print(f"Columns: {len(deviation.columns)}")
print(f"Output: {output_file}")

# Latest record for every patient
latest = (
    deviation.sort_values(["patient_id", "date"])
             .groupby("patient_id")
             .tail(1)
)

print("\nLatest personalized deviations:")

print(
    latest[
        [
            "patient_id",
            "date",
            "hr_change_pct",
            "hrv_change_pct",
            "sleep_change_pct",
            "steps_change_pct",
            "spo2_change_pct",
            "weight_change_pct"
        ]
    ]
    .round(2)
    .to_string(index=False)
)