import pandas as pd

input_file = "data/twin_state_dataset.csv"

df = pd.read_csv(input_file)

print("HeartTwin Risk Analysis")
print("========================")

print("\nOverall risk categories:")
print(df["risk_category"].value_counts())

print("\nAverage risk score:")
print(round(df["twin_risk_score"].mean(), 2))


# Compare normal vs deterioration periods
print("\nRisk score by actual deterioration state:")
print(
    df.groupby("deterioration")["twin_risk_score"]
      .agg(["count", "mean", "min", "max"])
)


print("\nRisk category by actual deterioration state:")
print(
    pd.crosstab(
        df["deterioration"],
        df["risk_category"]
    )
)


# Show highest-risk records
print("\nTop 10 highest-risk patient-days:")

top_risk = df.sort_values(
    "twin_risk_score",
    ascending=False
).head(10)

print(
    top_risk[
        [
            "patient_id",
            "date",
            "twin_risk_score",
            "risk_category",
            "deterioration",
            "risk_reasons"
        ]
    ].to_string(index=False)
)