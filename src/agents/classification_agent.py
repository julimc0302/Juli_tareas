from openai import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class InsightsAgent:
    def __init__(self, api_key=None):
        # Prioritize passed api_key, then env var
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        
        # Load the data for context with robust path resolution
        paths_to_try = [
            ("data/metrics/user_metrics.csv", "data/processed/classifications.csv"),
            ("peru-github-users/data/metrics/user_metrics.csv", "peru-github-users/data/processed/classifications.csv")
        ]
        
        found = False
        for user_path, repo_path in paths_to_try:
            if os.path.exists(user_path) and os.path.exists(repo_path):
                try:
                    self.user_metrics = pd.read_csv(user_path)
                    self.repos_classified = pd.read_csv(repo_path)
                    found = True
                    break
                except Exception:
                    continue
        
        if not found:
            self.user_metrics = pd.DataFrame()
            self.repos_classified = pd.DataFrame()

    def get_ecosystem_summary(self):
        """Prepare a comprehensive summary of the ecosystem for the LLM context."""
        if self.user_metrics.empty:
            return "No data available."
            
        # Basic stats
        total_devs = len(self.user_metrics)
        top_langs = self.user_metrics["primary_languages"].str.split(", ").explode().value_counts().head(10).to_dict()
        
        # Geographical Analysis
        # Extract city from location (simplified: take the first part before comma)
        self.user_metrics['city'] = self.user_metrics['location'].str.split(',').str[0].str.strip().str.upper()
        # Filter for known Peruvian cities/regions to avoid noise
        top_cities = self.user_metrics['city'].value_counts().head(5).to_dict()
        
        # City activity (Top cities by active developers)
        city_activity = self.user_metrics[self.user_metrics['is_active'] == True]['city'].value_counts().head(5).to_dict()

        # Industry Analysis
        top_industries = {}
        if not self.repos_classified.empty:
            top_industries = self.repos_classified["industry_name"].value_counts().head(8).to_dict()
        
        # Language-Industry Correlation
        lang_industry_corr = {}
        if not self.repos_classified.empty:
            for lang in list(top_langs.keys())[:5]:
                top_inds = self.repos_classified[self.repos_classified["language"] == lang]["industry_name"].value_counts().head(3).to_dict()
                if top_inds:
                    lang_industry_corr[lang] = top_inds
        
        # Company Analysis
        top_companies = self.user_metrics['company'].value_counts().head(5).to_dict()

        summary = {
            "total_developers": total_devs,
            "top_languages": top_langs,
            "top_cities_by_count": top_cities,
            "most_active_cities": city_activity,
            "top_companies": top_companies,
            "top_industries": top_industries,
            "language_to_industry_correlation": lang_industry_corr,
            "avg_stars_received": self.user_metrics["total_stars_received"].mean(),
            "active_developers_percentage": (self.user_metrics["is_active"].sum() / total_devs) * 100
        }
        return str(summary)

    def answer_question(self, question):
        """Answer a question using the data summary and the AI model."""
        if not self.client:
            return "Error: No OpenAI API Key provided. Please enter it in the dashboard sidebar."
            
        context = self.get_ecosystem_summary()
        
        prompt = f"""You are the 'Peru GitHub Insights Agent'. 
You have access to a dataset of 1,000 GitHub developers from Peru and their repositories.

SUMMARY OF THE DEVELOPER ECOSYSTEM:
{context}

USER QUESTION: {question}

INSTRUCTIONS:
1. Use the summary provided to answer the question accurately.
2. If the user asks for more specific details not in the summary, explain that you are analyzing the broader trends.
3. Keep the tone professional and helpful for a data analyst.
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful data analysis assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content

if __name__ == "__main__":
    # Test simulation
    # os.environ["OPENAI_API_KEY"] = "your-key-here"
    agent = InsightsAgent()
    print(agent.answer_question("What are the most popular programming languages in Peru?"))
