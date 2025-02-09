from datetime import datetime, timedelta, timezone
from github import Github, GithubException

class GitHubClient:
    def __init__(self, token: str):
        if not token:
            raise GithubException(message='Token not provided')
        self._client = Github(login_or_token=token)

    def get_trending_repos(self, days: int = 7, limit: int = 10):
        try:
            date_since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime('%Y-%m-%d')
            query = f'created:>{date_since}'

            repos = self._client.search_repositories(query=query, sort="stars", order="desc")
            
            repos_list = []
            for repo in repos[:limit]:
                repo_info = {
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "owner": repo.owner.login,
                    "stars": repo.stargazers_count,
                    "created_at": repo.created_at.isoformat(),
                    "url": repo.html_url
                }
                repos_list.append(repo_info)

            print(f"Succesfully fetched {len(repos_list)} trending repos")
            return repos_list
        
        except Exception as e:
            print(f"An error occurred trying to get trending repos: {e}")
    

    def get_repo_info(self, repo_name: str):

        try:
            repo = self._client.get_repo(repo_name)
            if repo is None:
                raise ValueError("Repository not found")
            repo_info = {
                "repo_id": repo.id,
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "language": repo.language,
                "stars": repo.stargazers_count,
                "forks": repo.forks,
                "owner": repo.owner.login,
                "owner_url": repo.owner.url,
                "html_url": repo.html_url,
                "created_at": repo.created_at.isoformat(),
                "updated_at": repo.updated_at.isoformat()
            }
            print(f"Successfully fetched repo: {repo_name}")
            return repo_info
        
        except Exception as e:
            print(f"An error occurred trying to get repo info: {e}")


