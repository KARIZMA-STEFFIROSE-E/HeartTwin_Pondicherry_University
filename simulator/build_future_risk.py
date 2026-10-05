import pandas as pd

input_file = "data/risk_trajectory.csv"
output_file = "data/future_risk.csv"

df = pd.read_csv(input_file)

def calculate_future_risk(row):
    score = row["twin_risk_score"]

    # Current Twin state
    if row["risk_category"] == "Elevated":
        score += 15
    elif row["risk_category"] == "Moderate":
        score += 8

    # Risk trajectory
    if row["risk_trajectory"] == "Worsening":
        score += 20
    elif row["risk_trajectory"] == "Improving":
        score -= 5

    # Limit to 0–100
    score = max(0, min(100, score))

    return score


df["future_risk_score"] = df.apply(calculate_future_risk, axis=1)

def future_risk_category(score):
    if score < 20:
        return "Low"
    elif score < 40:
        return "Moderate"
    elif score < 60:
        return "Elevated"
    else:
        return "High"

df["future_risk_category"] = df["future_risk_score"].apply(
    future_risk_category
)

df.to_csv(output_file, index=False)

print("Future-risk layer created successfully.")
print(f"Rows: {len(df)}")

print("\nFuture-risk categories:")
print(df["future_risk_category"].value_counts())

print("\nAverage future-risk score by actual deterioration:")
print(
    df.groupby("deterioration")["future_risk_score"]
      .agg(["count", "mean", "min", "max"])
      .round(2)
)

print("\nHighest future-risk records:")

print(
    df[
        [
            "patient_id",
            "date",
            "twin_risk_score",
            "risk_category",
            "risk_trajectory",
            "future_risk_score",
            "future_risk_category",
            "deterioration"
        ]
    ]
    .sort_values("future_risk_score", ascending=False)
    .head(15)
    .to_string(index=False)
)