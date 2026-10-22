# public-apis-qfao3v69

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This repository provides validation tooling for maintaining a curated, public-apis-style Markdown catalog of APIs. It is aimed at contributors submitting catalog entries and at maintainers or automation reviewing those contributions. The tooling checks that catalog entries follow the project's formatting conventions and verifies that added links are live, with a shell wrapper that runs link validation on the added lines of a pull request. Newcomers should see Getting Started for runnable steps and CONTRIBUTING.md for contribution guidelines.

---

## Core Features

- Validates Markdown catalog entries against a strict schema, checking title syntax, alphabetical ordering, description style, auth/HTTPS/CORS values, and category minimums.
- Checks link liveness by requesting each URL and reporting client errors, SSL failures, timeouts, redirects, and Cloudflare-protected responses.
- Validates only the lines added in a GitHub pull request diff, giving fast feedback to PR submitters and reviewers.
- Ships with unit tests for both validators, so contributors can verify behavior locally before submitting changes.

---

## Installation

Install public-apis-qfao3v69 using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/public-apis-qfao3v69
```

2. Install the project dependencies:

```sh
pip install -r scripts/requirements.txt
```

---

## Getting Started

This repository provides Python validators for a Markdown API catalog: `scripts/validate/format.py` checks catalog formatting rules, and `scripts/validate/links.py` checks that catalog links are reachable. A Bash wrapper, `scripts/github_pull_request.sh`, runs link validation on the added lines of a GitHub pull request.

**Prerequisites**

- Python with `pip`
- Network access (the link validator requests each catalog URL)
- Run the commands below from the repository root

**Steps**

1. Install the pinned dependencies:

```bash
   pip install -r scripts/requirements.txt
```

2. Run the format validator on a Markdown catalog file:

```bash
   python scripts/validate/format.py <markdown-file>
```

   Violations (e.g., entries out of alphabetical order, invalid `Auth`/`HTTPS`/`CORS` values, descriptions exceeding 100 characters) are reported with line numbers.

3. Run the link validator on the same file:

```bash
   python scripts/validate/links.py <markdown-file>
```

   Links are collected starting at the `## Index` section when present (otherwise from the whole file), and unreachable URLs are reported.

4. Optionally, validate the additions of a GitHub pull request:

```bash
   bash scripts/github_pull_request.sh <github-repo> <pull-number> <filename>
```

   The script downloads the PR diff, extracts the added lines, and runs the link validator on them. It changes to the directory in `$GITHUB_WORKSPACE`, so ensure that variable is set to the repository root.

Unit tests for both validators are located in `scripts/tests/`.

---

## Testing

Unit tests for both validators live in `scripts/tests/`:

- `scripts/tests/test_validate_format.py` — unit tests for the format validator (`scripts/validate/format.py`)
- `scripts/tests/test_validate_links.py` — unit tests for the link validator (`scripts/validate/links.py`)

There is no separate integration or end-to-end test directory; test coverage is limited to these unit tests.

No test-runner configuration file or documented run command is present in the repository, so run the test files under `scripts/tests/` with your preferred Python test runner. The validators depend on the packages pinned in `scripts/requirements.txt` (notably `requests==2.27.1`); make sure these are installed in your environment before running the tests.

For pull-request validation, see the `scripts/github_pull_request.sh` usage described in [Getting Started](#getting-started). No CI workflow configuration file appears in the repository tree, so automation beyond this script cannot be confirmed.

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to public-apis-qfao3v69.

---

## License

The licensing terms for this project are defined in the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). public-apis-qfao3v69 repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{public-apis-qfao3v69,

        author = {README Benchmark},

        title = {public-apis-qfao3v69 repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---