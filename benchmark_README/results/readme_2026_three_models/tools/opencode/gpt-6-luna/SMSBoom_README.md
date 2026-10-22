# SMSBoom

SMSBoom is a Python command-line program that sends HTTP requests to the SMS verification-code endpoints listed in its local JSON data files. The repository also contains a small Tkinter interface, but its start button is not wired to any action.

> **Use responsibly.** Sending unsolicited or repeated verification-code requests can disrupt services and harass phone-number owners, and may violate laws or service terms. Use this software only with explicit authorization, on systems and phone numbers you control, and at a rate those systems permit. The bundled endpoint lists refer to third-party services; their presence here does not imply permission, current availability, or successful delivery. The project does not verify consent or authorization for you.

## Contents

- [`smsboom.py`](smsboom.py) — Click-based command-line entry point.
- [`smsboom_GUI.py`](smsboom_GUI.py) — minimal Tkinter window; the button currently has no callback.
- [`api.json`](api.json) — request definitions with a URL, HTTP method, headers, and request data.
- [`GETAPI.json`](GETAPI.json) — URL strings requested with HTTP GET.
- [`utils/`](utils/) — request, API-model, and logging helpers.
- [`requirements.txt`](requirements.txt) — pinned Python dependencies.
- [`Dockerfile`](Dockerfile) — container recipe (see the note below).

## Requirements and installation

The included Dockerfile uses Python 3.9, which is a suitable baseline for the checked-in dependency pins.

1. Install Python 3.9 and create/activate a virtual environment if desired.
2. Install the dependencies:

   ```sh
   python -m pip install -r requirements.txt
   ```

3. Inspect the available commands and options:

   ```sh
   python smsboom.py --help
   python smsboom.py run --help
   ```

The requirements include Click, HTTPX, Loguru, and Pydantic (plus their pinned dependencies). `requirements-dev.txt` contains no additional packages. Tkinter is part of the Python installation on some systems; on others it must be installed separately to open the GUI.

### Docker

The Dockerfile declares `python:3.9-alpine` and an entry point for `smsboom.py`, but it installs dependencies through Pipenv with `--ignore-pipfile`. There is no `Pipfile` in this repository, so the checked-in Dockerfile is not self-contained as provided.

## Command-line commands

The command-line interface is defined in `smsboom.py`. Run `python smsboom.py --help` for Click's displayed command names and `--help` for a command's current options.

| Command | Behavior |
| --- | --- |
| `run` | Uses a thread pool to submit requests for the configured phone number(s) to entries from both JSON files. The defaults are 64 worker threads, one pass, and a 60-second interval. |
| `asyncrun` | Uses the asynchronous request path for entries from both JSON files. This path is configured for very high concurrency and should not be aimed at third-party services. |
| `onerun` | Sends requests sequentially through the entries from both JSON files; the source describes this as a single-thread/test mode. |
| `update` | Downloads replacement `api.json` and `GETAPI.json` files from the URL hard-coded in `smsboom.py` and writes them beside the script. |

For `run`, the available options are:

| Option | Default | Meaning |
| --- | --- | --- |
| `-p`, `--phone` | Prompted if omitted | Phone number; may be specified multiple times. The `run` command checks that supplied values contain digits only. |
| `-t`, `--thread` | `64` | Thread-pool worker count. |
| `-f`, `--frequency` | `1` | Number of passes through the request lists. |
| `-i`, `--interval` | `60` seconds | Delay after submitting each pass for a proxy. |
| `-e`, `--enable_proxy` | Off | Enables requests through the configured proxy list. |

`asyncrun` and `onerun` accept `-p`/`--phone` (multiple values are accepted by Click). However, the current request helpers return during the first iteration over phone numbers, so supplying more than one number does not reliably send requests for all of them.

## Request data

Both JSON files are loaded from the same directory as `smsboom.py` (or the executable when frozen). `api.json` is an array of objects with fields used by the `API` model: `url`, `method`, `header`, and `data`; `desc` is an optional label. `GETAPI.json` is an array of URL strings and those entries are requested with GET.

The request code substitutes `[phone]` with each supplied number and substitutes `[timestamp]` with the current Unix timestamp in `api.json` values. Review and maintain these files carefully: running any request command submits real network traffic to the configured URLs. Endpoint entries may be outdated, unavailable, malformed, or subject to rate limits and other server-side controls.

## Proxies and logging

When the CLI starts, it looks beside `smsboom.py` for `http_proxy.txt`, `socks5_proxy.txt`, and `socks4_proxy.txt`. Missing files are created. Put one proxy address per line in the appropriate file; the program adds the corresponding scheme (`http://`, `socks5://`, or `socks4://`). Proxy use is off by default and is enabled for `run` with `-e`. The `asyncrun` and `onerun` commands do not load the proxy files.

Logs are written to standard error. Importing the logging helper creates a `logs` directory in the current working directory, but file logging is commented out in the current implementation.

## Implementation notes

- The synchronous request functions use HTTPX with TLS certificate verification disabled (`verify=False`). The update command does the same. This weakens connection security; do not treat the connections as verified or secure.
- The threaded command submits work to a pool but does not collect or report each future's result. An HTTP response or a logged request does not establish that an SMS was delivered.
- The GUI in `smsboom_GUI.py` currently displays a phone-number field and a button, but the button is not connected to the CLI or request functions.
- No automated test suite is included in the repository.

## License

The repository includes an [Apache License, Version 2.0](LICENSE).
