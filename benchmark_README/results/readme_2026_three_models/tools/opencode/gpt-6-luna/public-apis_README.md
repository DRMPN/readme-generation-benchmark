# Public APIs

This project aims to help the community find and use free public APIs. API contributions should have full free access or a free tier and must not require the purchase of a device or service to use.

> **Repository contents:** This checkout contains the contribution guide and validation scripts, but no API catalog file. The catalog format described below is documented in [`CONTRIBUTING.md`](CONTRIBUTING.md).

## API entry format

Each API entry is a Markdown table row with these columns:

| API | Description | Auth | HTTPS | CORS | Call this API |
| --- | --- | --- | --- | --- | --- |
| API title linked to its documentation | Short description | Authentication method | HTTPS support | CORS support | Optional Postman collection link |

Use `OAuth`, `apiKey`, `X-Mashape-Key`, `User-Agent`, or `No` for the authentication value. Use `Yes` or `No` for HTTPS support, and `Yes`, `No`, or `Unknown` for CORS. The description should be no longer than 100 characters. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full formatting and pull request guidelines.

## Validation tools

The scripts in `scripts/validate/` check Markdown API-list files:

- `format.py` checks entry formatting, required values, category index entries, category size, and alphabetical order.
- `links.py` checks for duplicate links and, by default, requests the links to check their responses. Link checks require network access.

Install the pinned Python dependencies with:

```sh
python -m pip install -r scripts/requirements.txt
```

Run the format validator against a Markdown file:

```sh
python scripts/validate/format.py path/to/list.md
```

Check links in a Markdown file:

```sh
python scripts/validate/links.py path/to/list.md
```

To check only for duplicate links, without requesting them:

```sh
python scripts/validate/links.py path/to/list.md --only_duplicate_links_checker
```

The link checker reads from the `## Index` heading onward when that heading exists; otherwise, it scans the whole file.

## Tests

Run the unit tests from the `scripts` directory:

```sh
cd scripts
python -m unittest discover -s tests
```

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE).
