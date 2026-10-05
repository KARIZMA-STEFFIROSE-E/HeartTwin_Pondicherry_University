import pandas as pd

train_file = "data/train_dataset.csv"
test_file = "data/test_dataset.csv"

train = pd.read_csv(train_file)
test = pd.read_csv(test_file)

print("Training data shape:", train.shape)
print("Testing data shape:", test.shape)

print("\nTraining columns:")
print(train.columns.tolist())

print("\nTarget:")
print("future_deterioration")

print("\nTarget distribution in training:")
print(train["future_deterioration"].value_counts())