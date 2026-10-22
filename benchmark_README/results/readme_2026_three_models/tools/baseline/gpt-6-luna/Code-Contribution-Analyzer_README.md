# Code Contribution Analyzer

Code Contribution Analyzer is a Python project with a Flask API, SQLAlchemy models for users, repositories, and contributions, and client classes for querying GitHub, GitLab, and Bitbucket APIs. The web API exposes basic read endpoints and a user-creation endpoint. The provider clients provide methods for fetching repositories or projects and contributor-related data.

The repository also contains a web template, stylesheet, and JavaScript file. The JavaScript adds smooth scrolling to navigation links that point to page sections.

> **Current implementation note:** The supplied files show several integration gaps: the provider-specific client modules do not import `BaseClient`, and the web app and models initialize separate SQLAlchemy instances. These issues may need to be resolved before provider clients or database-backed routes work as intended. See [Implementation notes](#implementation-notes).

## Contents

- [Project layout](#project-layout)
- [Requirements](#requirements)
- [Setup](#setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
- [Testing](#testing)
- [Implementation notes](#implementation-notes)
- [Contributing and conduct](#contributing-and-conduct)
- [License](#license)

## Project layout

```text
src/
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

`src/api_clients/` contains a shared HTTP client and provider-specific subclasses. `src/web/` contains the Flask application, database model definitions, and web assets.

## Requirements

The supplied Python files import Flask, Flask-SQLAlchemy, Flask-CORS, and Requests. A compatible Python installation and these packages are needed to run the corresponding code. The repository file tree provided here does not include a dependency manifest or specify supported Python or package versions.

Install the imported packages directly if they are not already available:

```bash
python -m pip install Flask Flask-SQLAlchemy flask-cors requests
```

## Setup

Clone the repository and enter its directory:

```bash
git clone https://github.com/stephenombuya/Code-Contribution-Analyzer
cd Code-Contribution-Analyzer
```

Install the dependencies listed above. To start the Flask application using its current imports, run it from the web directory:

```bash
cd src/web
python app.py
```

When run as a script, `app.py` calls `db.create_all()` and starts Flask with debug mode enabled. The app configures its database URI from `DATABASE_URL`; if that variable is unset, it uses `sqlite:///code_analyzer.db`.

## Configuration

### Database

Set `DATABASE_URL` in the process environment to select the database URI used by the Flask application. If it is not set, the configured default is SQLite:

```bash
export DATABASE_URL="sqlite:///code_analyzer.db"
```

The database tables defined in `models.py` are `users`, `repositories`, and `contributions`. Their fields and relationships are described in [Data model](#data-model).

### Provider API tokens

Each provider client accepts a token as a constructor argument. The shared `BaseClient` uses that token in an `Authorization: Bearer ...` header and requests JSON responses. The supplied code does not define environment-variable names for provider tokens or load a `.env` file, so callers must provide tokens themselves.

## Usage

### Flask API

The application defines these routes:

| Method | Path | Behavior |
|---|---|---|
| `GET` | `/` | Returns a JSON welcome message. |
| `GET` | `/api/users` | Returns user IDs, names, and email addresses. |
| `POST` | `/api/users` | Creates a user from JSON fields `name` and `email`; returns a success message with status `201`. |
| `GET` | `/api/repositories` | Returns repository IDs, names, URLs, and user IDs. |
| `GET` | `/api/contributions` | Returns contribution IDs, repository IDs, languages, and lines of code. |

For example, the user-creation route expects a JSON request body containing both required fields:

```bash
curl -X POST http://127.0.0.1:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Ada Lovelace","email":"ada@example.com"}'
```

A successful response has the form:

```json
{"message": "User created successfully!"}
```

The list routes return JSON arrays. The supplied application code does not define routes for creating repositories or contributions.

### Data model

- **User**: required `name` and unique, required `email`; can be related to repositories.
- **Repository**: required `name`, `url`, and `user_id`; belongs to a user and can be related to contributions.
- **Contribution**: required `repository_id`, `language`, and integer `lines_of_code`; belongs to a repository.

### Provider API clients

`BaseClient` provides `get(endpoint)` and `post(endpoint, data)` methods. Both build a URL from the configured base URL and endpoint, send the bearer-authenticated request, raise an exception for an unsuccessful HTTP status, and return the decoded JSON response.

The provider subclasses specify these base URLs and operations:

- **GitHub** (`https://api.github.com`): fetch a user’s repositories or a repository’s contributors.
- **GitLab** (`https://gitlab.com/api/v4`): fetch projects or a project’s contributors.
- **Bitbucket** (`https://api.bitbucket.org/2.0`): fetch repositories or a repository’s commits. The latter method is named `fetch_repo_contributors`, but its endpoint is the repository commits endpoint.

These methods are thin wrappers around API requests; the supplied code does not show additional analysis, pagination, or response transformation.

## Development

Follow the project’s contribution instructions in `CONTRIBUTING.md`: create a feature branch, make focused changes, use clear present-tense commit messages, and open a pull request with context about the change. Python changes should follow PEP 8, use meaningful names, and include docstrings for functions and classes.

The JavaScript in `src/web/static/index.js` intercepts clicks on navigation links, prevents the default action, and smoothly scrolls to the element referenced by each link’s `href`. The repository also includes `styles.css` and `templates/index.html`; their detailed behavior is not established by the supplied file contents.

## Testing

The contribution guide recommends adding tests for new features and bug fixes under `tests/` and running:

```bash
pytest
```

No test files or test configuration are included in the supplied repository tree, so there is no documented project-specific test suite or additional test command.

## Implementation notes

Before relying on the current implementation, review these visible integration issues:

- `bitbucket_client.py`, `github_client.py`, and `gitlab_client.py` subclass `BaseClient` but do not import it. Importing those modules as supplied will fail unless the missing import is added.
- `app.py` creates a `SQLAlchemy` instance named `db`, while `models.py` creates a different instance and defines its models on that separate instance. The app’s `db.create_all()` therefore does not register those model classes with the same database instance used by the routes. The instances need to be aligned for database initialization and model queries to work together.
- `app.py` imports `models` as a top-level module. Running the script from `src/web`, as shown in [Setup](#setup), makes that import location available. Importing the application from another working directory may require package-aware imports or a different launch arrangement.
- The app enables CORS globally and runs with Flask debug mode enabled when started directly. Debug mode is appropriate for development, not a production deployment.

## Contributing and conduct

See [CONTRIBUTING.md](CONTRIBUTING.md) for the project’s contribution process and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community expectations. Bug reports and feature requests can be submitted through the repository’s GitHub issue tracker, as described in the contribution guide.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for the full text.
