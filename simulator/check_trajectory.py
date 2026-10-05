import pandas as pd

input_file = "data/risk_trajectory.csv"

df = pd.read_csv(input_file)

print("HeartTwin Trajectory Analysis")
print("============================")

print("\nTrajectory by actual deterioration state:")

trajectory_table = pd.crosstab(
    df["deterioration"],
    df["risk_trajectory"]
)

print(trajectory_table)


print("\nAverage risk by trajectory:")

print(
    df.groupby("risk_trajectory")["twin_risk_score"]
      .agg(["count", "mean", "min", "max"])
      .round(2)
)


print("\nWorsening trajectory records:")

worsening = df[
    df["risk_trajectory"] == "Worsening"
].sort_values(
    ["patient_id", "date"]
)

print(
    worsening[
        [
            "patient_id",
            "date",
            "twin_risk_score",
            "risk_category",
            "deterioration",
            "risk_trajectory",
            "risk_reasons"
        ]
    ].to_string(index=False)
)