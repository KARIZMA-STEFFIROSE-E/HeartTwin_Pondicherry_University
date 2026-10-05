import pandas as pd

input_file = "data/risk_trajectory.csv"
output_file = "data/patient_state.csv"

df = pd.read_csv(input_file)

df["date"] = pd.to_datetime(df["date"])

# Get the latest record for every patient
latest = (
    df.sort_values(["patient_id", "date"])
      .groupby("patient_id")
      .tail(1)
      .copy()
)

# Select the most useful dashboard fields
state = latest[
    [
        "patient_id",
        "date",
        "age",
        "sex",
        "bmi",
        "hypertension",
        "diabetes",
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
        "deterioration"
    ]
].copy()

state.to_csv(output_file, index=False)

print("Patient state created successfully.")
print(f"Patients: {len(state)}")
print(f"Output: {output_file}")

print("\nLatest Twin State:")
print(
    state[
        [
            "patient_id",
            "date",
            "twin_risk_score",
            "risk_category",
            "risk_trajectory",
            "risk_reasons"
        ]
    ].to_string(index=False)
)