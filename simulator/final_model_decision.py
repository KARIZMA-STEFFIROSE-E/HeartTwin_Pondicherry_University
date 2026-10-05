import pandas as pd


decision = pd.DataFrame({

    "component": [
        "Logistic Regression",
        "Random Forest",
        "GRU",
        "Digital Twin Risk Engine"
    ],

    "status": [
        "Evaluated",
        "Evaluated",
        "Evaluated",
        "Selected"
    ],

    "reason": [
        "Baseline ML model; limited generalization.",
        "Nonlinear ML experiment; poor positive-class detection.",
        "Temporal deep-learning experiment; ROC-AUC 0.347.",
        "Interpretable, personalized and suitable for prototype monitoring."
    ],

    "primary_system": [
        False,
        False,
        False,
        True
    ]
})


decision.to_csv(
    "data/final_model_decision.csv",
    index=False
)


print("\n==============================")
print("FINAL MODEL DECISION")
print("==============================\n")

print(
    decision.to_string(index=False)
)

print(
    "\nPrimary prototype model:"
)

print(
    "Personalized Digital Twin Risk Engine"
)

print(
    "\nSaved: data/final_model_decision.csv"
)