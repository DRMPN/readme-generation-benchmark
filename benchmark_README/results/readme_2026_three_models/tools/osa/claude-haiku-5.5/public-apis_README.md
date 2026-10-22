# public-apis-6xkrh1my

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

This project provides validation tooling for a Markdown-based curated list of APIs. It checks that entries follow the list's formatting conventions, including title link syntax, description rules, Auth, HTTPS, and CORS values, and category ordering, and it checks that linked URLs are reachable and not duplicated. The primary audience is contributors who submit entries through pull requests and maintainers who work on the validation logic. The tooling is implemented as Python modules and a shell script that runs link checks on pull request changes. Setup and run steps are described in Getting Started, and contribution guidelines are available in the repository.

---

## Core Features

- **Entry format validation:** Checks each API entry's title link, description, and Auth, HTTPS, and CORS values against the list's expected format. This helps contributors catch formatting errors before merging.
- **Link validation with duplicate detection:** Checks API URLs for broken links and flags duplicate links within the list. This keeps the list's links working and unique.
- **Pull request link checking:** Extracts links added in a pull request's diff and validates only those links. This gives reviewers fast feedback on new submissions without re-checking the entire list.
- **Category structure checks:** Verifies that categories are listed in alphabetical order and that the Index section matches the category headers. This keeps the list consistent and easy to navigate.

---

## Installation

Install public-apis-6xkrh1my using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/public-apis-6xkrh1my
```

2. Install the project dependencies:

```sh
pip install -r requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3 with `pip`
- Dependencies pinned in `scripts/requirements.txt`: `certifi`, `charset-normalizer`, `idna`, `requests`, and `urllib3`
- `bash`, `curl`, and `realpath`, used by `scripts/github_pull_request.sh`

### Steps

1. Clone the repository and change into its root directory.
2. Install the pinned dependencies:

```bash
pip install -r scripts/requirements.txt
```

3. Review the validation modules in `scripts/validate/`:
   - `format.py`: `check_file_format(lines)` takes a list of file lines and returns a list of error messages.
   - `links.py`:
     - `find_links_in_file(filename)` returns the URLs found in the file, starting at the `## Index` section.
     - `check_duplicate_links(links)` returns a tuple of `(has_duplicate, duplicates)`.
     - `check_if_link_is_working(link)` returns a tuple of `(has_error, error_message)`.
     - `check_if_list_of_links_are_working(list_of_links)` returns a list of error messages.
4. Review the tests in `scripts/tests/`, which include `test_validate_format.py` and `test_validate_links.py`.
5. To run the pull request link check, `scripts/github_pull_request.sh` requires the `GITHUB_WORKSPACE` environment variable and the pull request arguments. It downloads the pull request diff, extracts the added lines, and runs `scripts/validate/links.py` on them.

---

## Testing

Tests for the validation scripts are located in `scripts/tests/`:

- `scripts/tests/test_validate_format.py`: targets the format validation in `scripts/validate/format.py`.
- `scripts/tests/test_validate_links.py`: targets the link validation in `scripts/validate/links.py`.

When changing `scripts/validate/format.py` or `scripts/validate/links.py`, update or add tests in the matching file under `scripts/tests/`.

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to public-apis-6xkrh1my.

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). public-apis-6xkrh1my repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{public-apis-6xkrh1my,

        author = {README Benchmark},

        title = {public-apis-6xkrh1my repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---