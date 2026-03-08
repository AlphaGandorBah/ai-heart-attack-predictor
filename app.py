import streamlit as st

st.set_page_config(
    page_title="AI Heart Risk Predictor",
    page_icon="❤️",
    layout="wide"
)

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

col1, col2 = st.columns([1,2])

with col1:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712027.png",
        width=200
    )

with col2:
    st.title("AI Heart Attack Risk Predictor")
    st.write("""
    A machine learning powered system designed to estimate heart disease risk using clinical indicators.
    """)

st.markdown("---")

st.header("Why This System Matters")

st.write("""
Heart disease is among the **leading causes of death globally**.  
Early detection helps improve patient outcomes.

This application demonstrates how **Artificial Intelligence and Machine Learning** can assist healthcare professionals in assessing cardiovascular risk.
""")

st.markdown("---")

st.header("Medical Indicators Used")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    - Age  
    - Sex  
    - Chest Pain Type  
    - Resting Blood Pressure  
    - Cholesterol
    """)

with col2:
    st.markdown("""
    - Fasting Blood Sugar  
    - Rest ECG  
    - Maximum Heart Rate  
    - Exercise Induced Angina  
    - ST Depression
    """)

st.markdown("---")

st.subheader("Start Heart Risk Prediction")

st.write("Click below to enter patient information and generate a risk prediction.")

if st.button("Start Prediction ❤️", use_container_width=True):
    st.switch_page("pages/predictor.py")

st.info("This application is for educational purposes and should not replace medical consultation.")