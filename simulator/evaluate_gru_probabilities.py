import numpy as np
import pandas as pd
import torch

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# ==================================================
# 1. LOAD DATA
# ==================================================

data = np.load("data/gru_sequences.npz")

X = data["X"]
y = data["y"]
patient_ids = data["patient_ids"]


# ==================================================
# 2. SAME PATIENT SPLIT AS TRAINING
# ==================================================

patient_target = pd.DataFrame({
    "patient_id": patient_ids,
    "target": y
})

patient_target = (
    patient_target
    .groupby("patient_id")["target"]
    .max()
    .reset_index()
)

train_patients, test_patients = train_test_split(
    patient_target["patient_id"],
    test_size=0.4,
    random_state=42,
    stratify=patient_target["target"]
)

test_mask = np.isin(
    patient_ids,
    test_patients
)

X_test = X[test_mask]
y_test = y[test_mask]

test_patient_ids = patient_ids[test_mask]


# ==================================================
# 3. NORMALIZE USING TRAINING DATA
# ==================================================

train_mask = np.isin(
    patient_ids,
    train_patients
)

X_train = X[train_mask]

scaler = StandardScaler()

scaler.fit(
    X_train.reshape(-1, X_train.shape[2])
)

X_test_scaled = scaler.transform(
    X_test.reshape(-1, X_test.shape[2])
).reshape(X_test.shape)


# ==================================================
# 4. RECREATE MODEL
# ==================================================

class HeartGRU(torch.nn.Module):

    def __init__(self):

        super().__init__()

        self.gru = torch.nn.GRU(
            input_size=6,
            hidden_size=32,
            batch_first=True
        )

        self.dropout = torch.nn.Dropout(0.2)

        self.fc1 = torch.nn.Linear(32, 16)

        self.fc2 = torch.nn.Linear(16, 1)

        self.relu = torch.nn.ReLU()

    def forward(self, x):

        output, hidden = self.gru(x)

        x = output[:, -1, :]

        x = self.dropout(x)

        x = self.fc1(x)

        x = self.relu(x)

        x = self.dropout(x)

        x = self.fc2(x)

        return x


model = HeartGRU()

model.load_state_dict(
    torch.load(
        "data/gru_model.pth",
        map_location="cpu"
    )
)

model.eval()


# ==================================================
# 5. PREDICT
# ==================================================

X_test_tensor = torch.tensor(
    X_test_scaled,
    dtype=torch.float32
)

with torch.no_grad():

    logits = model(
        X_test_tensor
    )

    probabilities = torch.sigmoid(
        logits
    ).numpy().ravel()


# ==================================================
# 6. CREATE RESULTS TABLE
# ==================================================

results = pd.DataFrame({

    "patient_id": test_patient_ids,

    "actual_deterioration": y_test,

    "gru_probability": probabilities

})


results["prediction"] = (
    results["gru_probability"] >= 0.5
).astype(int)


print("\nGRU probability analysis:")
print(
    results.to_string(index=False)
)


print("\n--------------------------------")
print("Average probability by class")
print("--------------------------------")

print(
    results
    .groupby("actual_deterioration")["gru_probability"]
    .agg(["count", "mean", "min", "max"])
)


results.to_csv(
    "data/gru_predictions.csv",
    index=False
)

print(
    "\nSaved: data/gru_predictions.csv"
)