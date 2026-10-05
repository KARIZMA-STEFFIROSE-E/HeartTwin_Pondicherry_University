import pandas as pd

input_file = "data/features_dataset.csv"
output_file = "data/twin_state_dataset.csv"

df = pd.read_csv(input_file)

# ---------------------------------------------------------
# Risk contribution functions
# ---------------------------------------------------------

def calculate_risk(row):

    risk = 0
    reasons = []

    # Resting heart rate
    if row["hr_percent_change"] >= 10:
        risk += 15
        reasons.append("Resting HR increased")

    elif row["hr_percent_change"] >= 5:
        risk += 8
        reasons.append("Resting HR slightly increased")


    # HRV
    if row["hrv_percent_change"] <= -20:
        risk += 20
        reasons.append("HRV decreased")

    elif row["hrv_percent_change"] <= -10:
        risk += 10
        reasons.append("HRV slightly decreased")


    # Sleep
    if row["sleep_percent_change"] <= -15:
        risk += 15
        reasons.append("Sleep decreased")

    elif row["sleep_percent_change"] <= -10:
        risk += 8
        reasons.append("Sleep slightly decreased")


    # Steps / activity
    if row["steps_percent_change"] <= -30:
        risk += 15
        reasons.append("Activity decreased")

    elif row["steps_percent_change"] <= -15:
        risk += 8
        reasons.append("Activity slightly decreased")


    # SpO2
    if row["spo2_deviation"] <= -2:
        risk += 20
        reasons.append("SpO2 decreased")

    elif row["spo2_deviation"] <= -1:
        risk += 10
        reasons.append("SpO2 slightly decreased")


    # Weight
    if row["weight_percent_change"] >= 5:
        risk += 15
        reasons.append("Weight increased")

    elif row["weight_percent_change"] >= 3:
        risk += 8
        reasons.append("Weight slightly increased")


    # Cap score
    risk = min(risk, 100)

    return pd.Series([risk, "; ".join(reasons)])


# ---------------------------------------------------------
# Calculate Twin Risk Score
# ---------------------------------------------------------

df[["twin_risk_score", "risk_reasons"]] = df.apply(
    calculate_risk,
    axis=1
)


# ---------------------------------------------------------
# Risk categories
# ---------------------------------------------------------

def risk_category(score):

    if score < 20:
        return "Low"

    elif score < 40:
        return "Moderate"

    elif score < 60:
        return "Elevated"

    else:
        return "High"


df["risk_category"] = df["twin_risk_score"].apply(risk_category)


# ---------------------------------------------------------
# Save
# ---------------------------------------------------------

df.to_csv(output_file, index=False)

print("HeartTwin state engine completed!")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nRisk category distribution:")
print(df["risk_category"].value_counts())

print("\nRisk score range:")
print(
    "Minimum:",
    df["twin_risk_score"].min()
)

print(
    "Maximum:",
    df["twin_risk_score"].max()
)

print("\nOutput:")
print(output_file)