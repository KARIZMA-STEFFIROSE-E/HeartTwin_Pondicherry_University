import pandas as pd

input_file = "data/features_dataset.csv"

df = pd.read_csv(input_file)

print("HeartTwin Personal Baseline Analysis")
print("===================================")

print("\nPatients:")

baseline = (
    df.groupby("patient_id")
      .agg(
          baseline_hr=("resting_hr_baseline", "first"),
          baseline_hrv=("hrv_baseline", "first"),
          baseline_sleep=("sleep_hours_baseline", "first"),
          baseline_steps=("steps_baseline", "first"),
          baseline_spo2=("spo2_baseline", "first"),
          baseline_weight=("weight_kg_baseline", "first")
      )
      .round(2)
)

print(baseline.to_string())

print("\nBaseline ranges:")

print(
    baseline.agg(["min", "max", "mean"])
    .round(2)
    .to_string()
)