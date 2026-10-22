# Code Contribution Analyzer

A comprehensive tool for analyzing code contributions across multiple Git hosting platforms — **GitHub**, **GitLab**, and **Bitbucket**. The application aggregates contribution data (commits, pull/merge requests, issues, and reviews) and presents insights through a clean web interface.

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Frontend](#-frontend)
- [Contributing](#-contributing)
- [Code of Conduct](#-code-of-conduct)
- [License](#-license)

## ✨ Features

- **Multi-platform support**: Fetch contribution data from GitHub, GitLab, and Bitbucket through a unified interface.
- **Unified client architecture**: All platform clients inherit from a common base client, making it easy to add new providers.
- **Contribution metrics**: Analyze commits, pull/merge requests, issues, and reviewer activity per contributor.
- **REST API backend**: Flask-based API (`app.py`) that serves analysis results.
- **Interactive web UI**: A lightweight frontend (`index.html`, `styles.css`, `index.js`) to visualize contribution analytics.

## 📁 Project Structure

```
Code-Contribution-Analyzer-pso1easb/
├── app.py                 # Flask application entry point / API routes
├── models.py              # Data models (contributors, commits, PRs, etc.)
├── base_client.py         # Abstract base client shared by all providers
├── github_client.py       # GitHub API integration
├── gitlab_client.py       # GitLab API integration
├── bitbucket_client.py    # Bitbucket API integration
├── index.html             # Frontend page
├── styles.css             # Frontend styling
├── index.js               # Frontend logic (fetches from the API, renders results)
├── LICENSE
├── CODE_OF_CONDUCT.md
└── CONTRIBUTING.md
```

## ✅ Requirements

- Python 3.8+
- `pip` for installing Python dependencies
- A modern web browser
- (Optional) API tokens for the platforms you want to query

## 🚀 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/Code-Contribution-Analyzer-pso1easb.git
   cd Code-Contribution-Analyzer-pso1easb
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install flask requests
   ```

## ⚙️ Configuration

The clients look for access tokens via environment variables:

| Platform  | Environment Variable   | Required |
|-----------|------------------------|----------|
| GitHub    | `GITHUB_TOKEN`         | Optional (raises rate limits) |
| GitLab    | `GITLAB_TOKEN`         | Recommended for private repos |
| Bitbucket | `BITBUCKET_TOKEN`      | Recommended for private repos |

Example:

```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
export GITLAB_TOKEN="glpat-xxxxxxxxxxxx"
export BITBUCKET_TOKEN="xxxxxxxxxxxx"
```

## 💻 Usage

### 1. Start the backend

```bash
python app.py
```

By default the API runs at `http://localhost:5000`.

### 2. Open the frontend

Open `index.html` in your browser (or serve it statically), enter a repository (e.g., `owner/repo`), select a platform, and view the contribution analysis.

### 3. Query the API directly

```bash
curl http://localhost:5000/api/analyze?platform=github&repo=owner/repo
```

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/analyze` | Returns contribution analysis for a repository. Query params: `platform` (`github` / `gitlab` / `bitbucket`), `repo` |
| `GET`  | `/api/contributors` | Lists contributors for a repository |
| `GET`  | `/health` | Service health check |

## 🖥️ Frontend

The frontend is plain HTML/CSS/JavaScript with no build step:

- **index.html** – main page layout and input form
- **styles.css** – styling and responsive layout
- **index.js** – form handling, API calls, and rendering of results

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to submit issues and pull requests.

## 📜 Code of Conduct

This project follows the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold it.

## 📄 License

This project is licensed under the terms described in the [LICENSE](LICENSE) file.
