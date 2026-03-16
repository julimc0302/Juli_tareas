import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="GitHub Peru Analytics",
    page_icon="🇵🇪",
    layout="wide"
)

@st.cache_data
def load_data():
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
                
    st.error("Data files not found. Please run the collection and classification scripts first.")
    return None, None

def main():
    st.sidebar.title("Configuration")
    openai_key = st.sidebar.text_input("OpenAI API Key", type="password", help="Enter your key to use the AI Insights Agent.")
    if openai_key:
        st.session_state.openai_api_key = openai_key
    
    st.sidebar.divider()
    st.sidebar.title("Navigation")
    st.sidebar.info("Use the sidebar to explore different aspects of the Peruvian GitHub ecosystem.")
    
    st.title("🇵🇪 GitHub Peru Developer Ecosystem")
    st.markdown("""
    Welcome to the **GitHub Peru Analytics** dashboard. 
    This project analyzes the developer landscape in Peru, classifying 1,000+ repositories into industrial sectors 
    and identifying key technical trends.
    """)
    
    user_metrics, repos_classified = load_data()
    
    if user_metrics is not None:
        st.success(f"Successfully loaded data for {len(user_metrics)} developers and {len(repos_classified)} repositories.")
        
        # Dashboard Overview Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Developers", len(user_metrics))
        col2.metric("Total Repositories", len(repos_classified))
        col3.metric("Total Stars", int(user_metrics["total_stars_received"].sum()))
        col4.metric("Active Developers (%)", f"{(user_metrics['is_active'].sum() / len(user_metrics) * 100):.1f}%")

        st.info("👈 Navigate to different pages in the sidebar to view detailed analysis.")

        # Personal Branding Footer
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

if __name__ == "__main__":
    main()
