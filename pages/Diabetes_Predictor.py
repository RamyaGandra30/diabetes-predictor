import streamlit as st
import torch
import torch.nn as nn
import numpy as np
import joblib
import time




# ---------------------------
# Login Protection
# ---------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.switch_page("pages/Login.py")




# ---------------------------
# Logout Button
# ---------------------------
st.sidebar.write(f"Logged in as: {st.session_state.username}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.switch_page("pages/Login.py")

# ---------------------------
# Model Definition
# ---------------------------
class DiabetesModel(nn.Module):
    def __init__(self):
        super(DiabetesModel, self).__init__()
        self.fc1 = nn.Linear(8, 16)
        self.fc2 = nn.Linear(16, 8)
        self.fc3 = nn.Linear(8, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.sigmoid(self.fc3(x))
        return x

model = DiabetesModel()
model.load_state_dict(torch.load("models/global_model.pth", map_location="cpu"))
model.eval()

scaler = joblib.load("models/scaler.pkl")

# ---------------------------
# UI
# ---------------------------
st.title("🩺 Diabetes Risk Predictor")

 
# User Inputs (No Defaults)
# ---------------------------

st.subheader("🧾 Patient Clinical Information")

# Pregnancies
pregnancies = st.number_input(
    "Pregnancies",
    min_value=0,
    max_value=20,
    step=1
)
st.caption("Normal: 0–5 pregnancies | Typical dataset range: 0–17")

# Glucose
glucose = st.number_input(
    "Glucose Level (mg/dL)",
    min_value=0.0,
    max_value=300.0,
    format="%.2f"
)
st.caption("Normal (fasting): 70–99 mg/dL | Prediabetes: 100–125 | Diabetes: ≥126")

# Blood Pressure
blood_pressure = st.number_input(
    "Blood Pressure (mm Hg)",
    min_value=0.0,
    max_value=200.0,
    format="%.2f"
)
st.caption("Normal (Diastolic): 60–80 mm Hg | High: ≥90")

# Skin Thickness
skin_thickness = st.number_input(
    "Skin Thickness (mm)",
    min_value=0.0,
    max_value=100.0,
    format="%.2f"
)
st.caption("Normal: 10–40 mm | Dataset range: 0–99")

# Insulin
insulin = st.number_input(
    "Insulin Level (mu U/ml)",
    min_value=0.0,
    max_value=900.0,
    format="%.2f"
)
st.caption("Normal fasting insulin: 16–166 mu U/ml")

# ---------------------------
# BMI Calculator
# ---------------------------

st.subheader("📏 BMI Calculator")

height_cm = st.number_input(
    "Height (cm)",
    min_value=50.0,
    max_value=250.0,
    format="%.2f"
)

weight_kg = st.number_input(
    "Weight (kg)",
    min_value=10.0,
    max_value=300.0,
    format="%.2f"
)

if height_cm > 0:
    bmi = weight_kg / ((height_cm / 100) ** 2)
else:
    bmi = 0

st.info(f"Calculated BMI: {bmi:.2f}")
st.caption("Normal BMI: 18.5–24.9 | Overweight: 25–29.9 | Obese: ≥30")

# Diabetes Pedigree Function
diabetes_pedigree = st.number_input(
    "Diabetes Pedigree Function",
    min_value=0.0,
    max_value=3.0,
    format="%.3f"
)
st.caption("Higher value = stronger family history of diabetes | Dataset range: 0.078–2.42")

# Age
age = st.number_input(
    "Age",
    min_value=1,
    max_value=120,
    step=1
)
st.caption("Higher risk typically ≥45 years")

# ---------------------------
# Risk Level Function
# ---------------------------
def get_risk_level(prob):
    if prob < 0.3:
        return "🟢 Low Risk"
    elif prob < 0.7:
        return "🟠 Medium Risk"
    else:
        return "🔴 High Risk"

# ---------------------------
# Prediction Button
# ---------------------------
if st.button("Predict Diabetes Risk"):

    # Validation Check
    inputs = [
        pregnancies, glucose, blood_pressure,
        skin_thickness, insulin, bmi,
        diabetes_pedigree, age
    ]

    if any(value < 0 for value in inputs):
        st.error("❌ Values cannot be negative.")
    else:
        with st.spinner("Analyzing patient data..."):
            time.sleep(1.5)

            input_data = np.array([inputs])
            input_scaled = scaler.transform(input_data)
            input_tensor = torch.tensor(input_scaled, dtype=torch.float32)

            with torch.no_grad():
                prediction = model(input_tensor)
                probability = prediction.item()

            risk = get_risk_level(probability)

        st.success("Prediction Completed ✅")
        st.write(f"### Probability of Diabetes: {probability:.2f}")
        st.write(f"### Risk Level: {risk}")

        if probability > 0.5:
            st.error("⚠️ Patient Likely Diabetic")
        else:
            st.success("✅ Patient Likely Non-Diabetic")
