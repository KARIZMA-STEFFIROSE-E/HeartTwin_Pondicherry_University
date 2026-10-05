import pandas as pd

input_file = "data/personal_deviation.csv"
output_file = "data/top_contributing_signals.csv"

df = pd.read_csv(input_file)


def get_top_signals(row):

    signals = []

    # HR
    hr = row["hr_change_pct"]
    if abs(hr) >= 10:
        signals.append(
            ("Resting HR", hr, abs(hr))
        )

    # HRV
    hrv = row["hrv_change_pct"]
    if abs(hrv) >= 20:
        signals.append(
            ("HRV", hrv, abs(hrv))
        )

    # Sleep
    sleep = row["sleep_change_pct"]
    if sleep <= -15:
        signals.append(
            ("Sleep", sleep, abs(sleep))
        )

    # Activity
    steps = row["steps_change_pct"]
    if steps <= -20:
        signals.append(
            ("Activity", steps, abs(steps))
        )

    # SpO2
    spo2 = row["spo2_change_pct"]
    if spo2 <= -1:
        signals.append(
            ("SpO2", spo2, abs(spo2))
        )

    # Weight
    weight = row["weight_change_pct"]
    if weight >= 3:
        signals.append(
            ("Weight", weight, abs(weight))
        )

    # Sort by magnitude
    signals = sorted(
        signals,
        key=lambda x: x[2],
        reverse=True
    )

    # Take top 3
    top = signals[:3]

    names = []
    descriptions = []

    for name, change, magnitude in top:

        if change > 0:
            description = f"{name} ↑ {change:.1f}%"
        else:
            description = f"{name} ↓ {abs(change):.1f}%"

        names.append(name)
        descriptions.append(description)

    if not descriptions:
        return pd.Series({
            "top_signal_1": "None",
            "top_signal_2": "None",
            "top_signal_3": "None",
            "top_signal_summary": "No major personalized deviations detected"
        })

    while len(descriptions) < 3:
        descriptions.append("None")
        names.append("None")

    return pd.Series({
        "top_signal_1": descriptions[0],
        "top_signal_2": descriptions[1],
        "top_signal_3": descriptions[2],
        "top_signal_summary": "; ".join(descriptions)
    })


# Only calculate the latest day for each patient
df["date"] = pd.to_datetime(df["date"])

latest = (
    df.sort_values(["patient_id", "date"])
      .groupby("patient_id")
      .tail(1)
      .copy()
)

signals = latest.apply(
    get_top_signals,
    axis=1
)

final = pd.concat(
    [
        latest[["patient_id", "date"]],
        signals
    ],
    axis=1
)

final.to_csv(
    output_file,
    index=False
)

print("Top contributing signals created.")
print(f"Rows: {len(final)}")
print(f"Output: {output_file}")

print("\nTop contributing signals:")
print(
    final.to_string(index=False)
)