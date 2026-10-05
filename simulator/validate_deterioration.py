
import pandas as pd

# Load final digital twin state
df = pd.read_csv("data/final_twin_state.csv")

print("=" * 60)
print("HEARTTWIN VALIDATION - DETERIORATION CHECK")
print("=" * 60)

# Convert deterioration column to a clean boolean
df["deterioration_flag"] = df["deterioration"].astype(str).str.lower()

# Group by deterioration status
summary = (
    df.groupby("deterioration_flag")["twin_risk_score"]
    .agg(
        patient_count="count",
        mean_risk="mean",
        min_risk="min",
        max_risk="max"
    )
    .reset_index()
)

print("\nRisk by Deterioration Status:")
print(summary.to_string(index=False))

# Show individual patients
print("\nIndividual Patient Results:")

patient_summary = df[
    [
        "patient_id",
        "twin_risk_score",
        "risk_category",
        "risk_trajectory",
        "deterioration"
    ]
].copy()

print(patient_summary.to_string(index=False))

print("\nValidation check completed successfully.")

