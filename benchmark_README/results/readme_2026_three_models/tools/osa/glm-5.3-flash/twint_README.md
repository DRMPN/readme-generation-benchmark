# twint-zrppyme4

---

[![PyPi](https://badge.fury.io/py/twint.svg)](https://badge.fury.io/py/twint)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

TWINT is a Python-based Twitter scraping tool that collects tweets, users, and follower/following data without requiring the Twitter API. It is intended for developers and analysts who need to gather Twitter data for research, analysis, or data-science workflows. The project can be used in two ways: through a command-line interface for interactive scraping, or programmatically as a Python library via a configuration object passed to its run functions. Scraped data can be written to multiple output backends, including file-based formats and indexing services. See Getting Started for how to install and run your first scrape.

---

## Core Features

- Scrape tweets, users, followers, and favorites via both a command-line interface and a programmatic Python API, so you can integrate data collection into scripts or scheduled jobs.
- Filter and refine scrapes with search terms, usernames, geo location, language, date ranges, and engagement thresholds, giving precise control over the data you collect.
- Store results in multiple backends — CSV, JSON, pandas DataFrames, Elasticsearch, or a database — letting you plug output directly into your existing analysis or indexing workflow.
- Run scrapes reliably with automatic retries, exponential backoff, guest-token refresh, and resume support for interrupted jobs.
- Route requests through proxies including Tor (with automatic identity rotation) and rotate user agents to support different network setups.

---

## Installation

Install twint-zrppyme4 using one of the following methods:

**Using PyPi:**

```sh
pip install twint
```

---

## Getting Started

### Prerequisites

- Python 3.7 or later (the package uses `dataclasses`).
- The package installed locally. From the repository root:

```bash
pip install .
```

### Quickstart: CLI

1. Fetch a user's tweets into a CSV file. `--since`/`--until` accept `YYYY-MM-DD` or `YYYY-MM-DD HH:MM:SS` values, with `--until` later than `--since`:

```bash
twint -u <username> --since 2018-01-01 --until 2018-02-01 --csv -o output.csv
```

2. Keep the validation rules enforced by `twint/cli.py` in mind:
   - Every run needs at least one primary selector: `-u/--username`, `-s/--search`, `-g/--geo`, `--near`, `--all`, `--userid`, or `--custom-query`. The full combining rules are documented in the API Reference.
   - `--csv` and `--json` each require an output file: `-o file.csv` or `-o file.json`.

### Quickstart: Python API

Run the equivalent search programmatically with `twint.Config` and `twint.run.Search`:

```python
import twint

c = twint.Config()
c.Username = "username"
c.Search = "search term"
c.Since = "2018-01-01"
c.Limit = 1000
c.Store_csv = True
c.Output = "output.csv"
twint.run.Search(c)
```

For scheduled, repeated runs, `automate.py` at the repository root shows a working pattern built on the `schedule` library. In-depth usage details are in the project wiki referenced by `twint/cli.py`: https://github.com/twintproject/twint/wiki

---

## Architecture

TWINT is a monolithic Python package organized as a layered scraping pipeline:

- **CLI / API entry points** — `twint/cli.py` parses and validates command-line arguments, while `automate.py` demonstrates programmatic use by building a `twint.Config` and calling `twint.run.Search` directly.
- **Configuration** — `twint/config.py` defines a `Config` dataclass holding all scraping options (users, search terms, date filters, output formats, proxy/Tor settings).
- **Orchestration** — `twint/run.py` drives the async scraping loop: it manages guest tokens (`twint/token.py`), retries with exponential backoff, supports resuming from a checkpoint file, and triggers Tor identity rotation on timeouts.
- **Fetching and parsing** — `twint/get.py` performs async HTTP requests (via `aiohttp`, with proxy support through `aiohttp_socks` and user-agent rotation), and `twint/feed.py` parses the JSON/HTML responses into tweet/user feeds (`twint/tweet.py`, `twint/user.py` build URLs and objects via `twint/url.py`).
- **Output / storage** — parsed data flows to pluggable backends in `twint/storage/`: CSV/JSON writers (`write.py`, `write_meta.py`), pandas (`panda.py`), Elasticsearch (`elasticsearch.py`), and a database module (`db.py`). Formatting of console/file output is handled by `twint/format.py` and `twint/output.py`.

All I/O is asyncio-based. The exact database engine behind `storage/db.py` is not confirmed from the available context. A `Dockerfile` is provided for containerized use.

---

## API Reference

Twint's stable public surface is small: the `twint.Config` dataclass, the `twint.run` module, and the `twint` command-line interface (`twint/cli.py`). Modules below that layer (`run.Twint`, `get`, `feed`, `token`, `output`, `storage`) are internal pipeline code and are not part of the supported API.

### `twint.Config` — `twint/config.py`

`Config` is a Python `@dataclass`: create one instance per job, set its fields, and pass it to a `twint.run` function.

```python
import twint

c = twint.Config()
c.Username = "screen_name"   # or: c.Search = "keyword"
c.Store_csv = True
c.Output = "out.csv"
c.Limit = 100
twint.run.Search(c)
```

Complete field list (types and defaults exactly as declared in `config.py`; a dash means the value is unannotated or its purpose is not evidenced in the provided sources):

| Field | Type | Default | Purpose |
|---|---|---|---|
| `Username` | `Optional[str]` | `None` | User whose Tweets to scrape (`-u`). |
| `User_id` | `Optional[str]` | `None` | Target a user by ID (`--userid`); mutually exclusive with `-u`. |
| `Search` | `Optional[str]` | `None` | Search term or phrase (`-s`). |
| `Lookup` | `bool` | `False` | — |
| `Geo` | `str` | `""` | Geocoded-Tweet search (`-g`). |
| `Location` | `bool` | `False` | Show the user's location (experimental, `--location`). |
| `Near` | `str` | `None` | Search near a specified city (`--near`). |
| `Lang` | `Optional[str]` | `None` | Tweets in a specific language (`-l`). |
| `Output` | `Optional[str]` | `None` | Output file; required with `Store_csv`/`Store_json`. |
| `Elasticsearch` | `object` | `None` | Index results to Elasticsearch (`-es`). |
| `Year` | `Optional[int]` | `None` | Filter Tweets before the specified year. |
| `Since` | `Optional[str]` | `None` | Filter Tweets sent since this date (start of the window). |
| `Until` | `Optional[str]` | `None` | Filter Tweets sent until this date. |
| `Email` | `Optional[str]` | `None` | Filter Tweets that might contain email addresses. |
| `Phone` | `Optional[str]` | `None` | Filter Tweets that might contain phone numbers. |
| `Verified` | `bool` | `False` | Only verified users; use with `Search`. |
| `Store_csv` | `bool` | `False` | Write output as a `.csv` file. |
| `Store_json` | `bool` | `False` | Write output as a `.json` file. |
| `Custom` | — | `{"tweet": None, "user": None, "username": None}` | Custom output columns; `automate.py` assigns a list such as `["date", "time", "username", "tweet", ...]`. |
| `Show_hashtags` | `bool` | `False` | — |
| `Show_cashtags` | `bool` | `False` | — |
| `Limit` | `Optional[int]` | `None` | Limit on the total number of Tweets. |
| `Count` | `Optional[int]` | `None` | — |
| `Stats` | `bool` | `False` | — |
| `Database` | `object` | `None` | Database passed to `storage.db.Conn` in `run.Twint`. |
| `To` | `str` | `None` | — |
| `All` | — | `None` | `--all` mode; mutually exclusive with `Username`/`User_id`. |
| `Debug` | `bool` | `False` | Debug mode; `run.Twint.Feed` writes the raw response to `twint-last-request.log`. |
| `Format` | — | `None` | — |
| `Essid` | `str` | `""` | — |
| `Profile` | `bool` | `False` | Selects Tweet parsing (`feed.parse_tweets`) in `run.Twint.Feed`. |
| `Followers` | `bool` | `False` | Selects follower parsing (`feed.Follow`). |
| `Following` | `bool` | `False` | Selects following parsing (`feed.Follow`). |
| `Favorites` | `bool` | `False` | Selects favorites parsing (`feed.MobileFav`). |
| `TwitterSearch` | `bool` | `False` | Selects Tweet parsing for search runs (`feed.parse_tweets`). |
| `User_full` | `bool` | `False` | In follow mode, fetch full user profiles via `get.Multi`. |
| `Store_object` | `bool` | `False` | Store results as Python objects (triggers `output._clean_follow_list` at startup). |
| `Store_object_tweets_list` | `list` | `None` | List that collects stored Tweet objects. |
| `Store_object_users_list` | `list` | `None` | List that collects stored user objects. |
| `Store_object_follow_list` | `list` | `None` | List that collects stored follow entries. |
| `Pandas_type` | `type` | `None` | — |
| `Pandas` | `bool` | `False` | Store output as pandas dataframes (`storage/panda.py`). |
| `Index_tweets` | `str` | `"twinttweets"` | Elasticsearch index for Tweets. |
| `Index_follow` | `str` | `"twintgraph"` | Elasticsearch index for follow data. |
| `Index_users` | `str` | `"twintuser"` | Elasticsearch index for users. |
| `Retries_count` | `int` | `10` | Consecutive request errors tolerated before `run.Twint.Feed` stops. |
| `Resume` | `object` | `None` | Resume file; last cursor is read at startup and appended during the run. |
| `Images` | `bool` | `False` | — |
| `Videos` | `bool` | `False` | — |
| `Media` | `bool` | `False` | — |
| `Replies` | `bool` | `False` | — |
| `Pandas_clean` | `bool` | `True` | Runs `storage.panda.clean()` at startup when enabled. |
| `Lowercase` | `bool` | `True` | — |
| `Pandas_au` | `bool` | `True` | — |
| `Proxy_host` | `str` | `""` | Proxy host; set to `tor` to enable Tor identity rotation on timeouts. |
| `Proxy_port` | `int` | `0` | Proxy port. |
| `Proxy_type` | `object` | `None` | — |
| `Tor_control_port` | `int` | `9051` | Tor control port. |
| `Tor_control_password` | `str` | `None` | Required for automatic Tor identity rotation. |
| `Retweets` | `bool` | `False` | — |
| `Query` | `str` | `None` | — |
| `Hide_output` | `bool` | `False` | — |
| `Custom_query` | `str` | `""` | Raw custom query; bypasses the `-u`/`-s`/`-g`/`--near` requirement in `check()`. |
| `Popular_tweets` | `bool` | `False` | — |
| `Skip_certs` | `bool` | `False` | — |
| `Native_retweets` | `bool` | `False` | — |
| `Min_likes` | `int` | `0` | Minimum number of likes. |
| `Min_retweets` | `int` | `0` | Minimum number of retweets. |
| `Min_replies` | `int` | `0` | Minimum number of replies. |
| `Links` | `Optional[str]` | `None` | — |
| `Source` | `Optional[str]` | `None` | — |
| `Members_list` | `Optional[str]` | `None` | — |
| `Filter_retweets` | `bool` | `False` | — |
| `Translate` | `bool` | `False` | Enable translation of results (`TranslateSrc` to `TranslateDest`). |
| `TranslateSrc` | `str` | `"en"` | Source language for translation. |
| `TranslateDest` | `str` | `"en"` | Destination language for translation. |
| `Backoff_exponent` | `float` | `3.0` | Exponent for retry backoff delays (validated positive). |
| `Min_wait_time` | `int` | `0` | Floor, in seconds, for retry delays (validated non-negative). |
| `Bearer_token` | `str` | `None` | Set at runtime by `run.Twint`. |
| `Guest_token` | `str` | `None` | Managed at runtime by `twint.token.Token` (`refresh()`). |
| `deleted` | `list` | `None` | Initialized to `[]` by `run.Twint`; collects deleted Tweets found during a run. |

### `twint.run` — `twint/run.py`

- `twint.run.Search(config)` — runs a Tweet search with the supplied `Config`; the only `run` entry point exercised in the provided sources (see `automate.py`).

Internally, `run.py` defines the `Twint` orchestrator class, which handles guest-token refresh (`twint.token.Token`), retries with exponential backoff (`Retries_count`, `Backoff_exponent`, `Min_wait_time`), optional Tor identity rotation, and resume-file tracking. These are implementation details, not public API; the provided `run.py` source is truncated, so no other `twint.run` functions can be confirmed from it.

### Command line — `twint/cli.py`

`cli.py` builds an `argparse` program (`prog="twint"`, declared usage `python3 twint [options]`) and copies the parsed arguments onto a `Config` instance in `initialize()`. Options visible in the provided excerpt:

| Option | Purpose |
|---|---|
| `-u`, `--username` | User's Tweets you want to scrape |
| `-s`, `--search` | Search for Tweets containing this word or phrase |
| `-g`, `--geo` | Search for geocoded Tweets |
| `--near` | Near a specified city |
| `--location` | Show user's location (Experimental) |
| `-l`, `--lang` | Search for Tweets in a specific language |
| `-o`, `--output` | Save output to a file |
| `-es`, `--elasticsearch` | Index to Elasticsearch |
| `--year` | Filter Tweets before specified year |
| `--since DATE` | Filter Tweets sent since date (e.g. `2017-12-27 20:30:15` or `2017-12-27`) |
| `--until DATE` | Filter Tweets sent until date |
| `--email` | Filter Tweets that might have email addresses |
| `--phone` | Filter Tweets that might have phone numbers |
| `--verified` | Display Tweets only from verified users (use with `-s`) |
| `--csv` | Write as `.csv` file |
| `--tabs` | Separate CSV fields with tab characters, not commas |
| `--json` | Write as `.json` file |

`--userid`, `--all` and `--tl` are additionally confirmed by the validation messages in `check()`. The argparse listing in the provided source is truncated after `--json`; the remaining arguments consumed by `initialize()` mirror the `Config` fields listed above (e.g. limit/count, database, resume, proxy and Tor settings, translation and `Min_*` filters).

Validation enforced in `check()`:

- With a username, user list, or members list: `--verified` requires `-s`; `--userid` and `--all` are rejected.
- `--tl` cannot be combined with `-s` and requires `-u`.
- Without `-s`, a custom query or one of `-g`, `--near`, `--all`, `--userid` must be given.
- `--all` and `--userid` are mutually exclusive.
- `-o` is required with `--csv` or `--json`.
- The backoff exponent must be positive and the minimum wait time non-negative.

---

## Contributing

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). twint-zrppyme4 repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{twint-zrppyme4,

        author = {README Benchmark},

        title = {twint-zrppyme4 repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---