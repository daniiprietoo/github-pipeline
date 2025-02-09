import os
from dotenv import load_dotenv
from api_handler import GitHubClient
from cloud_db_handler import DatabaseClient
from google.cloud.sql.connector import Connector


def main():
    load_dotenv()
    git_token = os.getenv("GITHUB_TOKEN")
    db_connection_name = os.getenv("DB_CONNECTION_NAME")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    if not git_token:
        print("GitHub token not found in environment variables")
        return
    
    git_client = GitHubClient(token=git_token)

    connector = Connector()
    db_client = DatabaseClient(connector, db_connection_name, db_name, db_user, db_password)

    try:
        repos = git_client.get_trending_repos(7, 10)
        for repo in repos:
            print(repo)
            db_client.insert_repo(repo)
            db_client.insert_trend(repo)
            db_client.insert_issues_prs(repo)
    except Exception as e:
        print("An error occurred in main:", e)

if __name__ == "__main__":
    main()

