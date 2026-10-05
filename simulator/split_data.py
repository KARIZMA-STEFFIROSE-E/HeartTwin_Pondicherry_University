import pandas as pd
from sklearn.model_selection import train_test_split

input_file = "data/model_dataset.csv"

df = pd.read_csv(input_file)

# Determine whether each patient has a future deterioration event
patient_target = (
    df.groupby("patient_id")["future_deterioration"]
    .max()
    .reset_index()
)

print("Patient-level target:")
print(patient_target)

# Split patients, not individual rows
train_patients, test_patients = train_test_split(
    patient_target["patient_id"],
    test_size=0.4,
    random_state=42,
    stratify=patient_target["future_deterioration"]
)

train_df = df[df["patient_id"].isin(train_patients)].copy()
test_df = df[df["patient_id"].isin(test_patients)].copy()

train_df.to_csv("data/train_dataset.csv", index=False)
test_df.to_csv("data/test_dataset.csv", index=False)

print("\nTraining patients:")
print(sorted(train_patients.tolist()))

print("\nTesting patients:")
print(sorted(test_patients.tolist()))

print("\nTraining rows:", len(train_df))
print("Testing rows:", len(test_df))

print("\nTraining target distribution:")
print(train_df["future_deterioration"].value_counts())

print("\nTesting target distribution:")
print(test_df["future_deterioration"].value_counts())

print("\nSplit completed!")