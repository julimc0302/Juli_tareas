"""Reusable Plotly chart builders for the Streamlit dashboard."""

import pandas as pd
import plotly.express as px

def plot_top_developers(users_df: pd.DataFrame, top_n: int = 10):
    """Bar chart for top developers by impact score."""
    top = users_df.nlargest(top_n, "impact_score")[["login", "impact_score"]]
    fig = px.bar(
        top.sort_values("impact_score"),
        x="impact_score",
        y="login",
        orientation="h",
        title=f"Top {top_n} Developers by Impact",
        color="impact_score",
        color_continuous_scale="Blues",
    )
    fig.update_layout(showlegend=False)
    return fig

def plot_industry_distribution(classifications_df: pd.DataFrame, top_n: int = 10):
    """Pie chart for industry distribution."""
    if classifications_df.empty or "industry_name" not in classifications_df.columns:
        return None
    counts = classifications_df["industry_name"].value_counts().head(top_n)
    fig = px.pie(
        values=counts.values,
        names=counts.index,
        title=f"Top {top_n} Industries",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig

def plot_language_distribution(repos_df: pd.DataFrame, top_n: int = 15):
    """Horizontal bar chart for top programming languages."""
    if repos_df.empty or "language" not in repos_df.columns:
        return None
    counts = repos_df["language"].dropna().value_counts().head(top_n)
    fig = px.bar(
        x=counts.values,
        y=counts.index,
        orientation="h",
        title=f"Top {top_n} Languages",
        labels={"x": "Repositories", "y": "Language"},
        color=counts.values,
        color_continuous_scale="Viridis",
    )
    fig.update_layout(showlegend=False)
    fig.update_yaxes(autorange="reversed")
    return fig

def plot_geographic_distribution(users_df: pd.DataFrame):
    """Scatter map for geographic distribution of developers in Peru."""
    if "location" not in users_df.columns:
        return None

    city_reference = {
        "lima": {"city": "Lima", "lat": -12.0464, "lon": -77.0428},
        "arequipa": {"city": "Arequipa", "lat": -16.4090, "lon": -71.5375},
        "trujillo": {"city": "Trujillo", "lat": -8.1118, "lon": -79.0287},
        "cusco": {"city": "Cusco", "lat": -13.5319, "lon": -71.9675},
        "piura": {"city": "Piura", "lat": -5.1945, "lon": -80.6328},
        "chiclayo": {"city": "Chiclayo", "lat": -6.7714, "lon": -79.8409},
        "huancayo": {"city": "Huancayo", "lat": -12.0651, "lon": -75.2049},
        "iquitos": {"city": "Iquitos", "lat": -3.7437, "lon": -73.2516},
        "puno": {"city": "Puno", "lat": -15.8402, "lon": -70.0219},
        "peru": {"city": "Other Peru", "lat": -9.1900, "lon": -75.0152},
    }

    matched_rows = []
    for raw_location in users_df["location"].fillna("").astype(str):
        text = raw_location.lower()
        for keyword, city_data in city_reference.items():
            if keyword in text:
                matched_rows.append(city_data.copy())
                break

    if not matched_rows:
        return None

    geo_df = pd.DataFrame(matched_rows)
    geo_counts = geo_df.groupby(["city", "lat", "lon"]).size().reset_index(name="developers")

    fig = px.scatter_geo(
        geo_counts,
        lat="lat",
        lon="lon",
        size="developers",
        color="developers",
        hover_name="city",
        hover_data={"lat": False, "lon": False, "developers": True},
        projection="natural earth",
        title="Geographic Map of Developers (Peru)",
        scope="south america",
        color_continuous_scale="Blues"
    )
    fig.update_layout(showlegend=False)
    return fig

def add_footer():
    """Add personal branding footer to the page."""
    import streamlit as st
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            right: 15px;
            bottom: 10px;
            color: #888;
            font-size: 0.9rem;
            z-index: 1000;
        }
        </style>
        <div class="footer">
            Julia Massa Coronel 🇵🇪
        </div>
        """,
        unsafe_allow_html=True
    )
