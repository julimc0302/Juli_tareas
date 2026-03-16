import streamlit as st
import pandas as pd
import sys
import os

# Add root to path for imports
sys.path.append(os.getcwd())
from app.components.data_loader import load_processed_data
from app.components.charts import (
    plot_geographic_distribution,
    plot_industry_distribution,
    plot_language_distribution,
    plot_top_developers,
    add_footer
)

st.set_page_config(page_title="Ecosystem Overview", layout="wide", page_icon="📊")

st.title("📊 Ecosystem Overview")

user_metrics, repos_classified = load_processed_data()

if user_metrics is not None and not user_metrics.empty:
    # 1. Key Statistics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Developers", f"{len(user_metrics):,}")
    col2.metric("Total Repositories", f"{len(repos_classified):,}")
    col3.metric("Total Stars", f"{int(user_metrics['total_stars_received'].sum()):,}")
    
    # Calculate active %
    active_count = user_metrics['is_active'].sum()
    active_pct = (active_count / len(user_metrics)) * 100
    col4.metric("Active Developers", f"{active_pct:.1f}%")

    st.divider()

    # 2. Top Charts (Row 1)
    left, right = st.columns(2)
    with left:
        st.plotly_chart(plot_top_developers(user_metrics), use_container_width=True)
    with right:
        st.plotly_chart(plot_industry_distribution(repos_classified), use_container_width=True)

    # 3. Languages Chart
    st.plotly_chart(plot_language_distribution(repos_classified), use_container_width=True)

    # 4. Activity Timeline
    if "created_at" in repos_classified.columns:
        repos_trend = repos_classified.copy()
        repos_trend["created_at"] = pd.to_datetime(repos_trend["created_at"], errors="coerce")
        repos_trend = repos_trend.dropna(subset=["created_at"])
        if not repos_trend.empty:
            trend_df = (
                repos_trend.assign(month=repos_trend["created_at"].dt.to_period("M").dt.to_timestamp())
                .groupby("month")
                .size()
                .reset_index(name="repositories")
            )
            st.subheader("Activity Timeline (New Repositories)")
            st.line_chart(trend_df.set_index("month")["repositories"])

    # 5. Top Repositories Table
    st.subheader("Top 10 Repositories by Stars")
    top_repos = repos_classified.nlargest(10, "stargazers_count")[["name", "stargazers_count", "language", "industry_name"]]
    st.dataframe(top_repos, use_container_width=True, hide_index=True)

    # 6. Geographic Map
    geo_fig = plot_geographic_distribution(user_metrics)
    if geo_fig:
        st.plotly_chart(geo_fig, use_container_width=True)

    # Add Branding Footer
    add_footer()
else:
    st.warning("No data found. Please run the extraction scripts first.")
