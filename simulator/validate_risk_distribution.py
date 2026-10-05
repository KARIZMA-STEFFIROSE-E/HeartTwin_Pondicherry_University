
import pandas as pd

# Load final digital twin state
df = pd.read_csv("data/final_twin_state.csv")

print("=" * 60)
print("HEARTTWIN VALIDATION - RISK DISTRIBUTION")
print("=" * 60)

# Risk category distribution
print("\nRisk Category Distribution:")
print(
    df["risk_category"]
    .value_counts()
    .sort_index()
)

# Risk score statistics
print("\nRisk Score Statistics:")
print(
    df["twin_risk_score"]
    .describe()
)

# Trajectory distribution
print("\nRisk Trajectory Distribution:")
print(
    df["risk_trajectory"]
    .value_counts()
)

print("\nValidation check completed successfully.")
