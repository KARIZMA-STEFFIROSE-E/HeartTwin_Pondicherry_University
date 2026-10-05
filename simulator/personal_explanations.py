import pandas as pd

input_file = "data/personal_deviation.csv"
output_file = "data/personal_explanations.csv"

df = pd.read_csv(input_file)


def generate_explanation(row):
    reasons = []

    # Heart rate
    if row["hr_change_pct"] >= 10:
        reasons.append(
            f"Resting HR is {row['hr_change_pct']:.1f}% above personal baseline"
        )
    elif row["hr_change_pct"] <= -10:
        reasons.append(
            f"Resting HR is {abs(row['hr_change_pct']):.1f}% below personal baseline"
        )

    # HRV
    if row["hrv_change_pct"] <= -20:
        reasons.append(
            f"HRV is {abs(row['hrv_change_pct']):.1f}% below personal baseline"
        )
    elif row["hrv_change_pct"] >= 20:
        reasons.append(
            f"HRV is {row['hrv_change_pct']:.1f}% above personal baseline"
        )

    # Sleep
    if row["sleep_change_pct"] <= -15:
        reasons.append(
            f"Sleep is {abs(row['sleep_change_pct']):.1f}% below personal baseline"
        )

    # Activity
    if row["steps_change_pct"] <= -20:
        reasons.append(
            f"Activity is {abs(row['steps_change_pct']):.1f}% below personal baseline"
        )

    # SpO2
    if row["spo2_change_pct"] <= -1:
        reasons.append(
            f"SpO₂ is {abs(row['spo2_change_pct']):.1f}% below personal baseline"
        )

    # Weight
    if row["weight_change_pct"] >= 3:
        reasons.append(
            f"Weight is {row['weight_change_pct']:.1f}% above personal baseline"
        )

    if not reasons:
        return "No significant deviations from personal baseline detected"

    return "; ".join(reasons)


df["personalized_explanation"] = df.apply(
    generate_explanation,
    axis=1
)

df.to_csv(output_file, index=False)

print("Personalized explanations created.")
print(f"Rows: {len(df)}")
print(f"Output: {output_file}")

# Show latest explanation for each patient
latest = (
    df.sort_values(["patient_id", "date"])
      .groupby("patient_id")
      .tail(1)
)

print("\nLatest personalized explanations:")

print(
    latest[
        [
            "patient_id",
            "date",
            "personalized_explanation"
        ]
    ]
    .to_string(index=False)
)