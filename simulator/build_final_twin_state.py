import pandas as pd

patient_file = "data/personalized_patient_state.csv"
intelligence_file = "data/twin_intelligence_summary.csv"
prediction_file = "data/final_patient_predictions.csv"

output_file = "data/final_twin_state.csv"

# Load files
patient = pd.read_csv(patient_file)
intelligence = pd.read_csv(intelligence_file)
prediction = pd.read_csv(prediction_file)

# --------------------------------------------------
# 1. Get future-risk information
# --------------------------------------------------

prediction_columns = [
    "patient_id",
    "future_risk_score",
    "future_risk_category"
]

prediction = prediction[prediction_columns]

# --------------------------------------------------
# 2. Get intelligence information
# --------------------------------------------------

intelligence_columns = [
    "patient_id",
    "current_risk_interpretation",
    "key_contributing_signals",
    "persistence_interpretation",
    "trajectory_interpretation",
    "future_risk_interpretation",
    "overall_twin_interpretation",
    "risk_interpretation",
    "key_signal_summary",
    "doctor_facing_summary"
]

intelligence = intelligence[intelligence_columns]

# --------------------------------------------------
# 3. Merge everything
# --------------------------------------------------

final = patient.merge(
    prediction,
    on="patient_id",
    how="left"
)

final = final.merge(
    intelligence,
    on="patient_id",
    how="left"
)

# --------------------------------------------------
# 4. Save final Twin state
# --------------------------------------------------

final.to_csv(
    output_file,
    index=False
)

print("Final Twin state created.")
print(f"Patients: {len(final)}")
print(f"Columns: {len(final.columns)}")
print(f"Output: {output_file}")

# --------------------------------------------------
# 5. Display important dashboard fields
# --------------------------------------------------

display_columns = [
    "patient_id",
    "twin_risk_score",
    "risk_category",
    "future_risk_score",
    "future_risk_category",
    "risk_trajectory",
    "personalization_status",
    "key_signal_summary",
    "risk_interpretation",
    "doctor_facing_summary"
]

print("\nFinal Twin state:")
print(
    final[display_columns]
    .to_string(index=False)
)