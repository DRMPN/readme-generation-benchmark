# TWINT

TWINT is an advanced Twitter scraping and OSINT tool, packaged as a Python application with a `twint` command-line entry point. It can search for tweets, collect a user’s timeline, look up user information, and retrieve followers, following accounts, or liked tweets. Results can be printed or stored in files and supported data stores.

This repository identifies the package version as **2.1.21**. Its code makes requests to Twitter endpoints, parses returned data, and includes retry and rate-limit handling. Availability and completeness of results depend on the external service and its responses.

## Capabilities

The command-line interface and Python configuration support:

- Searching tweets by phrase, username, date range, language, location, or other filters.
- Collecting a user’s timeline, followers, following accounts, and liked tweets.
- Filtering searches by media, replies, verification status, links, source, minimum engagement counts, and other criteria.
- Outputting results as text, CSV, or JSON, with optional custom tweet or user formats.
- Saving data to SQLite or Elasticsearch, or collecting it in Pandas DataFrames.
- Using an HTTP, SOCKS4, SOCKS5, or Tor proxy.
- Optionally translating tweets through the included translation integration.

## Requirements and installation

The package requires **Python 3.6 or newer**. `setup.py` declares dependencies including `aiohttp`, `aiodns`, `beautifulsoup4`, `cchardet`, `dataclasses`, `elasticsearch`, `pysocks`, `pandas`, `aiohttp_socks`, `schedule`, `geopy`, `fake-useragent`, and `googletransx`.

Install from a local checkout:

```bash
python3 -m pip install .
```

For development, install the checkout in editable mode:

```bash
python3 -m pip install -e .
```

The package also provides a Dockerfile based on `python:3.6-buster`. It clones the project and installs it with `pip3 install . -r requirements.txt`, then starts a Bash shell. The Dockerfile refers to a `requirements.txt` file that is not present in the supplied repository tree; check that the file is available before using that build command.

## Command-line usage

After installation, run the program with `twint`. The CLI accepts a username, search phrase, geolocation, or nearby city as common search inputs. For example:

```bash
twint -s "example phrase" --since 2020-01-01 --until 2020-01-31
twint -u exampleuser --limit 100
twint -s "example phrase" --lang en --verified
twint -u exampleuser --followers
```

Save results as CSV or JSON by providing both an output path and the corresponding format flag:

```bash
twint -s "example phrase" --csv -o results.csv
twint -u exampleuser --json -o results.json
```

Other CLI options include `--timeline`, `--following`, `--favorites`, `--user-full`, `--userid`, `--count`, and `--stats`. Search filters include `--images`, `--videos`, `--media`, `--replies`, `--min-likes`, `--min-retweets`, `--min-replies`, `--links`, `--source`, and `--filter-retweets`. Use `twint --help` to inspect the argument parser’s available options and descriptions.

Some options have constraints enforced by the CLI. For example, `--verified` is intended for search, `--timeline` requires a username, and CSV or JSON output requires `-o`. The CLI also rejects non-positive `--backoff-exponent` values and negative `--min-wait-time` values.

## Python usage

The package exposes `twint.Config` and functions in `twint.run`. Configure a `Config` instance, then call the appropriate run function:

```python
import twint

config = twint.Config()
config.Search = "example phrase"
config.Since = "2020-01-01"
config.Until = "2020-01-31"
config.Limit = 100

twint.run.Search(config)
```

Use `twint.run.Profile(config)` for a user timeline, `Followers` or `Following` for account relationships, `Favorites` for liked tweets, and `Lookup` for user details. The `automate.py` file demonstrates scheduled jobs that configure searches and write CSV output; its example values such as usernames, search terms, and filenames are placeholders.

## Configuration and output

The CLI maps its options to attributes on `twint.Config`. In Python, set the corresponding attributes directly. Search and date attributes include `Search`, `Username`, `User_id`, `Geo`, `Near`, `Lang`, `Year`, `Since`, and `Until`. `Limit` caps the number of collected items. `To` and `All` add user-related search criteria, while `Custom_query` supplies a custom search query.

Output settings include `Output`, `Store_csv`, `Store_json`, and `Tabs`. CSV and JSON output use the path in `Output`; custom formats can be supplied through `Format`. The formatter recognizes tweet fields such as `{id}`, `{date}`, `{time}`, `{username}`, `{tweet}`, `{hashtags}`, `{likes}`, `{retweets}`, `{replies}`, and `{link}`. User formatting supports fields including `{id}`, `{name}`, `{username}`, `{bio}`, `{followers}`, and `{verified}`. `Show_hashtags`, `Show_cashtags`, and `Stats` control additional text output.

For persistence, set `Database` to a SQLite database path or `Elasticsearch` to an Elasticsearch connection value. Elasticsearch index names can be customized with `Index_tweets`, `Index_follow`, and `Index_users`; `Essid` identifies a scraping session. The code also supports Pandas storage through its storage module and configuration attributes such as `Pandas`, `Pandas_type`, and `Pandas_clean`.

Proxy configuration uses `Proxy_host`, `Proxy_port`, and `Proxy_type`; supported types in the request code are HTTP, SOCKS4, and SOCKS5. Setting the host to `tor` selects a local Tor proxy connection. Tor control options include `Tor_control_port` and `Tor_control_password`. Retry behavior can be adjusted with `Backoff_exponent` and `Min_wait_time`. `Debug` enables request and response diagnostic files; setting the environment variable `TWINT_DEBUG=debug` enables package logging to `twint.log`.

## Development

The project is organized as the `twint` Python package. Core modules cover command-line parsing, configuration, request construction, feed parsing, tweet and user models, output formatting, and execution. Storage backends are under `twint/storage/`.

The Travis configuration lists Python 3.6, 3.7, 3.8, and nightly; Python 3.8 and nightly are marked as allowed failures. Its install step uses `pip install -r requirements.txt`, so—as with the Dockerfile—verify that the referenced requirements file is available in your checkout.

## Testing

Run the repository’s test script with:

```bash
python test.py
```

The script exercises profile, search, following, followers, and favorites flows with regular, JSON, CSV, and SQLite output configurations. It uses a configured username and performs requests through the normal scraping code, so it is not a network-independent unit-test suite. It also removes the generated `test_twint.db`, `test_twint.json`, and `test_twint.csv` files when it reaches the cleanup step.

## License

This project is distributed under the **MIT License**. See [`LICENSE`](LICENSE) for the complete terms.
