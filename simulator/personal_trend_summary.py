import pandas as pd

input_file = "data/personal_deviation.csv"
output_file = "data/personal_trend_summary.csv"

df = pd.read_csv(input_file)
df["date"] = pd.to_datetime(df["date"])

# Sort data
df = df.sort_values(["patient_id", "date"])

# Define abnormal personalized deviations
df["abnormal_hr"] = df["hr_change_pct"].abs() >= 10
df["abnormal_hrv"] = df["hrv_change_pct"].abs() >= 20
df["abnormal_sleep"] = df["sleep_change_pct"] <= -15
df["abnormal_steps"] = df["steps_change_pct"] <= -20
df["abnormal_spo2"] = df["spo2_change_pct"] <= -1
df["abnormal_weight"] = df["weight_change_pct"] >= 3

abnormal_columns = [
    "abnormal_hr",
    "abnormal_hrv",
    "abnormal_sleep",
    "abnormal_steps",
    "abnormal_spo2",
    "abnormal_weight"
]

df["abnormal_signal_count"] = df[abnormal_columns].sum(axis=1)

# Look at the most recent 7 days for every patient
recent = (
    df.groupby("patient_id")
      .tail(7)
      .copy()
)

# Count abnormal days
summary = recent.groupby("patient_id").agg(
    abnormal_days=("abnormal_signal_count", lambda x: (x > 0).sum()),
    total_abnormal_signals=("abnormal_signal_count", "sum"),
    avg_hr_change=("hr_change_pct", "mean"),
    avg_hrv_change=("hrv_change_pct", "mean"),
    avg_sleep_change=("sleep_change_pct", "mean"),
    avg_steps_change=("steps_change_pct", "mean"),
    avg_spo2_change=("spo2_change_pct", "mean"),
    avg_weight_change=("weight_change_pct", "mean")
).reset_index()

# Determine dominant abnormal signals
def dominant_signals(row):
    signals = []

    if abs(row["avg_hr_change"]) >= 10:
        signals.append("HR")

    if abs(row["avg_hrv_change"]) >= 20:
        signals.append("HRV")

    if row["avg_sleep_change"] <= -15:
        signals.append("Sleep")

    if row["avg_steps_change"] <= -20:
        signals.append("Activity")

    if row["avg_spo2_change"] <= -1:
        signals.append("SpO2")

    if row["avg_weight_change"] >= 3:
        signals.append("Weight")

    if not signals:
        return "No persistent abnormal signal"

    return ", ".join(signals)


summary["dominant_signals"] = summary.apply(
    dominant_signals,
    axis=1
)

# Personalization status
def determine_status(row):
    if row["abnormal_days"] >= 5:
        return "Persistent deviation"
    elif row["abnormal_days"] >= 2:
        return "Emerging deviation"
    else:
        return "Stable personal baseline"


summary["personalization_status"] = summary.apply(
    determine_status,
    axis=1
)

# Round numerical values
numeric_columns = [
    "avg_hr_change",
    "avg_hrv_change",
    "avg_sleep_change",
    "avg_steps_change",
    "avg_spo2_change",
    "avg_weight_change"
]

summary[numeric_columns] = summary[numeric_columns].round(2)

summary.to_csv(output_file, index=False)

print("Personal trend summaries created.")
print(f"Rows: {len(summary)}")
print(f"Output: {output_file}")

print("\nPersonal trend summary:")
print(summary.to_string(index=False))