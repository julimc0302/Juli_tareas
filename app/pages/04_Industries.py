import streamlit as st
import pandas as pd
import sys
import os
import plotly.express as px

sys.path.append(os.getcwd())
from app.components.data_loader import load_processed_data

st.set_page_config(page_title="Industry Analysis", layout="wide")

st.title("🏭 Industry Analysis")

user_metrics, repos_classified = load_processed_data()

if repos_classified is not None:
    # Industry Distribution
    st.subheader("Distribution of Repositories by Industry (CIIU)")
    
    industry_counts = repos_classified["industry_name"].value_counts().reset_index()
    industry_counts.columns = ["Industry", "Count"]
    
    fig = px.pie(industry_counts, values="Count", names="Industry", hole=0.3)
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Repositories per Industry")
        selected_ind = st.selectbox("Select Industry", sorted(repos_classified["industry_name"].unique()))
        top_in_industry = repos_classified[repos_classified["industry_name"] == selected_ind].nlargest(5, "stargazers_count")
        st.table(top_in_industry[["name", "stargazers_count", "language"]])
        
    with col2:
        st.subheader("Developer Specialization")
        st.markdown("Most common industry per developer based on their repository portfolio.")
        # This requires counting industries per user from user_metrics if we saved it there
        if "primary_industry" in user_metrics.columns:
            spec_counts = user_metrics["primary_industry"].value_counts().reset_index()
            spec_counts.columns = ["Industry Code", "Count"]
            st.bar_chart(spec_counts.set_index("Industry Code"))
        else:
            st.info("Primary industry mapping not found in user metrics.")
