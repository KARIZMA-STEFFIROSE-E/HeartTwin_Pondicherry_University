import pandas as pd
import numpy as np

input_file = "data/features_dataset.csv"
output_file = "data/gru_sequences.npz"

df = pd.read_csv(input_file)

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values(["patient_id", "date"])


# Wearable signals used by the GRU
sequence_features = [
    "resting_hr",
    "hrv",
    "sleep_hours",
    "steps",
    "spo2",
    "weight_kg"
]

sequence_length = 7

X = []
y = []
patient_ids = []
end_dates = []


for patient_id, patient_df in df.groupby("patient_id"):

    patient_df = patient_df.sort_values("date").reset_index(drop=True)

    for i in range(sequence_length - 1, len(patient_df)):

        window = patient_df.iloc[
            i - sequence_length + 1 : i + 1
        ]

        sequence = window[sequence_features].values

        # Target = deterioration on the final day
        target = window.iloc[-1]["deterioration"]

        X.append(sequence)
        y.append(target)
        patient_ids.append(patient_id)
        end_dates.append(window.iloc[-1]["date"])


X = np.array(X, dtype=np.float32)
y = np.array(y, dtype=np.int32)


np.savez(
    output_file,
    X=X,
    y=y,
    patient_ids=np.array(patient_ids),
    dates=np.array(end_dates, dtype="datetime64[ns]")
)


print("GRU sequence data created.")
print(f"Sequences: {len(X)}")
print(f"Sequence shape: {X.shape}")
print(f"Features per day: {X.shape[2]}")
print(f"Sequence length: {X.shape[1]}")

print("\nTarget distribution:")
print(pd.Series(y).value_counts().sort_index())

print(f"\nOutput: {output_file}")