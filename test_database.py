import unittest
import sqlite3
from db_handler import DatabaseClient

class TestDatabaseClient(unittest.TestCase):
    def setUp(self):
        self.db_client = DatabaseClient(":memory")

    def test_table_creation(self):
        with self.db_client._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = {row[0] for row in cursor.fetchall()}
            self.assertIn("repositories", tables)
            self.assertIn("trends", tables)

    def test_insert_repo(self):
        repo = {
            "repo_id": 12345,
            "name": "TestRepo",
            "full_name": "user/TestRepo",
            "description": "A test repository",
            "language": "Python",
            "stars": 100,
            "forks": 10,
            "owner": "user",
            "owner_url": "https://github.com/user",
            "html_url": "https://github.com/user/TestRepo",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z"
        }
        
        self.db_client.insert_repo(repo)

        with self.db_client._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM repositories WHERE repo_id = ?;", (repo['repo_id'],))
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[1], repo["repo_id"])
            self.assertEqual(result[2], repo["name"])

    def test_insert_trend(self):
        repo = {
            "repo_id": 12345,
            "name": "TestRepo",
            "full_name": "user/TestRepo",
            "description": "A test repository",
            "language": "Python",
            "stars": 100,
            "forks": 10,
            "owner": "user",
            "owner_url": "https://github.com/user",
            "html_url": "https://github.com/user/TestRepo",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-02T00:00:00Z"
        }
        
        self.db_client.insert_trend(repo)

        with self.db_client._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM trends WHERE repo_id = ?;", (repo['repo_id'],))
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[1], repo["repo_id"])
            self.assertEqual(result[2], repo["stars"])
            self.assertEqual(result[3], repo["forks"])

if __name__ == "__main__":
    unittest.main()