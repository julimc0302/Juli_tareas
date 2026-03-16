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
            
        import json
        
        # Basic stats
        total_devs = len(self.user_metrics)
        # Convert Series/ValueCounts to pure Python dicts and handle np.float64
        top_langs = self.user_metrics["primary_languages"].str.split(", ").explode().value_counts().head(10).to_dict()
        top_langs = {str(k): int(v) for k, v in top_langs.items()}
        
        # Geographical Analysis
        # Handle possible NaN in location
        self.user_metrics['city'] = self.user_metrics['location'].fillna('DESCONOCIDO').str.split(',').str[0].str.strip().str.upper()
        top_cities = self.user_metrics['city'].value_counts().head(8).to_dict()
        top_cities = {str(k): int(v) for k, v in top_cities.items()}
        
        # Activity filter
        active_mask = (self.user_metrics['is_active'] == True) | (self.user_metrics['is_active'] == 'True') | (self.user_metrics['is_active'] == 1)
        city_activity = self.user_metrics[active_mask]['city'].value_counts().head(10).to_dict()
        city_activity = {str(k): int(v) for k, v in city_activity.items()}

        # Industry Analysis
        top_industries = {}
        if not self.repos_classified.empty:
            top_industries = self.repos_classified["industry_name"].value_counts().head(10).to_dict()
            top_industries = {str(k): int(v) for k, v in top_industries.items()}
        
        # Calculate Language-Industry Correlation
        lang_industry_corr = {}
        if not self.repos_classified.empty:
            for lang in list(top_langs.keys())[:5]:
                top_inds = self.repos_classified[self.repos_classified["language"] == lang]["industry_name"].value_counts().head(3).to_dict()
                if top_inds:
                    lang_industry_corr[lang] = {str(k): int(v) for k, v in top_inds.items()}
        
        # Company Analysis
        top_companies = self.user_metrics['company'].value_counts().head(8).to_dict()
        top_companies = {str(k): int(v) for k, v in top_companies.items() if pd.notna(k) and k != ''}

        summary = {
            "metadata": {
                "dataset_size": total_devs,
                "scope": "Top 1,000 developers from Peru on GitHub"
            },
            "technical_stats": {
                "top_languages": top_langs,
                "avg_stars_per_developer": round(float(self.user_metrics["total_stars_received"].mean()), 2),
                "overall_active_percentage_in_sample": round(float((active_mask.sum() / total_devs) * 100), 2)
            },
            "geographical_insights": {
                "top_cities_by_developer_count": top_cities,
                "cities_with_active_developers": city_activity,
                "most_active_city_factual": max(city_activity, key=city_activity.get) if city_activity else "LIMA"
            },
            "industrial_insights": {
                "top_industries": top_industries,
                "language_to_industry_correlation": lang_industry_corr
            },
            "professional_insights": {
                "top_companies": top_companies
            }
        }
        return json.dumps(summary, indent=2)

    def answer_question(self, question):
        """Answer a question using the data summary and the AI model."""
        if not self.client:
            return "Error: No OpenAI API Key provided. Please enter it in the dashboard sidebar."
            
        context = self.get_ecosystem_summary()
        
        prompt = f"""You are the 'Peru GitHub Insights Agent'. 
You have access to a detailed summary of a dataset containing the top 1,000 GitHub developers from Peru.

DATASET SUMMARY (JSON FORMAT - USE THIS):
{context}

USER QUESTION: {question}

CRITICAL RULES:
1. USE DATA: Always refer to specific numbers or rankings from the SUMMARY.
2. GEOGRAPHY: If asked about cities, check 'geographical_insights'. Even if LIMA is expected, use whatever city has the most 'active_developers'.
3. ACCURACY: If active_percentage is 0.5, it means 'Cero punto cinco por ciento (0.5%)'. DO NOT confuse it with 50%.
4. LIMITATIONS: If the user asks for data definitively NOT in the JSON, say you only have access to the provided summary of 1,000 developers.
5. LANGUAGE: Respond in the same language as the user (usually Spanish).
6. FORMAT: Use bold text for key insights and stats.
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un experto analista de datos del ecosistema tecnológico en Perú. Tu objetivo es dar respuestas cortas pero llenas de datos reales del resumen proporcionado."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content

if __name__ == "__main__":
    # Test simulation
    # os.environ["OPENAI_API_KEY"] = "your-key-here"
    agent = InsightsAgent()
    print(agent.answer_question("What are the most popular programming languages in Peru?"))
