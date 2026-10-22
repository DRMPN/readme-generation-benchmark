# twint-8vu9_od_

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)

**TWINT** — **TW**itter **INT**elligence Tool

An advanced Twitter scraping & OSINT tool written in Python that **doesn't use Twitter's API**, allowing you to scrape a user's followers, following, tweets, retweets, favorites, and more — while respecting Twitter's search limits.

---

## 📋 Table of Contents

- [Description](#-description)
- [Features](#-features)
- [Why Twint?](#-why-twint)
- [Installation](#-installation)
  - [From Source](#from-source)
  - [With pip](#with-pip)
  - [Docker](#docker)
- [Usage](#-usage)
  - [CLI Examples](#cli-examples)
  - [Module Examples](#module-examples)
- [Command Options](#-command-options)
- [Output Formats](#-output-formats)
  - [SQLite](#sqlite)
  - [Elasticsearch](#elasticsearch)
  - [Pandas](#pandas)
- [API Reference](#-api-reference)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📖 Description

Twint is a tool built with Python that allows you to scrape tweets from Twitter **without requiring the official Twitter API**. It leverages Twitter's search operators to scrape tweets from specific users, by hashtags, by geography, by language, and much more — all while remaining anonymous (no Twitter account or sign-in required).

## ✨ Features

- **Scrape tweets** from a user's timeline, search queries, hashtags, etc.
- **Scrape followers & following** of any public account
- **Scrape user info** (profile details, bio, stats)
- **No API key required** — no Twitter developer account needed
- **No rate limits** imposed by the API
- **Anonymous** — no login required
- **Date filtering** — tweets from/before/since specific dates (`--since`, `--until`)
- **Output flexibility:**
  - CSV
  - JSON
  - SQLite database
  - Elasticsearch
  - Pandas DataFrame
- **Favorites & media** scraping (tweets with images, videos)
- **Metadata output** (replies, retweets, favorites counts per tweet)
- **Geo-targeting** (nearby tweets by location/coordinates)
- **Automated** profile and tweet lookup via `automate.py`

## 🤔 Why Twint?

Twint is perfect for:

- **OSINT investigations** — researchers, journalists, investigators
- **Data analysis** — trend analysis, sentiment datasets
- **Academic research** — collecting tweet corpora
- **Marketing** — competitor and audience analysis

Traditional Twitter API scraping is limited to ~3200 tweets and only 7 days of search history. Twint bypasses these limitations — you can scrape **all historical tweets** from a target account.

## 🔧 Installation

### From Source

```bash
git clone https://github.com/twintproject/twint.git
cd twint
pip3 install . -r requirements.txt
```

### With pip

```bash
pip3 install twint
```

Or upgrade an existing installation:

```bash
pip3 install twint --upgrade
```

### Docker

Build the image from the included `Dockerfile`:

```bash
docker build -t twint .
```

Run a container:

```bash
docker run --rm -it twint -u username
```

**Requirements:** Python 3.6+ (tested on 3.6 – 3.8)

## 🚀 Usage

### CLI Examples

**Basic user timeline scrape:**
```bash
twint -u username
```

**Scrape tweets and save to CSV:**
```bash
twint -u username -o tweets.csv --csv
```

**Scrape tweets and save to JSON:**
```bash
twint -u username -o tweets.json --json
```

**Scrape tweets within a date range:**
```bash
twint -u username --since "2019-01-01 00:00:00" --until "2019-12-31 00:00:00"
```

**Scrape tweets mentioning a user:**
```bash
twint --username username --mention
```

**Scrape tweets by search term:**
```bash
twint -s "search term"
```

**Scrape tweets near a location:**
```bash
twint -u username --near "New York City"
```

**Scrape a user's followers:**
```bash
twint -u username --followers
```

**Scrape a user's following:**
```bash
twint -u username --following
```

**Scrape a user's favorites/likes:**
```bash
twint -u username --favorites
```

**Scrape tweets with geo-coordinates:**
```bash
twint --geo "48.8584,2.2945,1km"
```

**Limit results:**
```bash
twint -u username --limit 100
```

**Show only tweets with replies count:**
```bash
twint -u username --output tweets.json --json --min-faves 10
```

### Module Examples

Twint can also be used as a Python module.

**User timeline:**
```python
import twint

c = twint.Config()
c.Username = "username"
c.Store_object = True

twint.run.Search(c)
```

**Save tweets to a CSV file:**
```python
import twint

c = twint.Config()
c.Username = "username"
c.Output = "tweets.csv"
c.Store_csv = True

twint.run.Search(c)
```

**Scrape followers:**
```python
import twint

c = twint.Config()
c.Username = "username"
c.Followers = True
c.Output = "followers.csv"
c.Store_csv = True

twint.run.Followers(c)
```

**Scrape user profile info:**
```python
import twint

c = twint.Config()
c.Username = "username"
c.User_full = True

twint.run.Search(c)
```

**Pandas integration:**
```python
import twint
import pandas as pd

c = twint.Config()
c.Username = "username"
c.Pandas = True

twint.run.Search(c)

df = twint.storage.panda.Tweets_df
print(df.head())
```

## ⚙️ Command Options

| Option | Description |
|--------|-------------|
| `-u, --username` | Twitter username to scrape |
| `-s, --search` | Search terms / query |
| `-o, --output` | Output file path |
| `--csv` | Write output as CSV |
| `--json` | Write output as JSON |
| `--database` | Store output in SQLite database |
| `-es, --elasticsearch` | Write output to Elasticsearch |
| `--since` | Filter tweets sent after date (e.g. `2019-01-01 20:30:15`) |
| `--until` | Filter tweets sent before date |
| `--geo` | Geo search: `latitude,longitude,radius` |
| `--near` | Near a location (city or place) |
| `--limit` | Maximum number of tweets/results |
| `--followers` | Scrape followers of a user |
| `--following` | Scrape accounts a user follows |
| `--favorites` | Scrape a user's liked tweets |
| `--profile` | Scrape full user profile info |
| `--user-full` | Scrape detailed user information |
| `--verified` | Only scrape verified accounts |
| `--min-faves` | Minimum number of favorites |
| `--min-replies` | Minimum number of replies |
| `--min-retweets` | Minimum number of retweets |
| `--links` | Include or exclude tweets containing links (`include`/`exclude`) |
| `--media` | Tweets containing media |
| `--videos` | Tweets containing video |
| `--images` | Tweets containing images |
| `--replies` | Include replies in output |
| `--year` | Filter by year |
| `--month` | Filter by month |
| `--day` | Filter by day |
| `--followers-list` | Output followers list to file |
| `--translate` | Translate tweets |
| `--lang` | Tweet language filter |
| `--filter-reply` | Filter out reply tweets |
| `-pp, --pandas-pretty` | Pretty print Pandas output |

## 📦 Output Formats

### SQLite

```bash
twint -u username --database tweets.db
```

All tweets are stored in a structured SQLite table (`tweets`), and user data in a `users` table — queryable with any SQL client or Python's `sqlite3` module.

### Elasticsearch

```bash
twint -u username -es localhost:9200
```

Requires an Elasticsearch instance. Tweets are indexed into Elasticsearch for full-text search and Kibana dashboards.

### Pandas

```python
import twint

c = twint.Config()
c.Username = "username"
c.Pandas = True

twint.run.Search(c)
twint.storage.panda.Tweets_df        # Tweets DataFrame
twint.storage.panda.Followers_df     # Followers DataFrame
twint.storage.panda.Following_df     # Following DataFrame
twint.storage.panda.User_df          # User info DataFrame
```

## 🧩 API Reference

Twint exposes three main run functions:

- `twint.run.Search(c)` — search / scrape tweets
- `twint.run.Followers(c)` — scrape followers
- `twint.run.Following(c)` — scrape following

All configuration is done through the `twint.Config()` object:

```python
c = twint.Config()

# Core
c.Username = "username"
c.Search = "query"
c.Limit = 100

# Filters
c.Since = "2019-01-01"
c.Until = "2020-01-01"
c.Lang = "en"
c.Verified = True

# Output
c.Store_csv = True
c.Store_json = True
c.Output = "output.json"
c.Store_object = True
c.Database = "tweets.db"
c.Elasticsearch = "localhost:9200"
c.Pandas = True

# Callbacks
c.Custom = {"tweet": ["id", "date", "username"], "user": ["username"]}
c.Format = "custom output format: {date} - {username}: {tweet}"
```

**Custom callback example:**

```python
import twint

def callback(tweet):
    print(tweet.id, tweet.date, tweet.tweet)

c = twint.Config()
c.Username = "username"
c.Store_object = True
c.Store_object_tweets_list = False

twint.run.Search(c)
```

## 🧪 Testing

Run the test suite included in `test.py`:

```bash
python test.py
```

Tests cover core functionality including tweet searching, follower scraping, date locking (`datelock.py`), and output formatting (`format.py`).

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -am 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is intended for educational and research purposes. Use responsibly and in accordance with Twitter's Terms of Service. The authors are not responsible for any misuse of this tool.
