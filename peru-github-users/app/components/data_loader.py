import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_processed_data():
    # Robust path resolution for local and cloud deployment
    paths_to_try = [
        ("data/metrics/user_metrics.csv", "data/processed/classifications.csv"),
        ("peru-github-users/data/metrics/user_metrics.csv", "peru-github-users/data/processed/classifications.csv")
    ]
    
    for user_path, repo_path in paths_to_try:
        if os.path.exists(user_path) and os.path.exists(repo_path):
            try:
                user_metrics = pd.read_csv(user_path)
                repos_classified = pd.read_csv(repo_path)
                return user_metrics, repos_classified
            except Exception:
                continue
                
    st.error("Data files not found. Ensure you are running streamlit from the project root and data is available.")
    return None, None
