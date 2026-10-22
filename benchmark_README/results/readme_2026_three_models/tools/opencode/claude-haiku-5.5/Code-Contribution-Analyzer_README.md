# Code Contribution Analyzer

Code Contribution Analyzer is a Python project that aims to analyze a developer's code contributions across GitHub, GitLab, and Bitbucket. It contains three parts:

- A small Flask web application with a SQLAlchemy data model and a JSON API for users, repositories, and contributions.
- Thin API clients for GitHub, GitLab, and Bitbucket that fetch repository and contributor data.
- A static landing page (HTML, CSS, and JavaScript) served by the Flask app.

> **Status:** This is an early-stage project. Several parts are incomplete or not yet connected to each other. See [Known Limitations](#known-limitations) before relying on it.

## Table of Contents

- [Repository Layout](#repository-layout)
- [Components](#components)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Web Application](#running-the-web-application)
- [API Reference](#api-reference)
- [API Clients](#api-clients)
- [Data Model](#data-model)
- [Known Limitations](#known-limitations)
- [Contributing](#contributing)
- [License](#license)

## Repository Layout

```
.
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
└── src/
    ├── api_clients/
    │   ├── base_client.py        # Shared HTTP client (Bearer auth, GET/POST helpers)
    │   ├── github_client.py      # GitHub API client
    │   ├── gitlab_client.py      # GitLab API client
    │   └── bitbucket_client.py   # Bitbucket API client
    └── web/
        ├── app.py                # Flask application and routes
        ├── models.py             # SQLAlchemy models: User, Repository, Contribution
        ├── static/
        │   ├── index.js          # Smooth-scrolling navigation for the landing page
        │   └── styles.css        # Stylesheet for the landing page
        └── templates/
            └── index.html        # Landing page
```

## Components

### Web application (`src/web/app.py`)

A Flask app that:

- Enables CORS for all routes via `flask_cors`.
- Uses Flask-SQLAlchemy, configured by the `DATABASE_URL` environment variable (default: `sqlite:///code_analyzer.db`).
- Exposes a root route and the JSON API described in [API Reference](#api-reference).

### Data models (`src/web/models.py`)

Three SQLAlchemy models: `User`, `Repository`, and `Contribution`. See [Data Model](#data-model).

### API clients (`src/api_clients/`)

- `BaseClient` wraps `requests` with a base URL, a `Bearer` token `Authorization` header, and `Accept: application/json`. It provides `get(endpoint)` and `post(endpoint, data)` and raises an exception on HTTP error status codes.
- `GitHubClient`, `GitLabClient`, and `BitbucketClient` subclass `BaseClient` with their respective API base URLs. See [API Clients](#api-clients).

### Landing page (`src/web/templates/index.html`)

A single HTML page with sections for overview, features, usage, and contact, plus in-page navigation. `static/index.js` makes the navigation links scroll smoothly.

## Requirements

- Python 3
- Packages imported by the code:
  - `flask`
  - `flask-sqlalchemy`
  - `flask-cors`
  - `requests`

The repository does not currently include a `requirements.txt` or `pyproject.toml`, so no pinned versions are specified.

## Installation

```bash
git clone https://github.com/stephenombuya/Code-Contribution-Analyzer
cd Code-Contribution-Analyzer
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install flask flask-sqlalchemy flask-cors requests
```

## Configuration

| Variable       | Used by              | Default                          | Description                                  |
|----------------|----------------------|----------------------------------|----------------------------------------------|
| `DATABASE_URL` | `src/web/app.py`     | `sqlite:///code_analyzer.db`     | SQLAlchemy database URI.                     |

The API clients take a token as a constructor argument. The code does not read any token from an environment variable. Tokens are sent as `Authorization: Bearer <token>`.

You can place variables in a `.env` file. `.gitignore` excludes `.env`, but the code does not load `.env` automatically.

## Running the Web Application

From the repository root:

```bash
python src/web/app.py
```

When run directly, the app calls `db.create_all()` and starts Flask in debug mode (`app.run(debug=True)`), which by default serves at `http://127.0.0.1:5000/`.

Note: `app.py` imports `models` as a top-level module (`from models import ...`). Running the file directly as shown above makes that import work. See [Known Limitations](#known-limitations) for a database issue that may prevent the app from working.

## API Reference

All endpoints return JSON.

| Method | Path                 | Description                                              | Success response |
|--------|----------------------|----------------------------------------------------------|------------------|
| GET    | `/`                  | Returns a welcome message.                               | `200`            |
| GET    | `/api/users`         | Lists all users as `{id, name, email}`.                  | `200`            |
| POST   | `/api/users`         | Creates a user from a JSON body with `name` and `email`. | `201`            |
| GET    | `/api/repositories`  | Lists all repositories as `{id, name, url, user_id}`.    | `200`            |
| GET    | `/api/contributions` | Lists all contributions as `{id, repository_id, language, lines_of_code}`. | `200` |

Example:

```bash
curl -X POST http://127.0.0.1:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe", "email": "jane@example.com"}'
```

Response:

```json
{"message": "User created successfully!"}
```

The `POST` handler reads `name` and `email` directly from the request body. A missing field or a non-JSON body causes an unhandled error. The `email` field must be unique.

The API has no endpoints for creating repositories or contributions, and no endpoint that calls the API clients.

## API Clients

All clients take a token in their constructor and return parsed JSON. None of them are called from the web application.

### `GitHubClient(token)`

Base URL: `https://api.github.com`

- `fetch_user_repos(username)`: calls `users/{username}/repos`.
- `fetch_repo_contributors(owner, repo)`: calls `repos/{owner}/{repo}/contributors`.

### `GitLabClient(token)`

Base URL: `https://gitlab.com/api/v4`

- `fetch_user_projects()`: calls `projects`.
- `fetch_project_contributors(project_id)`: calls `projects/{project_id}/repository/contributors`.

### `BitbucketClient(token)`

Base URL: `https://api.bitbucket.org/2.0`

- `fetch_user_repositories()`: calls `repositories`.
- `fetch_repo_contributors(workspace, repo_slug)`: calls `repositories/{workspace}/{repo_slug}/commits`. Despite the method name, this returns commits, not a contributor list.

Example:

```python
from src.api_clients.github_client import GitHubClient

client = GitHubClient(token="<your-token>")
repos = client.fetch_user_repos("octocat")
```

Run this from the repository root. The `src/` directory has no `__init__.py`, so the import path may need adjusting depending on your Python version and setup.

## Data Model

| Table           | Columns                                                                                  | Relationships                                                    |
|-----------------|------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| `users`         | `id` (PK), `name` (String 100, required), `email` (String 100, required, unique)         | One user has many repositories.                                  |
| `repositories`  | `id` (PK), `name` (String 150, required), `url` (String 250, required), `user_id` (FK → `users.id`, required) | Each repository has one user and many contributions. |
| `contributions` | `id` (PK), `repository_id` (FK → `repositories.id`, required), `language` (String 50, required), `lines_of_code` (Integer, required) | Each contribution belongs to one repository. |

## Known Limitations

- **Database binding mismatch.** `app.py` creates its own `db = SQLAlchemy(app)`, while `models.py` defines a separate `db = SQLAlchemy()` and its models use that instance. The models are therefore not registered with the Flask app's `db`, and the routes that query or create records (`/api/users`, `/api/repositories`, `/api/contributions`) may fail at runtime. This has not been verified by running the code.
- **Clients are not integrated.** The API clients are not used by the web app, and nothing in the repository currently turns fetched data into `Repository` or `Contribution` records.
- **No line-count analysis.** No code computes lines of code per language. The `lines_of_code` and `language` fields exist in the model but nothing populates them.
- **Landing page overstates features.** The page lists "generate reports in various formats" and "interactive data visualization." The repository contains no code for either.
- **No tests.** `CONTRIBUTING.md` refers to a `tests/` directory and `pytest`, but the repository contains no tests.
- **Missing dependency file.** `CONTRIBUTING.md` refers to `requirements.txt`, which does not exist.
- **No authentication for the web API.** The endpoints are unauthenticated.
- **Debug mode.** `app.run(debug=True)` is for development only.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow, coding standards, and how to report bugs. Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
