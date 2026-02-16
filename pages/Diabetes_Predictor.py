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

pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20)
glucose = st.number_input("Glucose (mg/dL)", min_value=0.0, max_value=300.0)
blood_pressure = st.number_input("Blood Pressure", min_value=0.0)
skin_thickness = st.number_input("Skin Thickness", min_value=0.0)
insulin = st.number_input("Insulin", min_value=0.0)

height = st.number_input("Height (cm)", min_value=50.0)
weight = st.number_input("Weight (kg)", min_value=10.0)

bmi = weight / ((height / 100) ** 2)
st.info(f"BMI: {bmi:.2f}")

pedigree = st.number_input("Diabetes Pedigree", min_value=0.0)
age = st.number_input("Age", min_value=1)

def get_risk(prob):
    if prob < 0.3:
        return "Low Risk"
    elif prob < 0.7:
        return "Medium Risk"
    else:
        return "High Risk"

if st.button("Predict"):
    inputs = [pregnancies, glucose, blood_pressure,
              skin_thickness, insulin, bmi,
              pedigree, age]

    with st.spinner("Analyzing..."):
        time.sleep(1)

        input_data = np.array([inputs])
        input_scaled = scaler.transform(input_data)
        input_tensor = torch.tensor(input_scaled, dtype=torch.float32)

        with torch.no_grad():
            prediction = model(input_tensor)
            probability = prediction.item()

    st.success("Prediction Complete")
    st.write(f"Probability: {probability:.2f}")
    st.write(f"Risk Level: {get_risk(probability)}")
