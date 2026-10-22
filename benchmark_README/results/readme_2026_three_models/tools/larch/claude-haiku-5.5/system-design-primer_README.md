# System Design Primer (incimybi)

This repository is a study collection for system design and object-oriented (OO) design interviews. It bundles written guides, architecture diagrams, Python code snippets, runnable OO design solutions, and Anki flashcard decks. It appears to be a copy of the community-maintained [System Design Primer](https://github.com/donnemartin/system-design-primer) project.

> **Note on structure:** The file listing for this copy is flat, so the folder layout below is inferred from file names (for example, `mint_snippets.py` alongside `mint.png` and `mint.graffle`). Check the actual directory tree before relying on exact paths.

---

## Table of Contents

- [Purpose](#purpose)
- [Repository Contents](#repository-contents)
- [Repository Structure](#repository-structure)
- [Learning Path](#learning-path)
- [System Design Topics](#system-design-topics)
- [System Design Exercises](#system-design-exercises)
- [Object-Oriented Design Exercises](#object-oriented-design-exercises)
- [Anki Flashcard Decks](#anki-flashcard-decks)
- [Diagrams and Source Files](#diagrams-and-source-files)
- [Python Code Snippets and Solutions](#python-code-snippets-and-solutions)
- [Building an EPUB](#building-an-epub)
- [Translations](#translations)
- [Contributing](#contributing)
- [License](#license)

---

## Purpose

Large-scale system design interviews test your ability to:

- Clarify ambiguous requirements and define scope.
- Estimate traffic, storage, and bandwidth.
- Choose appropriate data stores, caches, and queues.
- Reason about trade-offs such as consistency versus availability and latency versus throughput.
- Communicate a design clearly with diagrams and rationale.

This repository supplies background reading, worked examples, and practice material for each of these skills.

---

## Repository Contents

| Category | What it contains |
|---|---|
| Core guides | `README.md` and `README-zh-Hans.md` with the main system design and OO design material |
| Exercise folders | One folder per system design problem (Pastebin, Twitter, Web Crawler, Mint, and others), each with a README, diagrams, and snippets |
| OO design folders | Solutions for hash map, LRU cache, parking lot, deck of cards, call center, and online chat |
| Diagrams | `.png` images for rendered diagrams and `.graffle` OmniGraffle source files for editing them |
| Flashcards | Three Anki decks (`.apkg`) for system design, exercises, and OO design |
| Study aids | `study_guide.graffle` and `study_guide.png` |
| Publishing tools | `generate-epub.sh` and `epub-metadata.yaml` for producing an EPUB version of the guide |
| Project docs | `CONTRIBUTING.md`, `TRANSLATIONS.md`, `LICENSE.txt` |

---

## Repository Structure

The layout below is inferred from the file listing:

```
system-design-primer-incimybi/
├── README.md                     # Main guide (English)
├── README-zh-Hans.md             # Main guide (Simplified Chinese)
├── CONTRIBUTING.md
├── TRANSLATIONS.md
├── LICENSE.txt
├── epub-metadata.yaml
├── generate-epub.sh
├── study_guide.graffle / .png
├── System Design.apkg
├── System Design Exercises.apkg
├── OO Design.apkg
├── <many image files>.png/.jpg   # Images referenced by the guides and flashcards
│
├── mint/                         # Design Mint.com
│   ├── README.md / README-zh-Hans.md
│   ├── mint_snippets.py
│   ├── mint_mapreduce.py
│   ├── mint.graffle / mint.png
│   └── mint_basic.graffle / mint_basic.png
│
├── pastebin/                     # Design Pastebin.com
│   ├── README.md / README-zh-Hans.md
│   ├── pastebin.py
│   ├── pastebin.graffle / pastebin.png
│   └── pastebin_basic.graffle / pastebin_basic.png
│
├── query_cache/                  # Design a key-value cache for query results
│   ├── README.md / README-zh-Hans.md
│   ├── query_cache_snippets.py
│   └── query_cache.graffle / query_cache.png (+ basic variants)
│
├── social_graph/                 # Design a social graph
│   ├── README.md / README-zh-Hans.md
│   ├── social_graph_snippets.py
│   └── social_graph.graffle / social_graph.png (+ basic variants)
│
├── sales_rank/                   # Design Amazon's sales rank by category
│   ├── README.md / README-zh-Hans.md
│   ├── sales_rank_mapreduce.py
│   └── sales_rank.graffle / sales_rank.png (+ basic variants)
│
├── scaling_aws/                  # Design AWS-style autoscaling
│   ├── README.md / README-zh-Hans.md
│   ├── scaling_aws.graffle / scaling_aws.png
│   └── scaling_aws_1.png … scaling_aws_7.png
│
├── twitter/                      # Design the Twitter timeline and search
│   ├── README.md / README-zh-Hans.md
│   └── twitter.graffle / twitter.png (+ basic variants)
│
├── web_crawler/                  # Design a web crawler
│   ├── README.md / README-zh-Hans.md
│   ├── web_crawler_snippets.py
│   ├── web_crawler_mapreduce.py
│   └── web_crawler.graffle / web_crawler.png (+ basic variants)
│
└── OO design solutions (each a Python package with __init__.py)
    ├── hash_map/        hash_map.py,     hash_map.ipynb
    ├── lru_cache/       lru_cache.py,    lru_cache.ipynb
    ├── parking_lot/     parking_lot.py,  parking_lot.ipynb
    ├── deck_of_cards/   deck_of_cards.py, deck_of_cards.ipynb
    ├── call_center/     call_center.py,  call_center.ipynb
    └── online_chat/     online_chat.py,  online_chat.ipynb
```

Each system design exercise folder follows a consistent pattern: a Markdown write-up, a Chinese translation, diagram sources, rendered images, and optional Python code.

---

## Learning Path

A suggested order for working through the material:

1. **Read the core guide.** Start with *How to approach a system design interview question* and the *System design topics* section in `README.md`.
2. **Study the building blocks.** Focus on scalability, caching, load balancing, databases, and asynchronous processing.
3. **Work through the exercises.** Begin with a basic one such as Pastebin or Web Crawler, then try Twitter, Social Graph, or AWS autoscaling.
4. **Practice OO design.** Implement the classes in the OO design folders, starting with LRU Cache and Hash Map, then Parking Lot and Deck of Cards.
5. **Review with flashcards.** Import the Anki decks to reinforce key numbers and concepts.
6. **Practice out loud.** Sketch the diagrams from memory and explain your trade-offs.

---

## System Design Topics

The core guide covers the following topics.

### Foundations

- **Performance vs. scalability.** Vertical scaling (bigger machines) versus horizontal scaling (more machines).
- **Latency vs. throughput.** Response time for one request versus requests handled per unit of time.
- **Availability vs. consistency.** Trade-offs under network partitions, as described by the **CAP theorem**.
- **Consistency patterns.** Weak, eventual, and strong consistency.
- **Availability patterns.** Fail-over and replication.

### Building Blocks

- **Domain Name System (DNS).** Name resolution and its latency impact.
- **Content Delivery Network (CDN).** Serving static assets from edge locations.
- **Load balancers.** Distributing traffic across servers, with layer 4 and layer 7 options.
- **Reverse proxies.** Caching, compression, and TLS termination at the edge.
- **Application layer.** Separating web servers from application logic, and microservices.
- **Service discovery.** Locating services in a dynamic environment.

### Data

- **Relational databases (RDBMS).** ACID properties, master-slave and master-master replication, and federation, sharding, and denormalization.
- **NoSQL.** Key-value, wide-column, document, and graph stores, and when each fits.
- **SQL vs. NoSQL.** Choosing based on structure, scale, and access patterns.
- **Caching.** Client, CDN, web server, database, and application caches; cache-aside, write-through, write-behind, and refresh-ahead strategies; eviction policies such as LRU.

### Asynchrony and Communication

- **Asynchronous processing.** Message queues, task queues, back pressure, and event-driven design.
- **Network protocols.** TCP versus UDP.
- **Remote procedure calls (RPC) and REST.** Trade-offs between the two styles.

### Security and Appendix

- **Security basics.** Authentication, authorization, encryption in transit and at rest.
- **Appendix.** Powers of two and a table of latency numbers every programmer should know.

---

## System Design Exercises

Each exercise walks through requirements, back-of-the-envelope estimates, high-level design, and deeper component design.

| Exercise | Folder | Key concepts |
|---|---|---|
| Design Pastebin.com | `pastebin/` | Object storage, key generation, expiration, read-heavy caching |
| Design the Twitter timeline and search | `twitter/` | Fan-out on write vs. read, timeline caching, search indexing |
| Design a web crawler | `web_crawler/` | URL frontier, politeness, deduplication, distributed crawling with MapReduce |
| Design Mint.com | `mint/` | Financial data aggregation, batch processing, MapReduce |
| Design a social graph | `social_graph/` | Graph storage, friend-of-friend queries, sharding graph data |
| Design Amazon's sales rank by category | `sales_rank/` | Aggregation pipelines, MapReduce for ranking |
| Design a key-value cache for query results | `query_cache/` | Cache eviction, memory management, cache invalidation |
| Design AWS-style autoscaling | `scaling_aws/` | Horizontal scaling, load balancing, scaling policies |

Each exercise folder usually contains:

- `README.md`: the full walkthrough.
- `README-zh-Hans.md`: the Chinese translation.
- `*.graffle` and `*.png`: the diagram source and its rendered image. The `_basic` variants show simpler versions of the diagrams.
- `*_snippets.py` or `*_mapreduce.py`: illustrative code.

---

## Object-Oriented Design Exercises

These exercises focus on class design, encapsulation, and clean interfaces. Each folder contains a Python implementation (`.py`) and a Jupyter notebook (`.ipynb`) for interactive exploration.

| Problem | Folder | Typical concepts |
|---|---|---|
| Hash map | `hash_map/` | Hashing, collision handling, resizing |
| LRU cache | `lru_cache/` | Doubly linked list, hash map, O(1) get and put |
| Parking lot | `parking_lot/` | Class hierarchy, allocation strategy, pricing |
| Deck of cards | `deck_of_cards/` | Modeling entities, shuffling, dealing |
| Call center | `call_center/` | Escalation chain, call routing, employee roles |
| Online chat | `online_chat/` | Users, rooms, messages, observer-style notifications |

To run an exercise:

```bash
# Run a solution module directly, if it has a main block
python lru_cache/lru_cache.py

# Or open the notebook interactively
jupyter notebook lru_cache/lru_cache.ipynb
```

---

## Anki Flashcard Decks

Three Anki decks are included for spaced-repetition study:

| Deck | Purpose |
|---|---|
| `System Design.apkg` | Core concepts, trade-offs, and building-block facts |
| `System Design Exercises.apkg` | Recall of requirements, estimates, and designs for each exercise |
| `OO Design.apkg` | OO design patterns and class-design questions |

To import a deck:

1. Install [Anki](https://apps.ankiweb.net/).
2. Choose **File → Import** and select the `.apkg` file.
3. Review cards daily. Anki schedules repetitions for you.

---

## Diagrams and Source Files

- **`.png` and `.jpg` files** are the rendered images used in the guides and flashcards. Many have randomly generated names (for example, `jj3A5N8.png`), which are typical of images uploaded to image hosts and referenced from Markdown.
- **`.graffle` files** are OmniGraffle source documents. Open them with [OmniGraffle](https://www.omnigroup.com/omnigraffle) to edit a diagram. After editing, export a new PNG and update the reference in the Markdown.
- **`_basic` variants** are simplified diagrams for introductory explanations.
- **`scaling_aws_1.png` through `scaling_aws_7.png`** are step-by-step frames for the AWS autoscaling walkthrough.

---

## Python Code Snippets and Solutions

Python files in this repository serve two purposes:

- **Snippets** (`*_snippets.py`, `*_mapreduce.py`) illustrate algorithms and data-processing patterns used in the system design write-ups, such as MapReduce jobs for sales ranking and web crawling.
- **OO solutions** (`hash_map.py`, `lru_cache.py`, and others) are self-contained class implementations for the object-oriented design exercises.

The code is intended for learning and is not production-hardened. Review it before reusing it in a real project.

Most OO solution folders are Python packages (they include `__init__.py`), so you can import them from the repository root:

```python
from lru_cache.lru_cache import LRUCache

cache = LRUCache(capacity=2)
cache.put(1, "a")
cache.put(2, "b")
print(cache.get(1))  # "a"
```

The exact class and method names depend on each implementation, so check the file before using it.

---

## Building an EPUB

The repository includes tooling to generate an EPUB ebook from the guide:

- `epub-metadata.yaml` holds the book metadata: title, author, language, rights, and similar fields.
- `generate-epub.sh` runs the conversion. It is typically implemented with [Pandoc](https://pandoc.org/), so install Pandoc first.

```bash
# Make the script executable, then run it
chmod +x generate-epub.sh
./generate-epub.sh
```

Read the script before running it to confirm its input and output paths.

---

## Translations

A Simplified Chinese translation is available for the main guide (`README-zh-Hans.md`) and for each exercise folder. `TRANSLATIONS.md` lists the available translations and their status. To add a translation, follow the process in `CONTRIBUTING.md`.

---

## Contributing

Contributions are welcome. Typical contributions include:

- Fixing errors or typos in the guides.
- Improving diagrams or adding clearer versions.
- Adding exercises, OO design problems, or code solutions.
- Updating or adding translations.
- Improving flashcards.

Read `CONTRIBUTING.md` before opening a pull request. When you change a guide, update the matching translation if one exists, and keep diagram sources (`.graffle`) and exported images (`.png`) in sync.

---

## License

The project is distributed under the terms in `LICENSE.txt`. The upstream System Design Primer is licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**, which permits reuse and adaptation with attribution. Check `LICENSE.txt` in this copy to confirm the terms that apply, including any terms for code files.

---

## Acknowledgments

This material builds on the work of the original System Design Primer contributors and the broader engineering community. Diagrams, examples, and the overall approach are adapted from publicly available system design resources. Refer to the upstream project and `LICENSE.txt` for attribution details.
