# System Design Primer

## Overview

This repository is a study resource for learning how to design large-scale systems and for preparing for **system design interviews**. Designing scalable systems is often considered one of the most difficult parts of a technical interview, and this project addresses that in two main ways:

1. **An interactive study guide** (the main `README.md` in the repository root) that walks through core system design topics — such as load balancing, caching, sharding, replication, SQL and NoSQL trade-offs, asynchronous processing, and communication patterns — along with rough usage calculations ("back-of-the-envelope" math) and key latency numbers.
2. **A collection of worked solutions** to common system design and object-oriented design interview questions, each written up step-by-step with diagrams and, in many cases, reference Python code.

The repository also includes **Anki flash card decks** for spaced-repetition review and **translated versions** of the guide in multiple languages.

## Repository Structure

```
├── CONTRIBUTING.md             # How to contribute
├── TRANSLATIONS.md             # Status of translation efforts
├── LICENSE.txt                 # License text
├── epub-metadata.yaml          # Metadata for EPUB generation
├── generate-epub.sh            # Script to build an EPUB of the guide
├── images/                     # Diagrams and figures used in the guide
├── resources/
│   ├── flash_cards/            # Anki flash card decks (.apkg)
│   │   ├── OO Design.apkg
│   │   ├── System Design.apkg
│   │   └── System Design Exercises.apkg
│   ├── study_guide.png         # High-level study guide diagram
│   └── study_guide.graffle     # OmniGraffle source for the diagram
└── solutions/
    ├── object_oriented_design/ # OOD exercise solutions
    └── system_design/          # System design exercise solutions
```

## Study Guide and Flash Cards

The main study guide lives in the root `README.md`. It links to every relevant topic so you can jump directly to what you need while studying or reviewing. The companion `resources/study_guide.png` provides a one-page visual overview, and its source is available as an OmniGraffle file (`study_guide.graffle`) if you want to modify it.

For review and retention, three Anki decks are provided in `resources/flash_cards/`:

* **System Design** — core concepts and vocabulary
* **System Design Exercises** — practice prompts and solutions
* **OO Design** — object-oriented design fundamentals

Import the `.apkg` files directly into [Anki](https://apps.ankiweb.net/) to start reviewing.

## System Design Exercises and Solutions

Each system design exercise follows a consistent four-step framework:

1. **Outline use cases and constraints** — scope the problem and state assumptions.
2. **Create a high-level design** — identify the major components.
3. **Design core components** — dive into detail, including data schemas and APIs.
4. **Scale the design** — benchmark, profile, identify bottlenecks, and address them iteratively.

The exercises available under `solutions/system_design/` are:

* **Mint.com** (`mint/`) — personal finance: linking accounts, extracting and categorizing transactions, and budgeting. Includes a MapReduce implementation for spending analysis (`mint_mapreduce.py`) and code snippets (`mint_snippets.py`).
* **Pastebin** (`pastebin/`) — short text sharing with a focus on read-heavy traffic, storage, and scaling considerations (`pastebin.py`).
* **Query Cache** (`query_cache/`) — caching query results with a write-behind (write-back) pattern (`query_cache_snippets.py`).
* **Sales Rank** (`sales_rank/`) — Amazon-style sales ranking with a MapReduce solution (`sales_rank_mapreduce.py`).
* **Scaling AWS** (`scaling_aws/`) — iteratively scaling a system from a single instance to millions of users on AWS, with seven progression diagrams.
* **Social Graph** (`social_graph/`) — data structures for a social network, including a BFS shortest-path implementation and sharded person servers (`social_graph_snippets.py`).
* **Twitter timeline and search** (`twitter/`) — designing news feeds, fan-out to followers, and search with a Lucene-style cluster.
* **Web Crawler** (`web_crawler/`) — crawling at scale, with a MapReduce implementation (`web_crawler_mapreduce.py`) and code snippets (`web_crawler_snippets.py`).

Each exercise directory contains:

* `README.md` — the full English walkthrough
* `README-zh-Hans.md` — a Simplified Chinese translation
* `.graffle` and `.png` files — OmniGraffle sources and rendered architecture diagrams (a "basic" version and a scaled version where applicable)
* Python files with reference implementations where appropriate

A blank `template/` directory with a `.graffle` file is provided if you want to practice writing your own solution using the same structure.

## Object-Oriented Design Solutions

Under `solutions/object_oriented_design/` you will find Python solutions to classic OOD interview questions, each packaged as a Python module plus a Jupyter notebook you can open and execute interactively:

* **Call Center** (`call_center/`)
* **Deck of Cards** (`deck_of_cards/`)
* **Hash Table** (`hash_table/`, a hash map implementation)
* **LRU Cache** (`lru_cache/`)
* **Online Chat** (`online_chat/`)
* **Parking Lot** (`parking_lot/`)

## Setup

This repository is primarily documentation, so getting started is straightforward:

```bash
$ git clone https://github.com/donnemartin/system-design-primer.git
$ cd system-design-primer
```

Then browse the root `README.md` in your editor or on GitHub.

If you want to work with the Python solution files and Jupyter notebooks, install Python (3.x) and Jupyter:

```bash
$ pip install jupyter
$ jupyter notebook
```

To review the flash cards, install Anki and import the `.apkg` decks from `resources/flash_cards/`.

## Generating the EPUB

The guide can be compiled into an EPUB ebook using the included script:

```bash
$ ./generate-epub.sh
```

The script relies on `epub-metadata.yaml`, which holds the EPUB metadata (title, author, etc.). Inspect the script for its exact dependencies (such as a Pandoc installation) before running it.

## Usage Suggestions

* **Studying:** Read the root `README.md` end to end, then revisit topics using the links. Use the flash cards daily for retention.
* **Interview practice:** Pick an exercise from `solutions/system_design/`, read only its use cases and constraints, attempt the high-level design yourself on paper or a whiteboard, then compare against the provided solution and diagrams.
* **Notebooks:** Open the `.ipynb` files in Jupyter to read and execute the OOD implementations interactively.
* **Diagrams:** Open the `.png` files for rendered diagrams; open `.graffle` files in OmniGraffle if you want to edit them.

## Translations

The guide is maintained in English, and translations are tracked in `TRANSLATIONS.md`. As of this snapshot:

* **Live** (merged into `master`): Japanese, Simplified Chinese, Traditional Chinese
* **In progress:** Korean, Russian
* **Stalled** (help wanted): Arabic, Bengali, Brazilian Portuguese, French, German, Greek, Hebrew, Italian, Persian, Spanish, Thai, Turkish, Ukrainian, Vietnamese

Several system design solutions (Mint, Social Graph, Twitter, etc.) include `README-zh-Hans.md` Simplified Chinese versions alongside the English originals. If you would like to contribute a new translation, see the Contributing section below.

## Contributing

Contributions are welcome. Please read `CONTRIBUTING.md` before opening a pull request. The general workflow is:

1. Fork the main repository on GitHub.
2. Clone your fork locally:
   ```bash
   $ git clone git@github.com:YourLogin/system-design-primer.git
   $ cd system-design-primer
   ```
3. Create a feature branch (don't work directly on `master`):
   ```bash
   $ git checkout -b my-feature
   ```
4. Commit your changes:
   ```bash
   $ git add modified_files
   $ git commit
   ```
5. Push and open a pull request:
   ```bash
   $ git push -u origin my-feature
   ```

For **bug reports and feature requests**, submit an issue on GitHub. Pull requests are reviewed against the contributing guidelines; a pull request template is provided at `.github/PULL_REQUEST_TEMPLATE.md`.

### Translation contributions

* Make content changes to the English version first, then port them to translations.
* Changes to a single language should go directly to that language's file, one language per pull request.
* Prefix translation-related pull requests and issues with the language code (e.g., "es: Improve grammar").
* Tag the language maintainer (see `TRANSLATIONS.md`) for review; a review by a native speaker is required before merging.
* New translations should use standard IETF language tags (`fr`, `uk`, `zh-Hant`) as file suffixes (`README-xx.md`), and a translation should only be merged once it is complete and reviewed.

## Testing

This repository does not ship with a formal automated test suite. The primary way to verify the reference implementations is to run the Jupyter notebooks in `solutions/object_oriented_design/` and execute their cells interactively. The Python files accompanying each system design exercise are self-contained reference snippets intended for reading alongside the corresponding `README.md` walkthroughs rather than as an executable library.

## License

The license text for this project is provided in `LICENSE.txt`. Please refer to that file for the full terms governing use, modification, and redistribution of this repository's contents.
