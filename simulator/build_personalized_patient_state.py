import pandas as pd

state_file = "data/patient_state.csv"
explanation_file = "data/personal_explanations.csv"
trend_file = "data/personal_trend_summary.csv"

output_file = "data/personalized_patient_state.csv"

# Load files
state = pd.read_csv(state_file)

explanations = pd.read_csv(explanation_file)
explanations["date"] = pd.to_datetime(explanations["date"])

trends = pd.read_csv(trend_file)

# Get latest personalized explanation for each patient
latest_explanations = (
    explanations
    .sort_values(["patient_id", "date"])
    .groupby("patient_id")
    .tail(1)
)

latest_explanations = latest_explanations[
    ["patient_id", "personalized_explanation"]
]

# Select trend information
trend_columns = [
    "patient_id",
    "abnormal_days",
    "total_abnormal_signals",
    "dominant_signals",
    "personalization_status"
]

trends = trends[trend_columns]

# Merge patient state + explanations + trends
final_state = state.merge(
    latest_explanations,
    on="patient_id",
    how="left"
)

final_state = final_state.merge(
    trends,
    on="patient_id",
    how="left"
)

# Personalized interpretation
def interpret(row):

    if row["personalization_status"] == "Persistent deviation":
        return "Persistent deviation from personal baseline"

    elif row["personalization_status"] == "Emerging deviation":
        return "Emerging deviation from personal baseline"

    else:
        return "Stable relative to personal baseline"


final_state["personalized_status"] = final_state.apply(
    interpret,
    axis=1
)

# Save final personalized state
final_state.to_csv(output_file, index=False)

print("Personalized patient state created.")
print(f"Rows: {len(final_state)}")
print(f"Output: {output_file}")

print("\nAvailable columns:")
print(final_state.columns.tolist())

print("\nFinal personalized patient state:")
print(final_state.to_string(index=False))