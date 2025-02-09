import os
from dotenv import load_dotenv
from api_handler import GitHubClient
from db_handler import DatabaseClient

def main():
    load_dotenv()
    git_token = os.getenv("GITHUB_TOKEN")
    if not git_token:
        print("GitHub token not found in environment variables")
        return
    
    git_client = GitHubClient(token=git_token)
    db_client = DatabaseClient("repos.db")

    try:
        repos = git_client.get_trending_repos(7, 10)
        for repo in repos:
            repo_info = git_client.get_repo_info(repo["full_name"])
            
            db_client.insert_repo(repo_info)
            db_client.insert_trend(repo_info)
    except Exception as e:
        print("An error occurred in main:", e)

if __name__ == "__main__":
    main()

