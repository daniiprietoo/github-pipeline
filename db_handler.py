import sqlite3
from typing import Dict

class DatabaseClient:
    def __init__(self, path: str):
        self.db_path = path
        self._set_up_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)
    
    def _set_up_db(self):
        with self._get_conn() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS repositories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    repo_id INTEGER UNIQUE,  
                    name TEXT NOT NULL,       
                    full_name TEXT UNIQUE NOT NULL, 
                    description TEXT,         
                    language TEXT,            
                    stars INTEGER,            
                    forks INTEGER,            
                    owner TEXT,               
                    owner_url TEXT,           
                    html_url TEXT UNIQUE,     
                    created_at TEXT,          
                    updated_at TEXT,          
                    collected_at TEXT DEFAULT CURRENT_TIMESTAMP 
                );
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS languages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    repo_id INTEGER,
                    language TEXT NOT NULL,
                    bytes INTEGER, 
                    FOREIGN KEY (repo_id) REFERENCES repositories (repo_id)
                );
            """)

            conn.execute("""
            CREATE TABLE IF NOT EXISTS trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                repo_id INTEGER,
                stars INTEGER,
                forks INTEGER,
                recorded_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (repo_id) REFERENCES repositories (repo_id)
            );
            """)

            conn.commit()
            print("Database successfully set up")

    def insert_repo(self, repo: Dict):
        with self._get_conn() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO repositories (repo_id, name, full_name, description, language, stars, forks, owner, owner_url, html_url, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(repo_id) DO UPDATE SET
                                stars=excluded.stars,
                                forks=excluded.forks,
                                updated_at=excluded.updated_at
                """,
                    (
                        repo["repo_id"],
                        repo["name"],
                        repo["full_name"],
                        repo.get("description", ""),
                        repo.get("language", "Unknown"),
                        repo["stars"],
                        repo["forks"],
                        repo["owner"],
                        repo["owner_url"],
                        repo["html_url"],
                        repo["created_at"],
                        repo["updated_at"],
                    ),
                )

                conn.commit()
                print(f'Repo {repo['repo_id']} was successfully added into repositories')

            except Exception as e:
                print(f"Error inserting repo in repositories {repo['full_name']}: {e}")

    def insert_trend(self, repo: Dict):
        with self._get_conn() as conn:
            try:
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO trends (repo_id, stars, forks)
                    VALUES (?, ?, ?);
                """, (
                    repo['repo_id'],
                    repo['stars'],
                    repo['forks']
                ))

                
                conn.commit()
                print(f'Repo {repo['repo_id']} was successfully added into trends')
            except Exception as e:
                print(f"Error inserting repo in trends {repo['full_name']}: {e}")
