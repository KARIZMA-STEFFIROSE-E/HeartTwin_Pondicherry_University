import pandas as pd

ehr_file = "data/ehr_patient_profiles.csv"
wearable_file = "data/wearable/wearable_labeled.csv"

ehr = pd.read_csv(ehr_file)
wearable = pd.read_csv(wearable_file)

merged = wearable.merge(
    ehr,
    on="patient_id",
    how="left"
)

output_file = "data/merged_dataset.csv"

merged.to_csv(output_file, index=False)

print("Merged dataset created!")
print("Rows:", len(merged))
print("Columns:", len(merged.columns))
print(output_file)