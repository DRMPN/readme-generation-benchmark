# twint

An advanced Twitter scraping and OSINT tool, written in Python. twint can be used as a command-line tool or imported as a Python library. It scrapes tweets, user profiles, followers, follows, and favorites without requiring Twitter API credentials. The package is version 2.1.21.

## Overview

twint provides:

- **Tweet search and timelines**: search by keyword, username, location, language, and date range, or collect a user's full timeline.
- **User data**: profile information, followers, and accounts a user follows, with optional full user details.
- **Favorites**: tweets a user has liked.
- **Filtering**: minimum likes, retweets, and replies, plus filters for images, videos, links, verified users, retweets, and replies.
- **Translation**: optional translation of tweets through Google Translate, using the `googletransx` package.
- **Output options**: plain text, CSV, JSON, SQLite, Elasticsearch, and pandas DataFrames (HDF5 or Pickle).
- **Proxy support**: HTTP, SOCKS4, and SOCKS5 proxies, plus Tor with automatic identity rotation.

## Requirements

- Python 3.6 or later (`REQUIRES_PYTHON = '>=3.6.0'`). The package classifiers list Python 3.6, 3.7, and 3.8.
- The following packages are installed automatically from `setup.py`:
  - `aiohttp`, `aiodns`, `aiohttp_socks`, `pysocks`
  - `beautifulsoup4`, `cchardet`
  - `dataclasses`
  - `elasticsearch`
  - `pandas`
  - `schedule`
  - `geopy`
  - `fake-useragent`
  - `googletransx`

## Installation

### From source

Clone the repository and install it with pip:

```bash
git clone https://github.com/twintproject/twint.git
cd twint
pip3 install .
```

This installs a `twint` console command, which maps to `twint.cli:run_as_command`.

### With Docker

The included `Dockerfile` uses `python:3.6-buster`. It clones the repository into `/root/twint`, installs it with `pip3 install . -r requirements.txt`, and starts a Bash shell.

```bash
docker build -t twint .
docker run -it twint
```

> **Note:** The `Dockerfile` and `.travis.yml` both install from `requirements.txt`, but that file was not among the supplied repository files, so its contents are not described here.

## Usage

### Command line

Run `twint` with one of the primary target options. The CLI requires at least one of `-u`, `-s`, `-g`, or `--near`, unless you use `--all`, `--userid`, or `-cq`/`--custom-query`.

Examples based on the available options:

```bash
# Tweets from a user
twint -u username

# Search for a phrase, starting from a date
twint -s "python" --since 2018-01-01

# Full timeline of a user (tweets, retweets, and replies); requires -u
twint -u username -tl

# Save results to CSV or JSON (an output file is required)
twint -u username --csv -o tweets.csv
twint -s "osint" --json -o results.json

# Users who follow an account, with full user details
twint -u username --followers --user-full -o followers.csv

# Tweets an account has liked
twint -u username --favorites

# Filter by engagement
twint -s "climate" --min-likes 10 --min-retweets 5

# Read usernames from a file or a comma-separated list
twint --userlist users.txt --followers
```

### Option groups

**Targets**

- `-u, --username`: a user's tweets.
- `-s, --search`: tweets containing a word or phrase.
- `-g, --geo`: geocoded tweets.
- `--near`: tweets near a specified city.
- `--userid`: a Twitter user ID.
- `--all USERNAME`: all tweets associated with a user.
- `--to USERNAME`: tweets sent to a user.
- `-cq, --custom-query`: a custom search query.
- `--followers`, `--following`, `--favorites`: relationship and favorite scraping.
- `-tl, --timeline`: a full user timeline.
- `--userlist`: a file path or comma-separated list of users.

**Filters**

- `--since`, `--until`: date filters, such as `"2017-12-27 20:30:15"` or `2017-12-27`.
- `--year`, `-l/--lang`, `--verified`, `--email`, `--phone`.
- `--images`, `--videos`, `--media`, `--replies`, `-nr/--native-retweets`, `-fr/--filter-retweets`, `--retweets`.
- `--min-likes`, `--min-retweets`, `--min-replies`, `--links`, `--source`, `--members-list`.
- `--limit`: number of tweets to collect.
- `-pt, --popular-tweets`: popular tweets instead of recent ones.

**Output**

- `-o, --output`: output file.
- `--csv`, `--json`, `--tabs` (tab-separated CSV).
- `--hashtags`, `--cashtags`, `--stats`, `--count`, `-ho/--hide-output`.
- `--format`: a custom output template with placeholders such as `{id}`, `{username}`, `{tweet}`, `{likes}`, and `{link}`.
- `--user-full`: collect all user information. Use it with `--followers` or `--following`, or alone for user lookup.
- `--translate`, `--translate-dest` (default `en`).

**Storage**

- `-db, --database`: SQLite database file.
- `-es, --elasticsearch`: Elasticsearch host.
- `-it`, `-if`, `-iu`: custom Elasticsearch index names for tweets, follows, and users.
- `--essid`: an Elasticsearch session ID that differentiates scraping sessions.
- `-pc, --pandas-clean`: clean the pandas DataFrames at each scrape.

**Networking and resilience**

- `--proxy-type`, `--proxy-host`, `--proxy-port`.
- `--tor-control-port` (default `9051`) and `--tor-control-password` (default `my_password`). These apply when `--proxy-host` is set to `tor`.
- `-sc, --skip-certs`: skip certificate verification.
- `--backoff-exponent` (default `3.0`): the exponent used for polynomial backoff after errors.
- `--min-wait-time` (default `15`): minimum wait in seconds after a rate-limit error.
- `--resume TWEET_ID`: resume from a tweet ID.
- `--debug`: store debug information.

The CLI also checks for contradictory arguments. For example, `-tl` requires `-u`, `--csv` and `--json` require `-o`, and `--tl` cannot be combined with `-s`. The CLI prints an error and exits when a check fails.

### Python library

The `twint` package exposes a `Config` dataclass and `run` functions. The following example is based on `automate.py`:

```python
import twint

c = twint.Config()
c.Username = "username"
c.Search = "search term"
c.Since = "2018-01-01"
c.Limit = 1000
c.Store_csv = True
c.Custom = ["date", "time", "username", "tweet", "link", "likes", "retweets", "replies", "mentions", "hashtags"]
c.Output = "filename.csv"
twint.run.Search(c)
```

Other run functions include `twint.run.Profile`, `twint.run.Following`, `twint.run.Followers`, `twint.run.Favorites`, and `twint.run.Lookup`.

### Scheduled scraping

`automate.py` runs two search jobs once at startup and then every hour using the `schedule` package. Each job writes to its own CSV file. Edit the placeholder username, search term, and output filenames before running it. The script also includes commented examples for other schedules, such as every minute, daily at a set time, or on a given weekday.

## Configuration

Scraping behavior is controlled by the `Config` dataclass in `twint/config.py`. Its fields include:

- Targets: `Username`, `User_id`, `Search`, `Geo`, `Near`, `Custom_query`.
- Dates and limits: `Since`, `Until`, `Year`, `Limit`.
- Outputs: `Output`, `Store_csv`, `Store_json`, `Database`, `Elasticsearch`, `Pandas`, `Store_object`.
- Elasticsearch indexes: `Index_tweets` (default `twinttweets`), `Index_follow` (default `twintgraph`), and `Index_users` (default `twintuser`).
- Retry behavior: `Retries_count` (default `10`), `Backoff_exponent` (default `3.0`), and `Min_wait_time` (default `0` in the dataclass; the CLI default is `15`).
- Filters: `Min_likes`, `Min_retweets`, `Min_replies`, `Links`, `Source`, `Members_list`, `Filter_retweets`.
- Translation: `Translate`, `TranslateSrc` (default `en`), and `TranslateDest` (default `en`).
- Proxy settings: `Proxy_host`, `Proxy_port`, `Proxy_type`, `Tor_control_port`, and `Tor_control_password`.

### Environment variables

- `TWINT_DEBUG`: set to `debug` to enable debug logging. Logs are written to `twint.log` in the working directory. Any other value, or no value, defaults to `info`.

### Debug files

- `--debug` writes request URLs to `twint-request_urls.log`.
- `--debug` also saves the last raw response to `twint-last-request.log`.

### Output file layout

When the `-o` value has no file extension, twint treats it as a directory. It creates the directory if needed and writes files such as `tweets.csv`, `followers.json`, or `users.csv` inside it. When the value has an extension, twint writes to that file directly.

### Proxies

- `--proxy-type` accepts `http`, `socks4`, or `socks5`. Other values cause an error.
- `--proxy-host tor` connects to Tor on `127.0.0.1:9050`. When a timeout occurs, twint requests a new Tor identity through the control port, using `--tor-control-port` and `--tor-control-password`.

## Storage backends

- **CSV and JSON**: written with the `-o` option. Field lists can be customized through `Config.Custom`.
- **SQLite**: `-db` creates tables for `users`, `tweets`, `retweets`, `replies`, `favorites`, `followers`, `following`, `followers_names`, and `following_names`.
- **Elasticsearch**: `-es` indexes tweets, follows, and users into the configured indexes. The `elasticsearch/README.md` file in the repository links to the project wiki for setup, and includes a dashboard image.
- **Pandas**: `twint.storage.panda` provides `save` and `read` functions for HDF5 (`.h5`) and Pickle (`.pkl`) files.

> **Note:** The CLI defines a `--store-pandas` option, but `initialize()` in `cli.py` does not copy it into `Config`. The pandas workflow is therefore best used through the Python library.

## Development

### Project layout

- `twint/cli.py`: command-line parser, validation, and dispatch.
- `twint/config.py`: the `Config` dataclass.
- `twint/run.py`: the `Twint` scraper class and the public `run` functions.
- `twint/get.py`, `twint/feed.py`, `twint/url.py`: HTTP requests, response parsing, and endpoint URLs.
- `twint/tweet.py`, `twint/user.py`: data models and parsing.
- `twint/output.py`, `twint/format.py`, `twint/verbose.py`: output handling and formatting.
- `twint/storage/`: SQLite, Elasticsearch, pandas, and file writers.
- `twint/token.py`: guest token retrieval.
- `twint/datelock.py`: date range handling.
- `automate.py`: a scheduled scraping example.

### Packaging

`setup.py` reads the version from `twint/__version__.py`, uses the MIT license, and includes the `twint` and `twint.storage` packages. It also reads `README.md` as the long description. The `MANIFEST.in` file was included in the repository tree, but its contents were not supplied.

### Continuous integration and deployment

`.travis.yml` configures Travis CI on Bionic:

- Python versions: 3.6, 3.7, 3.8, and nightly. Python 3.8 and nightly are allowed to fail.
- Install step: `pip install -r requirements.txt`.
- Test step: `python test.py`.
- Deployment: publishes to PyPI on tagged builds, using the Python 3.7 job.

### Issue templates

The `.github/ISSUE_TEMPLATE.md` and `.github/ISSUE_TEMPLATE/ISSUE_TEMPLATE.md` files ask reporters to confirm they use Python 3.6 and the latest version of twint, to include the exact command they ran, and to describe their environment. They also ask that questions and feature requests be labeled in the title.

### Funding

`.github/FUNDING.yml` lists a Patreon account (`twintproject`) and a PayPal link.

## Testing

`test.py` is the project's test script. It runs the public scraping functions against the Twitter account `verified`, so it requires network access.

The script:

1. Runs `Profile`, `Search`, `Following`, `Followers`, and `Favorites` with a limit of 20 items.
2. Applies four test types to each run: a standard run, a JSON output test, a CSV output test (with custom fields), and a SQLite database test.
3. Removes the generated `test_twint.db`, `test_twint.json`, and `test_twint.csv` files.
4. Prints `[+] Testing complete!` when finished.

Run the tests from the repository root:

```bash
pip3 install .
python3 test.py
```

## License

twint is released under the MIT License. The copyright notice reads "Copyright (c) 2018 Cody Zacharias." The full license text is in the `LICENSE` file. The software is provided "as is," without warranty of any kind.
