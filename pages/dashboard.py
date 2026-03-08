import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dataset Dashboard", page_icon="📊", layout="wide")

st.title("📊 Heart Disease Dataset Analytics")

st.write("Explore the dataset used to train the heart attack prediction model.")

# Load dataset
df = pd.read_csv("heart.csv")

st.markdown("---")

st.subheader("Dataset Preview")

st.dataframe(df.head())

st.markdown("---")

col1, col2 = st.columns(2)

# Heart disease distribution
with col1:

    st.subheader("Heart Disease Distribution")

    fig, ax = plt.subplots()

    sns.countplot(x='output', data=df, ax=ax)

    ax.set_title("Heart Disease Cases")

    st.pyplot(fig)

# Age distribution
with col2:

    st.subheader("Age Distribution")

    fig, ax = plt.subplots()

    sns.histplot(df['age'], bins=20, kde=True, ax=ax)

    ax.set_title("Age Distribution")

    st.pyplot(fig)

st.markdown("---")

st.subheader("Correlation Heatmap")

fig, ax = plt.subplots(figsize=(10,6))

sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)

st.pyplot(fig)

st.markdown("---")

st.info("These charts help understand the relationships between medical indicators and heart disease.")