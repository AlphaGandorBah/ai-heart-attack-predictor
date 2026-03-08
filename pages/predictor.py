import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objects as go

st.set_page_config(page_title="Heart Risk Prediction", page_icon="❤️", layout="wide")

# Load trained model
model = pickle.load(open("model.pkl","rb"))

st.title("❤️ Heart Attack Risk Prediction")

st.write("Fill in the patient's medical information below to estimate heart disease risk.")

st.markdown("---")

# Input layout
col1, col2 = st.columns(2)

with col1:

    age = st.number_input(
        "Age",
        20,100,
        help="Age of the patient in years"
    )

    sex = st.selectbox(
        "Sex",
        [0,1],
        format_func=lambda x:"Female" if x==0 else "Male",
        help="Biological sex of the patient"
    )

    cp = st.selectbox(
        "Chest Pain Type",
        [0,1,2,3],
        format_func=lambda x:[
            "Typical Angina",
            "Atypical Angina",
            "Non-Anginal Pain",
            "Asymptomatic"
        ][x],
        help="Type of chest pain experienced"
    )

    trtbps = st.number_input(
        "Resting Blood Pressure",
        80,200,
        help="Resting blood pressure in mmHg"
    )

    chol = st.number_input(
        "Cholesterol Level",
        100,600,
        help="Serum cholesterol in mg/dl"
    )

    fbs = st.selectbox(
        "Fasting Blood Sugar >120 mg/dl",
        [0,1],
        format_func=lambda x:"Yes" if x==1 else "No",
        help="Indicates if fasting blood sugar exceeds 120 mg/dl"
    )

with col2:

    restecg = st.selectbox(
        "Rest ECG Result",
        [0,1,2],
        format_func=lambda x:[
            "Normal",
            "ST-T Abnormality",
            "Left Ventricular Hypertrophy"
        ][x],
        help="Electrocardiogram result"
    )

    thalachh = st.number_input(
        "Maximum Heart Rate",
        60,220,
        help="Maximum heart rate achieved"
    )

    exng = st.selectbox(
        "Exercise Induced Angina",
        [0,1],
        format_func=lambda x:"Yes" if x==1 else "No",
        help="Chest pain during exercise"
    )

    oldpeak = st.number_input(
        "ST Depression",
        0.0,10.0,
        help="Depression induced by exercise relative to rest"
    )

    slp = st.selectbox(
        "Slope of ST Segment",
        [0,1,2],
        help="Slope of peak exercise ST segment"
    )

    caa = st.number_input(
        "Number of Major Vessels",
        0,4,
        help="Number of major vessels colored by fluoroscopy"
    )

    thall = st.selectbox(
        "Thalassemia",
        [0,1,2,3],
        help="Blood disorder indicator"
    )

st.markdown("---")

# Prediction button
if st.button("Predict Heart Risk ❤️", use_container_width=True):

    input_data = pd.DataFrame({
        'age':[age],
        'sex':[sex],
        'cp':[cp],
        'trtbps':[trtbps],
        'chol':[chol],
        'fbs':[fbs],
        'restecg':[restecg],
        'thalachh':[thalachh],
        'exng':[exng],
        'oldpeak':[oldpeak],
        'slp':[slp],
        'caa':[caa],
        'thall':[thall]
    })

    # Model prediction
    prediction = model.predict(input_data)

    # Safe probability extraction
    proba = model.predict_proba(input_data)

    if hasattr(proba,"iloc"):
        probability = proba.iloc[0,1]
    else:
        probability = proba[0][1]

    st.subheader("Prediction Result")

    if prediction[0] == 1:
        st.error("⚠️ High Risk of Heart Disease")
    else:
        st.success("✅ Low Risk of Heart Disease")

    st.write(f"Risk Probability: **{probability:.2f}**")

    # Risk Gauge Visualization
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability*100,
        title={'text':"Heart Disease Risk (%)"},
        gauge={
            'axis':{'range':[0,100]},
            'bar':{'color':"red"},
            'steps':[
                {'range':[0,30],'color':"green"},
                {'range':[30,60],'color':"yellow"},
                {'range':[60,100],'color':"red"}
            ]
        }
    ))

    st.plotly_chart(fig)

    st.markdown("---")

    st.subheader("Health Guidance")

    if probability > 0.6:

        st.warning("""
Possible elevated cardiovascular risk detected.

Recommended actions:

• Consult a cardiologist  
• Monitor blood pressure regularly  
• Reduce cholesterol intake  
• Maintain regular physical activity  
""")

    else:

        st.info("""
Risk appears relatively low.

Recommended lifestyle:

• Maintain balanced diet  
• Regular physical exercise  
• Routine medical checkups  
""")