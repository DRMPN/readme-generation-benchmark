# public-apis-s_v294ls

A curated collection of free, public APIs presented as a structured, machine-readable dataset — complete with automated validation tooling to keep entries well-formatted and their links alive.

## Overview

This repository serves two purposes:

1. **A dataset of public APIs** — stored in `links.py`, the project provides a list of publicly available APIs with metadata (name, description, URL, category, and authentication requirements).
2. **A validation toolkit** — a small Python package that automatically verifies that every entry is correctly formatted and that every link actually resolves, so the dataset stays accurate over time.

## Repository Structure

```
public-apis-s_v294ls/
├── LICENSE                       # Project license
├── CONTRIBUTING.md               # Guidelines for contributing new entries
├── requirements.txt              # Python dependencies
│
├── links.py                      # The dataset: list of public API entries
├── format.py                     # Schema/format definitions and formatting helpers
│
├── test_validate_links.py        # Tests that validate all URLs are reachable
├── test_validate_format.py       # Tests that validate all entries match the schema
│
├── github_pull_request.sh        # Helper script for the PR workflow
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.7+
- `pip`

### Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/your-username/public-apis-s_v294ls.git
cd public-apis-s_v294ls
pip install -r requirements.txt
```

## Usage

### Browsing the APIs

The dataset lives in `links.py`. You can import it in your own project:

```python
from links import APIS

for api in APIS:
    print(api.name, api.url, api.category)
```

### Validating the Dataset

Run the test suite to verify that every entry is well-formatted and every link works:

```bash
# Validate entry format (required fields, correct structure)
python -m pytest test_validate_format.py -v

# Validate links (checks HTTP status of each URL)
python -m pytest test_validate_links.py -v
```

Or run everything at once:

```bash
python -m pytest -v
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first. The general workflow is:

1. Fork the repository and create a new branch.
2. Add or update API entries in `links.py`, following the format defined in `format.py`.
3. Run both validation test suites locally to make sure your entry passes.
4. Submit a pull request — the `github_pull_request.sh` script can help automate parts of this flow.

All pull requests are automatically checked to ensure:

- **Format validity** — entries contain all required fields with correct types (`test_validate_format.py`).
- **Link liveness** — the API's URL returns a valid HTTP response (`test_validate_links.py`).

## License

This project is released under the terms of the [LICENSE](LICENSE) file included in this repository.

## Acknowledgments

Inspired by the open-source "public-apis" movement — thanks to everyone who curates, maintains, and contributes to free public API directories.
