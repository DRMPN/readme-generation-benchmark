# public-apis

This repository contains the contribution guidelines and Python validation tooling for the `public-apis` project, a collection of free public APIs organized into categories. The supplied files cover the entry format, pull request rules, and scripts that check Markdown entries for formatting problems, duplicate links, and broken links. The API list itself is not among the supplied files, so this README does not describe its contents.

## Overview

Each entry in the API list is a row in a Markdown table with five columns: API, Description, Auth, HTTPS, and CORS. The project's tooling checks that these rows follow the required format. It also checks that links are unique and still reachable.

The repository contains:

- `CONTRIBUTING.md`: the contribution rules, entry format, and pull request guidelines.
- `LICENSE`: the MIT License.
- `scripts/validate/format.py`: checks the Markdown table format.
- `scripts/validate/links.py`: finds links, checks for duplicates, and tests whether links respond.
- `scripts/github_pull_request.sh`: a shell script that validates the links added by a pull request.
- `scripts/requirements.txt`: pinned Python dependencies.
- `scripts/tests/`: `unittest` test modules for the validators.

The `.gitattributes` and `.gitignore` files are present, but their contents were not supplied, so this README does not describe them.

## Requirements

- Python 3, with the packages listed in `scripts/requirements.txt`. The supplied files do not state a specific Python version.
- Bash and `curl`, `realpath`, and `egrep` on the PATH, if you plan to run `github_pull_request.sh`.
- The `GITHUB_WORKSPACE` environment variable set to the repository root, if you run `github_pull_request.sh`.

## Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd public-apis
   ```

2. Install the pinned Python dependencies:

   ```bash
   pip install -r scripts/requirements.txt
   ```

   The pinned packages are:

   | Package | Version |
   | --- | --- |
   | certifi | 2021.10.8 |
   | charset-normalizer | 2.0.10 |
   | idna | 3.3 |
   | requests | 2.27.1 |
   | urllib3 | 1.26.8 |

   `requests` is the only package the validators import directly, and it is used by `links.py` to test links.

## Usage

### Validating entry format

`scripts/validate/format.py` checks a Markdown file that contains the API tables. Pass the file path as the only argument:

```bash
python scripts/validate/format.py README.md
```

If no file is passed, the script prints `No .md file passed (file should contain Markdown table syntax)` and exits with status 1. If errors are found, each one is printed on its own line in the form `(Lnnn) message`, where `nnn` is the one-based line number, and the script exits with status 1. If the file passes, it prints nothing and exits normally.

The checker verifies the following:

- Categories are listed in alphabetical order.
- Each category header (`### Name`) appears in the `## Index` section as a `* [Name](#...)` entry.
- Each category has at least three entries.
- Each entry has all five columns.
- Each column value starts and ends with exactly one space.
- Titles use `[TITLE](LINK)` syntax and do not end with "API".
- Descriptions start with a capital letter, do not end with punctuation, and are no longer than 100 characters.
- The Auth value is wrapped in backticks, unless it is `No`, and is one of the accepted values.
- The HTTPS value is `Yes` or `No`.
- The CORS value is `Yes`, `No`, or `Unknown`.

### Checking links

`scripts/validate/links.py` searches a Markdown file for URLs. It only considers content from the `## Index` heading onward. If that heading is absent, it scans the whole file.

```bash
python scripts/validate/links.py README.md
```

The script runs two checks in order:

1. **Duplicate check.** It reports any URL that appears more than once, ignoring trailing slashes, and exits with status 1 if it finds any.
2. **Working-link check.** It sends a request to each link and reports failures. Requests use a randomly chosen browser-style User-Agent and a `host` header derived from the URL. Each request has a 25-second timeout.

To run only the duplicate check, use either flag:

```bash
python scripts/validate/links.py README.md -odlc
python scripts/validate/links.py README.md --only_duplicate_links_checker
```

Failed links are reported with one of these prefixes:

| Prefix | Meaning |
| --- | --- |
| `ERR:CLT` | The server returned an HTTP status code of 400 or higher. |
| `ERR:SSL` | An SSL error occurred. |
| `ERR:CNT` | A connection error occurred. |
| `ERR:TMO` | The request timed out. |
| `ERR:TMR` | Too many redirects occurred. |
| `ERR:UKN` | Any other request error occurred. |

A response with status 403 or 503 from a Cloudflare server is not treated as an error when the page body contains a known Cloudflare challenge string. The script's comments explain that these responses come from Cloudflare protection rather than a broken link.

Running the script with an unrecognized third argument prints a usage message and exits with status 1.

### Validating pull request links

`scripts/github_pull_request.sh` checks the links added by a pull request:

```bash
GITHUB_WORKSPACE=/path/to/repo scripts/github_pull_request.sh <github-repo> <pull-number> <filename>
```

For example:

```bash
GITHUB_WORKSPACE=$(pwd) scripts/github_pull_request.sh public-apis/public-apis 1234 README.md
```

The script:

1. Changes to `$GITHUB_WORKSPACE`.
2. Converts the file path to an absolute path with `realpath`.
3. Downloads the pull request diff from `patch-diff.githubusercontent.com`.
4. Keeps only lines containing `+` and saves them to `additions.txt`.
5. Runs `scripts/validate/links.py` on `additions.txt`.

It exits with status 1 if the argument count is not three, if the repository or pull request number is empty, or if link validation fails.

The script runs `links.py` on the added lines only. It does not run `format.py`.

## Configuration

The supplied files do not include a configuration file. Configuration is set through constants in the source code and through command-line arguments.

### Formatting rules (`scripts/validate/format.py`)

These module-level constants define the rules the format checker enforces:

| Constant | Value | Purpose |
| --- | --- | --- |
| `auth_keys` | `apiKey`, `OAuth`, `X-Mashape-Key`, `User-Agent`, `No` | Accepted Auth values. |
| `https_keys` | `Yes`, `No` | Accepted HTTPS values. |
| `cors_keys` | `Yes`, `No`, `Unknown` | Accepted CORS values. |
| `num_segments` | `5` | Number of columns each entry must have. |
| `min_entries_per_category` | `3` | Minimum entries per category. |
| `max_description_length` | `100` | Maximum description length in characters. |

The `punctuation` set used for description checks has the parentheses removed. The source comments say this is temporary and that descriptions ending in `()` will need to follow a new policy later.

Changing these values changes what the validator accepts. Update the tests in `scripts/tests/test_validate_format.py` to match.

### Link checking (`scripts/validate/links.py`)

Link-checking behavior is also set in code:

- The request timeout is 25 seconds.
- Status codes 403 and 503 are checked against Cloudflare indicators.
- The User-Agent is chosen at random from a fixed list of four browser strings.
- The URL search starts at the `## Index` heading.

### Command-line options

| Script | Option | Effect |
| --- | --- | --- |
| `links.py` | `-odlc` or `--only_duplicate_links_checker` | Runs only the duplicate check. |
| `github_pull_request.sh` | three positional arguments | Repository, pull request number, and file name. |

The shell script also depends on the `GITHUB_WORKSPACE` environment variable.

## Contributing

The full guidelines are in `CONTRIBUTING.md`. In summary:

- Only add APIs that have free, full access or a free tier, and that do not require buying a device or service.
- Do not add a new version of an API that is already listed. Entries are not updated in place.
- Keep categories and entries in alphabetical order.
- Use one link per pull request.
- Title pull requests `Add Api-name API`, for example `Add Blockchain API`.
- Do not include a top-level domain in an API name, and do not end the name with "API".
- Keep descriptions under 100 characters.
- Squash commits before opening a pull request, and target the `master` branch.
- Search existing pull requests and issues for duplicates first.

`CONTRIBUTING.md` also says that opening a pull request triggers a build that checks all links, and that contributors should confirm the build passes. The build configuration is not among the supplied files.

## Development

The Python code is organized as a package:

- `scripts/validate/__init__.py` imports the `format` and `links` modules.
- `scripts/validate/format.py` contains format checks. Its functions include `check_file_format`, `check_entry`, `check_title`, `check_description`, `check_auth`, `check_https`, and `check_cors`.
- `scripts/validate/links.py` contains link checks. Its functions include `find_links_in_text`, `find_links_in_file`, `check_duplicate_links`, `has_cloudflare_protection`, and `check_if_link_is_working`.

The modules use type hints. Error messages in `format.py` are built by `error_message`, which formats line numbers as `(Lnnn)`.

To add a new formatting rule, add a check function in `format.py`, call it from `check_entry` or `check_file_format`, and add a unit test. To add a new link failure type, extend `check_if_link_is_working` and its error prefix scheme.

## Testing

The tests use Python's built-in `unittest` framework.

- `scripts/tests/test_validate_format.py` covers error message formatting, category parsing, alphabetical order, title, description, Auth, HTTPS, and CORS validation, entry validation, and whole-file checks, including the minimum entry count, Index references, column count, and segment padding.
- `scripts/tests/test_validate_links.py` covers link extraction from text, invalid argument handling, duplicate detection, the fake User-Agent, host extraction from URLs, and Cloudflare protection detection using a fake response object.

The test modules import from the `validate` package directly, for example `from validate.format import error_message`. The supplied files do not include a test runner configuration. Based on these imports, the tests appear to be run from the `scripts` directory:

```bash
cd scripts
python -m unittest discover -s tests
```

The link tests shown do not make network requests, but the `check_if_link_is_working` path is not covered by the supplied tests.

## License

This project is licensed under the MIT License. Copyright (c) 2022 public-apis. See the [LICENSE](LICENSE) file for the full text.
