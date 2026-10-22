# Code Contribution Analyzer

A Flask-based web application and REST API for tracking and analyzing code contributions. It fetches contribution data from GitHub, GitLab, and Bitbucket, stores it locally, and exposes it through a JSON API with a simple web frontend.

## Features

- Fetches user repositories and contributors from **GitHub**, **GitLab**, and **Bitbucket** APIs.
- Stores users, repositories, and contribution metrics (language, lines of code) in a database.
- REST API endpoints for querying users, repositories, and contributions.
- Built-in web frontend served from `src/web/templates` and `src/web/static`.

## Project Structure

```
.
├── src/
│   ├── api_clients/
│   │   ├── base_client.py      # Shared HTTP client with bearer-token auth
│   │   ├── github_client.py    # GitHub API client
│   │   ├── gitlab_client.py    # GitLab API client
│   │   └── bitbucket_client.py # Bitbucket API client
│   └── web/
│       ├── app.py              # Flask application and API routes
│       ├── models.py           # SQLAlchemy models (User, Repository, Contribution)
│       ├── templates/
│       │   └── index.html      # Frontend page
│       └── static/
│           ├── styles.css
│           └── index.js
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── LICENSE
```

## Requirements

- Python 3 with the following packages: `Flask`, `Flask-SQLAlchemy`, `Flask-CORS`, and `requests`.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/stephenombuya/Code-Contribution-Analyzer
   cd Code-Contribution-Analyzer
   ```

2. Install the dependencies:
   ```bash
   pip install flask flask-sqlalchemy flask-cors requests
   ```

## Configuration

The application reads configuration from environment variables:

- `DATABASE_URL` — SQLAlchemy database URI. Defaults to `sqlite:///code_analyzer.db` if not set.
- API clients require a personal access token for the respective platform (GitHub, GitLab, or Bitbucket), passed when instantiating the client.

## Running the Application

Start the Flask development server from the repository root:

```bash
python src/web/app.py
```

On startup, the application creates the database tables (`db.create_all()`) and runs in debug mode.

## API Endpoints

| Method | Endpoint             | Description                              |
|--------|----------------------|------------------------------------------|
| GET    | `/`                  | Welcome message                          |
| GET    | `/api/users`         | List all stored users                    |
| POST   | `/api/users`         | Create a user (`name`, `email` required) |
| GET    | `/api/repositories`  | List all stored repositories             |
| GET    | `/api/contributions` | List all stored contributions            |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on reporting bugs, requesting features, and submitting pull requests. Please review the [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## License

This project is licensed under the [MIT License](LICENSE).
