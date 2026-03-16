import pandas as pd
import json
import os

base_path = r"C:\Users\Julia\Downloads\sumer school\python\Tareas2\Juli_tareas"
users_path = os.path.join(base_path, "data", "processed", "users.csv")
repos_path = os.path.join(base_path, "data", "processed", "repositories.csv")
class_path = os.path.join(base_path, "data", "processed", "classifications.csv")

def get_metrics():
    print("--- README Metrics Extraction ---")
    
    # 1. Counts
    users_df = pd.read_csv(users_path)
    repos_df = pd.read_csv(repos_path)
    class_df = pd.read_csv(class_path)
    
    print(f"Total Users: {len(users_df)}")
    print(f"Total Repositories: {len(repos_df)}")
    
    # 2. Top Languages
    top_langs = repos_df['language'].value_counts().head(5)
    print("\nTop 5 Languages:")
    print(top_langs)
    
    # 3. Industry Distribution
    top_industries = class_df['industry_name'].value_counts().head(5)
    print("\nTop 5 Industries:")
    print(top_industries)
    
    # 4. Activity
    users_df['created_at'] = pd.to_datetime(users_df['created_at'])
    start_date = users_df['created_at'].min().strftime('%Y-%m-%d')
    end_date = users_df['created_at'].max().strftime('%Y-%m-%d')
    print(f"\nData Period: {start_date} to {end_date}")

if __name__ == "__main__":
    get_metrics()
