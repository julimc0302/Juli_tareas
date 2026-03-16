import streamlit as st
import pandas as pd
import sys
import os
from collections import Counter

sys.path.append(os.getcwd())
from app.components.data_loader import load_processed_data

st.set_page_config(page_title="Language Analytics", layout="wide")

st.title("💻 Language Analytics")

user_metrics, repos_classified = load_processed_data()

if repos_classified is not None:
    st.subheader("Programming Language Distribution")
    
    lang_counts = repos_classified["language"].value_counts().reset_index()
    lang_counts.columns = ["Language", "Count"]
    
    st.bar_chart(lang_counts.set_index("Language"))
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Developers per Language")
        selected_lang = st.selectbox("Select a Language", sorted(repos_classified["language"].dropna().unique()))
        
        # We need to find users who have this language in their primary list
        top_devs = user_metrics[user_metrics["primary_languages"].str.contains(selected_lang, na=False)].nlargest(10, "impact_score")
        st.dataframe(top_devs[["login", "impact_score", "total_stars_received"]], use_container_width=True)
        
    with col2:
        st.subheader("Language by Industry Correlation")
        # Show which languages are most common in a specific industry
        selected_ind = st.selectbox("Select an Industry", sorted(repos_classified["industry_name"].unique()))
        ind_langs = repos_classified[repos_classified["industry_name"] == selected_ind]["language"].value_counts().head(5)
        st.write(f"Top 5 languages in **{selected_ind}**:")
        st.table(ind_langs)
