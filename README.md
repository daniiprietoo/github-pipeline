# GitHub Pipeline

This project is a GitHub pipeline that fetches trending repositories from GitHub, stores them in a SQLite database, and tracks their trends over time.

## Prerequisites

- Python 3.13 or higher
- GitHub Personal Access Token

## Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/github-pipeline.git
    cd github-pipeline
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv .venv
    source .venv/bin/activate
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a [.env](http://_vscodecontentref_/1) file in the root directory and add your GitHub token:

    ```env
    GITHUB_TOKEN=your_github_token_here
    ```

## Usage

1. Run the main script to fetch trending repositories and store them in the database:

    ```sh
    python main.py
    ```

2. To run the tests:

    ```sh
    python -m unittest discover
    ```

## Project Structure

- [main.py](http://_vscodecontentref_/2): The entry point of the application.
- [api_handler.py](http://_vscodecontentref_/3): Contains the [GitHubClient](http://_vscodecontentref_/4) class for interacting with the GitHub API.
- [db_handler.py](http://_vscodecontentref_/5): Contains the [DatabaseClient](http://_vscodecontentref_/6) class for interacting with the SQLite database.
- [test_database.py](http://_vscodecontentref_/7): Contains unit tests for the database client.
- [.env](http://_vscodecontentref_/8): Environment file containing the GitHub token.
- [.gitignore](http://_vscodecontentref_/9): Specifies files and directories to be ignored by Git.
- [.python-version](http://_vscodecontentref_/10): Specifies the Python version for the project.
- [pyproject.toml](http://_vscodecontentref_/11): Contains project metadata and dependencies.
- [README.md](http://_vscodecontentref_/12): This file.

## License

This project is licensed under the MIT License.