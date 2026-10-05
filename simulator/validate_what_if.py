
import pandas as pd

# Load what-if simulation results
df = pd.read_csv("data/what_if_simulation.csv")

print("=" * 60)
print("HEARTTWIN VALIDATION - WHAT-IF SIMULATION")
print("=" * 60)

# Check whether simulated risk increased, stayed the same,
# or decreased after a 30% activity reduction.

df["risk_difference"] = (
    df["simulated_risk_score"]
    - df["current_risk_score"]
)

# Count outcomes
increased = (df["risk_difference"] > 0).sum()
unchanged = (df["risk_difference"] == 0).sum()
decreased = (df["risk_difference"] < 0).sum()

print("\nScenario: 30% reduction in daily activity")

print(f"\nRisk increased: {increased} patients")
print(f"Risk unchanged: {unchanged} patients")
print(f"Risk decreased: {decreased} patients")

# Check for unexpected decreases
unexpected = df[df["risk_difference"] < 0]

if len(unexpected) == 0:
    print("\nPASS: No patient had a lower risk after activity reduction.")
else:
    print("\nWARNING: Some patients had lower simulated risk:")
    print(
        unexpected[
            [
                "patient_id",
                "current_risk_score",
                "simulated_risk_score"
            ]
        ].to_string(index=False)
    )

# Show all patient results
print("\nPatient-level results:")

print(
    df[
        [
            "patient_id",
            "current_risk_score",
            "simulated_risk_score",
            "risk_difference",
            "current_risk_category",
            "simulated_risk_category"
        ]
    ].to_string(index=False)
)

print("\nValidation check completed successfully.")
