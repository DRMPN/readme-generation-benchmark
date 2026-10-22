# twint-ucyvyzc1

> **Note:** This README was written from the repository's file listing alone, without access to the source code. Descriptions of behavior, options, and features are based on the file names and on the upstream [twint](https://github.com/twintproject/twint) project, which this layout resembles. Verify the details against the code and run `twint --help` before relying on them.

## Overview

**twint-ucyvyzc1** is a Python package and command-line tool for scraping Twitter data without using the official Twitter API. It can collect tweets and user profiles, search by keyword, hashtag, or location, and export results to several formats and storage backends, including CSV, JSON, SQLite, Elasticsearch, and pandas DataFrames.

The repository is laid out as a standard Python package with a CLI entry point, a configuration object for programmatic use, separate storage backends, and a test suite.

## Features

- **Tweet scraping** by username, keyword search, hashtag, or geographic area
- **User profile collection**, including followers, following, and favorites
- **Date filtering** with `since` and `until` bounds
- **Result limits** to cap how many tweets or users are fetched
- **Multiple output formats**: plain text, CSV, JSON
- **Storage backends**: SQLite database, Elasticsearch, and pandas DataFrames
- **Command-line interface** for quick, scriptable queries
- **Python library API** for embedding scraping into applications and pipelines
- **Proxy support** for routing requests through a proxy host and port
- **Docker support** for running the tool in a containerized environment
- **Automation module** for running scheduled or repeated jobs

## Project Structure

```
twint-ucyvyzc1/
├── twint/                    # Main package
│   ├── __init__.py           # Package exports
│   ├── __version__.py        # Version string
│   ├── cli.py                # Command-line argument parsing
│   ├── config.py             # Configuration object used by all searches
│   ├── run.py                # Entry points that start a search or lookup
│   ├── get.py                # HTTP requests and response retrieval
│   ├── feed.py               # Parsing of timeline and feed responses
│   ├── tweet.py              # Tweet data model
│   ├── user.py               # User data model
│   ├── url.py                # URL construction for Twitter endpoints
│   ├── token.py              # Guest token handling
│   ├── datelock.py           # Date range handling for since/until
│   ├── output.py             # Console and file output formatting
│   ├── format.py             # Output formatting helpers
│   ├── verbose.py            # Logging and verbosity control
│   ├── automate.py           # Scheduled and repeated task support
│   ├── storage/              # Storage backends
│   │   ├── __init__.py
│   │   ├── write.py          # File writers (CSV, JSON, text)
│   │   ├── write_meta.py     # Metadata writers
│   │   ├── db.py             # SQLite storage
│   │   ├── elasticsearch.py  # Elasticsearch storage
│   │   └── panda.py          # pandas DataFrame storage
├── test.py                   # Test suite
├── setup.py                  # Packaging and installation script
├── MANIFEST.in               # Extra files to include in source distributions
├── Dockerfile                # Container build definition
├── LICENSE
└── README.md
```

The module layout above is inferred from the file names. Some file names, such as `__init__.py`, appear more than once, so the exact placement of each file should be confirmed in the repository.

## Requirements

- Python 3.6 or later (confirm the minimum version in `setup.py`)
- Network access to Twitter's public web endpoints
- Optional: an Elasticsearch instance, if you use the Elasticsearch backend
- Optional: Docker, if you use the container image

Python dependencies are listed in `setup.py`. Typical dependencies for a tool like this include `aiohttp`, `aiodns`, `beautifulsoup4`, `fake-useragent`, `schedule`, `pandas`, and `elasticsearch`.

## Installation

### From PyPI

```bash
pip install twint
```

### From source

```bash
git clone https://github.com/<your-account>/twint-ucyvyzc1.git
cd twint-ucyvyzc1
pip install .
```

For development, install in editable mode:

```bash
pip install -e .
```

### With Docker

Build the image:

```bash
docker build -t twint-ucyvyzc1 .
```

Run a command in the container:

```bash
docker run --rm twint-ucyvyzc1 -u jack --limit 20
```

To keep output on the host, mount a directory:

```bash
docker run --rm -v "$(pwd)/output:/app/output" twint-ucyvyzc1 -s "python" -o /app/output/python.csv --csv
```

## Usage

### Command line

Run `twint --help` for the full list of options. Common examples:

**Fetch tweets from a user:**

```bash
twint -u elonmusk --limit 50
```

**Search for a keyword within a date range:**

```bash
twint -s "climate change" --since "2023-01-01" --until "2023-06-30" --limit 200
```

**Save results to CSV:**

```bash
twint -u nasa --csv -o nasa_tweets.csv
```

**Save results to JSON:**

```bash
twint -s "open source" --json -o results.json
```

**Store results in a SQLite database:**

```bash
twint -s "machine learning" --database ml.db
```

**Send results to Elasticsearch:**

```bash
twint -s "python" --elasticsearch localhost:9200
```

**Fetch a user's followers or following list:**

```bash
twint -u username --followers
twint -u username --following
```

**Hide console output while saving to a file:**

```bash
twint -s "news" --csv -o news.csv --hide-output
```

### Python library

Import the package and configure a search with the `Config` object:

```python
import twint

c = twint.Config()
c.Username = "nasa"
c.Limit = 20
c.Store_csv = True
c.Output = "nasa_tweets.csv"

twint.run.Search(c)
```

**Keyword search with a date range:**

```python
import twint

c = twint.Config()
c.Search = "data science"
c.Since = "2023-01-01"
c.Until = "2023-03-31"
c.Limit = 500
c.Store_json = True
c.Output = "data_science.json"

twint.run.Search(c)
```

**Load results into a pandas DataFrame:**

```python
import twint

c = twint.Config()
c.Search = "python"
c.Limit = 100
c.Pandas = True

twint.run.Search(c)
df = twint.storage.panda.Tweets_df
print(df.head())
```

**Store results in SQLite from Python:**

```python
import twint

c = twint.Config()
c.Username = "github"
c.Database = "github.db"

twint.run.Search(c)
```

### Configuration options

The `Config` object controls every search. Commonly used attributes include:

| Attribute | Purpose |
|---|---|
| `Username` | Scrape tweets from a specific user |
| `Search` | Keyword or hashtag query |
| `Since` / `Until` | Date bounds, in `YYYY-MM-DD` format |
| `Limit` | Maximum number of results to fetch |
| `Store_csv` | Write results to CSV |
| `Store_json` | Write results to JSON |
| `Output` | Path of the output file |
| `Database` | Path of the SQLite database |
| `Elasticsearch` | Elasticsearch host and port |
| `Pandas` | Keep results in a pandas DataFrame |
| `Lang` | Restrict results to a language code |
| `Near` / `Geo` | Restrict by location |
| `Proxy_host` / `Proxy_port` | Route requests through a proxy |
| `Hide_output` | Suppress console output |
| `Format` | Custom output format string |

Check `twint/config.py` for the full list and default values.

## Output

Depending on the options you choose, results are written as:

- **Console text**: one tweet or user per line, unless `Hide_output` is set
- **CSV**: one row per tweet or user, with a header row
- **JSON**: one object per line, or a JSON array depending on the writer
- **SQLite**: tables created and populated automatically in the database file
- **Elasticsearch**: documents indexed into the configured index
- **pandas DataFrame**: available in memory after the search completes

Each tweet record generally includes the tweet ID, text, author, timestamp, and engagement counts such as likes, retweets, and replies. User records include profile fields such as bio, location, follower count, and following count.

## Testing

The test suite lives in `test.py`. Run it with:

```bash
python -m unittest test
```

or with pytest, if installed:

```bash
pytest test.py
```

Some tests access live Twitter endpoints, so they need network access and may fail if Twitter changes its responses or rate limits the connection.

## Troubleshooting

- **Empty results or errors**: Twitter frequently changes its web endpoints and guest token behavior. Update to the latest version of this package and check the issue tracker.
- **Rate limiting**: Reduce `Limit`, add pauses between runs, or use a proxy.
- **Elasticsearch connection errors**: Confirm the host and port are reachable and that the cluster version is compatible with the installed client library.
- **Date parsing errors**: Dates must use `YYYY-MM-DD` format.
- **Docker permission errors on output files**: Make sure the mounted output directory is writable by the container user.

## Limitations and Legal Notice

This tool scrapes publicly accessible web pages and is not affiliated with or endorsed by Twitter or X Corp. Scraping may violate the platform's terms of service. Responsible use includes:

- Respecting rate limits and avoiding excessive request volume
- Complying with applicable data protection laws, such as GDPR, when collecting or storing personal data
- Not using collected data for harassment, spam, or unauthorized profiling

Because the tool depends on undocumented web endpoints, it may stop working without notice.

## Contributing

1. Fork the repository and create a feature branch.
2. Make your changes and add tests to `test.py` where practical.
3. Run the test suite before opening a pull request.
4. Describe the change clearly in the pull request, including any new options or output formats.

Bug reports and feature requests are welcome in the issue tracker.

## License

This project is distributed under the license in the `LICENSE` file. Check that file for the terms that apply.

## Acknowledgments

This project builds on the [twint](https://github.com/twintproject/twint) project and the open-source libraries it depends on.
