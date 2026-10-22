# Professional Programming Notes and Training

This repository is a collection of software-development guidance, training material, reference documents, and code examples. It is intended for reading and learning rather than as a packaged application: the supplied files do not define a build, release, or project-wide test workflow.

The material is opinionated and practical. It covers topics such as code and database antipatterns, error handling, testing, web development, and front-end programming. Some documents are introductory, some are short topic notes, and some include unfinished sections marked `TODO`.

## Contents

- [`antipatterns/`](antipatterns/README.md) — examples and discussion of practices to avoid.
- [`training/web-dev/`](training/web-dev/README.md) — an opinionated learning path for web development.
- [`training/front-end/`](training/front-end/README.md) — introductory front-end material aimed at back-end and infrastructure developers.
- [`training/learning-python/`](training/learning-python/README.md) — points to a separate Python education repository.
- [`feature-flags.md`](feature-flags.md) — guidance on when feature flags can help with releases, testing, and gradual rollouts.
- [`glossary.md`](glossary.md) — definitions of software and systems concepts.
- [`cheatsheets/`](cheatsheets/) — Clean Architecture and Clean Code PDF documents.
- [`images/`](images/) — illustrations referenced by the written material.

## What you will find

### Antipatterns

The antipattern collection discusses code practices, error handling, testing, databases, SQLAlchemy, scalability, and MVCS design. Its guidance includes using early returns to reduce nesting, making function arguments explicit, avoiding silent exception handling, and keeping tests deterministic. SQLAlchemy examples show alternatives to loading full objects when checking for existence, and the testing notes discuss fixture scope, query tests, and the tradeoffs of end-to-end tests.

The collection includes Python examples under `antipatterns/python-examples/` and a SQLAlchemy `EXISTS` example under `antipatterns/sqlalchemy-examples/`. These are teaching examples, not a complete application or a packaged library. Some antipattern documents have unfinished sections.

### Training material

The web-development training proposes a learning route from a programming language and web fundamentals to practical exercises and more advanced topics. It includes recommendations for learning programming, architecture, databases, command-line tools, distributed systems, networking, security, and version control.

The front-end curriculum moves through modern JavaScript, React, TypeScript, the browser, CSS and HTML, and front-end development practices. The front-end guide describes itself as an introduction and presentation support, not an exhaustive course. Its prerequisites include familiarity with HTTP, browsers, HTML and CSS, programming basics, and some JavaScript experience. The JavaScript lesson suggests CodeSandbox for trying examples, and the React lesson describes setting up a simple app there.

## Setup

There is no application to install or configure before reading the documents. Browse the Markdown files in a repository viewer or text editor. Open the PDFs in `cheatsheets/` with a PDF reader.

The examples are intended to illustrate particular ideas. No repository-wide dependency manifest or environment setup instructions are supplied. In particular, the SQLAlchemy example imports SQLAlchemy, so running that example requires an environment where that package is available. The front-end lessons link to external learning resources and online sandboxes; using those services is optional for reading the repository.

## Usage

Start with the collection that best fits your goal:

- For code-quality guidance, browse [`antipatterns/README.md`](antipatterns/README.md), then open the relevant topic document.
- For a broad self-directed learning plan, use [`training/web-dev/README.md`](training/web-dev/README.md).
- For front-end topics, follow the curriculum in [`training/front-end/README.md`](training/front-end/README.md). Its numbered lessons provide the sequence.
- For a focused topic, read [`feature-flags.md`](feature-flags.md) or look up a term in [`glossary.md`](glossary.md).
- For printable reference material, see the Clean Architecture and Clean Code PDFs in `cheatsheets/`.

The notes express recommendations and tradeoffs rather than a mandatory style standard. For example, the feature-flag document recommends considering flags for large refactors, integration changes, performance work, and new flows, while leaving simple changes to engineering judgment. Read examples in context and adapt the guidance to the requirements of your own system.

## Configuration

There is no application configuration. The repository does include a `.pre-commit-config.yaml` for automated checks on changes. It configures these hooks:

- `check-yaml`, `end-of-file-fixer`, and `trailing-whitespace` from `pre-commit-hooks` at `v2.3.0`.
- Black at `19.3b0`.
- Doctoc at `v1.4.0`, with the table-of-contents title set to `## Table of Contents`.

The Doctoc hook is configured to manage generated Markdown table-of-contents sections. Where a document has the generated-section comments, retain them so the tool can update the section.

## Development and contributing

Contributions can improve explanations, correct examples, add useful references, or fill in unfinished sections. Keep changes focused on the relevant document and preserve the repository’s Markdown structure. When editing a document with a generated table of contents, update it using the configured Doctoc hook rather than manually changing the generated section.

To enable the configured hooks locally, install `pre-commit` (the contribution notes give `pipx` as an example installation method), then run:

```bash
pre-commit install
```

The contribution instructions do not specify a pull-request template, branching strategy, or commit-message format.

## Testing

No project-wide test suite or test command is documented. The Python and SQLAlchemy files are standalone examples illustrating material in the Markdown; they are not presented as a comprehensive automated test suite.

When changing examples, review them against the text they support. The repository’s testing guidance favors focused, deterministic checks and cautions against overly broad or flaky end-to-end tests. The configured pre-commit hooks provide checks for YAML formatting, whitespace, Black formatting, and generated table of contents; they do not constitute a behavioral test suite.

## License

This repository is distributed under the MIT License. The license identifies the copyright holder as Charles-Axel Dein, copyright 2017. See [`LICENSE`](LICENSE) for the complete terms, including the requirement to include the copyright and permission notice in copies or substantial portions of the software.
