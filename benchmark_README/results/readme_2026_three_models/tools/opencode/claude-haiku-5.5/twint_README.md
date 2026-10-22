# TWINT

TWINT (Twitter Intelligence Tool, formerly Tweep) is a Python tool for scraping Twitter data without using the official Twitter API. It can be used from the command line or imported as a Python library.

It is described in the package metadata as "An advanced Twitter scraping & OSINT tool."

- **Version:** 2.1.21 (`twint/__version__.py`)
- **License:** MIT (see [LICENSE](LICENSE))
- **Author:** Cody Zacharias
- **Project URL:** <https://github.com/twintproject/twint>
- **Wiki:** <https://github.com/twintproject/twint/wiki> (referenced by the source for in-depth documentation)

## Features

Based on the command-line options and modules in this repository, TWINT can:

- Collect a user's tweets (`-u`), or a full timeline including tweets, retweets and replies (`-tl`).
- Search tweets by word or phrase (`-s`), geolocation (`-g`), or nearby city (`--near`), with a custom query option (`-cq`).
- Filter searches by date (`--since`, `--until`), language (`-l`), author (`--to`, `--all`), verified users (`--verified`), media (`--images`, `--videos`, `--media`), links, and minimum likes, retweets or replies.
- Collect a user's followers (`--followers`), accounts they follow (`--following`), or tweets they liked (`--favorites`).
- Look up full user profile information (`--user-full`).
- Process many accounts at once from a comma-separated list or a file (`--userlist`).
- Save results as CSV (`--csv`), JSON (`--json`), or a SQLite database (`-db`).
- Index results into Elasticsearch (`-es`).
- Route requests through a proxy, including Tor (`--proxy-type`, `--proxy-host`, `--proxy-port`).
- Translate tweets with Google Translate (`--translate`).
- Be used from Python through the `twint` package (see [Python usage](#python-usage)).

## Requirements

- Python 3. `setup.py` declares `python_requires='>=3.6.0'`, and the package classifiers list Python 3.6, 3.7 and 3.8. The CI configuration (`.travis.yml`) tests Python 3.6, 3.7 and 3.8, plus a nightly build.
- Network access to Twitter/X.
- The Python dependencies listed below, which are installed automatically by `pip`.

Declared dependencies (from `setup.py`):

`aiohttp`, `aiodns`, `beautifulsoup4`, `cchardet`, `dataclasses`, `elasticsearch`, `pysocks`, `pandas`, `aiohttp_socks`, `schedule`, `geopy`, `fake-useragent`, `googletransx`

`setup.py` also lists a `dependency_links` entry pointing to a git fork of `googletrans`. This is the only non-PyPI source declared.

## Installation

### From PyPI

```bash
pip install twint
```

The package is published as `twint` (the name set in `setup.py`).

### From source

Clone the repository and install it from the project root:

```bash
git clone https://github.com/twintproject/twint.git
cd twint
pip install .
```

> **Note:** The `Dockerfile` and `.travis.yml` both run `pip install -r requirements.txt`, but this repository does not contain a `requirements.txt` file. Dependencies are declared in `setup.py`, so `pip install .` is the working method in this repository.

### Docker

The included `Dockerfile` builds an image from `python:3.6-buster`. It clones the upstream repository and runs `pip3 install . -r requirements.txt`. Because `requirements.txt` is not present in this repository, that install step will fail as written unless the file is added or the `-r requirements.txt` part is removed.

## Command-line usage

After installation, the `twint` command is available:

```bash
twint -u username
```

TWINT requires at least one of `-u`, `-s`, `-g`, `--near`, `-cq`, `--all`, or `--userid`. Running it with none of these prints an error.

### Examples

```bash
# Tweets from a user, saved to CSV
twint -u username --csv -o tweets.csv

# Search for a phrase within a date range, limited to 100 results, saved as JSON
twint -s "python" --since 2020-01-01 --until 2020-12-31 --limit 100 --json -o results.json

# Full timeline of a user (tweets, retweets and replies)
twint -tl -u username

# Followers of a user, with full user information
twint --followers -u username --user-full --csv -o followers.csv

# Store results in a SQLite database
twint -u username -db tweets.db

# Scrape a list of accounts from a file, one per line
twint --userlist users.txt --csv -o out.csv
```

### Main options

This is a selection of options from `twint/cli.py`. Run `twint --help` for the complete list.

| Option | Description |
| --- | --- |
| `-u`, `--username` | Scrape tweets from this user. |
| `-s`, `--search` | Search tweets containing this word or phrase. |
| `-tl`, `--timeline` | Collect every tweet from a user's timeline (requires `-u`). |
| `-g`, `--geo` | Search geocoded tweets. |
| `--near` | Search near a specified city. |
| `-cq`, `--custom-query` | Use a custom search query. |
| `-l`, `--lang` | Restrict to a language. |
| `--since`, `--until` | Date filters, e.g. `2017-12-27` or `"2017-12-27 20:30:15"`. |
| `--limit` | Number of tweets to collect. |
| `--verified` | Only tweets from verified users (use with `-s`). |
| `--followers`, `--following` | Collect a user's followers or accounts they follow. |
| `--favorites` | Collect tweets a user has liked. |
| `--user-full` | Collect full user information (use with `--followers` or `--following`). |
| `--userlist` | Read usernames from a comma-separated list or a file. |
| `--csv`, `--json` | Output format. Requires `-o`. |
| `--tabs` | Separate CSV fields with tabs instead of commas. |
| `-o`, `--output` | Output file. |
| `-db`, `--database` | Store tweets in a SQLite database. |
| `-es`, `--elasticsearch` | Index results into Elasticsearch at the given address. |
| `-it`, `-if`, `-iu` | Custom Elasticsearch index names for tweets, follows and users. |
| `--images`, `--videos`, `--media` | Only tweets with images, videos, or either. |
| `--replies` | Include replies. |
| `-fr`, `--filter-retweets` | Exclude retweets. |
| `-nr`, `--native-retweets` | Only native retweets. |
| `--min-likes`, `--min-retweets`, `--min-replies` | Minimum engagement thresholds. |
| `--translate`, `--translate-dest` | Translate tweets (destination defaults to `en`). |
| `--proxy-type`, `--proxy-host`, `--proxy-port` | Route requests through a proxy. |
| `--tor-control-port`, `--tor-control-password` | Tor control settings when `--proxy-host` is `tor`. |
| `--resume` | Path to a file used to record and resume the scrape position. |
| `--backoff-exponent`, `--min-wait-time` | Retry/backoff tuning after errors. |
| `--debug` | Store debug information in logs. |
| `-ho`, `--hide-output` | Do not print tweets to the terminal. |

Some options are present in the parser but have limitations you should know about:

- `--store-pandas` is defined in `twint/cli.py`, but the value is never copied to the configuration, so it currently has no effect from the command line. Pandas storage is available through the Python API (see `twint/storage/panda.py`).
- The help text for `--resume` says it takes a Tweet ID, but the code treats it as a file path: it reads the last line of that file to resume, and appends the latest position to it.
- `--format` is accepted by the parser, and its help text refers to the wiki for details. The repository does not document its behavior further.

## Python usage

TWINT can also be imported as a library. Each `twint.run` function takes a `twint.Config` object:

```python
import twint

c = twint.Config()
c.Username = "username"
c.Limit = 20
c.Store_csv = True
c.Output = "tweets.csv"

twint.run.Search(c)
```

Available run functions in `twint/run.py` include `twint.run.Search`, `twint.run.Profile`, `twint.run.Following`, `twint.run.Followers`, `twint.run.Favorites`, and `twint.run.Lookup`.

Configuration fields are defined in `twint/config.py`. `test.py` sets `Store_object = True`; see `twint/output.py` for how that flag is used.

### Scheduled jobs

`automate.py` is an example script that uses the `schedule` package to run TWINT searches repeatedly. It contains placeholder values (for example `"insert username here"`) that must be edited before use, and it runs in an infinite loop.

## Elasticsearch

The `elasticsearch/` directory contains a short README that points to the [Elasticsearch page](https://github.com/twintproject/twint/wiki/Elasticsearch) in the project wiki. Index names can be customized with `-it`, `-if`, and `-iu`, and the session can be labeled with `--essid`.

## Environment variables

- `TWINT_DEBUG`: set to `debug` to enable debug logging to a `twint.log` file in the current directory. Any other value (or none) uses the `info` level.

## Testing

`test.py` runs the library against live Twitter data for the account `verified`. It runs profile, search, following, followers and favorites collection in several output modes (plain, JSON, CSV and SQLite), then removes the generated test files. It requires network access and can be affected by changes on Twitter's side.

```bash
python test.py
```

The CI configuration in `.travis.yml` runs this script.

## Project structure

```
twint/
  cli.py          Command-line argument parsing and dispatch
  run.py          Scrape orchestration and public run functions
  config.py       Config dataclass
  get.py          HTTP requests and user lookups
  feed.py         Response parsing
  tweet.py        Tweet data model and formats
  user.py         User data model
  output.py       Output handling for each format
  storage/        Storage backends: db (SQLite), elasticsearch, panda (pandas), write (CSV/JSON)
  token.py        Guest token handling
  datelock.py     Date range handling
  verbose.py      Console messages
test.py           Live test script
automate.py       Example scheduler script
elasticsearch/    Elasticsearch notes
setup.py          Package metadata and dependencies
Dockerfile        Docker build (see note above)
```

## Limitations and notes

- TWINT scrapes Twitter/X pages rather than using the official API. Its behavior depends on the current state of Twitter/X, which can change without notice. The repository's own tests depend on live data.
- Use of this tool is subject to Twitter/X's terms of service and to the laws that apply to you. The authors provide the software without warranty (see the license).
- Some options and features are documented only in the upstream wiki, which is not included in this repository.

## Contributing

Issues and pull requests are handled on the project's GitHub page: <https://github.com/twintproject/twint>. The repository includes issue templates in `.github/`.

## License

TWINT is released under the MIT License. See [LICENSE](LICENSE) for the full text.
