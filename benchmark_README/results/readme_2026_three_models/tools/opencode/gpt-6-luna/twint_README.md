# TWINT

TWINT (Twitter Intelligence Tool) is a Python command-line program and library for scraping Twitter data. It can search tweets, collect a user's timeline, inspect user profiles, and collect follower/following lists or liked tweets. Results can be printed, written to files, or sent to supported storage backends.

This repository contains version **2.1.21**. The project describes itself as an advanced Twitter scraping and OSINT tool.

## Capabilities

- Search tweets by query, or collect a user's timeline.
- Filter searches by dates, language, location, verified status, media, engagement counts, and other criteria.
- Look up user information and collect followers, following, or liked tweets.
- Write tweet and user results as CSV or JSON, store data in SQLite, or index data in Elasticsearch.
- Use the Python API with a `twint.Config` object and the functions in `twint.run`.

The available data and results depend on what the service returns to the scraper. This project is not a guarantee of complete or uninterrupted data collection; endpoints and access limits can change.

## Requirements

The package metadata declares **Python 3.6 or later**. Installation also installs the dependencies declared in `setup.py`:

`aiohttp`, `aiodns`, `beautifulsoup4`, `cchardet`, `dataclasses`, `elasticsearch`, `pysocks`, `pandas`, `aiohttp_socks`, `schedule`, `geopy`, `fake-useragent`, and `googletransx`.

## Installation

From a clone or source directory of this repository, run:

```bash
python -m pip install .
```

The package installs a `twint` command. To see the command's available options:

```bash
twint --help
```

## Command-line examples

Search for tweets containing a phrase, limit the number of results, and write them to CSV:

```bash
twint --search "climate change" --limit 100 --csv --output tweets.csv
```

Search within a date range and write JSON lines to a file:

```bash
twint --search "climate change" --since 2020-01-01 --until 2020-02-01 --json --output tweets.json
```

Collect a user's timeline:

```bash
twint --username example --timeline --limit 100
```

Collect followers or accounts a user follows:

```bash
twint --username example --followers
twint --username example --following
```

To collect liked tweets, use `--favorites` with a username:

```bash
twint --username example --favorites
```

Unless a file output option is selected, results are printed to the terminal. For CSV or JSON output, provide both the format option and `--output` with a destination path. `--tabs` selects tab-separated fields for CSV output.

### Common options

| Option | Purpose |
| --- | --- |
| `-s`, `--search` | Search for tweets containing a word or phrase. |
| `-u`, `--username` | Select a user for timeline, profile, or related collection modes. |
| `--timeline` | Collect a user's timeline; use with `--username`. |
| `--userid` | Select a user by ID. |
| `-g`, `--geo`; `--near` | Search using geolocation criteria. |
| `--since`, `--until`, `--year` | Apply date or year limits. |
| `-l`, `--lang` | Select a language. |
| `--followers`, `--following`, `--favorites` | Collect a user's followers, following, or liked tweets. |
| `--limit` | Set a result limit. |
| `--csv`, `--json`, `--output` | Select file format and destination. |
| `-db`, `--database` | Store results in a SQLite database file. |
| `-es`, `--elasticsearch` | Configure Elasticsearch output. Index names can be set with `--index-tweets`, `--index-follow`, and `--index-users`. |
| `--images`, `--videos`, `--media` | Filter for tweets with the corresponding media. |
| `--min-likes`, `--min-retweets`, `--min-replies` | Set minimum engagement counts. |
| `--retweets`, `--filter-retweets`, `--native-retweets` | Control retweet collection/filtering. |
| `--resume` | Resume using a file containing a tweet ID. |

Run `twint --help` for the complete option list, including proxy, translation, output formatting, and search-specific options.

## Python API

Create a configuration, set the fields you need, and pass it to a function in `twint.run`:

```python
import twint

config = twint.Config()
config.Search = "climate change"
config.Since = "2020-01-01"
config.Until = "2020-02-01"
config.Limit = 100

twint.run.Search(config)
```

The principal run functions are `Search`, `Profile`, `Lookup`, `Followers`, `Following`, and `Favorites`. The corresponding configuration uses fields such as `Search`, `Username`, `User_id`, `Since`, `Until`, and `Limit`. Output and storage can be configured with fields including `Output`, `Store_csv`, `Store_json`, `Database`, and `Elasticsearch`.

For example, to write search results to CSV through the API:

```python
config = twint.Config()
config.Search = "climate change"
config.Store_csv = True
config.Output = "tweets.csv"
twint.run.Search(config)
```

For more detail on the configuration and custom output formats, consult the source in `twint/config.py` and `twint/cli.py`.

## Storage notes

- **CSV and JSON:** enable `Store_csv` or `Store_json` and set `Output` (or use the corresponding CLI options). CSV output supports tab separators via `--tabs`.
- **SQLite:** set `Database` in the API or pass a filename with `--database`. The implementation creates its tables when opening the database.
- **Elasticsearch:** configure the Elasticsearch connection with `Elasticsearch` in the API or `--elasticsearch` on the CLI. The default index names are `twinttweets`, `twintgraph`, and `twintuser`; the CLI provides options to override them.

## License

This project is distributed under the MIT License; see [LICENSE](LICENSE).
