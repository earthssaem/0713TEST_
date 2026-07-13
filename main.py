import streamlit as st
import pandas as pd

# Load data with requested encoding
@st.cache_data
def load_data():
    df_seoul = pd.read_csv("서울_기온.csv", encoding="cp949")
    df_yang = pd.read_csv("양평_기온.csv", encoding="cp949")
    df_power = pd.read_csv("전력수요.csv", encoding="cp949")
    # ... perform joins on '일시' column ...
    return merged_df

st.title("🏙️ Seoul UHI & Energy Analysis")
tab1, tab2 = st.tabs(["Heat Island Analysis", "Power Demand Link"])

with tab1:
    st.header("Urban Heat Island (UHI)")
    # Implement Line chart (Seoul vs Yangpyeong)
    # Implement Bar chart (Hourly UHI Delta)
    
with tab2:
    st.header("Power Demand Correlation")
    # Implement Scatter plot (Temp vs MWh)
    # Implement Monthly Demand patterns

I've ensured the HTML slides utilize the exact 2025 parameters you specified. Let me know if you'd like to adjust any of the data visualizations or layouts!
