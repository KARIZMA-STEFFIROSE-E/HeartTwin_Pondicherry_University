
import streamlit as st
import pandas as pd

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="HeartTwin | Digital Twin",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

DATA_FILE = "data/final_twin_state.csv"

df = pd.read_csv(DATA_FILE)

df["date"] = pd.to_datetime(df["date"])

# ============================================================
# HEADER
# ============================================================

st.title("HeartTwin")

st.subheader(
    "Personalized Digital Twin for Early Heart-Failure Deterioration"
)

st.markdown(
    """
    **Doctor-facing monitoring prototype**

    HeartTwin combines historical patient information with dynamic
    wearable signals to monitor changes from each patient's personal baseline.
    """
)

st.divider()

# ============================================================
# PATIENT SELECTION
# ============================================================

patient_ids = sorted(df["patient_id"].unique())

selected_patient = st.selectbox(
    "Select Patient",
    patient_ids
)

patient = (
    df[df["patient_id"] == selected_patient]
    .iloc[0]
)

# ============================================================
# PATIENT OVERVIEW
# ============================================================

st.header("Patient Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Patient ID",
        patient["patient_id"]
    )

with col2:
    st.metric(
        "Age",
        f"{int(patient['age'])} years"
    )

with col3:
    st.metric(
        "Sex",
        patient["sex"]
    )

with col4:
    st.metric(
        "BMI",
        f"{patient['bmi']:.1f}"
    )

# ============================================================
# BACKGROUND RISK FACTORS
# ============================================================

st.subheader("Background Risk Factors")

risk_col1, risk_col2, risk_col3 = st.columns(3)

with risk_col1:
    st.write(
        f"**Hypertension:** "
        f"{'Yes' if patient['hypertension'] == 1 else 'No'}"
    )

with risk_col2:
    st.write(
        f"**Diabetes:** "
        f"{'Yes' if patient['diabetes'] == 1 else 'No'}"
    )

with risk_col3:
    st.write(
        f"**Current Weight:** "
        f"{patient['weight_kg']:.1f} kg"
    )

st.divider()

# ============================================================
# CURRENT DIGITAL TWIN STATE
# ============================================================

st.header("Current Digital Twin State")

risk1, risk2, risk3 = st.columns(3)

with risk1:
    st.metric(
        "Current Risk Score",
        f"{patient['twin_risk_score']:.0f}/100"
    )

with risk2:
    st.metric(
        "Current Risk Category",
        patient["risk_category"]
    )

with risk3:
    st.metric(
        "Risk Trajectory",
        patient["risk_trajectory"]
    )

# ============================================================
# CURRENT RISK LEVEL
# ============================================================

st.subheader("Current Risk Level")

current_score = float(
    patient["twin_risk_score"]
)

st.progress(
    min(current_score / 100, 1.0)
)

if patient["risk_category"] == "Low":

    st.success(
        "Low current risk signal"
    )

elif patient["risk_category"] == "Moderate":

    st.warning(
        "Moderate current risk signal"
    )

elif patient["risk_category"] == "Elevated":

    st.warning(
        "Elevated current risk signal"
    )

else:

    st.error(
        "High current risk signal"
    )

# ============================================================
# NEAR-TERM RISK
# ============================================================

st.header("Near-Term Risk Signal")

future1, future2, future3 = st.columns(3)

with future1:

    st.metric(
        "Future Risk Score",
        f"{patient['future_risk_score']:.0f}/100"
    )

with future2:

    st.metric(
        "Future Risk Category",
        patient["future_risk_category"]
    )

with future3:

    score_change = (
        float(patient["future_risk_score"])
        -
        float(patient["twin_risk_score"])
    )

    st.metric(
        "Risk Change",
        f"{score_change:+.0f}"
    )

# ============================================================
# FUTURE RISK LEVEL
# ============================================================

st.subheader("Near-Term Risk Level")

future_score = float(
    patient["future_risk_score"]
)

st.progress(
    min(future_score / 100, 1.0)
)

if patient["future_risk_category"] == "Low":

    st.success(
        "Low near-term risk signal"
    )

elif patient["future_risk_category"] == "Moderate":

    st.warning(
        "Moderate near-term risk signal"
    )

elif patient["future_risk_category"] == "Elevated":

    st.warning(
        "Elevated near-term risk signal"
    )

else:

    st.error(
        "High near-term risk signal"
    )

st.caption(
    "Near-term risk is a prototype monitoring signal generated "
    "from the Digital Twin state and trajectory. It is not a "
    "clinical diagnosis or medical prediction."
)

st.divider()

# ============================================================
# DOCTOR ALERT PANEL
# ============================================================

st.header("Doctor Review Panel")

future_category = patient[
    "future_risk_category"
]

trajectory = patient[
    "risk_trajectory"
]

personalization = patient[
    "personalization_status"
]

if future_category == "High":

    st.error(
        "High-priority review signal: multiple physiological "
        "changes are contributing to the near-term risk estimate."
    )

elif future_category == "Elevated":

    st.warning(
        "Review recommended: the patient's physiological pattern "
        "shows changes that may warrant closer monitoring."
    )

elif future_category == "Moderate":

    st.info(
        "Monitoring signal: moderate changes detected relative "
        "to the patient's personalized baseline."
    )

else:

    st.success(
        "No major near-term deterioration signal detected."
    )

# ============================================================
# WHY IS THE TWIN CONCERNED?
# ============================================================

st.subheader("Why is the Twin Concerned?")

st.info(
    patient["doctor_facing_summary"]
)

# ============================================================
# KEY SIGNALS
# ============================================================

st.subheader(
    "Key Changes From Personal Baseline"
)

st.write(
    patient["key_signal_summary"]
)

# ==========================

# -----------------------------
# WHAT-IF SIMULATION
# -----------------------------

st.markdown("---")
st.header("What-If Simulation")

st.write(
    "Simulate how a 30% reduction in daily activity could change "
    "the patient's digital-twin risk state."
)

what_if_df = pd.read_csv("data/what_if_simulation.csv")

selected_what_if = what_if_df[
    what_if_df["patient_id"] == selected_patient
]

if not selected_what_if.empty:

    what_if = selected_what_if.iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Current Steps",
            f"{what_if['current_steps']:.0f}"
        )

    with col2:
        st.metric(
            "Simulated Steps",
            f"{what_if['simulated_steps']:.0f}"
        )

    with col3:
        st.metric(
            "Risk Change",
            f"+{what_if['risk_change']:.0f}"
        )

    st.write(
        f"**Scenario:** Daily activity reduced by 30%"
    )

    st.write(
        f"Current risk: **{what_if['current_risk_score']:.0f} "
        f"({what_if['current_risk_category']})**"
    )

    st.write(
        f"Simulated risk: **{what_if['simulated_risk_score']:.0f} "
        f"({what_if['simulated_risk_category']})**"
    )

    st.write(
        f"Activity relative to personal baseline: "
        f"**{what_if['simulated_deviation_percent']:.1f}%**"
    )

    st.info(
        "This is a simulated scenario based on the digital-twin "
        "risk engine. It is not a medical prediction or diagnosis."
    )

