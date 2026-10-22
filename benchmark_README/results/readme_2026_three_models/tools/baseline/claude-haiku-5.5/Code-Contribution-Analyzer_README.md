# Code Contribution Analyzer

Code Contribution Analyzer is a Flask-based web application with a small REST-style API for storing users, repositories, and per-language contribution records. The repository also includes Python API client classes for GitHub, GitLab, and Bitbucket, which are intended to fetch repository and contributor data from those platforms.

## Overview

The project has two main parts:

- **Web application (`src/web/`)**: A Flask app (`app.py`) backed by SQLAlchemy models (`models.py`). It exposes JSON endpoints for users, repositories, and contributions, and includes a front-end template (`templates/index.html`), a stylesheet (`static/styles.css`), and a small script (`static/index.js`).
- **API clients (`src/api_clients/`)**: A `BaseClient` class that wraps `requests` with bearer-token authentication, plus subclasses for:
  - GitHub (`https://api.github.com`)
  - GitLab (`https://gitlab.com/api/v4`)
  - Bitbucket (`https://api.bitbucket.org/2.0`)

### Data Model

The database contains three tables defined in `src/web/models.py`:

| Model | Table | Key Fields |
|---|---|---|
| `User` | `users` | `id`, `name` (max 100), `email` (max 100, unique) |
| `Repository` | `repositories` | `id`, `name` (max 150), `url` (max 250), `user_id` (foreign key to `users.id`) |
| `Contribution` | `contributions` | `id`, `repository_id` (foreign key to `repositories.id`), `language` (max 50), `lines_of_code` (integer) |

Relationships are defined so that a user has many repositories and a repository has many contributions.

## Requirements

No `requirements.txt` file is included in the supplied file tree, although `CONTRIBUTING.md` tells contributors to run `pip install -r requirements.txt`. Based on the imports in the source files, the project depends on:

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- requests

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/stephenombuya/Code-Contribution-Analyzer
   cd Code-Contribution-Analyzer
   ```

2. Install the dependencies listed above. For example:

   ```bash
   pip install flask flask-sqlalchemy flask-cors requests
   ```

3. Create a `.env` file in the project root if you need to supply configuration values (see [Configuration](#configuration)). The application does not load `.env` files itself, so you will need to export the variables in your shell or load them through another tool.

## Usage

### Running the Web Application

`app.py` imports its models with `from models import User, Repository, Contribution`, so the application must be started from inside `src/web/`:

```bash
cd src/web
python app.py
```

When run directly, the application calls `db.create_all()` to create the database tables and then starts the Flask development server with `debug=True`.

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Returns a welcome message: `{"message": "Welcome to Code Contribution Analyzer API"}` |
| `GET` | `/api/users` | Returns all users with `id`, `name`, and `email` |
| `POST` | `/api/users` | Creates a user. Requires a JSON body with `name` and `email`. Returns `201` with a success message. |
| `GET` | `/api/repositories` | Returns all repositories with `id`, `name`, `url`, and `user_id` |
| `GET` | `/api/contributions` | Returns all contributions with `id`, `repository_id`, `language`, and `lines_of_code` |

Example request to create a user:

```bash
curl -X POST http://127.0.0.1:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe", "email": "jane@example.com"}'
```

Because `POST /api/users` reads `request.json` and accesses `name` and `email` directly, a request with missing fields will currently fail with a server error rather than a structured validation message.

### Using the API Clients

The client classes can be imported from `src/api_clients/` and instantiated with a personal access token:

```python
from api_clients.github_client import GitHubClient

client = GitHubClient(token="YOUR_TOKEN")
repos = client.fetch_user_repos("octocat")
contributors = client.fetch_repo_contributors("octocat", "Hello-World")
```

Available methods:

- `GitHubClient.fetch_user_repos(username)` and `GitHubClient.fetch_repo_contributors(owner, repo)`
- `GitLabClient.fetch_user_projects()` and `GitLabClient.fetch_project_contributors(project_id)`
- `BitbucketClient.fetch_user_repositories()` and `BitbucketClient.fetch_repo_contributors(workspace, repo_slug)`

`BaseClient` provides `get(endpoint)` and `post(endpoint, data)` methods. Both call `raise_for_status()`, so HTTP errors raise exceptions. Requests are sent with `Authorization: Bearer <token>` and `Accept: application/json` headers.

### Front-End

`index.js` attaches click handlers to links matching `nav ul li a`. Each handler prevents the default jump and smoothly scrolls to the element whose ID matches the link's `href`. The page layout and styling are defined in `templates/index.html` and `static/styles.css`.

## Configuration

The only environment variable read by the supplied code is:

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `sqlite:///code_analyzer.db` | SQLAlchemy database URI used by the Flask app |

Example:

```bash
export DATABASE_URL="sqlite:///my_analyzer.db"
```

`CONTRIBUTING.md` refers to adding API keys to a `.env` file. However, the API client classes accept the token as a constructor argument, and no supplied file reads a token from the environment. Applications using the clients must pass the token in explicitly.

## Project Structure

```
.
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── .gitignore
└── src/
    ├── api_clients/
    │   ├── base_client.py
    │   ├── bitbucket_client.py
    │   ├── github_client.py
    │   └── gitlab_client.py
    └── web/
        ├── app.py
        ├── models.py
        ├── static/
        │   ├── index.js
        │   └── styles.css
        └── templates/
            └── index.html
```

## Known Limitations

The supplied source files show several gaps that you should be aware of before running the project:

- **Separate SQLAlchemy instances.** `app.py` creates `db = SQLAlchemy(app)`, while `models.py` creates its own unbound `db = SQLAlchemy()`. The models are defined on the `models.db` instance, which is not the one initialized with the Flask app, so database operations may fail at runtime. Sharing a single `db` object between the two modules would address this.
- **Missing import in client modules.** `bitbucket_client.py`, `github_client.py`, and `gitlab_client.py` subclass `BaseClient` but do not import it. Each file needs `from base_client import BaseClient` (or the equivalent package-relative import) to work.
- **No `requirements.txt` or tests.** `CONTRIBUTING.md` references both a `requirements.txt` file and a `tests/` directory, but neither is present in the supplied file tree.
- **The API clients are not connected to the web app.** No route in `app.py` calls the client classes.
- **Debug mode.** The application runs with `debug=True`, which should be disabled in any non-development deployment.

## Development

Contributions are welcome. The steps below are taken from `CONTRIBUTING.md`:

1. Fork the repository on GitHub.
2. Clone your fork and install dependencies.
3. Create a descriptive feature branch, such as `fix-bug-123` or `add-new-feature`.
4. Make and test your changes.
5. Commit with clear, present-tense messages (for example, "Add feature X").
6. Push the branch to your fork and open a pull request against the original repository.

The contributing guidelines ask for:

- Python code that follows [PEP 8](https://peps.python.org/pep-0008/)
- Meaningful variable and function names
- Docstrings for all functions and classes
- Tests for new features and bug fixes

Bug reports and feature requests should be filed on the project's [Issues](https://github.com/stephenombuya/Code-Contribution-Analyzer/issues) page. Questions can be raised in the [Discussions](https://github.com/stephenombuya/Code-Contribution-Analyzer/discussions) section.

## Testing

`CONTRIBUTING.md` says to add tests to a `tests/` directory and run them with `pytest`:

```bash
pytest
```

No test files or `tests/` directory are included in the supplied repository files, so running `pytest` may not discover any tests at present. A manual check of the API can be done by starting the server and calling the endpoints listed above.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md), version 2.1. Instances of unacceptable behavior can be reported to the address listed in that document.

## License

This project is licensed under the MIT License. Copyright (c) 2025 Stephen Ombuya. See the [LICENSE](LICENSE) file for the full text.
