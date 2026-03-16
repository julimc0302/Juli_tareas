import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.getcwd())
from app.components.data_loader import load_processed_data

st.set_page_config(page_title="Developer Explorer", layout="wide")

st.title("👤 Developer Explorer")

user_metrics, repos_classified = load_processed_data()

if user_metrics is not None:
    st.markdown("Search and filter through the 1,000 developers identified in Peru.")
    
    # Search functionality
    search_query = st.text_input("Search by username, name, or company")
    
    filtered_df = user_metrics.copy()
    if search_query:
        filtered_df = filtered_df[
            filtered_df["login"].str.contains(search_query, case=False, na=False) |
            filtered_df["name"].str.contains(search_query, case=False, na=False) |
            filtered_df["company"].str.contains(search_query, case=False, na=False)
        ]
        
    # Filters
    col_f1, col_f2 = st.columns(2)
    min_stars = col_f1.slider("Minimum Stars Received", 0, int(user_metrics["total_stars_received"].max()), 0)
    is_active_only = col_f2.checkbox("Show only active developers (last push < 90 days)")
    
    filtered_df = filtered_df[filtered_df["total_stars_received"] >= min_stars]
    if is_active_only:
        filtered_df = filtered_df[filtered_df["is_active"] == True]
    
    st.write(f"Showing **{len(filtered_df)}** developers")
    
    st.dataframe(
        filtered_df.drop(columns=['year'], errors='ignore'), 
        use_container_width=True
    )
    
    # CSV Export
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download results as CSV",
        csv,
        "peru_developers_filtered.csv",
        "text/csv"
    )
