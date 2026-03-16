import streamlit as st
import pandas as pd
import sys
import os

# Add root to path for imports
sys.path.append(os.getcwd())
from app.components.data_loader import load_processed_data

st.set_page_config(page_title="Ecosystem Overview", layout="wide")

st.title("📊 Ecosystem Overview")

user_metrics, repos_classified = load_processed_data()

if user_metrics is not None:
    # Key Statistics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Developers", len(user_metrics))
    col2.metric("Total Repositories", len(repos_classified))
    col3.metric("Total Stars", int(user_metrics["total_stars_received"].sum()))
    col4.metric("Avg Repos/User", round(user_metrics["total_repos"].mean(), 2))

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Top 10 Developers by Impact Score")
        top_devs = user_metrics.nlargest(10, "impact_score")[["login", "impact_score", "total_stars_received", "followers"]]
        st.dataframe(top_devs, use_container_width=True)

    with col_right:
        st.subheader("Top 10 Repositories by Stars")
        top_repos = repos_classified.nlargest(10, "stargazers_count")[["name", "stargazers_count", "language", "industry_name"]]
        st.dataframe(top_repos, use_container_width=True)

    st.subheader("Account Creation Trend")
    # Convert created_at to datetime and extract year
    user_metrics['year'] = pd.to_datetime(user_metrics['created_at']).dt.year
    trend = user_metrics['year'].value_counts().sort_index()
    st.line_chart(trend)
