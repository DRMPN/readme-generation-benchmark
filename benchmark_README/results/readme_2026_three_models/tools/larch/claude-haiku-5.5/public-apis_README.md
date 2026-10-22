# public-apis-9nhmzqub

A set of Python tools that validate the contents of a public API directory. The scripts check that entries are correctly formatted and that their links are reachable, so that contributions stay consistent and broken entries are caught before they are merged. The validators run locally and in continuous integration, and a shell helper automates pull request checks.

> **Note:** This README was inferred from the repository's file names. Verify the usage commands, options, and descriptions against the source code before publishing.

## Table of Contents

- [Features](#features)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Running the Tests](#running-the-tests)
- [Continuous Integration](#continuous-integration)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Format validation** (`format.py`): checks that entries follow the required structure, such as field presence, ordering, allowed values, and Markdown syntax.
- **Link validation** (`links.py`): checks that the URLs referenced by entries are reachable and return valid responses.
- **Pull request automation** (`github_pull_request.sh`): a shell script that runs the checks against the changes in a pull request.
- **Test coverage**: unit tests for both validators.
- **Minimal dependencies**: all Python dependencies are listed in `requirements.txt`.

## Repository Structure

```
public-apis-9nhmzqub/
├── LICENSE                     # Project license
├── CONTRIBUTING.md             # Guidelines for contributors
├── __init__.py                 # Marks the package root
├── format.py                   # Format validation logic
├── links.py                    # Link validation logic
├── github_pull_request.sh      # Script for pull request checks
├── requirements.txt            # Python dependencies
├── __init__.py                 # Marks the tests/package directory
├── test_validate_format.py     # Tests for format validation
└── test_validate_links.py      # Tests for link validation
```

| File | Purpose |
|------|---------|
| `format.py` | Parses entries and reports formatting errors. |
| `links.py` | Sends requests to each link and reports broken or unreachable URLs. |
| `github_pull_request.sh` | Wrapper for running validations on a pull request, typically from CI. |
| `test_validate_format.py` | Unit tests for `format.py`. |
| `test_validate_links.py` | Unit tests for `links.py`. |
| `requirements.txt` | Pinned or minimum versions of required packages. |
| `CONTRIBUTING.md` | Explains how to add or modify entries. |

## Requirements

- Python 3.8 or later (adjust to the version your code requires)
- pip
- Network access, for link validation
- Bash, for `github_pull_request.sh`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/public-apis-9nhmzqub.git
   cd public-apis-9nhmzqub
   ```

2. (Recommended) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate        # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Validate formatting

```bash
python format.py
```

Run this from the directory containing the API list. The script reports any entries that do not match the expected format and exits with a non-zero status code if errors are found.

### Validate links

```bash
python links.py
```

This checks every link in the list. Because it makes network requests, it can take a while on large lists. Broken links are reported with their status codes or error messages.

### Run checks on a pull request

```bash
bash github_pull_request.sh
```

The script runs the validators against the changes in the current pull request. It is intended mainly for CI, but it can also be run locally when the environment variables or Git context it expects are available.

## Running the Tests

Run the full test suite with:

```bash
python -m unittest discover
```

Or run a single test module:

```bash
python -m unittest test_validate_format
python -m unittest test_validate_links
```

If the project uses pytest, you can run:

```bash
pytest
```

The link tests may make network requests. If you want to run tests offline, mock the HTTP calls in `test_validate_links.py`.

## Continuous Integration

The validators are designed to run automatically on every pull request. A typical CI workflow:

1. Checks out the repository.
2. Installs the packages from `requirements.txt`.
3. Runs `format.py` to validate structure.
4. Runs `links.py` to check URLs.
5. Runs the test suite.
6. Fails the build if any step reports an error.

Example GitHub Actions step:

```yaml
- name: Install dependencies
  run: pip install -r requirements.txt

- name: Validate format
  run: python format.py

- name: Validate links
  run: python links.py
```

## Contributing

Contributions are welcome. Before opening a pull request:

1. Read [CONTRIBUTING.md](CONTRIBUTING.md).
2. Run the format and link validators locally.
3. Run the test suite and make sure it passes.
4. Keep each pull request focused on a single change.

If you are fixing a bug in a validator, please add or update a test that reproduces the problem.

## License

This project is licensed under the terms in the [LICENSE](LICENSE) file.
