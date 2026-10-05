import pandas as pd


comparison = pd.DataFrame({

    "Model": [
        "Logistic Regression",
        "Random Forest",
        "GRU"
    ],

    "ROC_AUC": [
        0.356,
        None,
        0.347
    ],

    "Positive_Recall": [
        0.14,
        0.00,
        0.00
    ],

    "Positive_F1": [
        0.09,
        0.00,
        0.00
    ],

    "Role": [
        "Baseline ML experiment",
        "Nonlinear ML experiment",
        "Temporal deep-learning experiment"
    ]
})


print("\n==============================")
print("MODEL COMPARISON")
print("==============================\n")

print(
    comparison.to_string(index=False)
)


comparison.to_csv(
    "data/model_comparison.csv",
    index=False
)


print(
    "\nSaved: data/model_comparison.csv"
)


print("\nConclusion:")
print(
    "The tested ML models showed limited generalization "
    "on the small synthetic patient-level holdout set."
)

print(
    "The interpretable Digital Twin risk engine is therefore "
    "retained as the primary prototype monitoring approach."
)