# Public APIs Validation Tools

This repository contains Python utilities and tests for validating Public APIs project content. The validators are organized by concern: `links.py` handles link validation, and `format.py` handles format validation. The test files cover those two areas.

## Repository contents

| File | Purpose |
|---|---|
| `links.py` | Link-validation utilities |
| `format.py` | Format-validation utilities |
| `test_validate_links.py` | Tests for link validation |
| `test_validate_format.py` | Tests for format validation |
| `github_pull_request.sh` | Shell helper for pull-request-related automation |
| `requirements.txt` | Python dependencies |
| `CONTRIBUTING.md` | Contribution guidance |
| `LICENSE` | License terms |
| `__init__.py` | Marks a directory as a Python package |

## Requirements

- Python 3
- The dependencies listed in `requirements.txt`

Install the dependencies from the repository root:

```bash
python -m pip install -r requirements.txt
```

## Running the tests

Run the test suite from the repository root:

```bash
python -m pytest
```

To run an individual test file:

```bash
python -m pytest test_validate_links.py
python -m pytest test_validate_format.py
```

If `pytest` is not installed as a project dependency, install it separately:

```bash
python -m pip install pytest
```

## Validation utilities

The validation code is split into two modules:

- **Link validation** — `links.py` contains the utilities exercised by `test_validate_links.py`.
- **Format validation** — `format.py` contains the utilities exercised by `test_validate_format.py`.

For the available functions and expected inputs, refer to the modules and their tests. The tests are also useful examples of how the validators are expected to behave.

## Pull-request helper

`github_pull_request.sh` is a shell script for pull-request-related automation. Review the script before running it, especially if you are working with a fork or an untrusted pull request. Any required environment variables, credentials, or command-line arguments should be taken from the script itself and the project’s contribution guidance.

## Contributing

Before making a change, read [`CONTRIBUTING.md`](CONTRIBUTING.md). Run the relevant tests after updating the validators, and run the full test suite before submitting a pull request.

## License

See [`LICENSE`](LICENSE) for the terms under which this project is distributed.
