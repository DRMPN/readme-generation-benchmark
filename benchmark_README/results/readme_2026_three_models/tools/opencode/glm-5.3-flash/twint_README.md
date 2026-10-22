# TWINT - Twitter Intelligence Tool

TWINT (formerly known as **Tweep**) is an advanced Twitter scraping & OSINT tool written in Python that doesn't use Twitter's API, allowing you to scrape a user's followers, following, Tweets and more while evading most API limitations.

> **Project status:** the upstream repository ([twintproject/twint](https://github.com/twintproject/twint)) has been archived on GitHub and the project is no longer actively maintained. In-depth and up-to-date documentation is available on the [Wiki](https://github.com/twintproject/twint/wiki).

## How it works

TWINT does not require Twitter API keys. It retrieves a guest token from twitter.com and, using Twitter's public web bearer token, queries the same endpoints the website uses (`api.twitter.com/2/search/adaptive.json` for searches, `api.twitter.com/2/timeline/profile/{user_id}.json` for timelines, and `mobile.twitter.com` for profiles, followers, following, and favorites).

## Features

- Scrape Tweets from a user's timeline, search results, followers, following, and likes (favorites)
- Filter by date range, year, language, geolocation, media type, engagement counts, source client, and more
- Save output as CSV, JSON, SQLite, Pandas (HDF5/Pickle), or index it to Elasticsearch
- Custom output format strings
- Proxy support (SOCKS5, HTTP, ...) including automatic Tor identity rotation on timeouts
- Optional on-the-fly translation via Google Translate
- Resume interrupted scrapes from a Tweet ID
- Python API for use in scripts and notebooks

## Requirements

- Python 3.6+
- Dependencies (installed automatically): `aiohttp`, `aiodns`, `beautifulsoup4`, `cchardet`, `dataclasses`, `elasticsearch`, `pysocks`, `pandas`, `aiohttp_socks`, `schedule`, `geopy`, `fake-useragent`, `googletransx`

## Installation

**From PyPI:**

```
pip3 install twint
```

**From source:**

```
git clone https://github.com/twintproject/twint.git
cd twint
pip3 install .
```

**Docker:** the included `Dockerfile` (based on `python:3.6-buster`) clones and installs the latest code from GitHub at build time.

```
docker build -t twint .
docker run -it twint bash
```

## Command-line usage

Installing the package also installs the `twint` console command.

```
# Collect Tweets from a user
twint -u username

# Search a user's Tweets for a term
twint -u username -s "search term"

# Search all of Twitter for a term
twint -s "search term"

# Collect a user's full timeline (Tweets, Retweets and Replies)
twint -u username -tl

# Scrape a user's followers / following / likes
twint -u username --followers
twint -u username --following
twint -u username --favorites

# Filter by date range
twint -u username --since 2015-12-20 --until 2016-01-15

# Save as CSV or JSON (an output file is required with --csv/--json)
twint -u username --csv -o file.csv
twint -u username --json -o file.json

# Store in a SQLite database
twint -u username --database tweets.db

# Index to Elasticsearch
twint -u username -es localhost:9200

# Custom output format
twint -u username --format "{username} {date} {time} {tweet}"

# Use a proxy
twint -u username --proxy-type socks5 --proxy-host 127.0.0.1 --proxy-port 9050

# Search Tweets from a list of users (comma-separated string or file)
twint --userlist "user1,user2"
```

### Command-line options

All options accepted by the `twint` command:

**Scraping targets and search**

| Option | Description |
| --- | --- |
| `-u`, `--username` | User's Tweets you want to scrape |
| `-s`, `--search` | Search for Tweets containing this word or phrase |
| `-tl`, `--timeline` | Collect every Tweet from a user's Timeline (Tweets, RTs & Replies) |
| `--followers` | Scrape a person's followers |
| `--following` | Scrape a person's follows |
| `--favorites` | Scrape Tweets a user has liked |
| `--user-full` | Collect all user information (use with `--followers` or `--following` only) |
| `--to` | Search Tweets to a user |
| `--all` | Search all Tweets associated with a user |
| `--userid` | Twitter user id |
| `--userlist` | Userlist from list or file |
| `--members-list` | Filter the Tweets sent by users in a given list |
| `-cq`, `--custom-query` | Custom search query |
| `-pt`, `--popular-tweets` | Scrape popular Tweets instead of recent ones |

**Filters**

| Option | Description |
| --- | --- |
| `--year` | Filter Tweets before the specified year |
| `--since` | Filter Tweets sent since date (e.g. `"2017-12-27 20:30:15"` or `2017-12-27`) |
| `--until` | Filter Tweets sent until date (e.g. `"2017-12-27 20:30:15"` or `2017-12-27`) |
| `-l`, `--lang` | Search for Tweets in a specific language |
| `-g`, `--geo` | Search for geocoded Tweets |
| `--near` | Near a specified city |
| `--location` | Show user's location (Experimental) |
| `--email` | Filter Tweets that might have email addresses |
| `--phone` | Filter Tweets that might have phone numbers |
| `--verified` | Display Tweets only from verified users (use with `-s`) |
| `--images` | Display only Tweets with images |
| `--videos` | Display only Tweets with videos |
| `--media` | Display Tweets with only images or videos |
| `--replies` | Display replies to a subject |
| `--links` | Include or exclude Tweets containing one or more links |
| `--source` | Filter the Tweets for a specific source client |
| `--min-likes` | Filter the Tweets by minimum number of likes |
| `--min-retweets` | Filter the Tweets by minimum number of retweets |
| `--min-replies` | Filter the Tweets by minimum number of replies |
| `--retweets` | Include user's Retweets (Warning: limited) |
| `-nr`, `--native-retweets` | Filter the results for retweets only |
| `-fr`, `--filter-retweets` | Exclude retweets from the results |

**Output**

| Option | Description |
| --- | --- |
| `-o`, `--output` | Save output to a file |
| `--csv` | Write as `.csv` file |
| `--tabs` | Separate CSV fields with tab characters, not commas |
| `--json` | Write as `.json` file |
| `--hashtags` | Output hashtags in a separate column |
| `--cashtags` | Output cashtags in a separate column |
| `--format` | Custom output format (see Wiki for details) |
| `-ho`, `--hide-output` | Hide output, no Tweets will be displayed |
| `--count` | Display the number of Tweets scraped at the end of the session |
| `--stats` | Show the number of replies, retweets, and likes |
| `-db`, `--database` | Store Tweets in a SQLite3 database |
| `--store-pandas` | Save Tweets in a DataFrame (Pandas) file |
| `--pandas-type` | Specify HDF5 or Pickle (HDF5 as default) |
| `-pc`, `--pandas-clean` | Automatically clean the Pandas DataFrame at every scrape |

**Elasticsearch**

| Option | Description |
| --- | --- |
| `-es`, `--elasticsearch` | Index to Elasticsearch |
| `--essid` | Elasticsearch Session ID, used to differentiate scraping sessions |
| `-it`, `--index-tweets` | Custom Elasticsearch index name for Tweets (default: `twinttweets`) |
| `-if`, `--index-follow` | Custom Elasticsearch index name for Follows (default: `twintgraph`) |
| `-iu`, `--index-users` | Custom Elasticsearch index name for Users (default: `twintuser`) |

**Connection and reliability**

| Option | Description |
| --- | --- |
| `--proxy-type` | Socks5, HTTP, etc. |
| `--proxy-host` | Proxy hostname or IP |
| `--proxy-port` | The port of the proxy server |
| `--tor-control-port` | If `--proxy-host` is set to `tor`, the control port (default: 9051) |
| `--tor-control-password` | If `--proxy-host` is set to `tor`, the password for the control port |
| `-sc`, `--skip-certs` | Skip certs verification, useful for SSC |
| `--resume` | Resume from a Tweet ID |
| `--limit` | Number of Tweets to pull (increments of 20) |
| `--backoff-exponent` | Exponent for the polynomial backoff in case of errors |
| `--min-wait-time` | Minimum wait time in case of a scraping limit error |
| `--debug` | Store information in debug logs |
| `--translate` | Get Tweets translated by Google Translate |
| `--translate-dest` | Language to translate Tweets to (ISO2, default: `en`) |

### Custom output format

With `--format` you can build a custom line for each Tweet using these placeholders:
`{id}`, `{conversation_id}`, `{date}`, `{time}`, `{user_id}`, `{username}`, `{name}`, `{place}`, `{timezone}`, `{urls}`, `{photos}`, `{video}`, `{thumbnail}`, `{tweet}`, `{language}`, `{hashtags}`, `{cashtags}`, `{replies}`, `{retweets}`, `{likes}`, `{link}`, `{is_retweet}`, `{user_rt_id}`, `{quote_url}`, `{near}`, `{geo}`, `{mentions}`, `{translate}`, `{trans_src}`, `{trans_dest}`.

## Python API

All CLI functionality is also available programmatically through `twint.Config` and the runners in `twint.run`:

```python
import twint

c = twint.Config()
c.Username = "username"
c.Search = "search term"
c.Limit = 100
c.Store_csv = True
c.Output = "tweets.csv"

twint.run.Search(c)
```

Available runners:

| Function | Purpose |
| --- | --- |
| `twint.run.Search(c)` | Twitter search |
| `twint.run.Profile(c)` | A user's timeline (also selected with `-tl`) |
| `twint.run.Followers(c)` | A user's followers |
| `twint.run.Following(c)` | Who a user follows |
| `twint.run.Favorites(c)` | Tweets a user has liked |
| `twint.run.Lookup(c)` | User information |

### Pandas integration

When scraping, captured Tweets and users are also exposed as pandas DataFrames:

```python
c = twint.Config()
c.Username = "username"
c.Limit = 100
c.Pandas = True

twint.run.Search(c)

Tweets_df = twint.storage.panda.Tweets_df   # Tweets
Follow_df = twint.storage.panda.Follow_df   # followers / following
User_df = twint.storage.panda.User_df       # users
```

Use `c.Pandas_au = False` to disable automatic DataFrame population, `c.Pandas_clean = False` to keep existing data between runs, and `c.Pandas_type = "Pickle"` to store as Pickle instead of HDF5.

## Storage options

- **CSV / JSON** — `--csv` / `--json` write to the file given with `-o`.
- **SQLite** — `-db` creates a `tweets`, `users`, `followers`, and `following` table in the database file.
- **Pandas** — see the section above, or write a DataFrame file with `--store-pandas`.
- **Elasticsearch** — `-es` indexes Tweets, users, and follows into Elasticsearch. A how-to (including Kibana dashboards) is available in [`elasticsearch/README.md`](elasticsearch/README.md) and on the [Wiki](https://github.com/twintproject/twint/wiki/Elasticsearch).

## Scheduling

[automate.py](automate.py) shows how to combine `twint.Config` with the `schedule` library to run scraping jobs periodically (e.g. every hour).

## Debugging

- Set the environment variable `TWINT_DEBUG=debug` to write a debug log to `twint.log`.
- Pass `--debug` to store the last request in `twint-last-request.log`.

## Testing

`python test.py` runs the suite used by CI (Travis CI tests Python 3.6, 3.7, 3.8 and nightly). It performs search, timeline, follower, following, and favorites runs against a live account, exercising the vanilla, JSON, CSV, and SQLite output paths, then cleans up the generated files. An internet connection is required.

## Contributing

Issues and pull requests are welcome. Please follow the issue template (`.github/ISSUE_TEMPLATE.md`) when reporting bugs and include the exact command you ran, a description of the issue, and your environment details.

## Donation

If you appreciate TWINT, donations are accepted via [Patreon](https://www.patreon.com/twintproject) and [PayPal](https://paypal.me/noneprivacy) (see `.github/FUNDING.yml`).

## License

MIT — copyright (c) 2018 Cody Zacharias. See [LICENSE](LICENSE).
