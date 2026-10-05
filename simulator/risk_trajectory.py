import pandas as pd

input_file = "data/twin_state_dataset.csv"
output_file = "data/risk_trajectory.csv"

df = pd.read_csv(input_file)

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values(
    ["patient_id", "date"]
).copy()


# ---------------------------------------------------------
# Previous risk states
# ---------------------------------------------------------

df["risk_1d_ago"] = (
    df.groupby("patient_id")["twin_risk_score"]
      .shift(1)
)

df["risk_2d_ago"] = (
    df.groupby("patient_id")["twin_risk_score"]
      .shift(2)
)


# ---------------------------------------------------------
# 3-day risk trend
# ---------------------------------------------------------

df["risk_3d_avg"] = (
    df.groupby("patient_id")["twin_risk_score"]
      .transform(
          lambda x: x.rolling(
              window=3,
              min_periods=1
          ).mean()
      )
)


# ---------------------------------------------------------
# Risk change
# ---------------------------------------------------------

df["risk_change_3d"] = (
    df["twin_risk_score"] -
    df["risk_3d_avg"]
)


# ---------------------------------------------------------
# Risk trajectory
# ---------------------------------------------------------

def trajectory(row):

    if pd.isna(row["risk_2d_ago"]):
        return "Insufficient history"

    if (
        row["twin_risk_score"] >
        row["risk_1d_ago"] >
        row["risk_2d_ago"]
    ):
        return "Worsening"

    elif (
        row["twin_risk_score"] <
        row["risk_1d_ago"] <
        row["risk_2d_ago"]
    ):
        return "Improving"

    else:
        return "Stable"


df["risk_trajectory"] = df.apply(
    trajectory,
    axis=1
)


# ---------------------------------------------------------
# Save
# ---------------------------------------------------------

df.to_csv(
    output_file,
    index=False
)

print("Risk trajectory engine completed!")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nTrajectory distribution:")
print(
    df["risk_trajectory"].value_counts()
)

print("\nOutput:")
print(output_file)