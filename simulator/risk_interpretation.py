import pandas as pd

intelligence_file = "data/twin_intelligence.csv"
future_file = "data/final_patient_predictions.csv"

output_file = "data/risk_interpretation.csv"

# Load files
df = pd.read_csv(intelligence_file)
future = pd.read_csv(future_file)

# Get future-risk information
future_columns = [
    "patient_id",
    "future_risk_score",
    "future_risk_category"
]

future = future[future_columns]

# Merge future risk into intelligence data
df = df.merge(
    future,
    on="patient_id",
    how="left"
)


def interpret_risk(row):

    current = row["twin_risk_score"]
    trajectory = row["risk_trajectory"]
    future = row["future_risk_score"]

    # Highest priority: high future risk
    if future >= 60:
        interpretation = (
            "High near-term risk signal. Multiple indicators suggest "
            "that the patient's physiological state may deteriorate "
            "if the current pattern persists."
        )

    elif future >= 40:
        interpretation = (
            "Elevated near-term risk signal. The patient's current "
            "physiological pattern shows changes that warrant closer monitoring."
        )

    elif current >= 40:
        interpretation = (
            "Elevated current risk signal. Several physiological indicators "
            "are currently outside the patient's usual pattern."
        )

    elif trajectory == "Worsening":
        interpretation = (
            "Worsening trajectory detected. Recent physiological changes "
            "are moving away from the patient's usual baseline."
        )

    elif trajectory == "Improving":
        interpretation = (
            "Improving trajectory detected. Recent physiological changes "
            "are moving toward the patient's usual baseline."
        )

    else:
        interpretation = (
            "Current physiological state appears relatively stable "
            "compared with the patient's personal baseline."
        )

    return interpretation


df["risk_interpretation"] = df.apply(
    interpret_risk,
    axis=1
)

# Save
df.to_csv(output_file, index=False)

print("Risk interpretations created.")
print(f"Rows: {len(df)}")
print(f"Output: {output_file}")

print("\nRisk interpretation:")

print(
    df[
        [
            "patient_id",
            "twin_risk_score",
            "risk_category",
            "future_risk_score",
            "future_risk_category",
            "risk_trajectory",
            "risk_interpretation"
        ]
    ].to_string(index=False)
)