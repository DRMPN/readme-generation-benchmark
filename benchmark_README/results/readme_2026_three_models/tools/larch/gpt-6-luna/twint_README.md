# Twint

Twint is a Python tool for searching and collecting publicly available Twitter/X posts and user information without using the official API. It can be used from the command line or imported into Python scripts.

> **Compatibility note:** Twint relies on Twitter/X’s website and internal endpoints, which can change without notice. Searches may return incomplete results or stop working when the service changes. This repository may also depend on older Python packages; check the project’s installation and runtime behavior in your environment.

## Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Command-line usage](#command-line-usage)
- [Python usage](#python-usage)
- [Output options](#output-options)
- [Docker](#docker)
- [Project layout](#project-layout)
- [Troubleshooting](#troubleshooting)
- [Responsible use](#responsible-use)
- [License](#license)

## Features

Depending on the available data and the current behavior of Twitter/X, Twint can be used to:

- Search for posts by username, search term, or other criteria.
- Restrict searches by date, language, or location.
- Retrieve public profile and account-related information.
- Save results as CSV or JSON, or work with database and other output integrations.
- Run searches interactively from the command line or programmatically from Python.

Results and available options depend on the service, the query, and the version of this project.

## Requirements

- Python 3
- The dependencies declared by `setup.py`
- Network access to Twitter/X

Because this project uses web-facing endpoints rather than a stable official API, network access alone does not guarantee that a query will succeed.

## Installation

### Install from a local checkout

From the repository root:

```bash
python -m pip install .
```

For development, install the checkout in editable mode:

```bash
python -m pip install -e .
```

### Install from a package index

If a compatible package release is available in your environment:

```bash
python -m pip install twint
```

Installation success does not guarantee compatibility with the current Twitter/X website or with every Python version.

## Command-line usage

After installation, the `twint` command may be available. You can also try running the package as a module:

```bash
twint --help
```

```bash
python -m twint --help
```

Use the help output for the exact options supported by your installed version.

### Search posts

Search for posts from a user:

```bash
twint -u username
```

Search for a phrase or term:

```bash
twint -s "search terms"
```

Combine a username and a search term:

```bash
twint -u username -s "search terms"
```

### Limit a search by date

Use ISO-style dates:

```bash
twint -u username --since 2020-01-01 --until 2020-01-31
```

Date boundaries and inclusivity may vary with the version and the service’s search behavior.

### Save results

Write results to a file:

```bash
twint -u username -o results.csv --csv
```

```bash
twint -s "search terms" -o results.json --json
```

Check `twint --help` for the output flags available in your checkout.

### User-related searches

Some versions provide commands or options for retrieving public account information and relationships, such as followers, following accounts, favorites, or profile details. These options may be subject to service limits and may not be available in every version. Consult the installed command’s help:

```bash
twint --help
```

## Python usage

Twint can also be called from a Python script. A typical search has this form:

```python
import twint

config = twint.Config()
config.Username = "username"
config.Limit = 20

twint.run.Search(config)
```

A search-term example:

```python
import twint

config = twint.Config()
config.Search = "search terms"
config.Limit = 50

twint.run.Search(config)
```

To store results as CSV, configure the output options supported by your version:

```python
import twint

config = twint.Config()
config.Username = "username"
config.Store_csv = True
config.Output = "results.csv"

twint.run.Search(config)
```

The Python API and configuration fields can differ between releases. If an example does not work, inspect `config.py` and the package’s command-line help for the names supported by this checkout.

## Output options

The repository includes modules for output and integrations, including CSV/JSON writing, database storage, Elasticsearch, and pandas-related handling. Availability and configuration depend on the installed dependencies and the options implemented by this version.

Use the command-line help and the relevant modules to confirm the supported format and settings before running a large collection job. When saving results, make sure the destination path is writable and that there is adequate disk space.

## Docker

A `Dockerfile` is included. From the repository root, build an image with:

```bash
docker build -t twint .
```

Run the image using the command and options supported by the image:

```bash
docker run --rm twint --help
```

If you want output files to persist on the host, mount a host directory into the container and write results there. For example:

```bash
docker run --rm \
  -v "$PWD/output:/output" \
  twint -u username -o /output/results.csv --csv
```

The correct entry point may depend on the contents of the `Dockerfile`; inspect it if the example command does not match the image configuration.

## Project layout

The repository separates the main functionality into modules, including:

- `config.py` — configuration for searches and output.
- `run.py`, `get.py`, `feed.py`, `tweet.py`, and `user.py` — search and data retrieval logic.
- `cli.py` — command-line interface.
- `output.py`, `format.py`, `write.py`, and `write_meta.py` — result formatting and writing.
- `db.py`, `elasticsearch.py`, and `panda.py` — database and data-tool integrations.
- `url.py`, `token.py`, and `datelock.py` — supporting request and query utilities.
- `setup.py` — package installation configuration.
- `Dockerfile` — container build instructions.

## Troubleshooting

### The command is not found

Confirm that installation completed successfully and that the Python environment’s executable directory is on your `PATH`. You can also try:

```bash
python -m twint --help
```

### A search returns no results

Try a simpler query, remove date or location restrictions, and verify that the account or search term is public. Search availability can also change independently of this project.

### Requests fail or results are incomplete

Twitter/X may change its website, request behavior, or access controls. Try again later and check whether the version of this repository is compatible with the current service. Do not assume that a successful run returns every matching post.

### An output integration cannot be imported

Some integrations may require optional packages. Check the dependency declarations in `setup.py` and install the relevant dependencies in the same Python environment as Twint.

## Responsible use

Use Twint only to access information you are authorized to collect. Respect applicable laws, privacy expectations, and the service’s terms and access restrictions. Avoid collecting or redistributing sensitive personal information, and use appropriate safeguards when storing or sharing results.

## License

See the [`LICENSE`](LICENSE) file for the license and applicable terms.
