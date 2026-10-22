# System Design Primer

This repository collects study material for system design interviews and object-oriented design. It contains worked solutions to design problems, Python sketches for selected components, flash card decks, a study guide diagram, and a translation process for the written content.

## Overview

Each system design solution follows the same four-step outline:

1. **Outline use cases and constraints**: gather requirements, scope the problem, and state assumptions.
2. **Create a high-level design**: list the important components, usually shown in a diagram.
3. **Design core components**: go into detail on each component, including data schemas, APIs, and sample code.
4. **Scale the design**: identify bottlenecks, evaluate alternatives and trade-offs, and repeat.

The solutions link to shared "system design topics" (for example caching, sharding, load balancers, and consistency patterns) rather than repeating that background in every document. Each design document describes its own problem scope and assumptions, so the numbers and components differ between problems.

## Repository Contents

### System design solutions

Under `solutions/system_design/`, each problem has its own directory. The directories include:

| Directory | Problem |
|---|---|
| `mint/` | Design Mint.com (financial account aggregation, categorization, budgets) |
| `pastebin/` | Design Pastebin.com (or Bit.ly) |
| `query_cache/` | Design a key-value cache for recent web server queries |
| `sales_rank/` | Design Amazon's sales rank by category feature |
| `scaling_aws/` | Design a system that scales to millions of users on AWS |
| `social_graph/` | Design the data structures for a social network |
| `twitter/` | Design Twitter timeline and search |
| `web_crawler/` | Web crawler design |
| `template/` | A diagram template (`template.graffle`) |

Most problem directories contain a `README.md`, a `README-zh-Hans.md` (Simplified Chinese), diagram sources in `.graffle` format with matching `.png` renderings, and one or more Python files. The Python files include sketches such as `mint_mapreduce.py`, `sales_rank_mapreduce.py`, `web_crawler_mapreduce.py`, and `*_snippets.py`, plus an `__init__.py` in many directories.

### Object-oriented design solutions

Under `solutions/object_oriented_design/`, six problems each have a Python module and a Jupyter notebook:

- `call_center`
- `deck_of_cards`
- `hash_table` (`hash_map.py`)
- `lru_cache`
- `online_chat`
- `parking_lot`

Each directory includes an `__init__.py`, a `.py` implementation, and a `.ipynb` notebook.

### Study resources

Under `resources/`:

- `flash_cards/` contains three Anki-format deck packages (`.apkg`): `OO Design.apkg`, `System Design.apkg`, and `System Design Exercises.apkg`.
- `study_guide.graffle` and `study_guide.png` provide an editable diagram and a rendered image of a study guide.

### Images

The `images/` directory holds the PNG and JPG files referenced by the written material.

### Translations

Translated content is stored as `README-<language-code>.md` files alongside the English versions. The `TRANSLATIONS.md` file records each language's status and maintainers.

## Getting Started

Clone the repository:

```bash
git clone https://github.com/donnemartin/system-design-primer.git
cd system-design-primer
```

No dependency manifest (such as `requirements.txt` or `setup.py`) is included in the supplied file tree, so this README does not list installation steps for the Python code. The sample MapReduce classes reference `MRJob`, which suggests the `mrjob` library is needed to run them, but the repository does not specify this.

To read the material, open the Markdown files on GitHub or in any Markdown viewer. To explore the object-oriented solutions, open the `.ipynb` notebooks in Jupyter or inspect the `.py` modules directly.

## Usage

### Studying a system design problem

1. Open the problem's `README.md` (for example, `solutions/system_design/pastebin/README.md`).
2. Read Step 1 and write down your own clarifying questions before reading the stated assumptions.
3. Compare your high-level design with the diagram in Step 2 (`.png` files are embedded in the Markdown).
4. Review the detailed components and sample code in Step 3.
5. Use the bottleneck discussion in Step 4 to practice benchmarking, profiling, and trade-off reasoning.

Each document notes that the interviewer should be consulted about how much code to write and whether back-of-the-envelope calculations are expected.

### Working with the code samples

The Python files are educational sketches, not complete applications. For example, `query_cache` describes a `QueryApi`, `Node`, `LinkedList`, and `Cache` design, but several methods are left as `...`. The `scaling_aws` and `social_graph` documents likewise describe architecture rather than runnable services.

The object-oriented solutions are more self-contained. Each has a `.py` module that can be imported, and a notebook that accompanies it.

### Using the study materials

- Import the `.apkg` files into Anki to review flash cards.
- Open the `.graffle` files in OmniGraffle to edit diagrams; the matching `.png` files show the rendered output.

## Configuration

The supplied tree contains no runtime configuration files for the code. The configuration-related files are:

- **`.gitattributes`**: Git attribute settings for the repository. Its contents were not included in the supplied material.
- **`.gitignore`**: patterns that Git should ignore. Its contents were not included in the supplied material.
- **`epub-metadata.yaml`**: a metadata file, presumably for building an EPUB edition of the content.
- **`generate-epub.sh`**: a shell script, presumably the EPUB build step that uses `epub-metadata.yaml`.

The contents of `epub-metadata.yaml` and `generate-epub.sh` were not included in the supplied material, so this README does not describe their options or invocation. Check those files directly before running the script.

## Development

### Reporting bugs and requesting features

Submit bug reports or requests as issues on the [GitHub issues page](https://github.com/donnemartin/system-design-primer/issues).

### Submitting pull requests

From `CONTRIBUTING.md`:

1. Fork the main repository on GitHub.
2. Clone your fork locally.
3. Create a branch for your changes. Do not work on `master`:
   ```bash
   git checkout -b my-feature
   ```
4. Edit files, then stage and commit them:
   ```bash
   git add modified_files
   git commit
   ```
5. Push the branch:
   ```bash
   git push -u origin my-feature
   ```
6. Open a pull request from your fork.

The pull request template asks contributors to review the Contributing Guidelines and, for translations, to tag the language maintainer and prefix the title with a language code, such as `ja: Fix ...`.

### Translation workflow

According to `CONTRIBUTING.md` and `TRANSLATIONS.md`:

- The English version is the primary version. Content changes are made in English first, then translated.
- Changes that only improve an existing translation are made directly in that language's file.
- Each pull request should modify only one language.
- Pull requests and issues that concern a single translation should be prefixed with the language code, for example `es: Improve grammar`.
- Translations need review by a native speaker, preferably the language maintainer, before merging.
- New languages should be added as a single `README-xx.md` file using standard IETF language tags (for example, `fr` rather than a country code). Language variants use the shortest tag, such as `zh-Hant`.
- A complete, reviewed translation of the English README is required before merging into `master`.

### Translation status

`TRANSLATIONS.md` groups languages by status:

- **Live**: Japanese, Simplified Chinese, and Traditional Chinese.
- **In Progress**: Korean and Russian.
- **Stalled** (help wanted): Arabic, Bengali, Brazilian Portuguese, French, German, Greek, Hebrew, Italian, Persian, Spanish, Thai, Turkish, Ukrainian, and Vietnamese.

## Testing

The supplied file tree contains no test files, test directories, test runner configuration, or CI workflow files. The only file under `.github/` is the pull request template.

Verification of the content is handled through review. Translations require review by a native speaker, and pull requests follow the checklist in the PR template. Some code samples are excerpts with elided bodies (`...`) or incomplete definitions, so they are illustrative rather than runnable test subjects. Any automated testing would need to be added separately.

## License

The repository includes a `LICENSE.txt` file. Its contents were not included in the supplied material, so this README does not state the license terms. See `LICENSE.txt` in the repository root for the applicable terms.

## Acknowledgments

The translation process template is credited to [The Art of Command Line](https://github.com/jlevy/the-art-of-command-line), as noted in `CONTRIBUTING.md`.
