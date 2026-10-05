import pandas as pd

input_file = "data/personalized_patient_state.csv"
output_file = "data/twin_intelligence.csv"

df = pd.read_csv(input_file)


def generate_intelligence(row):
    signals = []

    # Current risk
    if row["twin_risk_score"] >= 60:
        risk_text = "High current physiological risk signal"
    elif row["twin_risk_score"] >= 40:
        risk_text = "Elevated current physiological risk signal"
    elif row["twin_risk_score"] >= 20:
        risk_text = "Moderate current physiological risk signal"
    else:
        risk_text = "Low current physiological risk signal"

    # Personal deviations
    explanation = row["personalized_explanation"]

    if "Resting HR" in explanation:
        signals.append("Resting HR deviation")

    if "HRV" in explanation:
        signals.append("HRV deviation")

    if "Sleep" in explanation:
        signals.append("Sleep deviation")

    if "Activity" in explanation:
        signals.append("Activity deviation")

    if "SpO₂" in explanation:
        signals.append("SpO₂ deviation")

    if "Weight" in explanation:
        signals.append("Weight deviation")

    # Persistent pattern
    if row["personalization_status"] == "Persistent deviation":
        persistence_text = (
            "Multiple deviations persist relative to the patient's personal baseline"
        )

    elif row["personalization_status"] == "Emerging deviation":
        persistence_text = (
            "Emerging deviation from the patient's personal baseline"
        )

    else:
        persistence_text = (
            "No meaningful persistent deviation from the patient's personal baseline"
        )

    # Trajectory
    if row["risk_trajectory"] == "Worsening":
        trajectory_text = "Risk trajectory is worsening"

    elif row["risk_trajectory"] == "Improving":
        trajectory_text = "Risk trajectory is improving"

    else:
        trajectory_text = "Risk trajectory is currently stable"

    # Future risk
    if "future_risk_category" in row.index:

        if row["future_risk_category"] == "High":
            future_text = "Future risk signal is high"

        elif row["future_risk_category"] == "Elevated":
            future_text = "Future risk signal is elevated"

        elif row["future_risk_category"] == "Moderate":
            future_text = "Future risk signal is moderate"

        else:
            future_text = "Future risk signal is low"

    else:
        future_text = "Future risk signal available from trajectory model"

    # Overall interpretation
    if (
        row["twin_risk_score"] >= 40
        or row["risk_trajectory"] == "Worsening"
        or row["personalization_status"] == "Persistent deviation"
    ):
        overall = (
            "The digital twin detects a meaningful change from the patient's "
            "usual physiological pattern and recommends closer monitoring."
        )

    elif row["personalization_status"] == "Emerging deviation":
        overall = (
            "The digital twin detects emerging deviations from the patient's "
            "personal baseline that should be monitored over time."
        )

    else:
        overall = (
            "The digital twin currently detects a relatively stable physiological "
            "pattern compared with the patient's personal baseline."
        )

    return pd.Series({
        "current_risk_interpretation": risk_text,
        "key_contributing_signals": ", ".join(signals)
            if signals else "No major personalized deviations",
        "persistence_interpretation": persistence_text,
        "trajectory_interpretation": trajectory_text,
        "future_risk_interpretation": future_text,
        "overall_twin_interpretation": overall
    })


intelligence = df.apply(generate_intelligence, axis=1)

final = pd.concat([df, intelligence], axis=1)

final.to_csv(output_file, index=False)

print("Twin intelligence created.")
print(f"Rows: {len(final)}")
print(f"Output: {output_file}")

print("\nTwin intelligence summary:")

print(
    final[
        [
            "patient_id",
            "risk_category",
            "risk_trajectory",
            "personalization_status",
            "current_risk_interpretation",
            "key_contributing_signals",
            "overall_twin_interpretation"
        ]
    ].to_string(index=False)
)