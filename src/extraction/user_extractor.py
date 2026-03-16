import requests
import time
import csv

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use PAT from .env
TOKEN = os.getenv('GITHUB_TOKEN')
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def search_users(query, max_users=1000):
    """Search for users up to max_users."""
    users = []
    page = 1
    per_page = 100
    
    while len(users) < max_users:
        url = f"https://api.github.com/search/users?q={query}&per_page={per_page}&page={page}"
        print(f"Searching page {page}...")
        
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 403:
            reset_time = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
            sleep_time = max(reset_time - time.time(), 0) + 1
            print(f"Rate limited on search. Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)
            continue
            
        response.raise_for_status()
        data = response.json()
        items = data.get("items", [])
        
        if not items:
            break
            
        users.extend(items)
        
        if "next" not in response.links or len(users) >= max_users:
            break
            
        page += 1
        time.sleep(1) # Be gentle to the Search API
        
    return users[:max_users]

def get_user_details(username):
    """Fetch all available details for a specific user."""
    url = f"https://api.github.com/users/{username}"
    
    while True:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 403:
            reset_time = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
            sleep_time = max(reset_time - time.time(), 0) + 1
            print(f"Rate limited on user query. Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)
            continue
            
        if response.status_code == 404:
            print(f"User {username} not found.")
            return None
            
        response.raise_for_status()
        return response.json()

def main():
    target_users = 1000
    print(f"Starting extraction of {target_users} GitHub users from Peru (with full details)...")
    
    # 1. Search for 1000 users
    query = "location:peru"
    search_results = search_users(query, max_users=target_users)
    print(f"Found {len(search_results)} users from search. Now fetching full details...")
    
    if not search_results:
        print("No users found.")
        return
        
    all_user_data = []
    
    # 2. For each user, get full details
    for idx, user_basic in enumerate(search_results, 1):
        username = user_basic['login']
        print(f"[{idx}/{len(search_results)}] Fetching details for {username}...")
        
        details = get_user_details(username)
        if details:
            # We want to flatten the data, removing nested dictionaries or lists if any
            # though the user endpoint mostly returns flat data.
            all_user_data.append(details)
            
        # The User API allows 5000 requests per hour. No need for long sleeps,
        # but a tiny pause helps prevent triggering abuse mechanisms.
        time.sleep(0.1) 
        
    if not all_user_data:
        print("Failed to fetch user details.")
        return
        
    # 3. Save to CSV
    # Extract all possible keys from the first user to make the CSV headers
    # (The GitHub API consistently returns the same keys for user profiles)
    keys = list(all_user_data[0].keys())
    
    filename = "data/processed/users.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_user_data)
        
    print(f"\nData successfully saved to {filename}")

if __name__ == "__main__":
    main()
