# Code-Contribution-Analyzer-nc3smdct

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

The Code Contribution Analyzer is a Python web application that aggregates code contribution data from git hosting platforms and exposes it through a JSON REST API together with a browser-based frontend. It targets developers who want to track repository and contribution activity across providers such as GitHub and GitLab, either programmatically via the API endpoints or interactively through the web interface. The backend relies on authenticated provider API clients and stores users, repositories, and contribution records in a database. For runnable setup and usage steps, see the Getting Started section.

---

## Core Features

- Aggregates code contribution data from git hosting platforms through dedicated GitHub and GitLab API clients, giving developers a single place to pull user, repository, and contributor information.
- Exposes a JSON REST API where users can be listed and created (POST /api/users), and repositories and contributions can be listed (GET /api/repositories, GET /api/contributions), enabling programmatic consumption from scripts and other tools.
- Persists users, repositories, and contributions in a relational database via SQLAlchemy, with the database configurable through the DATABASE_URL environment variable.
- Provides a shared base client with bearer-token authentication and GET/POST helpers, on which the GitHub and GitLab clients are built; a Bitbucket client module (`bitbucket_client.py`) is also present in the repository.
- Ships a browser frontend with server-rendered templates and static JavaScript/CSS, so contribution data can be viewed without writing custom client code.

---

## Installation

No setup file for dependencies was found in the repository, so the backend packages must be installed manually.

**Using the current local checkout:**

1. Open the repository root:

```sh
cd path/to/Code-Contribution-Analyzer-nc3smdct
```

2. Install the backend dependencies:

```bash
pip install flask flask-sqlalchemy flask-cors requests
```

3. Continue with the [Getting Started](#getting-started) section to run the application.

---

## Getting Started

Follow the steps below to set up and run the application locally.

### Prerequisites

- Python installed on your machine.
- The following packages, used by the backend: `Flask`, `Flask-SQLAlchemy`, `Flask-CORS`, and `requests`.
- (Optional) A personal access token for GitHub or GitLab if you plan to use the API clients in `src/api_clients/` (`GitHubClient` and `GitLabClient` accept a bearer token).

### Quickstart

1. Install the backend dependencies as described in [Installation](#installation).

2. Start the Flask app. Run it from `src/web/` so that `app.py` can import `models.py`:

```bash
   cd src/web
   python app.py
```

   The app runs in debug mode (`app.run(debug=True)`) and creates the SQLite database (`code_analyzer.db`) on startup via `db.create_all()`.

3. Verify the server is running:

```bash
   curl http://127.0.0.1:5000/
```

   You should receive a JSON response with a welcome message from the API.

4. Try the core API endpoints:

```bash
   # Create a user
   curl -X POST http://127.0.0.1:5000/api/users -H "Content-Type: application/json" -d '{"name": "Alice", "email": "alice@example.com"}'

   # List users
   curl http://127.0.0.1:5000/api/users

   # List repositories and contributions
   curl http://127.0.0.1:5000/api/repositories
   curl http://127.0.0.1:5000/api/contributions
```

### Configuration

- By default the app uses a local SQLite database (`sqlite:///code_analyzer.db`). You can override this by setting the `DATABASE_URL` environment variable before starting the app.

---

## Architecture

The project is a modular monolith built around a single Flask application, with the following major subsystems:

- **Web/API layer** (`src/web/app.py`): a single Flask app exposing a JSON REST API — `GET/POST /api/users`, `GET /api/repositories`, `GET /api/contributions` — with CORS enabled. Handlers query or update SQLAlchemy models and return JSON responses.
- **Data layer** (`src/web/models.py`): SQLAlchemy models `User`, `Repository`, and `Contribution`, linked by foreign keys (`users.id`, `repositories.id`) with one-to-many relationships (a user has repositories; a repository has contributions). Storage defaults to SQLite (`sqlite:///code_analyzer.db`) and can be overridden via the `DATABASE_URL` environment variable; tables are created at startup with `db.create_all()`.
- **Provider clients** (`src/api_clients/`): platform integrations built on a shared `BaseClient` that provides bearer-token authentication and generic `get`/`post` helpers over `requests`. `GitHubClient` and `GitLabClient` subclass it with provider-specific endpoints (e.g., fetching repositories/projects and contributors); a `bitbucket_client.py` module is also present, though its contents were not available for review.
- **Frontend** (`src/web/templates/`, `src/web/static/`): a lightweight browser UI served from HTML templates with static JavaScript and CSS, alongside the JSON API.

Control/data flow: external API consumers call the Flask endpoints, which read from and write to the relational database via the SQLAlchemy models. Provider clients call the respective hosting-platform REST APIs over HTTPS using bearer tokens.

Note: the provided code does not show direct wiring between `app.py` and the `api_clients` package, so the exact integration path between the web layer and the provider clients is not evidenced.

---

## API Reference

### REST API (`src/web/app.py`)

All routes return JSON responses. CORS is enabled on the Flask app.

| Method | Endpoint | Purpose |
|--------|----------|----------|
| `GET` | `/` | Welcome message for the API. |
| `GET` | `/api/users` | List all users. |
| `POST` | `/api/users` | Create a user; the JSON body must include `name` and `email`. |
| `GET` | `/api/repositories` | List all repositories. |
| `GET` | `/api/contributions` | List all contributions. |

### API clients (`src/api_clients/`)

`BaseClient` sets `Authorization: Bearer <token>` and `Accept: application/json` headers and provides generic `get` and `post` helpers over `requests`; both raise on HTTP errors and return the parsed JSON body.

| Class | Description |
|-------|-------------|
| `GitHubClient` | Extends `BaseClient` with GitHub-specific endpoints, including fetching repositories and contributors. |
| `GitLabClient` | Extends `BaseClient` with GitLab-specific endpoints, including fetching projects and contributors. |

The exact method signatures and base URLs for each client are defined in the source files under `src/api_clients/`; consult the code for details.

A `bitbucket_client.py` file exists in the tree, but its interface is not covered here (source content not provided).

### Data models (`src/web/models.py`)

SQLAlchemy models backing the endpoints above:

- `User` (table `users`): `id`, `name`, `email` (unique); related repositories exposed via `User.repositories` (backref `Repository.user`).
- `Repository` (table `repositories`): `id`, `name`, `url`, `user_id` (FK → `users.id`); related contributions exposed via `Repository.contributions` (backref `Contribution.repository`).
- `Contribution` (table `contributions`): `id`, `repository_id` (FK → `repositories.id`), `language`, `lines_of_code`.

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to Code-Contribution-Analyzer-nc3smdct.
- **[Code of Conduct](./CODE_OF_CONDUCT.md)**: Please review the code of conduct before contributing.

---

## License

Refer to the [LICENSE](./LICENSE) file for the licensing terms that apply to this project.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). Code-Contribution-Analyzer-nc3smdct repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{Code-Contribution-Analyzer-nc3smdct,

        author = {README Benchmark},

        title = {Code-Contribution-Analyzer-nc3smdct repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---