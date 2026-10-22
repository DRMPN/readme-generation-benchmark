# Antipatterns and Engineering Notes

This repository is a collection of software engineering notes. It covers common antipatterns in code, databases, error handling, SQLAlchemy, and testing, along with short write-ups on feature flags and a glossary of engineering terms. It also contains front-end and web development training material and a few reference cheatsheets. The content is written in Markdown, with some Python and JavaScript code examples. Several files are marked as works in progress.

## Overview

The repository has four main parts:

- **Antipatterns** (`antipatterns/`): Markdown guides that describe patterns to avoid, usually with "Bad" and "Good" code examples. Topics include:
  - Code antipatterns, such as strict email validation, late returns, repeated names, and opaque function arguments
  - Error handling antipatterns, such as hiding exceptions and unnecessary re-raising
  - Database antipatterns, specifically using `VARCHAR` instead of `TEXT` in PostgreSQL
  - SQLAlchemy antipatterns, such as lazy loading in properties, identity comparison with `None`, and loading full objects to check existence
  - MVCS antipatterns, covering association tables and Domain-Driven Design
  - Scalability antipatterns and test antipatterns
- **Feature flags** (`feature-flags.md`): An explanation of why feature flags are useful, when to use them, and when not to, with references.
- **Glossary** (`glossary.md`): Short definitions of terms such as conceptual integrity, the end-to-end principle, stability, reliability, the Two Generals' Problem, the Law of Demeter, and the second-system effect.
- **Training** (`training/`): Ramp-up material for developers. It includes a front-end course for back-end developers (JavaScript, React, TypeScript, the browser, CSS/HTML, and front-end practices), a web development learning path, and a pointer to a separate Python learning repository.

Supporting files include a `CONTRIBUTING.md` guide, a `.pre-commit-config.yaml` file, two PDF cheatsheets (Clean Architecture and Clean Code), and an `images/` directory with diagrams and illustrations used in the Markdown files.

## Repository Layout

```
.pre-commit-config.yaml
CONTRIBUTING.md
LICENSE
feature-flags.md
glossary.md
antipatterns/        # Antipattern guides and Python/SQLAlchemy example code
cheatsheets/         # Clean Architecture and Clean Code PDFs
images/              # Diagrams used across the documents
training/
  front-end/         # Modern JavaScript, React, TypeScript, browser, CSS/HTML, practices
  learning-python/   # README pointing to an external repository
  web-dev/           # Learning web development roadmap and topic list
```

## Setup

The repository has no build step, package manifest, or dependency file. To work with the content, clone it and open the Markdown files in any editor or Markdown viewer.

To contribute, install the pre-commit hooks. `CONTRIBUTING.md` suggests installing `pre-commit` with a tool such as `pipx`, then running this command from the repository root:

```bash
pre-commit install
```

## Usage

Start with the document that matches your question:

- **Code review or design questions:** read `antipatterns/code-antipatterns.md`. Each section explains why a pattern is problematic and gives an alternative.
- **Exception handling:** read `antipatterns/error-handling-antipatterns.md`. The file includes a runnable example in `antipatterns/python-examples/`.
- **SQLAlchemy queries:** read `antipatterns/sqlalchemy-antipatterns.md`. The file `antipatterns/sqlalchemy-examples/exists.py` compares two ways of checking whether a record exists.
- **Tests:** read `antipatterns/tests-antipatterns.md`, which includes the test pyramid diagram.
- **Release strategy:** read `feature-flags.md`.
- **Vocabulary:** read `glossary.md`.
- **Front-end training:** follow the numbered curriculum in `training/front-end/README.md`, which lists the modules in order.
- **Web development roadmap:** read `training/web-dev/README.md`.

The Python examples can be run directly. For example, `reraise_exceptions_bad.py` deliberately contains a typo (`brad` instead of `bread`) to show the error that a bare `except` hides. The SQLAlchemy example imports `sqlalchemy` and uses an in-memory SQLite database. The repository does not specify a SQLAlchemy version.

## Configuration

The only configuration file is `.pre-commit-config.yaml`. It defines these hooks:

| Repository | Revision | Hooks |
|---|---|---|
| `pre-commit/pre-commit-hooks` | `v2.3.0` | `check-yaml`, `end-of-file-fixer`, `trailing-whitespace` |
| `psf/black` | `19.3b0` | `black` |
| `thlorenz/doctoc` | `v1.4.0` | `doctoc`, with the argument `--title "## Table of Contents"` |

The `doctoc` hook regenerates the table of contents in Markdown files. Each file begins with a comment block marked "START doctoc generated TOC." Do not edit the content inside that block by hand. Instead, run the hook so that it updates the block.

## Development

Follow these guidelines when changing the content:

1. Install the pre-commit hooks as described in [Setup](#setup).
2. Keep the existing file structure. Antipattern guides belong in `antipatterns/`, and training modules belong in `training/`.
3. Follow the existing format in each document. Most antipattern sections use a `Bad:` code block followed by a `Good:` code block, with an explanation of the trade-offs.
4. Leave the doctoc-generated table of contents to the hook. Let it regenerate the table after you edit headings.
5. Place images in the `images/` directory or in the subdirectory for the relevant section, such as `training/front-end/img/`.
6. Keep Python examples correct and runnable where practical. The repository is primarily prose, but its code samples are meant to illustrate specific points.

`CONTRIBUTING.md` contains only the hook installation instructions. It does not describe a pull request process or other contribution rules.

## Testing

The repository has no test suite, test runner configuration, or CI workflow. The only automated checks are the pre-commit hooks, which validate YAML, fix end-of-file newlines, remove trailing whitespace, format Python with Black, and regenerate tables of contents.

The antipatterns documentation discusses testing practices, but those files describe guidance rather than tests of this repository.

## Known Gaps

Some documents are incomplete. Readers should be aware of the following:

- `antipatterns/README.md` links to `python-antipatterns.md`, which does not appear in the repository. The Python-specific content is in `code-antipatterns.md` instead.
- `antipatterns/mvcs-antipatterns.md` exists but is not listed in `antipatterns/README.md`.
- Several sections contain only a `TODO` marker, including the sections on the scalability antipatterns, the explicit session passing and implicit transaction handling in SQLAlchemy, and several test antipatterns.
- The training section "Learn about Promises" and the "How `this` works in arrow functions" section are placeholders.
- `training/front-end/05-css-html-restart.md` and `training/front-end/06-front-end-development-practices.md` contain brief outlines rather than full material.
- `training/front-end/02-react.md` ends with an "Advanced" self-assessment heading that has no questions under it.
- `training/learning-python/README.md` contains only a link to an external repository.

## Contributing

Contributions follow the same approach as the rest of the repository. Install the pre-commit hooks, make focused changes, and let the hooks regenerate the table of contents. `CONTRIBUTING.md` documents the hook installation step.

## License

This project is licensed under the MIT License. The license text is in `LICENSE`, and the copyright notice reads "Copyright (c) 2017 Charles-Axel Dein."
