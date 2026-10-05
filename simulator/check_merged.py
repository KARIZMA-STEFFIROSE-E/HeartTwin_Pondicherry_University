import pandas as pd

file_path = "data/merged_dataset.csv"

df = pd.read_csv(file_path)

print("\nFirst 5 rows:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())