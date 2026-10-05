import pandas as pd

input_file = "data/model_dataset.csv"

df = pd.read_csv(input_file)

print("HeartTwin Prediction Dataset")
print("============================")

print("\nDataset shape:")
print(df.shape)

print("\nTarget distribution:")
print(df["future_deterioration"].value_counts())

print("\nTarget percentage:")
print(
    df["future_deterioration"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print("\nPatients:")
print(df["patient_id"].unique())

print("\nTraining dataset:")
train = pd.read_csv("data/train_dataset.csv")
print(train.shape)

print("\nTesting dataset:")
test = pd.read_csv("data/test_dataset.csv")
print(test.shape)

print("\nTraining patients:")
print(sorted(train["patient_id"].unique()))

print("\nTesting patients:")
print(sorted(test["patient_id"].unique()))