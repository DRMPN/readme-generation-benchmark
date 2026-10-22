# SMSBoom

SMSBoom (短信轰炸机) is a Python tool that sends SMS verification-code requests to a phone number by replaying the SMS-sending HTTP endpoints of a large collection of third-party websites and applications — a technique commonly known as SMS bombing (短信轰炸). The code describes itself as a 短信测压 ("SMS pressure test") tool, but its effect is to bombard a phone number with verification SMS originating from dozens of unrelated services.

This is a snapshot of the SMSBoom project; its built-in `update` command pulls endpoint lists from a mirror of the upstream GitHub repository (`OpenEthan/SMSBoom`).

> **⚠️ Notice**
>
> Running this tool against a phone number without the owner's consent is harassment. It violates the terms of service of every targeted service and is unlawful in many jurisdictions. This README documents the repository for reference, audit, and defensive purposes, and **intentionally does not include step-by-step operating instructions**.

## How it works

- Two JSON files define the request surface:
  - `api.json` — 87 structured endpoint definitions (description, URL, HTTP method, headers, body). The placeholders `[phone]` and `[timestamp]` are substituted at request time.
  - `GETAPI.json` — 1,018 raw GET-style URL strings containing a `[phone]` placeholder (many are near-duplicates with escaped/unescaped variants).
- At runtime every endpoint is rewritten with the target number and requested with `httpx`, with TLS certificate verification disabled (`verify=False`) and a `Referer` header pointing back at the endpoint's own site.
- Requests are sent with a randomly chosen browser `User-Agent` from a pool in `utils/__init__.py`.
- `smsboom.py` provides four Click commands:
  - `run` — submits the endpoint requests to a `ThreadPoolExecutor` (default 64 workers), repeating in waves separated by an interval;
  - `asyncRun` — fires every endpoint concurrently via `asyncio` (the code's own docstring claims "真异步百万并发", i.e. true async million-level concurrency);
  - `oneRun` — walks the endpoints once, single-threaded (described in-code as being for testing);
  - `update` — re-downloads `api.json` and `GETAPI.json` from a mirror of the upstream GitHub repository.
- Optional proxy support: proxy lists are read from `http_proxy.txt`, `socks5_proxy.txt`, and `socks4_proxy.txt` located next to the script (empty files are created if missing).

All bundled endpoints are Chinese-language services. Embedded dates (for example, `debug/api.js` is marked 最后更新：2022-04-12) indicate the lists were collected around 2019–2022 and should be assumed outdated.

## Repository layout

| Path | Purpose |
| --- | --- |
| `smsboom.py` | Click-based CLI entry point (`run`, `asyncRun`, `oneRun`, `update`) |
| `smsboom_GUI.py` | Minimal Tkinter front end (see below) |
| `utils/req.py` | `httpx` request helpers: synchronous, proxied, and asyncio-based |
| `utils/models.py` | Pydantic `API` model handling `[phone]`/`[timestamp]` substitution and header handling |
| `utils/log.py` | loguru logging setup (stderr output; a `logs/` directory is created but file logging is commented out) |
| `utils/sql.py` | Small SQLite helper (`API200` table) used to store validated endpoint URLs |
| `utils/__init__.py` | Pool of browser `User-Agent` strings |
| `api.json` | 87 structured endpoint definitions with method, headers, and body templates |
| `GETAPI.json` | 1,018 raw GET endpoint URLs with `[phone]` placeholders |
| `debug/` | Experimental endpoint-harvesting scripts (see below) |
| `img/` | Screenshots and GIFs (Windows command-line navigation, a packaged `smsboom_pyinstall.exe`) used as documentation images |
| `logo.ico` | Application icon |
| `.github/workflows/run.yaml` | Manual-dispatch GitHub Actions workflow that installs the requirements and invokes `smsboom.py run` with a phone number taken from the `NUMBER` repository secret and 32 threads |
| `Dockerfile` | `python:3.9-alpine` image that installs dependencies with pipenv and runs `smsboom.py` |
| `requirements.txt` / `requirements-dev.txt` | Pinned runtime dependencies; the dev file is a pipenv-generated lock that additionally pins Flask/SQLAlchemy packages |
| `LICENSE` | Apache License 2.0 |

### GUI (`smsboom_GUI.py`)

Builds a Tkinter window titled "SMSBoom - 短信轰炸机 ©落落" with a phone-number entry field and a 启动轰炸 ("start") button. The button has no callback bound, so the GUI is an unwired skeleton rather than a functional front end for the core logic.

### `debug/` tooling

- `spider-api.py` — crawls third-party SMS-bombing websites listed in `hz-web.json`, extracts their endpoint URLs, validates them with 254 threads, stores the results in SQLite (`api.db`), and can export them to `GETAPI.json` via its `save_api` command.
- `tou_api.py` — converts `touapi.json` (derived from `api.js`, a dump of endpoints harvested from third-party pages) into `api_tou.json`.
- These scripts import packages (`requests`, `prettytable`, `tqdm`, `urllib3`) that are not declared in either requirements file; they are experimental and not needed by the main tool.

## Dependencies

Python 3.x (the CI workflow uses 3.8; the Docker image uses 3.9). Direct runtime dependencies, as pinned in `requirements.txt`:

| Package | Version | Used for |
| --- | --- | --- |
| `click` | 8.1.2 | Command-line interface |
| `httpx` | 0.22.0 | HTTP client (synchronous and asynchronous) |
| `loguru` | 0.6.0 | Logging |
| `pydantic` | 1.9.0 | Endpoint data model |

The remaining pins in `requirements.txt` are transitive dependencies. `requirements-dev.txt` is a pipenv-generated lock file that additionally pins Flask, Flask-Admin, Flask-SQLAlchemy, and SQLAlchemy, none of which are imported by any script in the tree.

## Known caveats

- The `Dockerfile` runs `pipenv install --deploy --ignore-pipfile`, which requires a `Pipfile`/`Pipfile.lock`; neither file is present in the repository, so the image build fails as written. The pinned dependencies in `requirements.txt` can be installed with `pip` instead.
- The endpoint data is static and dated; many of the listed hosts should be assumed dead or patched.
- All HTTP clients are created with TLS certificate verification disabled (`verify=False`).
- File logging in `utils/log.py` is commented out; only stderr output is active, although a `logs/` directory is created on import.

## For defenders

The technique this tool demonstrates — replaying unauthenticated, un-throttled "send SMS code" endpoints — is straightforward to prevent on the service side:

- Require a fresh captcha or risk check on every SMS send, and rate-limit per phone number as well as per IP and device.
- Do not reveal in responses whether a send succeeded, or how many sends remain.
- Monitor for bursts of verification SMS to a single number across otherwise unrelated accounts.

## License

Released under the [Apache License 2.0](LICENSE).
