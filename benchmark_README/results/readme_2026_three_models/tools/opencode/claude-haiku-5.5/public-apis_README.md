# public-apis

A community list of free, public APIs, along with Python scripts that validate the list's formatting and check its links. This repository contains the contribution guidelines, the validation tooling, and the project license.

> **Note:** This copy of the repository does not include the API catalog file. The directory contains only `CONTRIBUTING.md`, `LICENSE`, `.gitattributes`, `.gitignore`, and the `scripts/` directory. The sections below describe the tooling and contribution rules that are present.

## Contents

- [Purpose](#purpose)
- [Repository layout](#repository-layout)
- [Adding an API](#adding-an-api)
- [Validation scripts](#validation-scripts)
- [Running the tests](#running-the-tests)
- [Contributing](#contributing)
- [License](#license)

## Purpose

According to `CONTRIBUTING.md`, the list exists to help the community build applications and use free, public APIs quickly and easily. Submissions must offer full, free access or at least a free tier, and must not depend on purchasing a device or service. Submissions identified as marketing for paid APIs are not accepted.

## Repository layout

```
.
├── CONTRIBUTING.md                     # Formatting rules and pull request guidelines
├── LICENSE                             # MIT License
├── .gitattributes                      # Git attributes (text=auto; export-ignore rules)
├── .gitignore                          # Ignored files (Python caches, virtualenvs, etc.)
└── scripts/
    ├── requirements.txt                # Pinned Python dependencies for the scripts
    ├── github_pull_request.sh          # Validates links added by a GitHub pull request
    ├── validate/
    │   ├── __init__.py
    │   ├── format.py                   # Checks the format of the API list Markdown file
    │   └── links.py                    # Checks for duplicate links and broken links
    └── tests/
        ├── __init__.py
        ├── test_validate_format.py     # Unit tests for validate/format.py
        └── test_validate_links.py      # Unit tests for validate/links.py
```

## Adding an API

Each API is a row in a Markdown table under a category heading (`### Category`). Categories are listed in an Index section. The table columns are:

| Column | Meaning |
| --- | --- |
| API | Title linked to the API documentation, in `[TITLE](LINK)` form |
| Description | A short description of the API |
| Auth | Authentication requirement (see accepted values below) |
| HTTPS | `Yes` or `No` |
| CORS | `Yes`, `No`, or `Unknown` |
| Call this API | Optional link to a public Postman collection (Run in Postman button) |

Example entry, as shown in `CONTRIBUTING.md`:

```
| [NASA](https://api.nasa.gov) | NASA data, including imagery | No | Yes | Yes | [Run in Postman Button]
```

Accepted values for the **Auth** column, each written in backticks (except `No`):

- `OAuth`: the API supports OAuth
- `apiKey`: the API uses a private key string or token
- `X-Mashape-Key`: the name of the header that may need to be sent
- `User-Agent`: the name of the header to send with requests
- `No`: the API requires no authentication

Without proper [CORS configuration](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS), an API can only be used server side.

### Pull request guidelines

From `CONTRIBUTING.md`:

- Do not submit a new version of an API that is already listed. The old version is deprecated instead.
- Keep entries in alphabetical order within each section.
- Pad each table column with one space on either side.
- Keep descriptions to 100 characters or fewer.
- Place an API in the section that best matches the service it offers.
- Add one link per pull request.
- Title the pull request `Add <Name> API`, for example `Add Blockchain API`.
- Use short, descriptive commit messages.
- Search existing pull requests and issues before opening a new one.
- Do not include the top-level domain in the API name (`Gmail`, not `Gmail.com`).
- Do not end the API name with `API`.
- Make sure the API has proper documentation.
- Squash commits before opening a pull request.
- Target the `master` branch.

## Validation scripts

### `scripts/validate/format.py`

Checks the format of the API list Markdown file. It takes the file path as its only argument:

```
python scripts/validate/format.py <file.md>
```

The script reports errors with line numbers and exits with status 1 if any are found. It checks that:

- Each category has at least 3 entries.
- Each category appears in the Index section.
- Entries within each category are in alphabetical order.
- Titles use `[TITLE](LINK)` syntax and do not end with "API".
- Descriptions start with a capital letter, do not end with punctuation, and do not exceed 100 characters.
- The Auth value is one of the accepted values, enclosed in backticks (except `No`).
- The HTTPS value is `Yes` or `No`.
- The CORS value is `Yes`, `No`, or `Unknown`.
- Each row has at least five columns, with exactly one space at the start and end of each cell.

### `scripts/validate/links.py`

Extracts URLs from a file and checks them.

```
python scripts/validate/links.py <file> [-odlc | --only_duplicate_links_checker]
```

- If the file contains a `## Index` heading, only the text from that heading onward is scanned. Otherwise the whole file is scanned.
- It first checks for duplicate links (trailing slashes are ignored). If duplicates are found, it prints them and exits with status 1.
- Unless `-odlc` or `--only_duplicate_links_checker` is passed, it then requests each link with a 25-second timeout and a browser-like `User-Agent` header. Responses with HTTP status 400 or higher are reported as errors. Cloudflare challenge pages on 403 and 503 responses are not treated as errors.
- Errors are labeled by type: `CLT` (client error status), `SSL`, `CNT` (connection), `TMO` (timeout), `TMR` (too many redirects), and `UKN` (unknown).

### `scripts/github_pull_request.sh`

Checks the links added by a GitHub pull request. It requires three arguments and the `GITHUB_WORKSPACE` environment variable:

```
GITHUB_WORKSPACE=/path/to/repo scripts/github_pull_request.sh <owner/repo> <pull-number> <file>
```

The script downloads the pull request's diff, keeps only lines that begin with `+`, and runs `scripts/validate/links.py` on them. It uses `curl`, `realpath`, and `egrep`, so those must be available.

## Running the tests

The tests use Python's `unittest` module. They import from the `validate` package, so they are presumably run from the `scripts/` directory. The repository does not state a test command.

```
cd scripts
python -m unittest discover -s tests
```

## Dependencies

`scripts/requirements.txt` pins the following packages:

- `requests==2.27.1` (used by `links.py`)
- `urllib3==1.26.8`, `idna==3.3`, `charset-normalizer==2.0.10`, `certifi==2021.10.8` (dependencies of `requests`)

Install them with:

```
pip install -r scripts/requirements.txt
```

The repository does not specify a Python version. `format.py` uses only the standard library.

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a pull request. It covers the formatting rules, pull request guidelines, and the workflow for forking and syncing the repository. Per that file, opening a pull request triggers a build that checks all links, and the build must pass before the pull request is reviewed.

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for the full text. Copyright (c) 2022 public-apis.
