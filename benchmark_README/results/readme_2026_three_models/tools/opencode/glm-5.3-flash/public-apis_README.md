# public-apis

public-apis is a community-maintained catalog of free public APIs, intended to help developers
build applications and use free, public APIs quickly and easily. APIs are organized into
categories and recorded as Markdown tables. The repository also contains tooling that
automatically validates the formatting of the catalog and the links it contains.

## Catalog format

APIs are listed in tables, one table per category. Each entry follows this format:

| API | Description | Auth | HTTPS | CORS | Call this API |
| --- | --- | --- | --- | --- | --- |
| [NASA](https://api.nasa.gov) | NASA data, including imagery | No | Yes | Yes | [Run in Postman Button] |

Column descriptions:

- **API** — the API name, as a Markdown link to the API's documentation.
- **Description** — a short description of the API (maximum 100 characters).
- **Auth** — how the API authenticates. Accepted values are:
  - `OAuth` — the API supports OAuth
  - `apiKey` — the API uses a private key string/token for authentication
  - `X-Mashape-Key` — the name of the header which may need to be sent
  - `User-Agent` — the name of the header to be sent with requests to the API
  - `No` — the API requires no authentication to run
- **HTTPS** — whether the API supports HTTPS (`Yes` or `No`).
- **CORS** — whether the API supports [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) (`Yes`, `No`, or `Unknown`). Without proper CORS configuration, an API will only be usable server side.
- **Call this API** — an optional link to a [Postman collection](https://learning.postman.com/docs/publishing-your-api/run-in-postman/creating-run-button/), shown as a "Run in Postman" button.

Entries are sorted alphabetically within each category, and every category appears in the index.

## Repository structure

```
.
├── CONTRIBUTING.md        # How to contribute to the catalog
├── LICENSE                # MIT license
├── scripts/
│   ├── requirements.txt   # Python dependencies for the validation scripts
│   ├── github_pull_request.sh  # Script that validates links added in pull requests
│   ├── validate/
│   │   ├── format.py      # Validates the formatting of catalog Markdown tables
│   │   └── links.py       # Checks for duplicate and broken links
│   └── tests/
│       ├── test_validate_format.py
│       └── test_validate_links.py
```

## Validation tooling

The `scripts/` directory contains Python tooling that keeps the catalog consistent.

### Format validation (`scripts/validate/format.py`)

Checks a Markdown file of catalog entries and reports errors for:

- Categories not sorted in alphabetical order.
- Category headers that are missing from the index.
- Entries with malformed titles (must use `[TITLE](LINK)` syntax) or titles ending in `... API`.
- Descriptions that are not capitalized, exceed 100 characters, or end with punctuation.
- Invalid `Auth`, `HTTPS`, or `CORS` values (see the accepted values above).
- Entries missing required columns, or table cells not padded with exactly one space on each side.
- Categories with fewer than the minimum required number of entries.

Usage:

```bash
python scripts/validate/format.py <file.md>
```

### Link validation (`scripts/validate/links.py`)

Checks a Markdown file for:

- Duplicate links anywhere in the document.
- Whether every link is working (HTTP requests are made with a fake user agent; Cloudflare
  protection challenges are detected and not reported as errors).

Usage:

```bash
python scripts/validate/links.py <file.md>              # check duplicates and link liveness
python scripts/validate/links.py <file.md> -odlc        # only check for duplicate links
```

The `-odlc` / `--only_duplicate_links_checker` flag skips the link liveness check.

### Running the tests

The test suite in `scripts/tests/` uses Python's built-in `unittest` framework and is meant to be
run from the `scripts/` directory:

```bash
pip install -r scripts/requirements.txt
cd scripts
python -m unittest discover tests
```

### Pull request link checking (`scripts/github_pull_request.sh`)

`scripts/github_pull_request.sh <github-repo> <pull-number> <filename>` downloads the diff for a
pull request from GitHub, extracts the added lines, and runs link validation against them. This
is the mechanism behind the build that checks the validity of links when a pull request is opened;
contributors are expected to make sure that build passes.

## Contributing

Contributions are welcome — please read [CONTRIBUTING.md](CONTRIBUTING.md) for the full guidelines.
Key points:

- APIs must have full, free access or at least a free tier, and must not depend on purchasing a
  device or service. The list is not a marketing tool; pull requests that exist to market paid
  company APIs will not be accepted.
- Each pull request should add one API, with a properly documented endpoint, and keep the
  alphabetical ordering within its section.
- Pull request titles follow the format `Add <name> API` (e.g. `Add Blockchain API`), should not
  include the top-level domain, and should not end with `API` in the entry name.
- Commits should be squashed before opening the pull request, and the PR should target the
  `master` branch.
- After opening a pull request, make sure the link-validation build passes.

## License

This project is licensed under the [MIT License](LICENSE).
