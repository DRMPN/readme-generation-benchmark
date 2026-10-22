# SMSBoom-9h7lzdis

> **Note:** I could only see the file names in this repository, not their contents. The descriptions below are inferred from the names and should be checked against the code before publishing. Items marked **[TODO]** need confirmation from the source.

---

## Table of Contents

- [Overview](#overview)
- [⚠️ Disclaimer and Responsible Use](#️-disclaimer-and-responsible-use)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Command-Line Interface](#command-line-interface)
  - [Graphical User Interface](#graphical-user-interface)
  - [API Server](#api-server)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Database](#database)
- [Logging](#logging)
- [Docker](#docker)
- [Screenshots and Demos](#screenshots-and-demos)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Overview

**SMSBoom-9h7lzdis** is a Python project that sends automated, repeated requests to SMS verification and one-time-password (OTP) endpoints of third-party web services. It is packaged as:

- a **command-line tool** (`smsboom.py`),
- a **desktop GUI** (`smsboom_GUI.py`),
- a **web API service** (`spider-api.py`, `tou_api.py`) with a JavaScript client (`api.js`) and a Docker image.

The project uses a local SQLite database (`api.db`) to store the list of supported service endpoints and related data, and JSON files to describe API definitions.

---

## ⚠️ Disclaimer and Responsible Use

This software triggers SMS messages to phone numbers. Sending SMS messages to a number without the owner's consent can constitute harassment and may be illegal under laws such as the Telecommunications Consumer Protection Act (US), the Privacy and Electronic Communications Regulations (UK), and similar laws elsewhere.

**By using this software you agree that:**

1. You will only test with phone numbers that you own or have explicit written permission to test.
2. You will not use this tool to harass, intimidate, or flood any person or service.
3. You are solely responsible for complying with the terms of service of every third-party platform you interact with and all applicable laws.
4. The authors and contributors accept no liability for misuse or resulting damage.

The intended use is security research, rate-limit testing of your own services, and education about OTP abuse prevention.

---

## Features

Based on the project files, the tool appears to provide:

- **Multi-service SMS request dispatching** using a service list stored in the database and JSON definitions.
- **Three interfaces:** CLI, desktop GUI (with a Windows `logo.ico` icon), and HTTP API.
- **Pluggable API definitions** via several JSON files (`api.json`, `touapi.json`, `api_tou.json`, `GETAPI.json`, `hz-web.json`).
- **Persistent storage** with SQLite (`api.db`), accessed through `sql.py` and `models.py`.
- **Centralized request handling** in `req.py`.
- **Logging** through `log.py`.
- **Docker support** for running the API service in a container.
- **Separate dev dependencies** for testing and tooling.

**[TODO]** Confirm which features are actually implemented, such as rate limiting, proxy support, threading or async, and retry logic.

---

## Project Structure

```
SMSBoom-9h7lzdis/
├── LICENSE                 # Project license
├── smsboom.py              # CLI entry point
├── smsboom_GUI.py          # GUI entry point
├── logo.ico                # Application icon
├── api.db                  # SQLite database
├── __init__.py             # Package initializer
├── hz-web.json             # API definition (hz-web service)
├── api.js                  # JavaScript API client
├── spider-api.py           # Web API server
├── tou_api.py              # Additional API module
├── touapi.json             # API definition (tou service)
├── api_tou.json            # API definition (tou service, alternate)
├── GETAPI.json             # API definition (GET-based endpoints)
├── api.json                # General API definition
├── Dockerfile              # Container build instructions
├── __init__.py             # Package initializer
├── req.py                  # HTTP request handling
├── sql.py                  # Database access helpers
├── models.py               # Data models
├── log.py                  # Logging configuration
├── cmd1.png                # Command-line screenshot
├── cmd2.png                # Command-line screenshot
├── GIF111.gif              # Demo animation
├── test2.gif               # Demo animation
├── e.g.1.png               # Example screenshot
├── smsboom_GUI.py          # GUI application (see above)
├── requirements.txt        # Runtime dependencies
└── requirements-dev.txt    # Development dependencies
```

### Key Components

| File | Purpose (inferred) |
|------|--------------------|
| `smsboom.py` | Parses arguments and runs the dispatcher from the terminal |
| `smsboom_GUI.py` | Provides the graphical front end |
| `spider-api.py` | Runs the HTTP service that exposes the tool over the network |
| `tou_api.py` | Supplementary API logic |
| `req.py` | Builds and sends HTTP requests to target endpoints |
| `sql.py` | Executes queries against `api.db` |
| `models.py` | Defines the data structures for services and records |
| `log.py` | Configures log output and log files |
| `api*.json`, `touapi.json`, `GETAPI.json`, `hz-web.json` | Describe the endpoints, methods, headers, and payloads for each service |
| `api.js` | Client-side helper for calling the API from JavaScript |
| `Dockerfile` | Builds a container image for the API service |

---

## Requirements

- **Python 3.8+** **[TODO]** confirm the minimum version
- **pip**
- **Docker** (optional, for containerized deployment)
- **Node.js** (optional, only if you use `api.js` directly)
- A desktop environment with Tk support for the GUI **[TODO]** confirm the GUI toolkit

Python packages are listed in `requirements.txt` (runtime) and `requirements-dev.txt` (development).

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/SMSBoom-9h7lzdis.git
cd SMSBoom-9h7lzdis
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

For development:

```bash
pip install -r requirements-dev.txt
```

### 4. Verify the database

`api.db` ships with the repository. If it is missing or corrupted, **[TODO]** describe how to recreate it (for example, `python -m sql --init`).

---

## Usage

### Command-Line Interface

**[TODO]** Replace the examples below with the real flags from `smsboom.py`.

```bash
python smsboom.py --help
```

Example (illustrative only):

```bash
python smsboom.py --target <phone-number> --count <n> --delay <seconds>
```

See `cmd1.png` and `cmd2.png` for example terminal output.

### Graphical User Interface

```bash
python smsboom_GUI.py
```

The GUI is useful for users who prefer not to use the terminal. Screenshots and demo animations are in the [Screenshots and Demos](#screenshots-and-demos) section.

### API Server

Start the server:

```bash
python spider-api.py
```

**[TODO]** Confirm the default host, port, and any environment variables. A typical default would be `http://127.0.0.1:5000`.

Once running, the API can be called with any HTTP client:

```bash
curl -X POST http://127.0.0.1:5000/<endpoint> \
     -H "Content-Type: application/json" \
     -d '{"phone": "<your-own-number>"}'
```

---

## API Reference

**[TODO]** Fill this section from `api.json`, `GETAPI.json`, and the route definitions in `spider-api.py`.

| Method | Endpoint | Description | Request body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/<endpoint>` | **[TODO]** | — | **[TODO]** |
| `POST` | `/<endpoint>` | **[TODO]** | **[TODO]** | **[TODO]** |

### JavaScript Client

`api.js` provides a wrapper for calling the API from Node.js or a browser.

```javascript
// Example usage (illustrative; confirm exported names in api.js)
const api = require('./api.js');
```

---

## Configuration

Configuration appears to be driven by the JSON definition files and possibly environment variables.

- **Service definitions:** `api.json`, `touapi.json`, `api_tou.json`, `GETAPI.json`, `hz-web.json`
- **Database:** `api.db` (SQLite)
- **Logging:** `log.py`
- **Container:** `Dockerfile`

**[TODO]** Document each setting, its default, and whether it can be set through an environment variable.

---

## Database

The project uses SQLite. `sql.py` handles queries and `models.py` defines the schema objects.

**[TODO]** Add the table names, columns, and relationships. Example layout:

| Table | Columns | Purpose |
|-------|---------|---------|
| **[TODO]** | **[TODO]** | **[TODO]** |

To inspect the database:

```bash
sqlite3 api.db ".tables"
```

---

## Logging

`log.py` sets up logging. **[TODO]** Confirm:

- the log file location,
- the log level and how to change it,
- the log format.

---

## Docker

Build the image:

```bash
docker build -t smsboom-api .
```

Run the container:

```bash
docker run -p 5000:5000 smsboom-api
```

**[TODO]** Confirm the exposed port in the `Dockerfile` and add any required environment variables or volume mounts (for example, to persist `api.db` and logs).

---

## Screenshots and Demos

| File | Description |
|------|-------------|
| `cmd1.png` | Command-line interface |
| `cmd2.png` | Command-line interface (second example) |
| `e.g.1.png` | Example output |
| `GIF111.gif` | Animated demo |
| `test2.gif` | Animated demo |

Example image embedding:

```markdown
![CLI example](cmd1.png)
![GUI demo](GIF111.gif)
```

---

## Development

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

**[TODO]** Add the test command (for example, `pytest`), linting tools, and code style guidelines.

Suggested workflow:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Make your changes and add tests.
4. Open a pull request with a clear description.

---

## Troubleshooting

| Problem | Possible cause | Solution |
|---------|----------------|----------|
| `ModuleNotFoundError` | Dependencies not installed | Run `pip install -r requirements.txt` |
| Database errors | `api.db` missing or locked | Restore `api.db` or close other processes using it |
| GUI does not start | Tk not available | Install Tk for your Python distribution |
| API port in use | Another process on the same port | Change the port or stop the conflicting process |
| Docker build fails | Outdated base image or network issue | Rebuild with `--no-cache` |

---

## Contributing

Contributions are welcome, provided they support legitimate, defensive, or educational goals. Pull requests that add features whose main purpose is harassment, or that bypass consent or safeguards, will not be accepted.

1. Read this README and the LICENSE.
2. Open an issue to discuss significant changes.
3. Follow the development workflow above.

---

## License

This project is licensed under the terms in the [LICENSE](LICENSE) file. **[TODO]** State the license name here (for example, MIT or GPL-3.0).

---

## Acknowledgements

- Thanks to all contributors and to the open-source libraries this project depends on.
- **[TODO]** Credit any upstream projects, API references, or inspiration sources.

---

*If you find this project useful for security testing, please use it responsibly and only on systems and phone numbers you are authorized to test.*
