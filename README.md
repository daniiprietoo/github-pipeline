# GitHub Trending Repositories Pipeline

## Overview

This project automates the process of fetching trending repositories from GitHub, storing them in a PostgreSQL database on Google Cloud SQL. It uses the GitHub API, Google Cloud SQL Connector, and SQLAlchemy

## Features

- **Automated Data Collection:** Fetches trending repositories from GitHub based on specified criteria (e.g., date range, number of stars).
- **Google Cloud SQL Integration:** Stores repository data in a PostgreSQL database on Google Cloud SQL for persistent storage and scalability.
- **Key Metrics Tracking:** Tracks key metrics such as stars, forks, open issues, and pull requests over time.
- **Modular Design:** Separates concerns into distinct modules for API interaction, database handling, and main application logic.
- **Environment Variable Configuration:** Uses environment variables for sensitive information such as API tokens and database credentials.
- **GitHub Actions Automation:** Automates the data collection and storage process using GitHub Actions for scheduled execution.

## Prerequisites

- **Python 3.11 or higher:** Ensure you have Python 3.11 or higher installed.
- **GitHub Personal Access Token:** Create a personal access token with the `public_repo` scope.
- **Google Cloud Account:** You'll need a Google Cloud account with billing enabled.
- **Google Cloud SDK (gcloud):** Install and configure the Google Cloud SDK.
- **Google Cloud SQL Instance:** Create a PostgreSQL instance on Google Cloud SQL.
- **Environment Variables:** Set the following environment variables:
    - `GIT_TOKEN`: Your GitHub Personal Access Token.
    - `DB_CONNECTION_NAME`: The connection name of your Google Cloud SQL instance (e.g., `project:region:instance`).
    - `DB_NAME`: The name of the PostgreSQL database.
    - `DB_USER`: The PostgreSQL username.
    - `DB_PASSWORD`: The PostgreSQL password.
    - `GCP_SA_KEY`: The contents of your Google Cloud Service Account key file.

## Setup

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/github-pipeline.git
    cd github-pipeline
    ```

2.  **Create a Virtual Environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Linux/macOS
    .venv\Scripts\activate  # On Windows
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**

    *   Create a [.env](http://_vscodecontentref_/1) file in the root directory of the project.
    *   Add the required environment variables to the [.env](http://_vscodecontentref_/2) file:

        ```
        GIT_TOKEN="your_github_token"
        DB_CONNECTION_NAME="your-project:your-region:your-instance"
        DB_NAME="your_database_name"
        DB_USER="your_db_user"
        DB_PASSWORD="your_db_password"
        ```

5.  **Set up Google Cloud Authentication:**

    *   Create a Google Cloud Service Account with the necessary permissions to access Cloud SQL.
    *   Download the Service Account key file in JSON format.
    *   Store the contents of the JSON key file as a GitHub secret named `GCP_SA_KEY`.

## Usage

1.  **Run the Main Script:**

    ```bash
    python main.py
    ```

    This script will:

    *   Fetch trending repositories from GitHub.
    *   Store the repository information in the `repositories` table.
    *   Store the trending metrics (stars, forks) in the `trends` table.
    *   Store the issues and pull requests data in the `issues_prs` table.

2. **Run the dashboard locally:**

    ```bash
    streamlit run dashboard.py
    ```
    *   Get the top 10 repos with most stars from the Google Cloud SQL Instance

    *   Display them in a pretty way
  
   ![image](https://github.com/user-attachments/assets/72d75b7e-96cd-4e5f-9ef2-3407c5bdd79d)

## Database Schema

The project uses the following database schema in PostgreSQL:

-   **`repositories` Table:**
    -   [id](http://_vscodecontentref_/9) (SERIAL PRIMARY KEY): Unique identifier for the repository.
    -   [repo_id](http://_vscodecontentref_/10) (INTEGER UNIQUE): GitHub repository ID.
    -   [name](http://_vscodecontentref_/11) (VARCHAR(255) NOT NULL): Repository name.
    -   [full_name](http://_vscodecontentref_/12) (VARCHAR(255) UNIQUE NOT NULL): Full repository name (owner/repo).
    -   [description](http://_vscodecontentref_/13) (TEXT): Repository description.
    -   [language](http://_vscodecontentref_/14) (VARCHAR(255)): Primary programming language.
    -   [owner](http://_vscodecontentref_/15) (VARCHAR(255)): Repository owner's username.
    -   [owner_url](http://_vscodecontentref_/16) (VARCHAR(255)): URL of the repository owner's profile.
    -   [html_url](http://_vscodecontentref_/17) (VARCHAR(255) UNIQUE): Repository URL.
    -   [created_at](http://_vscodecontentref_/18) (TIMESTAMP): Repository creation timestamp.
    -   [updated_at](http://_vscodecontentref_/19) (TIMESTAMP): Repository last updated timestamp.
    -   [collected_at](http://_vscodecontentref_/20) (TIMESTAMP DEFAULT CURRENT_TIMESTAMP): Timestamp when the repository data was collected.

-   **`trends` Table:**
    -   [id](http://_vscodecontentref_/21) (SERIAL PRIMARY KEY): Unique identifier for the trend record.
    -   [repo_id](http://_vscodecontentref_/22) (INTEGER, FOREIGN KEY referencing `repositories.repo_id`): GitHub repository ID.
    -   [stars](http://_vscodecontentref_/23) (INTEGER): Number of stars.
    -   [forks](http://_vscodecontentref_/24) (INTEGER): Number of forks.
    -   [recorded_at](http://_vscodecontentref_/25) (TIMESTAMP DEFAULT CURRENT_TIMESTAMP): Timestamp when the trend data was recorded.

-   **`issues_prs` Table:**
    -   [id](http://_vscodecontentref_/26) (SERIAL PRIMARY KEY): Unique identifier for the issues/PRs record.
    -   [repo_id](http://_vscodecontentref_/27) (INTEGER, FOREIGN KEY referencing `repositories.repo_id`): GitHub repository ID.
    -   [open_issues](http://_vscodecontentref_/28) (INTEGER): Number of open issues.
    -   [closed_issues](http://_vscodecontentref_/29) (INTEGER): Number of closed issues.
    -   [open_prs](http://_vscodecontentref_/30) (INTEGER): Number of open pull requests.
    -   [closed_prs](http://_vscodecontentref_/31) (INTEGER): Number of closed pull requests.
    -   [recorded_at](http://_vscodecontentref_/32) (TIMESTAMP DEFAULT CURRENT_TIMESTAMP): Timestamp when the issues/PRs data was recorded.

## GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/run_main.yml`) that automates the data collection and storage process. The workflow is triggered on a schedule (e.g., daily) and performs the following steps:

1.  **Checks out the repository.**
2.  **Sets up Python 3.11.**
3.  **Installs the project dependencies.**
4.  **Authenticates with Google Cloud using a Service Account key.**
5.  **Executes the [main.py](http://_vscodecontentref_/33) script.**

To configure the GitHub Actions workflow:

1.  **Enable GitHub Actions** in your repository settings.
2.  **Add the following secrets** to your repository settings:
    -   `GIT_TOKEN`: Your GitHub Personal Access Token.
    -   `DB_CONNECTION_NAME`: The connection name of your Google Cloud SQL instance.
    -   `DB_NAME`: The name of your PostgreSQL database.
    -   `DB_USER`: The username for your PostgreSQL database.
    -   `DB_PASSWORD`: The password for your PostgreSQL database.
    -   `GCP_SA_KEY`: The contents of your Google Cloud Service Account key file.

## License

This project is licensed under the MIT License.
