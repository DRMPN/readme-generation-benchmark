# Code Contribution Analyzer

**Code Contribution Analyzer** is a Flask-based web application for analyzing code contributions across multiple Git hosting platforms — GitHub, GitLab, and Bitbucket. It exposes a REST API for managing users, repositories, and per-language contribution records, and ships with dedicated API clients for fetching repository and contributor data from each platform's public API.

## Overview

The project is organized into two main areas:

- **`src/api_clients/`** — lightweight HTTP clients for the GitHub, GitLab, and Bitbucket REST APIs, built on a shared `BaseClient` that handles Bearer-token authentication and JSON responses.
- **`src/web/`** — a Flask application that serves the REST API, stores data with SQLAlchemy (SQLite by default), and renders a simple browser frontend (HTML template with static CSS/JS).

## Features

- Unified API client architecture with Bearer-token authentication
- Platform-specific clients for GitHub, GitLab, and Bitbucket
- REST API endpoints for users, repositories, and contributions
- SQLAlchemy ORM models with `User → Repository → Contribution` relationships
- CORS enabled for cross-origin frontend consumption
- SQLite database by default, configurable via the `DATABASE_URL` environment variable
- Lightweight web frontend with smooth-scroll navigation

## Project Structure

```
.
├── src/
│   ├── api_clients/
│   │   ├── base_client.py        # Shared HTTP client (auth, GET/POST)
│   │   ├── github_client.py      # GitHub REST API v3 client
│   │   ├── gitlab_client.py      # GitLab API v4 client
│   │   └── bitbucket_client.py   # Bitbucket Cloud API 2.0 client
│   └── web/
│       ├── app.py                # Flask app and API routes
│       ├── models.py             # SQLAlchemy models
│       ├── templates/
│       │   └── index.html        # Frontend page
│       └── static/
│           ├── index.js          # Smooth-scroll navigation
│           └── styles.css        # Frontend styling
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
└── .gitignore
```

## Prerequisites

- Python 3
- `pip` for dependency management

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/stephenombuya/Code-Contribution-Analyzer
   cd code-contribution-analyzer
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   The core dependencies used by the source code are:

   - `Flask`
   - `Flask-SQLAlchemy`
   - `Flask-CORS`
   - `requests`

3. **Create a `.env` file** in the project root and add your API keys (see [Configuration](#configuration)).

## Configuration

### Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | SQLAlchemy database URI used by the Flask app | `sqlite:///code_analyzer.db` |
| `GITHUB_TOKEN` | GitHub personal access token passed to `GitHubClient` | — |
| `GITLAB_TOKEN` | GitLab personal access token passed to `GitLabClient` | — |
| `BITBUCKET_TOKEN` | Bitbucket access token passed to `BitbucketClient` | — |

Store your tokens in a `.env` file at the project root. When no `DATABASE_URL` is set, the application automatically falls back to a local SQLite database (`code_analyzer.db`).

## Running the Application

Run the Flask app from the `src/web` directory (so that `models.py` resolves correctly):

```bash
cd src/web
python app.py
```

On startup the application:

1. Calls `db.create_all()` to create the database tables if they do not exist
2. Starts the Flask development server in debug mode at `http://127.0.0.1:5000`

> **Note:** Debug mode is intended for development only. Do not run with `debug=True` in production.

## REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Welcome message |
| `GET` | `/api/users` | List all users |
| `POST` | `/api/users` | Create a new user |
| `GET` | `/api/repositories` | List all repositories |
| `GET` | `/api/contributions` | List all contributions |

### Examples

**Welcome:**

```bash
curl http://127.0.0.1:5000/
# {"message": "Welcome to Code Contribution Analyzer API"}
```

**List users:**

```bash
curl http://127.0.0.1:5000/api/users
```

```json
[{"id": 1, "name": "Jane Doe", "email": "jane@example.com"}]
```

**Create a user** (expects JSON with `name` and `email`; returns HTTP 201):

```bash
curl -X POST http://127.0.0.1:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe", "email": "jane@example.com"}'
```

**List repositories:**

```json
[{"id": 1, "name": "my-repo", "url": "https://github.com/jane/my-repo", "user_id": 1}]
```

**List contributions:**

```json
[{"id": 1, "repository_id": 1, "language": "Python", "lines_of_code": 1200}]
```

## Git Platform Clients

All clients extend a shared `BaseClient` (`src/api_clients/base_client.py`) that:

- Sends requests with an `Authorization: Bearer <token>` header and `Accept: application/json`
- Raises an exception on HTTP errors (`raise_for_status`)
- Returns parsed JSON for both `GET` and `POST` requests

### GitHubClient (`github_client.py`)

Base URL: `https://api.github.com`

| Method | Upstream endpoint |
|---|---|
| `fetch_user_repos(username)` | `GET /users/{username}/repos` |
| `fetch_repo_contributors(owner, repo)` | `GET /repos/{owner}/{repo}/contributors` |

### GitLabClient (`gitlab_client.py`)

Base URL: `https://gitlab.com/api/v4`

| Method | Upstream endpoint |
|---|---|
| `fetch_user_projects()` | `GET /projects` |
| `fetch_project_contributors(project_id)` | `GET /projects/{project_id}/repository/contributors` |

### BitbucketClient (`bitbucket_client.py`)

Base URL: `https://api.bitbucket.org/2.0`

| Method | Upstream endpoint |
|---|---|
| `fetch_user_repositories()` | `GET /repositories` |
| `fetch_repo_contributors(workspace, repo_slug)` | `GET /repositories/{workspace}/{repo_slug}/commits` |

### Example Usage

```python
from src.api_clients.github_client import GitHubClient

client = GitHubClient(token="your-github-token")

repos = client.fetch_user_repos("octocat")
contributors = client.fetch_repo_contributors("octocat", "hello-world")
```

## Data Models

Defined in `src/web/models.py` using Flask-SQLAlchemy:

| Model | Table | Fields | Relationships |
|---|---|---|---|
| `User` | `users` | `id`, `name`, `email` (unique) | Has many `Repository` records |
| `Repository` | `repositories` | `id`, `name`, `url`, `user_id` (FK → `users.id`) | Belongs to a `User`; has many `Contribution` records |
| `Contribution` | `contributions` | `id`, `repository_id` (FK → `repositories.id`), `language`, `lines_of_code` | Belongs to a `Repository` |

This schema lets you attribute repositories to users and break each repository's contributions down by programming language and lines of code.

## Frontend

The web frontend lives in `src/web/`:

- `templates/index.html` — the page template
- `static/styles.css` — styling
- `static/index.js` — intercepts navigation clicks and smooth-scrolls to the target sections

## Development

The project follows the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md):

- **Coding standards:** Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code, use meaningful variable and function names, write concise comments, and add docstrings to all functions and classes.
- **Workflow:**
  1. Fork the repository
  2. Clone your fork locally
  3. Install dependencies and create your `.env` file
  4. Create a descriptive feature branch (e.g., `git checkout -b add-new-feature`)
  5. Make and test your changes
  6. Commit with clear, present-tense messages (e.g., "Add feature X")
  7. Push to your fork and open a pull request with a detailed description

## Testing

- Add tests for new features and bug fixes in the `tests/` directory
- Use descriptive test names and document test cases
- Ensure all tests pass before submitting a pull request:

  ```bash
  pytest
  ```

## Contributing

Contributions are welcome — bug fixes, new features, documentation improvements, and enhancement suggestions. Please:

- Report bugs and request features via the [Issues](https://github.com/stephenombuya/Code-Contribution-Analyzer/issues) page, including reproduction steps, expected vs. actual behavior, and relevant logs or screenshots
- Ask questions or discuss ideas in [Discussions](https://github.com/stephenombuya/Code-Contribution-Analyzer/discussions)

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contribution process.

## Code of Conduct

This project adopts the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md) (version 2.1). By participating, you agree to uphold a respectful and inclusive environment. Report unacceptable behavior to the community leaders at **donofficialsoftwares@gmail.com**.

## License

This project is licensed under the [MIT License](LICENSE) — Copyright (c) 2025 Stephen Ombuya. You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, subject to the license terms.
