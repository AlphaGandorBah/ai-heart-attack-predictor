import streamlit as st
import pandas as pd
import pickle
import os
import plotly.graph_objects as go

# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------

st.set_page_config(
    page_title="Heart Attack Predictor",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Heart Attack Risk Prediction")

st.markdown(
"""
Enter the patient's medical information below and click **Predict Risk**
to estimate the probability of heart disease.
"""
)

# -----------------------------------------------------
# Load Model (Streamlit Cloud safe path)
# -----------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
model_path = os.path.join(BASE_DIR, "clean_model.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)

# -----------------------------------------------------
# Input Form
# -----------------------------------------------------

with st.form("prediction_form"):

    st.subheader("Patient Information")

    age = st.number_input("Age", 18, 100, 45)

    sex = st.selectbox("Sex", ["Male", "Female"])
    sex = 1 if sex == "Male" else 0

    cp = st.selectbox(
        "Chest Pain Type",
        [
            "Typical Angina",
            "Atypical Angina",
            "Non-anginal Pain",
            "Asymptomatic"
        ]
    )

    cp_map = {
        "Typical Angina": 0,
        "Atypical Angina": 1,
        "Non-anginal Pain": 2,
        "Asymptomatic": 3
    }

    cp = cp_map[cp]

    trtbps = st.number_input("Resting Blood Pressure", 80, 200, 120)

    chol = st.number_input("Cholesterol", 100, 600, 200)

    fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", ["No", "Yes"])
    fbs = 1 if fbs == "Yes" else 0

    restecg = st.selectbox(
        "Resting ECG",
        [
            "Normal",
            "ST-T abnormality",
            "Left ventricular hypertrophy"
        ]
    )

    restecg_map = {
        "Normal": 0,
        "ST-T abnormality": 1,
        "Left ventricular hypertrophy": 2
    }

    restecg = restecg_map[restecg]

    thalachh = st.number_input("Maximum Heart Rate Achieved", 70, 210, 150)

    exng = st.selectbox("Exercise Induced Angina", ["No", "Yes"])
    exng = 1 if exng == "Yes" else 0

    oldpeak = st.number_input("ST Depression", 0.0, 10.0, 1.0)

    slp = st.selectbox("Slope of ST Segment", ["Upsloping", "Flat", "Downsloping"])

    slp_map = {
        "Upsloping": 0,
        "Flat": 1,
        "Downsloping": 2
    }

    slp = slp_map[slp]

    caa = st.number_input("Number of Major Vessels (0-4)", 0, 4, 0)

    thall = st.selectbox(
        "Thalassemia",
        [
            "Normal",
            "Fixed defect",
            "Reversible defect"
        ]
    )

    thall_map = {
        "Normal": 1,
        "Fixed defect": 2,
        "Reversible defect": 3
    }

    thall = thall_map[thall]

    predict_button = st.form_submit_button("🔍 Predict Risk")

# -----------------------------------------------------
# Prediction
# -----------------------------------------------------

if predict_button:

    input_data = pd.DataFrame({
        "age": [age],
        "sex": [sex],
        "cp": [cp],
        "trtbps": [trtbps],
        "chol": [chol],
        "fbs": [fbs],
        "restecg": [restecg],
        "thalachh": [thalachh],
        "exng": [exng],
        "oldpeak": [oldpeak],
        "slp": [slp],
        "caa": [caa],
        "thall": [thall]
    })

    prediction = model.predict(input_data)[0]

    try:
        probability = model.predict_proba(input_data)[0][1]
    except:
        probability = 0

    st.divider()
    st.subheader("Prediction Result")

    if prediction == 1:
        st.error("⚠️ High Risk of Heart Disease")
    else:
        st.success("✅ Low Risk of Heart Disease")

    # -------------------------------------------------
    # Risk Gauge
    # -------------------------------------------------

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,
        title={'text': "Heart Disease Risk (%)"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "red"},
            'steps': [
                {'range': [0, 30], 'color': "green"},
                {'range': [30, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "red"}
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    st.caption("⚠️ This tool is for educational purposes only.")
