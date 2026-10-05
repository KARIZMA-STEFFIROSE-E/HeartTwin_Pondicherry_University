# HeartTwin — Personalized Digital Twin for Early Heart-Failure Deterioration

## 1. Project Overview

**HeartTwin** is a personalized digital-twin prototype designed to monitor physiological changes associated with potential heart-failure deterioration by combining **historical patient information** with **dynamic wearable signals**.

The system creates a patient-specific baseline and continuously compares incoming physiological measurements against that baseline. It generates an interpretable risk state, identifies important changes, tracks the direction of risk over time, and provides a near-term risk signal through a doctor-facing dashboard.

HeartTwin also includes a **What-If Simulation** that allows a user to explore how a simulated 30% reduction in daily activity could affect the digital-twin risk state.

> **Important:** HeartTwin is a research and prototype system. It is not a clinically validated diagnostic or medical decision-making system.

---

## 2. Problem Statement

Heart-failure deterioration can involve gradual changes in multiple physiological and behavioral signals rather than a single abnormal measurement.

Traditional monitoring may not adequately represent how an individual's current measurements differ from their own normal physiological state.

HeartTwin addresses this problem by creating a **personalized digital representation of the patient** that combines:

* Historical patient context
* Background risk factors
* Dynamic wearable measurements
* Patient-specific physiological baselines
* Changes and trends relative to those baselines

The objective is to provide an interpretable early-warning monitoring prototype that can help identify changing physiological patterns for further clinical review.

---

## 3. Healthcare Use Case

The primary use case is **early monitoring of potential heart-failure deterioration**.

HeartTwin monitors the following dynamic signals:

* Resting heart rate
* Heart-rate variability (HRV)
* Sleep duration
* Daily steps
* Oxygen saturation (SpO₂)
* Body weight

These signals are interpreted together with historical patient information such as:

* Age
* BMI
* Hypertension
* Diabetes
* Smoking history
* Cholesterol
* Cardiac history

Rather than relying only on population-level thresholds, HeartTwin emphasizes **deviation from each patient's personal baseline**.

---

## 4. Digital Twin Concept

The HeartTwin architecture follows the pipeline:

```text
Synthetic EHR
      ↓
Patient Profile
      ↓
Wearable / IoT Signals
      ↓
Personal Baseline
      ↓
Data Fusion
      ↓
Digital Twin State
      ↓
Risk Engine
      ↓
Personalized Intelligence
      ↓
Near-Term Risk Signal
      ↓
What-If Simulation
      ↓
Doctor-Facing Dashboard
```

The digital twin represents the patient's current physiological state using both historical context and continuously changing wearable measurements.

---

## 5. Data Sources

### Synthetic EHR

Synthetic historical patient information was generated using **Synthea** and used as the basis for the EHR component of the prototype.

The project also uses synthetic patient profiles to create a multi-patient experimental environment.

### Simulated Wearable Data

A custom wearable-data simulator generates daily measurements for multiple synthetic patients.

The simulated signals include:

* Resting heart rate
* HRV
* Sleep
* Steps
* SpO₂
* Weight

The simulator also introduces controlled deterioration patterns to evaluate whether the digital-twin risk engine responds appropriately to changing physiological states.

All data used in the prototype are synthetic or simulated and contain no real patient information.

---

## 6. Personalization

A major component of HeartTwin is the **personal baseline**.

For each patient, baseline values are calculated from their historical wearable measurements.

The system then evaluates deviations such as:

* Increased resting heart rate
* Reduced HRV
* Reduced sleep
* Reduced activity
* Reduced SpO₂
* Increased body weight

This allows the system to distinguish between a patient's usual physiological variation and potentially important changes from their own baseline.

---

## 7. Digital Twin Risk Engine

The final prototype uses an interpretable **Digital Twin Risk Engine**.

The engine combines deviations across multiple physiological signals into a risk score from **0–100**.

Risk categories are:

|  Score | Category |
| -----: | -------- |
|   0–19 | Low      |
|  20–39 | Moderate |
|  40–59 | Elevated |
| 60–100 | High     |

The system also calculates a risk trajectory:

* **Stable**
* **Improving**
* **Worsening**

The risk explanation identifies the major contributing personalized signals.

---

## 8. Machine Learning Experiments

Several machine-learning approaches were evaluated during development:

1. Logistic Regression
2. Random Forest
3. GRU-based temporal deep learning

The experiments were evaluated using a patient-level train/test split.

The tested models showed limited generalization on the held-out synthetic patients. Therefore, the final prototype does **not** present these models as clinically predictive models.

Instead, HeartTwin uses the interpretable Digital Twin Risk Engine for the final monitoring prototype.

This design decision prioritizes:

* Interpretability
* Patient-specific monitoring
* Transparent risk reasoning
* Explainability
* Prototype reliability

The machine-learning experiments remain included in the repository as part of the project's development and evaluation process.

---

## 9. Near-Term Risk Signal

HeartTwin generates a near-term risk signal using the current digital-twin state and risk trajectory.

The signal is intended to answer:

> **"If the patient's current physiological pattern continues, does the digital twin indicate increasing concern?"**

This is a **prototype monitoring signal**, not a clinically validated prediction of a future medical event.

---

## 10. What-If Simulation

HeartTwin includes an interactive scenario simulation.

The current implementation simulates:

> **A 30% reduction in daily activity**

The system recalculates the patient's digital-twin state under the simulated activity level and compares it with the current state.

This allows the dashboard to demonstrate how a change in an important behavioral signal can affect the personalized risk state.

The simulation is exploratory and is **not medical advice or a clinical prediction**.

---

## 11. Doctor-Facing Dashboard

HeartTwin includes a Streamlit-based dashboard designed as a conceptual doctor-facing monitoring interface.

The dashboard provides:

* Patient overview
* Background risk factors
* Current digital-twin risk
* Risk category
* Risk trajectory
* Near-term risk signal
* Personalized deviations
* Key contributing signals
* Wearable trends
* Risk explanation
* What-If activity simulation

The dashboard is intended to support **human review**, rather than replace clinical judgment.

---

## 12. Architecture

The complete system architecture is provided in:

**`architecture.pdf`**

The architecture illustrates the flow from synthetic EHR and wearable data through personalization, data fusion, digital-twin state generation, risk analysis, simulation, and dashboard visualization.

---

## 13. Technology Stack

### Programming

* Python 3.14

### Data Processing

* Pandas
* NumPy

### Machine Learning

* Scikit-learn
* PyTorch

### Dashboard

* Streamlit

### Synthetic Healthcare Data

* Synthea

### Development Environment

* Visual Studio Code
* Git
* GitHub

---

## 14. Project Structure

```text
HeartTwin/
│
├── data/
│   ├── ehr_patient.csv
│   ├── ehr_patient_profiles.csv
│   ├── wearable/
│   ├── features_dataset.csv
│   ├── final_twin_state.csv
│   ├── final_patient_predictions.csv
│   ├── personal_deviation.csv
│   ├── personal_explanations.csv
│   ├── risk_trajectory.csv
│   ├── what_if_simulation.csv
│   └── ...
│
├── simulator/
│   ├── wearable_simulator.py
│   ├── create_patient_profiles.py
│   ├── create_features.py
│   ├── twin_state.py
│   ├── risk_trajectory.py
│   ├── twin_intelligence.py
│   ├── risk_interpretation.py
│   ├── what_if_simulation.py
│   ├── dashboard.py
│   ├── validate_deterioration.py
│   ├── validate_false_alarms.py
│   └── ...
│
├── src/
│
├── architecture.pdf
├── README.md
├── LICENSE
└── .gitignore
```

---

## 15. Validation

The prototype was evaluated using several validation checks.

### Risk Distribution

Final prototype patients were distributed across:

* Low risk: 4
* Moderate risk: 4
* Elevated risk: 2
* High risk: 0

### Deterioration Separation

Average digital-twin risk:

| Patient State     | Mean Risk |
| ----------------- | --------: |
| Non-deterioration |       7.6 |
| Deterioration     |      40.0 |

The deterioration group therefore produced substantially higher average digital-twin risk scores in the synthetic evaluation environment.

### Review-Level Signal

* Non-deteriorating patients flagged Elevated/High: **0/5**
* Deteriorating patients flagged Elevated/High: **2/5**

### What-If Validation

Under the simulated 30% activity reduction:

* Risk increased: **10/10 patients**
* Risk unchanged: **0/10**
* Risk decreased: **0/10**

These results demonstrate the expected directional behavior of the prototype risk engine on the synthetic test environment.

They should **not** be interpreted as clinical performance metrics.

---

## 16. Limitations

HeartTwin is an early-stage proof-of-concept and has several limitations:

* The wearable data are simulated.
* The EHR environment is synthetic.
* The deterioration patterns are controlled synthetic scenarios.
* The final Digital Twin Risk Engine is rule-based and interpretable rather than clinically trained.
* The near-term risk signal has not been clinically validated.
* The system has not been evaluated on a real-world heart-failure cohort.
* The prototype does not provide medical diagnosis or treatment recommendations.
* The machine-learning experiments showed limited generalization on the available synthetic patient-level test split.

Future work should evaluate the approach using larger and more diverse real-world or appropriately de-identified datasets, stronger temporal validation, and clinical expert assessment.

---

## 17. Future Work

Potential future improvements include:

* Integration with real-world wearable datasets
* Larger patient populations
* Longitudinal clinical datasets
* Improved temporal modeling
* Personalized anomaly detection
* More robust uncertainty estimation
* Clinical expert evaluation
* External validation
* Integration with additional physiological signals
* Improved clinician workflow integration

---

## 18. How to Run

### 1. Clone the repository

```bash
git clone <GITHUB_REPOSITORY_URL>
cd HeartTwin
```

### 2. Install dependencies

```bash
pip install pandas numpy scikit-learn torch streamlit
```

### 3. Run the dashboard

```bash
python -m streamlit run simulator/dashboard.py
```

The dashboard will open in the browser.

---

## 19. Project Deliverables

### Architecture Diagram

`architecture.pdf`

### Presentation

`[ADD PRESENTATION LINK]`

### Demonstration Video

`[ADD 20+ MINUTE VIDEO LINK]`

### GitHub Repository

`[ADD GITHUB REPOSITORY LINK]`

---

## 20. Team

**Team Name:** [ADD TEAM NAME]

**College:** Pondicherry University

**Project:** HeartTwin — Personalized Digital Twin for Early Heart-Failure Deterioration

**Team Members:**

* [ADD MEMBER NAME]
* [ADD MEMBER NAME]
* [ADD MEMBER NAME]

---

## 21. License

This project is released under the license provided in the repository's `LICENSE` file.

See:

`LICENSE`

---

## 22. Disclaimer

HeartTwin is an educational and research-oriented digital-twin prototype.

It is **not a medical device, diagnostic system, treatment recommendation system, or clinically validated predictive model**.

Risk scores, future-risk signals, and What-If simulations are prototype computational outputs intended for demonstration and research purposes only. Clinical decisions should always be made by qualified healthcare professionals using validated clinical information.

---

## 23. Acknowledgement

This project was developed as part of the **Happiest Health Digital Twin Challenge 2026**.

The prototype explores how personalized digital-twin techniques can combine historical health information with dynamic wearable signals to support early monitoring of physiological deterioration.
