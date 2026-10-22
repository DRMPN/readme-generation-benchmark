# public-apis

**public-apis** is a community-maintained, collective list of free, public APIs for building software and web applications. Alongside the API list itself, this repository contains a set of automated validation scripts under `scripts/` that keep the list consistently formatted and its hyperlinks healthy. Every pull request triggers a build that runs these checks, and contributors are expected to confirm the build passes before their changes can be accepted.

This document covers that tooling: installation, usage, enforced rules, development, and testing.

## Overview

The repository provides three pieces of automation:

1. **Format validator** — `scripts/validate/format.py`. A pure standard-library Python script that verifies the structure and style of the API tables in a Markdown file: alphabetical ordering per category, required columns, title/description rules, allowed Auth/HTTPS/CORS values, index completeness, and minimum entries per category. Errors are printed with line numbers and the exit code is non-zero.
2. **Link validator** — `scripts/validate/links.py`. A Python script built on `requests` that extracts every URL from the file, rejects duplicate links, and by default issues an HTTP GET to each link to confirm it works. Duplicates or failing links cause a non-zero exit.
3. **Pull request checker** — `scripts/github_pull_request.sh`. A Bash wrapper for CI that downloads a pull request's diff, isolates the added lines, and runs the link validator against them.

All tools exit with `0` on success and `1` on failure, so they can be wired directly into a CI build.

## Repository structure

```
.
├── CONTRIBUTING.md                     # Contribution and formatting guidelines
├── LICENSE                             # MIT license
└── scripts/
    ├── github_pull_request.sh          # CI helper: validate links added by a PR
    ├── requirements.txt                # Pinned Python dependencies
    ├── validate/
    │   ├── __init__.py                 # Package initializer
    │   ├── format.py                   # Markdown table format validator
    │   └── links.py                    # Link extraction, duplicate and health checks
    └── tests/
        ├── __init__.py
        ├── test_validate_format.py     # Unit tests for format.py
        └── test_validate_links.py      # Unit tests for links.py
```

## Setup

### Prerequisites

- Python 3.6 or later (the code uses f-strings and type annotations)
- `pip` for dependency installation
- Outbound network access for link validation
- Bash, `curl`, and `python` on the `PATH` for the pull request script

### Installation

```bash
git clone <repository-url>
cd <repository-name>
pip install -r scripts/requirements.txt
```

`requests` is the only direct third-party dependency; `certifi`, `charset-normalizer`, `idna`, and `urllib3` are its transitive dependencies. All versions are pinned in `scripts/requirements.txt` for reproducible installs.

## Usage

### Format validation

```bash
python scripts/validate/format.py README.md
```

The script expects at least one argument: the path to a Markdown file containing the API table syntax. If none is supplied it prints `No .md file passed (file should contain Markdown table syntax)` and exits `1`. On success it exits `0` silently; on failure it prints one message per problem, prefixed with the 1-based line number (for example `(L042) ...`), and exits `1`.

### Link validation

```bash
python scripts/validate/links.py README.md
python scripts/validate/links.py README.md --only_duplicate_links_checker   # or -odlc
```

- Links are extracted starting at the `## Index` heading (the whole file is scanned if the heading is missing). URLs inside Markdown link syntax are recognized, along with plain `http(s)` URLs including query strings and anchors.
- The duplicate check always runs; trailing slashes are ignored when comparing links. Duplicates are printed and the script exits `1`; otherwise it prints `No duplicate links.`
- Unless `-odlc` / `--only_duplicate_links_checker` is passed, each link is fetched with a 25-second timeout, a randomized browser `User-Agent` drawn from a built-in pool, and a `host` header derived from the link.
- A status code of 400 or higher is reported as an error (`ERR:CLT`) unless the response shows Cloudflare protection — status 403 or 503, a `Server: cloudflare` header, and known challenge-page text in the body. Such responses are tolerated because the underlying API is usually reachable.
- Network failures are classified: SSL errors (`ERR:SSL`), connection errors (`ERR:CNT`), timeouts (`ERR:TMO`), too many redirects (`ERR:TMR`), and anything else (`ERR:UKN`).
- Any failing links are printed and the script exits `1`.

If a third argument is supplied, it must be `-odlc` or `--only_duplicate_links_checker`; anything else prints a usage message and exits `1`.

### Pull request link validation

```bash
scripts/github_pull_request.sh <github-repo> <pull-number> <filename>
```

The script requires exactly three arguments (repository, pull request number, and filename). It changes into `$GITHUB_WORKSPACE` — so it is intended for CI environments such as GitHub Actions — downloads the pull request diff from `patch-diff.githubusercontent.com` via `curl`, extracts the added lines into `additions.txt`, runs the link validator on them, and exits `1` with `link validation failed on additions!` if validation fails.

## API entry format

The API list is built from Markdown tables. Per `CONTRIBUTING.md`, entries use this shape:

| API | Description | Auth | HTTPS | CORS | Call this API |
| --- | --- | --- | --- | --- | --- |
| API Title (link to API documentation) | Description of API | Does this API require authentication? | Does the API support HTTPS? | Does the API support CORS? | Link to a public Postman collection |

Example entry:

```
| [NASA](https://api.nasa.gov) | NASA data, including imagery | No | Yes | Yes | [Run in Postman Button]
```

The format validator requires at least five columns per row — API, Description, Auth, HTTPS, and CORS — with these accepted values:

- **Auth**: `OAuth`, `apiKey`, `X-Mashape-Key`, `User-Agent`, or `No`. Every value except `No` must be wrapped in backticks.
- **HTTPS**: `Yes` or `No`.
- **CORS**: `Yes`, `No`, or `Unknown`.

## Validation rules

The format validator enforces the following (constants are defined at the top of `scripts/validate/format.py`):

- Every category heading (`### Category`) must be added to the `## Index` section and formatted correctly.
- Entries within each category must be in alphabetical (case-insensitive) order.
- Each category must contain at least `min_entries_per_category` (3) entries.
- Each entry row must include all required columns (`num_segments` = 5).
- Each table cell must be padded with exactly one space on each side.
- Titles must use the `[TITLE](LINK)` Markdown syntax and must not end with ` API`.
- Descriptions must start with a capital letter, must not end with punctuation (parentheses are currently exempt), and must not exceed `max_description_length` (100) characters.
- Auth, HTTPS, and CORS values must be one of the accepted options listed above.

## Configuration

Behavior is controlled by module-level constants that can be edited directly:

- `scripts/validate/format.py`: `auth_keys`, `https_keys`, `cors_keys`, `num_segments` (5), `min_entries_per_category` (3), and `max_description_length` (100).
- `scripts/validate/links.py`: the request timeout (25 seconds), the pool of user-agent strings, and the list of Cloudflare challenge-page markers.

Python dependencies are pinned in `scripts/requirements.txt`.

## Development

- `scripts/validate/format.py` uses only the standard library and is organized as small, independently testable functions (`check_title`, `check_description`, `check_auth`, `check_https`, `check_cors`, `check_entry`, `check_file_format`), each returning a list of error strings built by `error_message()`.
- `scripts/validate/links.py` separates pure helpers (`find_links_in_text`, `check_duplicate_links`, `get_host_from_link`, `has_cloudflare_protection`) from the network-touching code, making it easy to test without real HTTP traffic.
- If you change a validation rule, update the corresponding tests.

## Testing

The test suite uses Python's built-in `unittest` framework. Run it from the `scripts/` directory so that the `validate` package is importable:

```bash
cd scripts
python -m unittest discover
```

Alternatively, run each module explicitly:

```bash
cd scripts
python -m unittest tests.test_validate_format tests.test_validate_links
```

What is covered:

- **Format tests**: error-message formatting, category extraction, alphabetical-order detection, individual title/description/Auth/HTTPS/CORS checks, and full-file checks such as index completeness, minimum entries per category, missing columns, and cell spacing.
- **Link tests**: URL extraction from free text, duplicate detection, user-agent generation, host extraction, and Cloudflare-protection detection. HTTP responses are simulated with a lightweight `FakeResponse` stub, so no real network calls are made.

## Contributing

Contributions are welcome — see `CONTRIBUTING.md` for the full guidelines. Highlights:

- Only APIs with full free access (or at least a free tier) are accepted. APIs that depend on purchasing a device or service are rejected, and the list is not a marketing channel for commercial APIs.
- Follow the entry format and ordering rules above; descriptions must be at most 100 characters.
- Pull requests should add one link per PR, use a title in the form `Add <API name> API` (for example `Add Blockchain API`), use short descriptive commit messages, have all commits squashed, and target the `master` branch.
- Search previous pull requests and issues before opening a new one to avoid duplicates.
- Opening a pull request triggers a build that validates the project's links — make sure it passes before requesting review.

## License

This project is released under the [MIT License](LICENSE). Copyright (c) 2022 public-apis.
