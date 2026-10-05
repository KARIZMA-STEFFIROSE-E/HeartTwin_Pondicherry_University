
import pandas as pd

# Load final digital twin state
df = pd.read_csv("data/final_twin_state.csv")

print("=" * 60)
print("HEARTTWIN VALIDATION - FALSE ALARM CHECK")
print("=" * 60)

# Define elevated-or-higher as a review-level signal
high_risk = df["risk_category"].isin(
    ["Elevated", "High"]
)

# Non-deteriorating patients
normal_group = df[df["deterioration"] == 0]

# Deteriorating patients
deterioration_group = df[df["deterioration"] == 1]

# False alarms
false_alarms = normal_group[high_risk.loc[normal_group.index]]

# True review signals
true_signals = deterioration_group[
    high_risk.loc[deterioration_group.index]
]

print("\nNon-deteriorating patients:")
print(len(normal_group))

print("\nNon-deteriorating patients flagged Elevated/High:")
print(len(false_alarms))

if len(false_alarms) > 0:
    print("\nFalse-alarm patients:")
    print(
        false_alarms[
            ["patient_id", "twin_risk_score", "risk_category"]
        ].to_string(index=False)
    )
else:
    print("\nNo Elevated/High false alarms detected.")

print("\nDeteriorating patients:")
print(len(deterioration_group))

print("\nDeteriorating patients flagged Elevated/High:")
print(len(true_signals))

if len(true_signals) > 0:
    print("\nCorrectly flagged patients:")
    print(
        true_signals[
            ["patient_id", "twin_risk_score", "risk_category"]
        ].to_string(index=False)
    )

# Calculate rates
false_alarm_rate = (
    len(false_alarms) / len(normal_group) * 100
)

detection_rate = (
    len(true_signals) / len(deterioration_group) * 100
)

print(f"\nFalse alarm rate: {false_alarm_rate:.1f}%")
print(f"Deterioration detection rate: {detection_rate:.1f}%")

print("\nValidation check completed successfully.")
