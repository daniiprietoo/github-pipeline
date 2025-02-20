from typing import Dict
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone
import pandas as pd

Base = declarative_base()

class Repositories(Base):
    __tablename__ = 'repositories'

    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer, unique=True)
    name = Column(String(255), nullable=False)
    full_name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    language = Column(String(255))
    owner = Column(String(255))
    owner_url = Column(String(255))
    html_url = Column(String(255), unique=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    collected_at = Column(DateTime, default=datetime.utcnow)

class Trends(Base):
    __tablename__ = 'trends'

    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer, sqlalchemy.ForeignKey('repositories.repo_id'))
    stars = Column(Integer)
    forks = Column(Integer)
    recorded_at = Column(DateTime, default=datetime.utcnow)

class IssuesPrs(Base):
    __tablename__ = 'issues_prs'

    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer, sqlalchemy.ForeignKey('repositories.repo_id'))
    open_issues = Column(Integer)
    closed_issues = Column(Integer)
    open_prs = Column(Integer)
    closed_prs = Column(Integer)
    recorded_at = Column(DateTime, default=datetime.utcnow)


class DatabaseClient:
    def __init__(self, connector, connection_name:str, name: str, user: str, password: str):
        def get_conn():
            try:
                conn = connector.connect(
                    connection_name,
                    "pg8000",
                    user=user,
                    password=password,
                    db=name
                )
                return conn
            except Exception as e:
                print(f'Error connecting to PostgreSQL: {e}')
        
        self.engine = create_engine(
            f'postgresql+pg8000://',
            creator=get_conn,
            pool_pre_ping=True
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    

    def insert_repo(self, repo: Dict):
        session = self.Session()
        try:
            repo_obj = Repositories(
                repo_id=repo["repo_id"],
                name=repo["name"],
                full_name=repo["full_name"],
                description=repo.get("description", ""),
                language=repo.get("language", "Unknown"),
                owner=repo["owner"],
                owner_url=repo["owner_url"],
                html_url=repo["html_url"],
                created_at=datetime.fromisoformat(repo["created_at"].replace('Z', '+00:00')),
                updated_at=datetime.fromisoformat(repo["updated_at"].replace('Z', '+00:00'))
            )

            session.merge(repo_obj)
            session.commit()
            print(f"Repo {repo['repo_id']} was successfully added into repositories")
        except Exception as e:
            session.rollback()
            print(f"Error inserting in repositories {repo['full_name']}: {e}")
        finally:
            session.close()
    def insert_trend(self, repo: Dict):
        session = self.Session()

        try:
            trend_obj = Trends(
                repo_id=repo['repo_id'],
                stars=repo['stars'],
                forks=repo['forks']
            )
            session.add(trend_obj)
            session.commit()
            print(f"Repo {repo['repo_id']} was successfully added into trends")
        except Exception as e:
            session.rollback()
            print(f"Error inserting repo in trends {repo['full_name']}: {e}")
        finally:
            session.close()

    def insert_issues_prs(self, repo: Dict):
        session = self.Session()

        try:
            issues_prs_obj = IssuesPrs(
                repo_id=repo['repo_id'],
                open_issues=repo['open_issues'],
                closed_issues=repo['closed_issues'],
                open_prs=repo['open_prs'],
                closed_prs=repo['closed_prs']
            )
            session.add(issues_prs_obj)
            session.commit()
            print(f"Repo {repo['repo_id']} was successfully added into issues_prs")
        except Exception as e:
            session.rollback()
            print(f"Error inserting repo in issues_prs {repo['full_name']}: {e}")
        finally:
            session.close()

    def get_trending_repos(self):
        session = self.Session()
        try:
            one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)

            subquery = session.query(
                Repositories.repo_id,
                Repositories.full_name,
                Repositories.description,
                Repositories.language,
                Repositories.collected_at,
                func.max(Trends.stars).label('max_stars'),
                func.max(Trends.forks).label('max_forks')
            ).join(Trends, Repositories.repo_id == Trends.repo_id).\
              filter(Trends.recorded_at >= one_week_ago).\
              group_by(Repositories.repo_id, Repositories.full_name, Repositories.description, Repositories.language, Repositories.html_url, Repositories.collected_at).\
              subquery()

            main_query = session.query(
                subquery.c.full_name,
                subquery.c.description,
                subquery.c.language,
                subquery.c.max_stars,
                subquery.c.max_forks,
                subquery.c.collected_at
            ).order_by(subquery.c.max_stars.desc()).\
              limit(10)

            results = main_query.all()
            data = []
            for row in results: 
                data.append({
                    'repo_name': row.full_name,
                    'description': row.description,
                    'language': row.language,
                    'stars': row.max_stars,
                    'forks': row.max_forks,
                    'collected_at': row.collected_at
                })
            return pd.DataFrame(data)
        except Exception as e:
            print(f"Error fetching top 10 distinct trending repos for dashboard: {e}")
            return pd.DataFrame() 
        finally:
            session.close()