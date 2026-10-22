# System Design Primer

This repository is a study collection for system design and object-oriented design interview preparation. It contains worked design solutions for common interview questions, Python solution code for object-oriented design exercises, Anki flash card decks, and tooling for generating an EPUB book from the Markdown content.

## Contents

- [Repository layout](#repository-layout)
- [System design solutions](#system-design-solutions)
- [Object-oriented design solutions](#object-oriented-design-solutions)
- [Study resources](#study-resources)
- [Generating an EPUB](#generating-an-epub)
- [Translations](#translations)
- [Contributing](#contributing)
- [License](#license)
- [Known gaps in this snapshot](#known-gaps-in-this-snapshot)

## Repository layout

| Path | Description |
| --- | --- |
| `solutions/system_design/` | Markdown walkthroughs for system design questions, with supporting diagrams and some Python snippets. |
| `solutions/object_oriented_design/` | Python modules and Jupyter notebooks for object-oriented design exercises. |
| `images/` | Images referenced by the content. |
| `resources/` | Study guide artwork and Anki flash card decks. |
| `generate-epub.sh` | Script that builds EPUB files with Pandoc. |
| `epub-metadata.yaml` | Metadata used by the EPUB build (title "System Design Primer", author Donne Martin, date 2018). |
| `CONTRIBUTING.md` | Guidelines for bug reports, pull requests, and translations. |
| `TRANSLATIONS.md` | Translation status and maintainers by language. |
| `LICENSE.txt` | License information. |
| `.github/PULL_REQUEST_TEMPLATE.md` | Pull request checklist template. |

## System design solutions

Each walkthrough follows the same structure: outline use cases and constraints, create a high-level design, design core components, and then scale the design. Each one links to general topics rather than repeating them.

| Question | Location |
| --- | --- |
| Design a web crawler | `solutions/system_design/web_crawler/` |
| Design the Twitter timeline and search | `solutions/system_design/twitter/` |
| Design a key-value cache for recent web server query results | `solutions/system_design/query_cache/` |
| Design Mint.com | `solutions/system_design/mint/` |
| Design Pastebin.com (or Bit.ly) | `solutions/system_design/pastebin/` |
| Design the data structures for a social network | `solutions/system_design/social_graph/` |
| Design Amazon's sales rank by category feature | `solutions/system_design/sales_rank/` |
| Design a system that scales to millions of users on AWS | `solutions/system_design/scaling_aws/` |

Several of these directories include:

- `README.md`, the English walkthrough.
- `README-zh-Hans.md`, a Simplified Chinese version (present for most, but not all, questions).
- `.graffle` and `.png` files, the diagram sources and exported images.
- Python files with code fragments, such as `*_snippets.py`, and some MapReduce job examples, such as `mint/mint_mapreduce.py` and `sales_rank/sales_rank_mapreduce.py`.
- `__init__.py` files.

The `solutions/system_design/template/` directory contains a diagram template.

## Object-oriented design solutions

Each exercise lives in its own directory under `solutions/object_oriented_design/` and provides a Python module (`<name>.py`), a Jupyter notebook (`<name>.ipynb`), and an `__init__.py` file.

| Exercise | Directory |
| --- | --- |
| Call center | `call_center/` |
| Deck of cards | `deck_of_cards/` |
| Hash table | `hash_table/` (module `hash_map.py`) |
| LRU cache | `lru_cache/` |
| Online chat | `online_chat/` |
| Parking lot | `parking_lot/` |

Some of these files are incomplete. For example, `lru_cache/lru_cache.py` contains several methods that are only `pass`, so it should be treated as a skeleton rather than a finished implementation.

## Study resources

- `resources/flash_cards/` contains three Anki decks: `System Design.apkg`, `System Design Exercises.apkg`, and `OO Design.apkg`. Import them with [Anki](https://apps.ankiweb.net/).
- `resources/study_guide.png` and `resources/study_guide.graffle` contain the study guide artwork and its editable source.

## Generating an EPUB

`generate-epub.sh` uses [Pandoc](https://pandoc.org/) to build EPUB files. The script checks that `pandoc` is installed and exits if it is not.

The script expects these inputs in the repository root:

- `README.md`, the main content
- `README-ja.md`, `README-zh-Hans.md`, and `README-zh-TW.md`, for the translated books

It also appends the `README.md` file from each directory under `solutions/system_design/` (skipping `template` directories) to produce `README.epub`.

```bash
./generate-epub.sh
```

Note that the root-level Markdown files the script reads are not included in this snapshot (see [Known gaps](#known-gaps-in-this-snapshot)), so the script will not run successfully until they are added.

## Translations

TRANSLATIONS.md tracks translations and their maintainers, grouped as Live, In Progress, and Stalled. It lists Japanese, Simplified Chinese, and Traditional Chinese as live, and Korean and Russian as in progress. The other listed languages are marked as stalled and looking for maintainers.

## Contributing

Bug reports and feature requests go in the GitHub issue tracker. Pull requests should be made from a fork. Translation pull requests should change one language at a time, and the title should be prefixed with the language code (for example, `ja: Fix ...`). See [CONTRIBUTING.md](CONTRIBUTING.md) for the full process.

## License

See [LICENSE.txt](LICENSE.txt). The file states the copyright as 2017 Donne Martin and names the Creative Commons Attribution 4.0 International License (CC BY 4.0).

## Known gaps in this snapshot

- The main `README.md` content (the topic index that the solution pages link to with `#index-of-system-design-topics` and similar anchors) is not present in this repository. The links in the solution walkthroughs therefore point to sections that cannot be checked here.
- The root translation files referenced by `TRANSLATIONS.md` and `generate-epub.sh` (`README-ja.md`, `README-zh-Hans.md`, `README-zh-TW.md`) are not present.
- No automated tests, dependency manifest (such as `requirements.txt`), or CI configuration exist in this repository, so there is no documented way to run the Python code beyond importing the modules.
