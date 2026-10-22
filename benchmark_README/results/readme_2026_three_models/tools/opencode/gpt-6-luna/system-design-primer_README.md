# System Design Primer

This repository is a collection of system-design interview study materials. It combines written design walkthroughs, diagrams, selected Python examples, and object-oriented design exercises. The design writeups frame problems through use cases and constraints, outline a high-level architecture, examine core components, and discuss scaling choices and trade-offs.

## Contents

### System design case studies

Each case study is a standalone walkthrough with its own diagrams and, in some cases, code snippets. The writeups link to relevant system-design topic sections in the upstream project to avoid repeating general explanations.

| Case study | Material |
| --- | --- |
| [Scale a system on AWS](solutions/system_design/scaling_aws/README.md) | Iteratively scale a service, from a single server toward a larger architecture. |
| [Web crawler](solutions/system_design/web_crawler/README.md) | Crawl pages, build search indexes, and serve search results. |
| [Twitter timeline and search](solutions/system_design/twitter/README.md) | Post tweets, build timelines, and search tweets. |
| [Query-result cache](solutions/system_design/query_cache/README.md) | Cache recent search results, including an LRU cache design. |
| [Sales rank by category](solutions/system_design/sales_rank/README.md) | Calculate and serve popular products by category. |
| [Social-network graph](solutions/system_design/social_graph/README.md) | Find a shortest path between people in a large unweighted graph. |
| [Mint.com](solutions/system_design/mint/README.md) | Connect financial accounts, process transactions, and manage budgets. |
| [Pastebin / Bit.ly](solutions/system_design/pastebin/README.md) | Store and retrieve pastes or shortened links, with expiration and analytics. |

The case studies discuss topics such as databases and SQL/NoSQL trade-offs, caching, load balancing, horizontal scaling, queues, availability, consistency, security, and latency. Their stated numbers and designs are exercise assumptions and examples, not measurements of a deployed service.

### Object-oriented design

The `solutions/object_oriented_design/` directory contains Python files and Jupyter notebooks for these exercises:

- [Parking lot](solutions/object_oriented_design/parking_lot/)
- [LRU cache](solutions/object_oriented_design/lru_cache/)
- [Call center](solutions/object_oriented_design/call_center/)
- [Deck of cards](solutions/object_oriented_design/deck_of_cards/)
- [Hash table](solutions/object_oriented_design/hash_table/)
- [Online chat](solutions/object_oriented_design/online_chat/)

These are study examples, not a packaged application. Some methods are deliberately left as `pass` placeholders, and the repository does not include a shared test runner or dependency manifest. Review the specific file or notebook before treating an example as a complete implementation.

### Other resources

- `images/` contains image assets used by the materials.
- `resources/` contains a study-guide image and Graffle file, plus `.apkg` flash-card packages.
- `TRANSLATIONS.md` describes the translation contribution process and tracks translation status.
- `CONTRIBUTING.md` explains how to report issues, submit changes, and contribute translations.

## Reading the materials

Start with a case study relevant to the problem you are practicing. Each system-design walkthrough is organized around scoping use cases and constraints, sketching a high-level design, detailing core components, and considering how the design might scale. The proposed architectures are prompts for discussing trade-offs; they are not requirements to use a particular vendor or technology.

Some case-study documents link to topic anchors in the upstream repository's README. Those linked explanations are not separate topic files in this checkout.

## EPUB generation

`generate-epub.sh` uses [Pandoc](https://pandoc.org/) to generate an English EPUB by combining the root README with the system-design case-study READMEs. It also attempts to generate EPUBs from `README-ja.md`, `README-zh-Hans.md`, and `README-zh-TW.md` at the repository root. The corresponding root-level translated README files are not included in this checkout, so translated EPUB generation requires those files to be supplied.

With Pandoc installed and the required Markdown inputs present, run:

```sh
bash generate-epub.sh
```

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the repository's pull-request and translation guidelines, and [TRANSLATIONS.md](TRANSLATIONS.md) for translation information.

## License

The repository's `LICENSE.txt` states that its code and resources are provided under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
