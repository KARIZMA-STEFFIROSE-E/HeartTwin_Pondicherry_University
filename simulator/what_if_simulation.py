
import pandas as pd

# Load final digital twin state
twin_df = pd.read_csv("data/final_twin_state.csv")

# Load latest wearable features
features_df = pd.read_csv("data/features_dataset.csv")

# Get latest observation for each patient
latest_features = (
    features_df
    .sort_values("date")
    .groupby("patient_id")
    .tail(1)
)

# Keep only required columns and rename them
latest_features = latest_features[
    ["patient_id", "steps", "steps_baseline"]
].rename(
    columns={
        "steps": "latest_steps",
        "steps_baseline": "personal_baseline_steps"
    }
)

# Merge with final twin state
df = twin_df.merge(
    latest_features,
    on="patient_id",
    how="left"
)

# Simulate 30% reduction in activity
activity_drop = 0.30

results = []

for _, row in df.iterrows():

    current_steps = float(row["latest_steps"])
    baseline_steps = float(row["personal_baseline_steps"])
    current_risk = float(row["twin_risk_score"])

    # Simulated activity
    simulated_steps = current_steps * (1 - activity_drop)

    # Deviation from personal baseline
    if baseline_steps > 0:
        simulated_deviation = (
            (simulated_steps - baseline_steps)
            / baseline_steps
        ) * 100
    else:
        simulated_deviation = 0

    # Additional risk caused by simulated activity drop
    if simulated_deviation <= -30:
        additional_risk = 15
    elif simulated_deviation <= -15:
        additional_risk = 8
    else:
        additional_risk = 0

    # Simulated twin risk
    simulated_risk = min(
        100,
        current_risk + additional_risk
    )

    # Risk category
    if simulated_risk < 20:
        simulated_category = "Low"
    elif simulated_risk < 40:
        simulated_category = "Moderate"
    elif simulated_risk < 60:
        simulated_category = "Elevated"
    else:
        simulated_category = "High"

    results.append({
        "patient_id": row["patient_id"],
        "current_steps": round(current_steps, 2),
        "simulated_steps": round(simulated_steps, 2),
        "personal_baseline_steps": round(baseline_steps, 2),
        "simulated_deviation_percent": round(
            simulated_deviation, 2
        ),
        "current_risk_score": round(current_risk, 2),
        "simulated_risk_score": round(simulated_risk, 2),
        "current_risk_category": row["risk_category"],
        "simulated_risk_category": simulated_category,
        "risk_change": round(
            simulated_risk - current_risk,
            2
        )
    })

# Create output dataframe
result_df = pd.DataFrame(results)

# Save simulation results
result_df.to_csv(
    "data/what_if_simulation.csv",
    index=False
)

print("What-if simulation completed successfully.")
print("Scenario: 30% reduction in daily activity")
print()
print(result_df.to_string(index=False))

