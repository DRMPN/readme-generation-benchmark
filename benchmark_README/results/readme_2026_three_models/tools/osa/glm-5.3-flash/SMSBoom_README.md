# SMSBoom-95qy4w01

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

SMSBoom is a Python-based command-line tool that automates submitting SMS requests to third-party web endpoints, described in-code as SMS pressure testing. It is aimed at end users who run the tool directly rather than at developers consuming a library API. The project provides two interfaces: a command-line interface with configurable concurrency, frequency, and optional proxy support, plus a simple graphical interface built on Tkinter. API endpoint definitions are loaded from runtime data files, with a built-in update command to refresh them from a remote source when loading fails. See Getting Started for runnable setup and usage steps.

---

## Installation

Install SMSBoom-95qy4w01 using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/SMSBoom-95qy4w01
```

2. Install the project dependencies:

```sh
pip install -r requirements.txt
```

---

## Getting Started

**Prerequisites**

- Python 3 (the included Dockerfile is based on `python:3.9-alpine`).
- Dependencies are pinned in `requirements.txt`.

**Steps**

1. Install the dependencies:

```bash
    pip install -r requirements.txt
```

    Or use pipenv, exactly as the Dockerfile does:

```bash
    pip install pipenv && pipenv install --deploy --ignore-pipfile
```

    (Note: `requirements.txt` pins exact versions and also sets a PyPI mirror index.)

2. Make sure `api.json` and `GETAPI.json` exist in the project root. Both are loaded at runtime and define the request endpoints; if they are missing or cannot be parsed, the CLI logs an error and re-downloads the interface data from GitHub (the `update` command).

3. Run the CLI entry point (this is also the Docker container's entrypoint):

```bash
    python smsboom.py
```

4. View the available options with the built-in help:

```bash
    python smsboom.py --help
```

5. Alternatively, start the Tkinter GUI entry point:

```bash
    python smsboom_GUI.py
```

**Docker**

The `Dockerfile` installs the dependencies with pipenv and sets `pipenv run python smsboom.py` as the container entrypoint. Build the image with:

```bash
docker build .
```

---

## Contributing

---

## License

This project is protected under the Apache 2.0. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). SMSBoom-95qy4w01 repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{SMSBoom-95qy4w01,

        author = {README Benchmark},

        title = {SMSBoom-95qy4w01 repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---