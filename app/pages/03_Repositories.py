import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.getcwd())
from app.components.data_loader import load_processed_data
from app.components.charts import add_footer

st.set_page_config(page_title="Repository Browser", layout="wide")

st.title("📂 Repository Browser")

user_metrics, repos_classified = load_processed_data()

if repos_classified is not None:
    st.markdown("Explore and filter the 1,000+ repositories collected from Peru.")
    
    # Filters
    col_f1, col_f2, col_f3 = st.columns(3)
    
    industries = ["All"] + sorted(repos_classified["industry_name"].unique().tolist())
    selected_industry = col_f1.selectbox("Filter by Industry", industries)
    
    languages = ["All"] + sorted(repos_classified["language"].dropna().unique().tolist())
    selected_lang = col_f2.selectbox("Filter by Language", languages)
    
    min_stars = col_f3.number_input("Min Stars", 0, int(repos_classified["stargazers_count"].max()), 0)
    
    # Search
    search_query = st.text_input("Search in name or description")
    
    filtered_df = repos_classified.copy()
    
    if selected_industry != "All":
        filtered_df = filtered_df[filtered_df["industry_name"] == selected_industry]
    if selected_lang != "All":
        filtered_df = filtered_df[filtered_df["language"] == selected_lang]
    if min_stars > 0:
        filtered_df = filtered_df[filtered_df["stargazers_count"] >= min_stars]
    if search_query:
        filtered_df = filtered_df[
            filtered_df["name"].str.contains(search_query, case=False, na=False) |
            filtered_df["description"].str.contains(search_query, case=False, na=False)
        ]
        
    st.write(f"Showing **{len(filtered_df)}** repositories")
    
    # Display table with relevant columns
    display_cols = ["name", "industry_name", "language", "stargazers_count", "forks_count", "description", "full_name"]
    st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)
    
    # Detail View
    if len(filtered_df) > 0:
        st.divider()
        st.subheader("Repository Detail Selection")
        selected_repo_name = st.selectbox("Select a repository to see full README snippet and classification reasoning", filtered_df["full_name"])
        
        repo_detail = repos_classified[repos_classified["full_name"] == selected_repo_name].iloc[0]
        
        d_col1, d_col2 = st.columns([1, 1])
        with d_col1:
            st.markdown(f"**Classification:** {repo_detail['industry_name']} ({repo_detail['industry_code']})")
            st.markdown(f"**Confidence:** {repo_detail['confidence']}")
            st.markdown(f"**Reasoning:** {repo_detail['reasoning']}")
        with d_col2:
            st.markdown("**README Snippet:**")
            st.text_area("", repo_detail["readme"] if pd.notna(repo_detail["readme"]) else "No README available", height=200)

    # Add Branding Footer
    add_footer()
