# TWINT – Twitter Intelligence Tool

TWINT (formerly known as Tweep) is an advanced Twitter scraping and OSINT tool written in Python. It allows you to scrape tweets, retweets, replies, favourites, followers and following lists from Twitter without an account or API keys: TWINT fetches an anonymous guest token automatically and uses it for all requests.

In-depth documentation is available on the project wiki: https://github.com/twintproject/twint/wiki

## Features

- Scrape a user's tweets, full timeline (tweets, retweets and replies), favourites, followers and following
- Search tweets by keyword, phrase, geo location, language or custom query
- Filter results by date range, media type, engagement (likes/retweets/replies), source client, links and more
- Save results as CSV, JSON, plain text, a SQLite database, an Elasticsearch index or a Pandas DataFrame
- Optional automatic translation of tweets via Google Translate
- Proxy support (HTTP, SOCKS4, SOCKS5) and Tor integration with automatic identity rotation
- Resume interrupted scrapes, custom output formats, scheduled/recurring jobs

## Requirements

- Python 3.6 or newer (3.6, 3.7 and 3.8 are tested in CI)
- Dependencies are installed automatically and include: `aiohttp`, `aiodns`, `beautifulsoup4`, `cchardet`, `dataclasses`, `elasticsearch`, `pysocks`, `pandas`, `aiohttp_socks`, `schedule`, `geopy`, `fake-useragent`, `googletransx`

## Installation

From PyPI:

```bash
pip3 install twint
```

Or the latest version from GitHub:

```bash
pip3 install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint
```

Installing the package also installs the `twint` console command.

### Docker

The repository ships a `Dockerfile` based on `python:3.6-buster` that clones the repository, installs TWINT with its requirements and starts a bash shell:

```bash
docker build -t twint .
docker run -it twint
```

## Usage

### Command line

Some examples:

```bash
# Collect a user's tweets (limit in increments of 20)
twint -u username --limit 100

# Search tweets containing a word or phrase
twint -s "search phrase"

# Combine a user with a search term
twint -u username -s "pineapple"

# Restrict results to a date range
twint -u username --since 2017-12-27 --until 2018-01-01

# Save as CSV or JSON
twint -u username --csv -o tweets.csv
twint -u username --json -o tweets.json

# Store in a SQLite database
twint -u username -db tweets.db

# Index to Elasticsearch
twint -u username -es localhost:9200

# Scrape followers, following or favourites
twint -u username --followers
twint -u username --following
twint -u username --favorites

# Collect every tweet from a user's timeline
twint -u username --timeline

# Full user information (use with followers/following)
twint -u username --followers --user-full

# Only tweets from verified accounts
twint -s "search phrase" --verified
```

The complete option list is available with `twint --help`. Highlights, grouped by purpose:

| Group | Options |
| --- | --- |
| Search and filtering | `-u/--username`, `-s/--search`, `-g/--geo`, `--near`, `--location`, `-l/--lang`, `--year`, `--since`, `--until`, `--email`, `--phone`, `--verified`, `--to`, `--all`, `--userid`, `--userlist`, `--members-list`, `--min-likes`, `--min-retweets`, `--min-replies`, `--links`, `--source`, `--images`, `--videos`, `--media`, `--replies`, `--retweets`, `--native-retweets`, `--filter-retweets`, `--popular-tweets`, `-cq/--custom-query` |
| Output and storage | `-o/--output`, `--csv`, `--json`, `--tabs`, `--hashtags`, `--cashtags`, `-db/--database`, `-es/--elasticsearch`, `--essid`, `--store-pandas`, `--pandas-type`, `-pc/--pandas-clean`, `--format`, `-ho/--hide-output`, `--count`, `--stats` |
| Behaviour | `--limit`, `--resume`, `--debug`, `-sc/--skip-certs`, `--backoff-exponent`, `--min-wait-time`, `--translate`, `--translate-dest` |
| Proxies | `--proxy-type`, `--proxy-host`, `--proxy-port`, `--tor-control-port`, `--tor-control-password` |

Some combinations are rejected by design: `--verified` only works with `-s`; `-tl` requires `-u` and cannot be combined with `-s`; `--userid`/`--all` cannot be combined with `-u` or each other. At least one of `-u`, `-s`, `-g` or `--near` (or `-cq`) is required. `--csv` and `--json` require an output file via `-o`.

### As a Python module

TWINT can also be used as a library. Build a `twint.Config()` object and pass it to one of the runners:

```python
import twint

c = twint.Config()
c.Username = "username"
c.Search = "search phrase"
c.Since = "2018-01-01"
c.Limit = 1000
c.Store_csv = True
c.Output = "tweets.csv"

twint.run.Search(c)
```

Available runners: `twint.run.Search`, `twint.run.Profile`, `twint.run.Followers`, `twint.run.Following`, `twint.run.Favorites` and `twint.run.Lookup`. `Search` optionally accepts a callback. Config attributes mirror the CLI options (for example `Username`, `User_id`, `Search`, `Since`, `Until`, `Limit`, `Store_csv`, `Store_json`, `Output`, `Database`, `Elasticsearch`, `User_full`, `Translate`, `TranslateDest`, `Proxy_host`, `Proxy_port`, `Proxy_type`). Setting `c.Store_object = True` keeps scraped tweet/user objects in memory for programmatic use.

## Output and storage

- **Plain text** – with `-o file` (without `--csv`/`--json`), one tweet per line.
- **CSV/JSON** – with `--csv` or `--json`. Use `--tabs` for tab-separated CSV fields. Column selection is configurable in Python via `c.Custom` (e.g. `c.Custom["tweet"] = ["id", "username"]`). When the output path has no extension, files are created per object type (e.g. `tweets.csv`, `users.csv`, `usernames.csv`). JSON output is written as one record per line.
- **SQLite** – with `-db file.db`. The database is created with the tables `users`, `tweets`, `retweets`, `replies`, `favorites`, `followers`, `following`, `followers_names` and `following_names`.
- **Elasticsearch** – with `-es <host>`. Tweets, follows and users are indexed into `twinttweets`, `twintgraph` and `twintuser` by default; override with `-it`, `-if` and `-iu`. Use `--essid` to tag documents with a session ID. Tweet and user locations are geocoded (via `geopy`) into `geo_point` fields. See `elasticsearch/README.md` and the wiki for details.
- **Pandas** – with `--store-pandas` (HDF5 by default, or Pickle via `--pandas-type Pickle`). In Python, set `c.Pandas = True` and read the results after the run:

```python
twint.run.Search(c)
print(twint.storage.panda.Tweets_df)   # also Follow_df and User_df

twint.storage.panda.save("tweets", twint.storage.panda.Tweets_df, type="Pickle")
df = twint.storage.panda.read("tweets", type="Pickle")
```

## Custom output format

Use `--format` with placeholders such as `{id}`, `{conversation_id}`, `{date}`, `{time}`, `{timezone}`, `{user_id}`, `{username}`, `{name}`, `{place}`, `{tweet}`, `{language}`, `{hashtags}`, `{cashtags}`, `{mentions}`, `{urls}`, `{photos}`, `{video}`, `{thumbnail}`, `{replies}`, `{retweets}`, `{likes}`, `{link}`, `{is_retweet}`, `{user_rt_id}`, `{quote_url}`, `{near}`, `{geo}`, `{translate}`, `{trans_src}` and `{trans_dest}`. The default line format is `id date time timezone <username> tweet`, extended with hashtags, cashtags, engagement stats or translations when the corresponding options are enabled.

## Proxies and Tor

Proxies are configured with `--proxy-host`, `--proxy-port` and `--proxy-type` (allowed types: `http`, `socks4`, `socks5`; HTTPS is not supported). Setting `--proxy-host tor` uses a SOCKS5 connector on `127.0.0.1:9050`; on request timeouts TWINT can rotate the Tor identity through the control port configured with `--tor-control-port` (default `9051`) and `--tor-control-password`.

## Scheduling and automation

`automate.py` is a ready-made example of running recurring scrape jobs with the `schedule` library. Each job builds a `twint.Config()` and calls `twint.run.Search(c)`; jobs are registered with expressions such as `schedule.every().hour.do(jobone)` and executed in a `while True: schedule.run_pending()` loop.

## Debugging

- Set the environment variable `TWINT_DEBUG=debug` to write verbose logs (level and timestamp formatted) to `twint.log`.
- `--debug` stores the last API response in `twint-last-request.log` and all request URLs in `twint-request_urls.log`.
- On rate-limit errors TWINT sleeps using a polynomial backoff (tune with `--backoff-exponent` and `--min-wait-time`), rotates the user agent, and refreshes the guest token automatically when it expires.

## Development

The `twint` package is organised as follows:

```
twint/
├── cli.py          # argument parsing and validation
├── config.py       # Config dataclass
├── run.py          # runners: Search, Profile, Followers, Following, Favorites, Lookup
├── feed.py         # response/feed parsing
├── get.py          # asynchronous HTTP requests
├── url.py          # query and URL construction
├── token.py        # guest token fetching/refreshing
├── tweet.py        # tweet object
├── user.py         # user object
├── format.py       # output formatting
├── output.py       # output pipeline
├── datelock.py     # date range handling
├── verbose.py      # summary messages
└── storage/        # write.py, write_meta.py, db.py, elasticsearch.py, panda.py
```

### Testing

`python test.py` runs live integration checks that exercise `Search`, `Profile`, `Following`, `Followers` and `Favorites` in four modes each (plain, JSON, CSV and SQLite), then deletes the generated `test_twint.db`, `test_twint.json` and `test_twint.csv` files. Continuous integration (`.travis.yml`) runs this on Python 3.6, 3.7 and 3.8 (plus nightly), and deploys tagged commits to PyPI.

## Contributing and issues

When opening an issue, please follow `.github/ISSUE_TEMPLATE.md`: prefix the title with `[REQUEST]` or `[QUESTION]` when applicable, search existing issues for duplicates, and include the exact command you ran, a detailed description of the problem and your environment (OS, Anaconda/Jupyter/terminal), after confirming you are on Python 3.6 and the latest version of TWINT.

## Funding

Development is supported through Patreon (`twintproject`) and PayPal (`paypal.me/noneprivacy`) — see `.github/FUNDING.yml`.

## License

TWINT is released under the MIT License. Copyright (c) 2018 Cody Zacharias / The Twint Project. See the `LICENSE` file for the full text.
