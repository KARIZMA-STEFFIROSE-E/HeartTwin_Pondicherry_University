import pandas as pd

input_file = "data/features_dataset.csv"
output_file = "data/model_dataset.csv"

df = pd.read_csv(input_file)

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(["patient_id", "date"])

# Look at the NEXT 3 days for each patient
df["future_deterioration"] = (
    df.groupby("patient_id")["deterioration"]
      .transform(
          lambda x: x.shift(-1)
                   .rolling(window=3, min_periods=3)
                   .max()
                   .shift(-2)
      )
)

# Remove rows where 3 future days are not available
df = df.dropna(subset=["future_deterioration"]).copy()

df["future_deterioration"] = df["future_deterioration"].astype(int)

df.to_csv(output_file, index=False)

print("Model dataset created!")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nTarget distribution:")
print(df["future_deterioration"].value_counts())

print("\nPositive patients:")
positive_patients = (
    df[df["future_deterioration"] == 1]["patient_id"]
    .unique()
)

print(positive_patients)

print("\nOutput:")
print(output_file)