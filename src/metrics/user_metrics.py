import csv
from collections import Counter
from datetime import datetime
import os

def calculate_h_index(stars_list):
    """Calculate h-index based on repository stars."""
    stars = sorted(stars_list, reverse=True)
    h = 0
    for i, s in enumerate(stars):
        if s >= i + 1:
            h = i + 1
        else:
            break
    return h

def main():
    # Use paths relative to project root
    users_file = "data/processed/users.csv"
    repos_file = "data/processed/classifications.csv"
    output_file = "data/metrics/user_metrics.csv"
    
    if not os.path.exists(users_file) or not os.path.exists(repos_file):
        print(f"Required CSV files not found. ({users_file}, {repos_file})")
        return
        
    # 1. Load users
    users_data = {}
    with open(users_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            users_data[row["login"]] = row
            
    # 2. Load repos and map to users
    user_repos = {login: [] for login in users_data.keys()}
    with open(repos_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            owner_login = row["full_name"].split("/")[0]
            if owner_login in user_repos:
                user_repos[owner_login].append(row)

    print(f"Loaded {len(users_data)} users and mapped their repositories.")
    today = datetime.now()
    all_user_metrics = []
    
    # 3. Calculate metrics for each user
    for login, user in users_data.items():
        repos = user_repos.get(login, [])
        metrics = {
            "login": login,
            "name": user.get("name", ""),
            "company": user.get("company", ""),
            "location": user.get("location", ""),
            "created_at": user.get("created_at", "")
        }
        
        # Activity Metrics
        metrics["total_repos"] = len(repos)
        metrics["total_stars_received"] = sum(int(float(r.get("stargazers_count", 0))) for r in repos)
        metrics["total_forks_received"] = sum(int(float(r.get("forks_count", 0))) for r in repos)
        metrics["avg_stars_per_repo"] = (
            metrics["total_stars_received"] / metrics["total_repos"] 
            if metrics["total_repos"] > 0 else 0
        )
        
        created_dt_str = user.get("created_at", "").replace("Z", "")
        if created_dt_str:
            try:
                created_at = datetime.fromisoformat(created_dt_str)
                metrics["account_age_days"] = (today - created_at).days
            except ValueError:
                metrics["account_age_days"] = 0
        else:
            metrics["account_age_days"] = 0
            
        metrics["repos_per_year"] = (
            metrics["total_repos"] / (metrics["account_age_days"] / 365.0) 
            if metrics["account_age_days"] > 0 else 0
        )
        
        # Influence Metrics
        followers = int(float(user.get("followers", 0)))
        following = int(float(user.get("following", 0)))
        metrics["followers"] = followers
        metrics["following"] = following
        metrics["follower_ratio"] = (followers / following) if following > 0 else followers
        
        stars_list = [int(float(r.get("stargazers_count", 0))) for r in repos]
        metrics["h_index"] = calculate_h_index(stars_list)
        metrics["impact_score"] = metrics["total_stars_received"] + (metrics["total_forks_received"] * 2) + followers
        
        # Technical Metrics
        languages = [r.get("language") for r in repos if r.get("language")]
        lang_counts = Counter(languages)
        metrics["primary_languages"] = ", ".join([l for l, _ in lang_counts.most_common(3)])
        metrics["language_diversity"] = len(set(languages))
        
        # Industry Metrics
        industry_codes = [r["industry_code"] for r in repos]
        metrics["industries_served"] = len(set(industry_codes))
        metrics["primary_industry"] = Counter(industry_codes).most_common(1)[0][0] if industry_codes else None
        
        # Documentation Quality
        repos_with_readme = sum(1 for r in repos if len(r.get("readme", "").strip()) > 0)
        repos_with_license = sum(1 for r in repos if r.get("license", "").strip())
        metrics["has_readme_pct"] = repos_with_readme / len(repos) if repos else 0
        metrics["has_license_pct"] = repos_with_license / len(repos) if repos else 0
        
        # Engagement Metrics
        metrics["total_open_issues"] = sum(int(float(r.get("open_issues_count", 0))) for r in repos)
        last_push_days = None
        if repos:
            valid_pushes = []
            for r in repos:
                push_str = r.get("pushed_at", "").replace("Z", "")
                if push_str:
                    try: valid_pushes.append(datetime.fromisoformat(push_str))
                    except ValueError: pass
            if valid_pushes:
                last_push = max(valid_pushes)
                last_push_days = (today - last_push).days
                
        if last_push_days is not None:
            metrics["days_since_last_push"] = last_push_days
            metrics["is_active"] = last_push_days < 90
        else:
            metrics["days_since_last_push"] = ""
            metrics["is_active"] = False
            
        all_user_metrics.append(metrics)
        
    keys = list(all_user_metrics[0].keys())
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_user_metrics)
        
    print(f"Refreshed metrics saved to {output_file}")

if __name__ == "__main__":
    main()
