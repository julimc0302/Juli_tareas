import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Add root to path for imports
sys.path.append(os.getcwd())
from app.components.data_loader import load_processed_data
from app.components.charts import add_footer

st.set_page_config(page_title="Developers", page_icon="👥", layout="wide")

st.title("👥 Developer Explorer")

user_metrics, repos_classified = load_processed_data()

if user_metrics is not None and not user_metrics.empty:
    # --- Sidebar Filters ---
    st.sidebar.header("Filter Developers")
    
    search_query = st.sidebar.text_input("Search login/name/company")
    
    min_stars = st.sidebar.slider(
        "Minimum total stars",
        min_value=0,
        max_value=int(user_metrics["total_stars_received"].max()),
        value=0,
    )
    
    active_only = st.sidebar.checkbox("Show only active developers")
    
    # Get all unique languages from the comma-separated string
    all_langs = sorted(user_metrics["primary_languages"].str.split(", ").explode().dropna().unique())
    selected_languages = st.sidebar.multiselect("Filter by Language", all_langs)

    # Sort options
    sort_candidates = [
        col for col in user_metrics.columns 
        if pd.api.types.is_numeric_dtype(user_metrics[col])
    ]
    default_sort = "impact_score" if "impact_score" in sort_candidates else sort_candidates[0]
    sort_by = st.sidebar.selectbox("Sort by metric", options=sort_candidates, index=sort_candidates.index(default_sort))
    sort_desc = st.sidebar.checkbox("Sort descending", value=True)

    # --- Apply Filters ---
    filtered = user_metrics[user_metrics["total_stars_received"] >= min_stars]
    
    if active_only:
        filtered = filtered[filtered["is_active"] == True]
    
    if selected_languages:
        # Check if any selected language is present in the primary_languages string
        pattern = '|'.join([f"\\b{lang}\\b" for lang in selected_languages])
        filtered = filtered[filtered["primary_languages"].str.contains(pattern, case=False, na=False)]
        
    if search_query:
        mask = (filtered["login"].str.contains(search_query, case=False, na=False) | 
                filtered["name"].fillna("").str.contains(search_query, case=False, na=False) |
                filtered["company"].fillna("").str.contains(search_query, case=False, na=False))
        filtered = filtered[mask]

    filtered = filtered.sort_values(sort_by, ascending=not sort_desc)

    st.write(f"Showing **{len(filtered)}** developers")

    # --- Charts ---
    if not filtered.empty:
        fig = px.bar(
            filtered.nlargest(15, "impact_score").sort_values("impact_score"),
            x="impact_score",
            y="login",
            orientation="h",
            title="Top 15 Developers by Impact (Current Filters)",
            color="impact_score",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- Data Table ---
    show_cols = [
        "login", "name", "company", "total_repos", "total_stars_received", 
        "followers", "impact_score", "h_index", "primary_languages", "is_active"
    ]
    show_cols = [c for c in show_cols if c in filtered.columns]
    st.dataframe(filtered[show_cols], use_container_width=True, hide_index=True)

    # --- Developer Detail ---
    st.divider()
    st.subheader("🔍 Developer Detail")
    if filtered.empty:
        st.info("No developers available with current filters.")
    else:
        selected_login = st.selectbox("Select developer to view details", options=filtered["login"].tolist())
        detail = filtered[filtered["login"] == selected_login].iloc[0]
        
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("Impact Score", f"{detail.get('impact_score', 0):,.2f}")
        m_col2.metric("Followers", f"{int(detail.get('followers', 0)):,}")
        m_col3.metric("Total Stars", f"{int(detail.get('total_stars_received', 0)):,}")
        m_col4.metric("h-index", f"{int(detail.get('h_index', 0))}")
        
        st.dataframe(detail.to_frame(name="Value"), use_container_width=True)

    # --- Export ---
    st.download_button(
        label="Export Filtered List as CSV",
        data=filtered.to_csv(index=False),
        file_name="peru_developers_filtered.csv",
        mime="text/csv",
    )

    # Add Branding Footer
    add_footer()
else:
    st.warning("No data found. Please run the extraction scripts first.")
