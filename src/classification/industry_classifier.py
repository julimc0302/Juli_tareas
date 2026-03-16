import csv
import json
import time
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use Key from .env
api_key = os.getenv("OPENAI_API_KEY")
CLIENT = OpenAI(api_key=api_key)

INDUSTRIES = {
    "A": "Agriculture, forestry and fishing",
    "B": "Mining and quarrying",
    "C": "Manufacturing",
    "D": "Electricity, gas, steam supply",
    "E": "Water supply; sewerage",
    "F": "Construction",
    "G": "Wholesale and retail trade",
    "H": "Transportation and storage",
    "I": "Accommodation and food services",
    "J": "Information and communication",
    "K": "Financial and insurance activities",
    "L": "Real estate activities",
    "M": "Professional, scientific activities",
    "N": "Administrative and support activities",
    "O": "Public administration and defense",
    "P": "Education",
    "Q": "Human health and social work",
    "R": "Arts, entertainment and recreation",
    "S": "Other service activities",
    "T": "Activities of households",
    "U": "Extraterritorial organizations"
}

def classify_repo(repo_data):
    """Call OpenAI API to classify a single repository based on CIIU code."""
    name = repo_data.get("name", "")
    description = repo_data.get("description", "")
    language = repo_data.get("language", "")
    topics_str = repo_data.get("topics", "")
    readme = repo_data.get("readme", "")
    
    prompt = f"""Analyze this GitHub repository and classify it into ONE of the following industry categories based on its potential application or the industry it serves.

REPOSITORY INFORMATION:
- Name: {name}
- Description: {description or 'No description'}
- Primary Language: {language or 'Not specified'}
- Topics: {topics_str or 'None'}
- README Snippet: {readme[:1500] if readme else 'No README'}

INDUSTRY CATEGORIES:
{json.dumps(INDUSTRIES, indent=2)}

INSTRUCTIONS:
1. Analyze the repository's purpose and functionality.
2. Consider what industry would most benefit from or use this software.
3. If it's a general-purpose programming tool (e.g., utility library, personal site, "hello world"), default to "J" (Information and communication).
4. If it's related to learning, homework, or bootcamps, use "P" (Education).

Respond strictly in JSON format matching this exact schema:
{{
  "industry_code": "X",
  "industry_name": "Full industry name",
  "confidence": "high|medium|low",
  "reasoning": "Brief explanation of why this classification was chosen"
}}
"""
    
    try:
        response = CLIENT.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert at classifying software projects by industry. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error classifying {name}: {e}")
        return {
            "industry_code": "J",
            "industry_name": "Information and communication",
            "confidence": "low",
            "reasoning": "Fallback classification due to API error."
        }

def main():
    input_file = "data/processed/repositories.csv"
    output_file = "data/processed/classifications.csv"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return
        
    # Read existing repos
    repos = []
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            repos.append(row)
            
    print(f"Loaded {len(repos)} repositories to classify.")
    
    classified_data = []
    total = len(repos)
    
    for idx, repo in enumerate(repos, 1):
        print(f"[{idx}/{total}] Classifying: {repo['full_name']} ...", end=" ", flush=True)
        
        classification = classify_repo(repo)
        
        merged_repo = repo.copy()
        merged_repo["industry_code"] = classification.get("industry_code", "J")
        merged_repo["industry_name"] = classification.get("industry_name", "Information and communication")
        merged_repo["confidence"] = classification.get("confidence", "low")
        merged_repo["reasoning"] = classification.get("reasoning", "")
        
        classified_data.append(merged_repo)
        print(f"[{merged_repo['industry_code']}]")
        
    print(f"\nCompleted classification. Saving to {output_file}...")
    
    keys = list(classified_data[0].keys())
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(classified_data)
        
    print("Classification complete!")

if __name__ == "__main__":
    main()
