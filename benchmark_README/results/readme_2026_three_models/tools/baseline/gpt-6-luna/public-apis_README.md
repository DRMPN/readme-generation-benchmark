# public-apis Validation Tools

This repository contains Python scripts for checking the formatting and links in the public-apis Markdown listings, plus a shell helper for validating links added in a GitHub pull request. The checks support the contribution conventions described in [CONTRIBUTING.md](CONTRIBUTING.md).

## Repository contents

- `scripts/validate/format.py` checks API table entries and category organization.
- `scripts/validate/links.py` finds links, reports duplicates, and can check whether links respond successfully.
- `scripts/github_pull_request.sh` fetches a pull request diff and runs link validation on its additions.
- `scripts/tests/` contains unit tests for the format and link validation modules.
- `scripts/requirements.txt` lists the pinned Python dependencies.

## Setup

Use a Python environment with `pip`, then install the project’s listed dependencies:

```sh
python -m pip install -r scripts/requirements.txt
```

The requirements file pins `requests` and its listed supporting packages. No separate package build or installation step is defined in this repository; run the scripts directly from the project root.

The link checker makes HTTP requests to the URLs it finds, so checking links requires network access. Formatting checks and the unit tests do not require checking external URLs.

## Usage

### Check Markdown formatting

Pass the Markdown file to validate as the first argument:

```sh
python scripts/validate/format.py path/to/file.md
```

The formatter prints any detected issues and exits with a non-zero status when validation fails. If no errors are printed, the file passed the checks. The script requires a filename; if none is supplied, it exits with an explanatory message.

The checks cover category ordering, index entries, table-entry structure, and field values. The specific rules are summarized under [Formatting rules](#formatting-rules).

### Check links

Run the link validator with a Markdown filename:

```sh
python scripts/validate/links.py path/to/file.md
```

By default, it checks for duplicate links and then requests the discovered links to check their responses. To check duplicates only, use either supported option:

```sh
python scripts/validate/links.py path/to/file.md -odlc
python scripts/validate/links.py path/to/file.md --only_duplicate_links_checker
```

The link finder starts at the `## Index` heading when the file contains one; otherwise, it searches the whole file. Duplicate comparison ignores trailing slashes. Link checks use HTTP GET requests with a 25-second timeout. Responses with status codes of 400 or above are reported as errors unless the response is identified as Cloudflare protection. The checker also reports SSL, connection, timeout, redirect, and other request errors. Network responses can change, so a link-check failure should be reviewed in context.

### Validate pull-request additions

The helper script accepts a GitHub repository, pull request number, and filename:

```sh
scripts/github_pull_request.sh <github-repo> <pull-number> <filename>
```

It expects `GITHUB_WORKSPACE` to identify the project workspace. The script fetches the pull request diff from GitHub, extracts added lines, and runs the link validator on those additions. It uses `curl` to retrieve the diff and requires the shell utilities invoked by the script, including `realpath` and `egrep`, as well as Python. The script exits unsuccessfully if its link-validation step fails.

## Formatting rules

The contribution guide describes API listings with columns for API, Description, Auth, HTTPS, CORS, and a “Call this API” link. The formatter requires at least five entry segments and validates the API title, description, Auth, HTTPS, and CORS fields. It does not define a semantic check for the “Call this API” collection link.

For entries, follow these rules:

- Write the API title as a Markdown link in the form `[Title](URL)`. The title must not end in `API`.
- Capitalize the first character of the description. Keep it to 100 characters or fewer and do not end it with punctuation.
- Use one of the accepted Auth values: `No`, or a backtick-wrapped `apiKey`, `OAuth`, `X-Mashape-Key`, or `User-Agent`.
- Use `Yes` or `No` for HTTPS.
- Use `Yes`, `No`, or `Unknown` for CORS.
- Pad each table segment with exactly one space on either side, as described in the contribution guide.

Categories should be in alphabetical order, and each category header should also appear in the Index. The formatter requires at least three entries per category. See [CONTRIBUTING.md](CONTRIBUTING.md) for additional guidance on choosing entries, placement, descriptions, and pull requests.

## Configuration

The validation rules are defined as constants in `scripts/validate/format.py`; there is no separate configuration file. The current settings include five required entry segments, a minimum of three entries per category, and a maximum description length of 100 characters. Accepted Auth, HTTPS, and CORS values are also declared there.

The link checker’s behavior is implemented in `scripts/validate/links.py`. It selects a user-agent string from a built-in list for requests and includes logic to recognize certain Cloudflare protection responses. These settings are not exposed as command-line configuration options.

## Development and testing

Tests use Python’s built-in `unittest` framework. From the `scripts` directory, run:

```sh
cd scripts
python -m unittest discover -s tests
```

The format tests exercise field validation, category ordering, index presence, minimum category size, and table structure. The link tests cover URL extraction, duplicate detection, host parsing, user-agent generation, and Cloudflare response detection. The link unit tests use test data for these behaviors; running the separate link-checking command is what makes requests to external URLs.

When changing validation behavior, update or add tests in `scripts/tests/` to cover the relevant rule. Keep contribution guidance in `CONTRIBUTING.md` in mind when editing API listings.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for the full license text.
