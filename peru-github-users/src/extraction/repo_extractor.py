import requests
import time
import csv
import os
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use PAT from .env
TOKEN = os.getenv('GITHUB_TOKEN')
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_user_repos(username):
    """Fetch all public repositories for a specific user."""
    repos = []
    page = 1
    per_page = 100
    
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page={per_page}&page={page}"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 403:
            reset_time = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
            sleep_time = max(reset_time - time.time(), 0) + 1
            print(f"Rate limited on repo query. Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)
            continue
            
        if response.status_code == 404:
            break
            
        response.raise_for_status()
        page_repos = response.json()
        
        if not page_repos:
            break
            
        repos.extend(page_repos)
        
        if "next" not in response.links:
            break
            
        page += 1
        
    return repos

def get_repo_languages(languages_url):
    """Fetch the languages used in a repository."""
    while True:
        response = requests.get(languages_url, headers=HEADERS)
        
        if response.status_code == 403:
            reset_time = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
            sleep_time = max(reset_time - time.time(), 0) + 1
            time.sleep(sleep_time)
            continue
            
        if response.status_code != 200:
            return ""
            
        return ", ".join(list(response.json().keys()))

def get_repo_readme(owner, repo_name):
    """Fetch the README content for a repository."""
    url = f"https://api.github.com/repos/{owner}/{repo_name}/readme"
    
    while True:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 403:
            reset_time = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
            sleep_time = max(reset_time - time.time(), 0) + 1
            time.sleep(sleep_time)
            continue
            
        if response.status_code == 404:
            return "" # No README
            
        if response.status_code == 200:
            data = response.json()
            if "content" in data:
                try:
                    # Content is base64 encoded
                    decoded = base64.b64decode(data["content"]).decode('utf-8', errors='ignore')
                    return " ".join(decoded.split())[:1000]
                except Exception:
                    return ""
        
        return ""

def main():
    # Use paths relative to project root
    input_file = "data/processed/users.csv"
    output_file = "data/processed/repositories.csv"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Ensure you are running from the project root.")
        return
        
    # Read the 1000 users we found
    users = []
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            users.append(row["login"])
            
    print(f"Loaded {len(users)} users. Beginning repository extraction...")
    
    all_repos_data = []
    repos_collected = 0
    target_repos = 1000 
    
    for idx, username in enumerate(users, 1):
        if repos_collected >= target_repos:
            break
            
        print(f"[{idx}/{len(users)}] Fetching repos for user {username}... (Total so far: {repos_collected})")
        user_repos = get_user_repos(username)
        
        for repo in user_repos:
            if repo.get("fork"):
                continue
                
            owner = repo["owner"]["login"]
            name = repo["name"]
            
            languages_str = get_repo_languages(repo["languages_url"])
            readme_text = get_repo_readme(owner, name)
            
            repo_data = {
                "id": repo["id"],
                "name": name,
                "full_name": repo.get("full_name", ""),
                "description": repo.get("description", ""),
                "topics": ", ".join(repo.get("topics", [])),
                "language": repo.get("language", ""),
                "languages": languages_str,
                "stargazers_count": repo.get("stargazers_count", 0),
                "forks_count": repo.get("forks_count", 0),
                "watchers_count": repo.get("watchers_count", 0),
                "open_issues_count": repo.get("open_issues_count", 0),
                "created_at": repo.get("created_at", ""),
                "updated_at": repo.get("updated_at", ""),
                "pushed_at": repo.get("pushed_at", ""),
                "license": repo.get("license", {}).get("name", "") if repo.get("license") else "",
                "readme": readme_text
            }
            
            all_repos_data.append(repo_data)
            repos_collected += 1
            time.sleep(0.05)
            
    if not all_repos_data:
        print("Failed to fetch any repositories.")
        return
        
    print(f"\nSuccessfully collected {len(all_repos_data)} repositories.")
    
    keys = list(all_repos_data[0].keys())
    
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_repos_data)
        
    print(f"Data successfully saved to {output_file}")

if __name__ == "__main__":
    main()
