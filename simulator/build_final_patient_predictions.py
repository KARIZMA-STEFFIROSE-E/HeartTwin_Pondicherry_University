import pandas as pd

input_file = "data/future_risk.csv"
output_file = "data/final_patient_predictions.csv"

df = pd.read_csv(input_file)

df["date"] = pd.to_datetime(df["date"])

# Latest available state for every patient
latest = (
    df.sort_values(["patient_id", "date"])
      .groupby("patient_id")
      .tail(1)
      .copy()
)

# Clean missing risk reasons
latest["risk_reasons"] = latest["risk_reasons"].fillna(
    "No significant deviations detected"
)

# Create a dashboard-friendly table
final = latest[
    [
        "patient_id",
        "date",
        "age",
        "sex",
        "bmi",
        "hypertension",
        "diabetes",
        "smoking",
        "previous_cardiac_event",
        "cholesterol",

        "resting_hr",
        "hrv",
        "sleep_hours",
        "steps",
        "spo2",
        "weight_kg",

        "twin_risk_score",
        "risk_category",
        "risk_trajectory",
        "risk_reasons",

        "future_risk_score",
        "future_risk_category"
    ]
].copy()

final.to_csv(output_file, index=False)

print("Final patient prediction table created.")
print(f"Patients: {len(final)}")
print(f"Columns: {len(final.columns)}")
print(f"Output: {output_file}")

print("\nCurrent Patient Risk:")
print(
    final[
        [
            "patient_id",
            "twin_risk_score",
            "risk_category",
            "risk_trajectory",
            "future_risk_score",
            "future_risk_category"
        ]
    ]
    .sort_values("future_risk_score", ascending=False)
    .to_string(index=False)
)