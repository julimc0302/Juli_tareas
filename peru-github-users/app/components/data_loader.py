import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_processed_data():
    # Use paths relative to the root where streamlit run is called
    try:
        user_metrics = pd.read_csv("data/metrics/user_metrics.csv")
        repos_classified = pd.read_csv("data/processed/classifications.csv")
        return user_metrics, repos_classified
    except FileNotFoundError:
        st.error("Data files not found. Ensure you are running streamlit from the project root and data is processed.")
        return None, None
