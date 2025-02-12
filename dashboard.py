import streamlit as st
from dotenv import load_dotenv
import os
from google.cloud.sql.connector import Connector
from cloud_db_handler import DatabaseClient

load_dotenv()

@st.cache_resource
def get_db_client():
    db_connection_name = os.getenv("DB_CONNECTION_NAME")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    connector = Connector()
    db_client = DatabaseClient(connector, db_connection_name, db_name, db_user, db_password)
    return db_client

db_client = get_db_client()

st.title("⭐️ TOP 10 Trending Repos in Gitbub this Week ⭐️")

trending_repos_df = db_client.get_trending_repos()


if not trending_repos_df.empty:
    st.subheader("Repos Details")
    trending_repos_df.insert(0, 'Top', range(1, len(trending_repos_df) + 1))
    indexed_df = trending_repos_df.set_index('Top') 
    st.dataframe(indexed_df[['repo_name', 'stars', 'forks','description', 'language', 'collected_at']])
else:
    st.error("Failed to fetch repository data.")

