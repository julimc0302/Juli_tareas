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
        
        # Load the data for context
        try:
            self.user_metrics = pd.read_csv("data/metrics/user_metrics.csv")
            self.repos_classified = pd.read_csv("data/processed/classifications.csv")
        except Exception as e:
            print(f"Error loading data for agent: {e}")
            self.user_metrics = pd.DataFrame()
            self.repos_classified = pd.DataFrame()

    def get_ecosystem_summary(self):
        """Prepare a summary of the ecosystem for the LLM context."""
        if self.user_metrics.empty:
            return "No data available."
            
        summary = {
            "total_developers": len(self.user_metrics),
            "top_languages": self.user_metrics["primary_languages"].str.split(", ").explode().value_counts().head(5).to_dict(),
            "avg_stars": self.user_metrics["total_stars_received"].mean(),
            "top_industry": self.repos_classified["industry_name"].value_counts().idxmax(),
            "active_percentage": (self.user_metrics["is_active"].sum() / len(self.user_metrics)) * 100
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
