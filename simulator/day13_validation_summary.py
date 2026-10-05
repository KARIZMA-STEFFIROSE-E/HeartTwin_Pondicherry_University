import pandas as pd

# Load validation datasets
twin_df = pd.read_csv("data/final_twin_state.csv")
what_if_df = pd.read_csv("data/what_if_simulation.csv")

print("=" * 60)
print("HEARTTWIN - DAY 13 VALIDATION SUMMARY")
print("=" * 60)

# 1. Risk distribution
print("\n1. RISK DISTRIBUTION")

risk_counts = twin_df["risk_category"].value_counts()

for category in ["Low", "Moderate", "Elevated", "High"]:
    print(f"{category}: {risk_counts.get(category, 0)}")

# 2. Deterioration comparison
print("\n2. DETERIORATION VALIDATION")

deterioration_mean = twin_df[
    twin_df["deterioration"] == 1
]["twin_risk_score"].mean()

normal_mean = twin_df[
    twin_df["deterioration"] == 0
]["twin_risk_score"].mean()

print(f"Non-deterioration mean risk: {normal_mean:.1f}")
print(f"Deterioration mean risk: {deterioration_mean:.1f}")

# 3. Elevated/High detection
print("\n3. REVIEW-LEVEL SIGNAL VALIDATION")

normal_group = twin_df[twin_df["deterioration"] == 0]
deterioration_group = twin_df[twin_df["deterioration"] == 1]

normal_flagged = normal_group[
    normal_group["risk_category"].isin(["Elevated", "High"])
]

deterioration_flagged = deterioration_group[
    deterioration_group["risk_category"].isin(["Elevated", "High"])
]

print(
    f"Non-deteriorating patients flagged Elevated/High: "
    f"{len(normal_flagged)}/{len(normal_group)}"
)

print(
    f"Deteriorating patients flagged Elevated/High: "
    f"{len(deterioration_flagged)}/{len(deterioration_group)}"
)

# 4. What-if validation
print("\n4. WHAT-IF VALIDATION")

what_if_df["risk_difference"] = (
    what_if_df["simulated_risk_score"]
    - what_if_df["current_risk_score"]
)

increased = (
    what_if_df["risk_difference"] > 0
).sum()

decreased = (
    what_if_df["risk_difference"] < 0
).sum()

unchanged = (
    what_if_df["risk_difference"] == 0
).sum()

print(f"Risk increased: {increased}")
print(f"Risk unchanged: {unchanged}")
print(f"Risk decreased: {decreased}")

if decreased == 0:
    print("PASS: Activity reduction never decreased risk.")
else:
    print("WARNING: Some simulated risks decreased.")

# Final status
print("\n5. OVERALL VALIDATION STATUS")

if deterioration_mean > normal_mean and decreased == 0:
    print("PASS: HeartTwin validation checks completed successfully.")
else:
    print("REVIEW: Some validation checks require investigation.")

print("\nDay 13 validation completed.")