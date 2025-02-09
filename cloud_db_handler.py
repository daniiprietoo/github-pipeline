from typing import Dict
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Repositories(Base):
    __tablename__ = 'repositories'

    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer, unique=True)
    name = Column(String(255), nullable=False)
    full_name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    language = Column(String(255))
    stars = Column(Integer)
    forks = Column(Integer)
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
    __tablename__ = 'trends'

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
                stars=repo["stars"],
                forks=repo["forks"],
                owner=repo["owner"],
                owner_url=repo["owner_url"],
                html_url=repo["html_url"],
                created_at=datetime.fromisoformat(repo["created_at"].replace('Z', '+00:00')),
                updated_at=datetime.fromisoformat(repo["updated_at"].replace('Z', '+00:00'))
            )

            session.add(repo_obj)
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