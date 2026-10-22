# Code Contribution Analyzer

Code Contribution Analyzer is a Python project scaffold for recording users, repositories, and language/lines-of-code contribution records. It also contains small API-client wrappers for GitHub, GitLab, and Bitbucket, plus a static HTML page describing the intended product.

> **Implementation status:** The repository does not currently provide an end-to-end contribution analysis workflow. The web page's advertised fetching, reports, and visualizations are not implemented, and the web app's database/model wiring and provider-client imports need attention before those parts can be used reliably. See [Current limitations](#current-limitations).

## Contents

- `src/web/app.py` — Flask application and JSON routes.
- `src/web/models.py` — SQLAlchemy models for users, repositories, and contributions.
- `src/web/templates/index.html` — static product-description page.
- `src/web/static/` — stylesheet and small navigation script for that page.
- `src/api_clients/` — shared HTTP request helper and provider-specific endpoint wrappers.
- `CONTRIBUTING.md` — contribution instructions.
- `CODE_OF_CONDUCT.md` — community standards.
- `LICENSE` — MIT License.

## Requirements and setup

The repository does not include a dependency manifest or pinned dependency versions. The Python source imports Flask, Flask-SQLAlchemy, Flask-Cors, and `requests`. Install those packages in your environment, for example:

```bash
python -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate
python -m pip install Flask Flask-SQLAlchemy Flask-Cors requests
```

There is no documented, working application launch flow at present. `src/web/app.py` contains a direct-run entry point (`python app.py` from `src/web`), but the database/model mismatch described below means database-backed routes should not be assumed to work. The repository also contains no test suite or `tests/` directory.

## Web API

The Flask application enables CORS and defines these routes:

| Method | Path | Behavior |
| --- | --- | --- |
| `GET` | `/` | Returns `{"message":"Welcome to Code Contribution Analyzer API"}`. |
| `GET` | `/api/users` | Returns user records with `id`, `name`, and `email`. |
| `POST` | `/api/users` | Reads `name` and `email` from a JSON request body, creates a user, and responds with HTTP `201` on success. |
| `GET` | `/api/repositories` | Returns repository records with `id`, `name`, `url`, and `user_id`. |
| `GET` | `/api/contributions` | Returns contribution records with `id`, `repository_id`, `language`, and `lines_of_code`. |

The `User` model requires a unique email address. A repository belongs to a user, and a contribution belongs to a repository. The app reads its SQLAlchemy URI from `DATABASE_URL`; if it is unset, the configured URI is `sqlite:///code_analyzer.db`.

## Provider API-client code

`src/api_clients/base_client.py` defines GET and POST helpers that send bearer-token authorization and an `Accept: application/json` header, raise for unsuccessful HTTP responses, and return decoded JSON. Provider classes define these calls:

- `GitHubClient`: list a user's repositories and fetch a repository's contributors.
- `GitLabClient`: list projects and fetch a project's repository contributors.
- `BitbucketClient`: list repositories and fetch a repository's commits.

These are endpoint wrappers only; they are not connected to the Flask routes or to contribution storage/analysis. Their API responses are returned as-is.

## Current limitations

- `src/web/app.py` creates a `SQLAlchemy` extension, while `src/web/models.py` creates a separate extension for the model classes. As written, the app's database setup and the models are not registered with the same extension, so the database routes and table creation are not properly wired together.
- Each provider module subclasses `BaseClient` without importing it. The client classes therefore cannot be imported as-is without fixing that dependency.
- The Flask root route returns JSON. The HTML template is not rendered by a route, and the described analysis, report generation, and visualizations have no implementation in the checked-in code.
- There is no `requirements.txt`, packaging metadata, environment template, or automated test suite in the repository. The dependency command above is based on imports in the source and does not pin versions.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the project's contribution process and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community expectations. The contribution guide mentions `requirements.txt` and a `tests/` directory, but neither is currently present in this repository.

## License

This project is distributed under the [MIT License](LICENSE).
