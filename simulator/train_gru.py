import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score
)


# ==================================================
# 1. LOAD DATA
# ==================================================

data = np.load("data/gru_sequences.npz")

X = data["X"]
y = data["y"]
patient_ids = data["patient_ids"]

print("Loaded GRU data")
print("X shape:", X.shape)
print("y shape:", y.shape)


# ==================================================
# 2. PATIENT-LEVEL TRAIN / TEST SPLIT
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

train_mask = np.isin(patient_ids, train_patients)
test_mask = np.isin(patient_ids, test_patients)

X_train = X[train_mask]
y_train = y[train_mask]

X_test = X[test_mask]
y_test = y[test_mask]

print("\nTrain sequences:", len(X_train))
print("Test sequences:", len(X_test))

print("\nTrain patients:")
print(train_patients.tolist())

print("\nTest patients:")
print(test_patients.tolist())


# ==================================================
# 3. NORMALIZE DATA
# ==================================================

scaler = StandardScaler()

X_train_2d = X_train.reshape(
    -1,
    X_train.shape[2]
)

scaler.fit(X_train_2d)

X_train_scaled = scaler.transform(
    X_train_2d
).reshape(X_train.shape)

X_test_scaled = scaler.transform(
    X_test.reshape(-1, X_test.shape[2])
).reshape(X_test.shape)


# ==================================================
# 4. CONVERT TO PYTORCH TENSORS
# ==================================================

X_train_tensor = torch.tensor(
    X_train_scaled,
    dtype=torch.float32
)

y_train_tensor = torch.tensor(
    y_train,
    dtype=torch.float32
).view(-1, 1)

X_test_tensor = torch.tensor(
    X_test_scaled,
    dtype=torch.float32
)

y_test_tensor = torch.tensor(
    y_test,
    dtype=torch.float32
).view(-1, 1)


# ==================================================
# 5. DEFINE GRU MODEL
# ==================================================

class HeartGRU(nn.Module):

    def __init__(self):

        super().__init__()

        self.gru = nn.GRU(
            input_size=6,
            hidden_size=32,
            batch_first=True
        )

        self.dropout = nn.Dropout(0.2)

        self.fc1 = nn.Linear(
            32,
            16
        )

        self.fc2 = nn.Linear(
            16,
            1
        )

        self.relu = nn.ReLU()

    def forward(self, x):

        output, hidden = self.gru(x)

        # Last time step
        x = output[:, -1, :]

        x = self.dropout(x)

        x = self.fc1(x)

        x = self.relu(x)

        x = self.dropout(x)

        x = self.fc2(x)

        return x


model = HeartGRU()


print("\nGRU model created:")
print(model)


# ==================================================
# 6. LOSS + OPTIMIZER
# ==================================================

criterion = nn.BCEWithLogitsLoss(
    pos_weight=torch.tensor([3.0])
)

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)


# ==================================================
# 7. TRAIN
# ==================================================

epochs = 50

print("\nStarting training...\n")

for epoch in range(epochs):

    model.train()

    optimizer.zero_grad()

    outputs = model(
        X_train_tensor
    )

    loss = criterion(
        outputs,
        y_train_tensor
    )

    loss.backward()

    optimizer.step()

    if (epoch + 1) % 5 == 0:

        print(
            f"Epoch {epoch + 1:02d}/{epochs} "
            f"- Loss: {loss.item():.4f}"
        )


# ==================================================
# 8. EVALUATE
# ==================================================

model.eval()

with torch.no_grad():

    logits = model(
        X_test_tensor
    )

    probabilities = torch.sigmoid(
        logits
    ).numpy().ravel()


predictions = (
    probabilities >= 0.5
).astype(int)


print("\n==============================")
print("GRU EVALUATION")
print("==============================")


print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        predictions
    )
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


if len(np.unique(y_test)) == 2:

    auc = roc_auc_score(
        y_test,
        probabilities
    )

    print(
        f"\nROC-AUC: {auc:.3f}"
    )


# ==================================================
# 9. SAVE MODEL
# ==================================================

torch.save(
    model.state_dict(),
    "data/gru_model.pth"
)

print(
    "\nGRU model saved to:"
    " data/gru_model.pth"
)