# System Design Primer

A collection of study materials for learning system design and preparing for software engineering interviews. The repository combines written guides, design diagrams, Python examples, exercises, and study resources.

## What you’ll find here

- **System design fundamentals:** Concepts for reasoning about scalable, reliable systems and the trade-offs involved in designing them.
- **Worked design examples:** Diagrams and notes for systems such as Pastebin, a social network, a web crawler, a sales-rank service, and Twitter.
- **Scaling examples:** AWS-oriented diagrams illustrating possible system architectures and ways to scale them.
- **Python examples:** Small implementations and snippets, including MapReduce examples and object-oriented design exercises.
- **Study resources:** Anki decks, Jupyter notebooks, an EPUB-generation script, and diagrams in both image and editable Graffle formats.
- **Translations:** Some material is available in Simplified Chinese. See [`TRANSLATIONS.md`](TRANSLATIONS.md) for translation information.

## A suggested way to use the repository

1. **Start with the fundamentals.** Learn the vocabulary and building blocks used when discussing system design.
2. **Practice structured problem solving.** For each design exercise, clarify requirements, estimate scale, identify bottlenecks, and explain the trade-offs behind your choices.
3. **Study the examples.** Read an exercise’s notes and inspect its basic and full diagrams. Try to explain the design before looking at the provided solution.
4. **Use the code as a supplement.** Run or adapt the Python examples to explore particular algorithms and object-oriented designs. They are learning examples, not complete production services.
5. **Review and repeat.** Use the study decks and revisit designs with different assumptions, such as higher traffic, stricter availability needs, or lower latency targets.

## Repository contents

The file listing includes the following groups of materials. The exact paths depend on the repository’s directory structure; use the filenames to locate each group.

### System design examples

Several design folders include a `README.md`, diagrams, and sometimes Python snippets or MapReduce implementations:

- **Mint:** `mint.png`, `mint_basic.png`, `mint.graffle`, `mint_basic.graffle`, and `mint_mapreduce.py`
- **Pastebin:** `pastebin.png`, `pastebin_basic.png`, and corresponding Graffle diagrams, plus `pastebin.py`
- **Query cache:** `query_cache.png`, `query_cache_basic.png`, and corresponding Graffle diagrams, plus `query_cache_snippets.py`
- **Social graph:** `social_graph.png`, `social_graph_basic.png`, and corresponding Graffle diagrams, plus `social_graph_snippets.py`
- **Sales rank:** `sales_rank.png`, `sales_rank_basic.png`, and corresponding Graffle diagrams, plus `sales_rank_mapreduce.py`
- **Scaling on AWS:** `scaling_aws.png`, numbered scaling diagrams, and `scaling_aws.graffle`
- **Twitter:** `twitter.png`, `twitter_basic.png`, and corresponding Graffle diagrams
- **Web crawler:** `web_crawler.png`, `web_crawler_basic.png`, and corresponding Graffle diagrams, along with Python snippets and a MapReduce example

The `*_basic` diagrams provide a more introductory view of a design. The other diagrams and accompanying notes offer additional detail. Graffle files are editable diagram sources; PNG files are convenient for viewing.

### Object-oriented design exercises

The repository includes exercises and Python files for:

- Online chat
- Hash maps
- Deck of cards
- Call centers
- LRU caches
- Parking lots

Where available, `.ipynb` notebooks provide an interactive way to read or experiment with an exercise. The `.py` files provide the corresponding source code.

### Study and publishing resources

- `System Design.apkg`, `System Design Exercises.apkg`, and `OO Design.apkg` are Anki deck files.
- `study_guide.png` and `study_guide.graffle` provide a study-guide graphic and its editable source.
- `generate-epub.sh` is a shell script for generating an EPUB.
- `epub-metadata.yaml` contains EPUB metadata.
- Image files in the repository support the written material and diagrams.

## Working with the code

Python examples are intended to be read, run, and modified as learning exercises. Use Python 3 when working with them. For example, from the directory containing a script:

```bash
python3 pastebin.py
```

Some files define classes or functions rather than a standalone program, so they may need to be imported or explored in a Python shell instead of run directly.

To work with a notebook, start Jupyter in an environment where it is installed:

```bash
jupyter notebook
```

Then open the relevant `.ipynb` file. The notebooks and scripts are supplementary materials; the repository’s main focus is learning and practicing system design.

## Contributing and translations

Before making changes, read [`CONTRIBUTING.md`](CONTRIBUTING.md). For information about translated material, see [`TRANSLATIONS.md`](TRANSLATIONS.md) and the translated README files, including [`README-zh-Hans.md`](README-zh-Hans.md).

## License

See [`LICENSE.txt`](LICENSE.txt) for the license and terms that apply to this repository.
