import pandas as pd

risk_file = "data/risk_interpretation.csv"
signals_file = "data/top_contributing_signals.csv"

output_file = "data/twin_intelligence_summary.csv"

# Load data
risk = pd.read_csv(risk_file)
signals = pd.read_csv(signals_file)

# Select signal columns
signal_columns = [
    "patient_id",
    "top_signal_1",
    "top_signal_2",
    "top_signal_3"
]

signals = signals[signal_columns]

# Merge
df = risk.merge(
    signals,
    on="patient_id",
    how="left"
)


# Create clean signal summary
def clean_signal_summary(row):

    signals = []

    for column in [
        "top_signal_1",
        "top_signal_2",
        "top_signal_3"
    ]:

        value = row[column]

        if pd.notna(value) and value != "None":
            signals.append(value)

    if not signals:
        return "No major personalized deviations detected"

    return "; ".join(signals)


df["key_signal_summary"] = df.apply(
    clean_signal_summary,
    axis=1
)


# Create doctor-facing summary
def create_doctor_summary(row):

    risk = row["risk_category"]
    future = row["future_risk_category"]
    trajectory = row["risk_trajectory"]

    if risk == "Elevated" or future == "High":

        opening = (
            f"{risk} current risk signal with "
            f"{future} near-term risk signal."
        )

    elif future == "Elevated":

        opening = (
            f"{risk} current risk signal with "
            f"elevated near-term risk signal."
        )

    else:

        opening = (
            f"{risk} current risk signal with "
            f"{future} near-term risk signal."
        )

    return (
        opening
        + " "
        + f"Risk trajectory is {trajectory.lower()}. "
        + f"Key personalized signals: {row['key_signal_summary']}. "
        + f"{row['personalization_status']}."
    )


df["doctor_facing_summary"] = df.apply(
    create_doctor_summary,
    axis=1
)


# Save
df.to_csv(
    output_file,
    index=False
)

print("Twin intelligence summary created.")
print(f"Rows: {len(df)}")
print(f"Output: {output_file}")

print("\nDoctor-facing Twin summaries:")

print(
    df[
        [
            "patient_id",
            "risk_category",
            "future_risk_category",
            "risk_trajectory",
            "key_signal_summary",
            "doctor_facing_summary"
        ]
    ].to_string(index=False)
)