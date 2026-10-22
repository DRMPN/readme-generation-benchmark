# SMSBoom

SMSBoom is a Python command-line project that loads HTTP request definitions from JSON files and can send requests to those definitions using one or more supplied phone numbers. The repository also contains a small Tkinter interface and experimental scripts for inspecting and collecting API definitions.

The request data includes third-party phone-verification endpoints. Sending requests to them can cause messages to be sent to real people and may burden the services involved. **Use this project only with systems and phone numbers you own or are explicitly authorized to test. Do not use it to send unsolicited messages, overwhelm services, or target another person.** The repository does not establish that the listed endpoints are current, authorized, or suitable for testing.

## Repository contents

- `smsboom.py` — Click-based command-line entry point. It loads request definitions, handles proxy lists, and offers threaded, asynchronous, single-threaded, and data-update commands.
- `api.json` — JSON definitions for requests with a URL, HTTP method, headers, and data. Entries use `[phone]` and, in some cases, `[timestamp]` as replacement tokens.
- `GETAPI.json` — A list of GET request URLs that use `[phone]` as a replacement token.
- `utils/` — Request handling, API models, logging, and supporting code.
- `smsboom_GUI.py` — A basic Tkinter window with a phone-number entry and a button. The supplied code does not connect the button to request execution.
- `debug/` — Experimental API collection and conversion scripts, sample data, and an SQLite database.
- `requirements.txt` and `requirements-dev.txt` — Dependency manifests.
- `Dockerfile` — A container build definition.
- `.github/workflows/run.yaml` — A manually triggered GitHub Actions workflow.
- `img/` and `logo.ico` — Image and icon assets.

## Setup

The main script imports third-party packages including Click, HTTPX, and Pydantic. Install the project dependencies from the repository root using the supplied manifest:

```bash
python -m pip install -r requirements.txt
```

For development dependencies, the repository also provides `requirements-dev.txt`:

```bash
python -m pip install -r requirements-dev.txt
```

The included GitHub Actions workflow uses Python 3.8, while the Dockerfile starts from Python 3.9 Alpine. The files provided here do not declare a single supported Python-version range, so compatibility outside those environments is not guaranteed.

The Dockerfile copies the repository into `/src`, installs Pipenv, and runs `pipenv install --deploy --ignore-pipfile` before starting `smsboom.py`. The supplied file tree does not include a `Pipfile` or `Pipfile.lock`; check that these files are available before relying on the Docker build.

## Usage

The command-line program is invoked through `smsboom.py` and uses Click commands. To inspect the available command names and options without starting requests, run:

```bash
python smsboom.py --help
```

The available commands are:

- `run` — Submits the configured API and GET URL requests using a thread pool. Its options include phone-number input, thread count, frequency, interval, and an optional proxy mode. The code defaults to 64 threads, one execution wave, and a 60-second interval.
- `asyncRun` — Sends the loaded definitions through the asynchronous request implementation.
- `oneRun` — Iterates through the definitions in a single thread; the source describes it as intended for testing.
- `update` — Downloads replacement `api.json` and `GETAPI.json` files from the URLs defined in the script.

**Do not run the sending commands against real phone numbers or third-party services without explicit authorization.** The bundled request data is loaded automatically by the sending commands, and the code can contact every configured entry. `oneRun` is not a dry run: it also makes HTTP requests. The `update` command replaces the local JSON data files, so review changes before using updated data.

## Configuration

The request definitions are stored in `api.json` and `GETAPI.json` beside `smsboom.py`.

Each object in `api.json` can define a description (`desc`), URL (`url`), HTTP method (`method`), headers (`header`), and request data (`data`). The model defaults the method to `GET`; request data may be represented as a string or object. The request code sends object data as JSON and string data as form data. The runtime replaces `[phone]` with the supplied number and replaces `[timestamp]` in supported string content with a generated timestamp.

`GETAPI.json` is a JSON array of URL strings. The request code substitutes `[phone]` and sends each entry as a GET request.

When proxy mode is enabled, the program reads proxy entries from files beside the script: `http_proxy.txt`, `socks5_proxy.txt`, and `socks4_proxy.txt`. Each file is interpreted as one proxy address per line. Missing files are created by the loader. Proxy mode requires at least one loaded proxy; otherwise the program exits with an error.

Logs are written to standard error. The logging module also creates a `logs` directory in the current working directory, although file logging is commented out in the supplied implementation.

## Development

The main request model and transport functions are in `utils/models.py` and `utils/req.py`. `utils/models.py` handles token replacement and request fields; `utils/req.py` provides synchronous, proxy, and asynchronous request paths. Logging is configured in `utils/log.py`.

The scripts in `debug/` are separate experiments rather than a documented production workflow. For example, `debug/spider-api.py` fetches web pages and tests discovered URLs, while `debug/tou_api.py` converts data from one JSON structure to another. These scripts can make network requests and should be reviewed carefully before use.

When editing request data or code, validate JSON syntax and review the exact URLs, methods, headers, and payloads. Prefer local fixtures or controlled test services for development; do not test by sending verification messages to people or contacting services without permission.

## Testing

No dedicated automated test suite or test command is present in the supplied repository files. The `oneRun` command is described in the source as a testing mode, but it still sends network requests and is not a safe substitute for unit tests. The GitHub Actions workflow installs `requirements.txt` and runs the main script with a configured secret phone number; it is manually triggered and can cause real requests. Review its configuration and effects before enabling or running it.

For safe checks, inspect the CLI help, validate JSON files locally, and add tests using mocked HTTP clients or controlled endpoints before changing request behavior.

## License

This project is distributed under the Apache License, Version 2.0. See [`LICENSE`](LICENSE) for the complete terms.
