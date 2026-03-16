import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.extraction.user_extractor import main as extract_users_main
from src.extraction.repo_extractor import main as extract_repos_main

def main():
    print("--- 🇵🇪 Starting Full GitHub Peru Data Extraction ---")
    
    # 1. Extract Users
    print("\n[STEP 1/2] Extracting User Profiles...")
    extract_users_main()
    
    # 2. Extract Repositories
    print("\n[STEP 2/2] Extracting Repository Details & READMEs...")
    extract_repos_main()
    
    print("\n--- ✅ Full Extraction Complete! ---")
    print("Files saved to: data/processed/users.csv and data/processed/repositories.csv")

if __name__ == "__main__":
    main()
