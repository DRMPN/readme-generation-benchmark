# System Design Primer

A collection of system-design study material and coding examples. The repository brings together system-design case studies, object-oriented design exercises, Python examples and notebooks, diagrams, and packaged flash-card decks. It is intended for learning and interview preparation—not as a single application with a documented runtime or deployment workflow.

## Overview

The material covers both design reasoning and implementation examples:

- **System-design case studies** include Mint, Pastebin/Bit.ly, a query-result cache, sales ranking, AWS scaling, social-network data structures, Twitter, and web crawling.
- **Object-oriented design exercises** include a call center, deck of cards, hash table, LRU cache, online chat, and parking lot.
- **Reference materials** include diagrams, images, flash-card packages, and a study-guide diagram.
- **Code and notebooks** provide examples associated with several object-oriented exercises and selected system-design cases.

The case-study documents generally work through requirements and assumptions, a high-level design, core components, and ways to identify and address scaling bottlenecks. They are study examples: their assumptions and proposed architectures are discussion material, not claims about production systems.

## Repository layout

- `solutions/object_oriented_design/` contains Python modules and Jupyter notebooks for the listed object-oriented exercises.
- `solutions/system_design/` contains the system-design case studies. Many case-study directories include an English `README.md`, a Simplified Chinese version, diagrams, and Python snippets or MapReduce examples.
- `resources/flash_cards/` contains `.apkg` flash-card packages for object-oriented design and system-design topics.
- `resources/` also contains study-guide artwork.
- `images/` contains image assets used by the learning materials.
- `generate-epub.sh` and `epub-metadata.yaml` are provided for EPUB-related material.
- `CONTRIBUTING.md` and `TRANSLATIONS.md` explain contribution and translation processes.
- `LICENSE.txt` contains the project’s license terms.

## Getting started

The simplest way to use the repository is to read the Markdown documents directly. No installation is needed just to browse the guides and diagrams.

To make a local copy, follow the contribution guide’s fork-and-clone workflow. For example, after forking the repository on GitHub:

```sh
git clone git@github.com:YourLogin/system-design-primer.git
cd system-design-primer
```

Replace `YourLogin` with your GitHub account name. You can also browse the repository online without cloning it.

Start with a case-study `README.md` in `solutions/system_design/` or an exercise under `solutions/object_oriented_design/`. The Python files and notebooks provide code-oriented companions where available. The root contains flash-card packages and visual resources for use alongside the written material.

## Usage

### Study a system-design case

Choose a case-study directory, then read its `README.md` from beginning to end. The documents use example constraints to frame a design problem and discuss possible components, trade-offs, and scaling steps. Some cases include diagrams (`.png` or `.graffle`) and Python snippets or MapReduce-oriented examples.

The Simplified Chinese case-study documents are named `README-zh-Hans.md` where present. Translation status and translation contribution guidance are maintained separately in `TRANSLATIONS.md`.

### Work through an object-oriented exercise

Browse `solutions/object_oriented_design/` for an exercise. Where present, compare the `.py` implementation with the matching `.ipynb` notebook. The supplied files do not define a unified command-line interface or package entry point, so use these as individual learning examples rather than expecting one command to launch all exercises.

### Use the study resources

The `resources/flash_cards/` directory contains three `.apkg` packages: `OO Design.apkg`, `System Design Exercises.apkg`, and `System Design.apkg`. The repository also includes `resources/study_guide.png` and its editable `.graffle` counterpart, along with image assets in `images/`.

## Configuration and EPUB resources

`epub-metadata.yaml` is the repository’s EPUB metadata file, and `generate-epub.sh` is the associated shell script. The supplied files do not document script options, required tools, or a complete EPUB build procedure. Before attempting a build, inspect the script and metadata to determine what it expects in your environment. No application-specific configuration format or runtime settings are documented in the supplied repository text.

## Development and contributions

Contributions are welcome. The project’s `CONTRIBUTING.md` asks contributors to:

1. Fork the main repository and clone their fork.
2. Create a separate branch for their changes; do not work directly on `master`.
3. Commit the changes and push the branch to their fork.
4. Open a pull request for review.

For bug reports or requests, the contribution guide directs users to submit an issue on the project’s GitHub repository. Review the contribution guide before opening a pull request; `.github/PULL_REQUEST_TEMPLATE.md` also asks contributors to verify that their changes follow those guidelines.

### Translations

The English content is the source version. Translation contributions should follow it and should not diverge from its meaning. The translation guidance asks contributors to make content changes in English first, then translate them; translation-only improvements should be submitted against one language at a time. Translation pull requests should use the appropriate language code in the title and receive review from a native speaker, preferably the language maintainer.

See [`TRANSLATIONS.md`](TRANSLATIONS.md) for the listed language statuses, maintainers, and discussion links, and [`CONTRIBUTING.md`](CONTRIBUTING.md) for the process of maintaining or proposing a translation.

## Testing

The supplied repository text does not document a project-wide test suite, test runner, or standard test command. The object-oriented directories include Python source and notebooks, but no unified testing instructions are provided. When changing an example, review the relevant module and notebook and check that the affected material remains consistent. Do not assume that a repository-wide automated test command is available.

## License

See [`LICENSE.txt`](LICENSE.txt) for the applicable license and its terms.
