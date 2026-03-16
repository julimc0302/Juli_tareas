import pandas as pd
import json
import os

def main():
    print("Generating ecosystem metrics summary...")
    
    try:
        user_metrics = pd.read_csv("data/metrics/user_metrics.csv")
        repos = pd.read_csv("data/processed/classifications.csv")
        
        metrics = {
            "total_users": len(user_metrics),
            "total_repositories": len(repos),
            "top_industries": repos["industry_name"].value_counts().head(5).to_dict(),
            "top_languages": user_metrics["primary_languages"].str.split(", ").explode().value_counts().head(5).to_dict(),
            "average_h_index": float(user_metrics["h_index"].mean()),
            "active_users_pct": float((user_metrics["is_active"].sum() / len(user_metrics)) * 100),
            "generation_date": pd.Timestamp.now().isoformat()
        }
        
        output_path = "data/metrics/ecosystem_metrics.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=4)
            
        print(f"Ecosystem metrics saved to {output_path}")
        
    except Exception as e:
        print(f"Error generating metrics: {e}")

if __name__ == "__main__":
    main()
