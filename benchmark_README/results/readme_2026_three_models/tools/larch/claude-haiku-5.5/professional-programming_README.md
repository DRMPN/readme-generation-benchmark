# Professional Programming

A curated collection of guides, anti-pattern catalogs, and reference material on software engineering practice. It covers clean code and architecture, error handling, testing, databases and SQLAlchemy, scalability, front-end development (JavaScript, TypeScript, React, CSS/HTML), and team practices such as feature flags and MVP delivery. Most content is in Markdown, with supporting diagrams, a few Python examples, and two reference PDFs.

> **Note:** This README was written from the repository's file listing. File descriptions are inferred from file names and should be checked against the contents of each file.

## Table of Contents

- [Purpose](#purpose)
- [Repository Structure](#repository-structure)
- [Contents](#contents)
  - [Anti-Pattern Catalogs](#anti-pattern-catalogs)
  - [Architecture and Clean Code](#architecture-and-clean-code)
  - [Error Handling Examples](#error-handling-examples)
  - [Front-End Development Series](#front-end-development-series)
  - [Reference and Process](#reference-and-process)
  - [Images and Diagrams](#images-and-diagrams)
- [Getting Started](#getting-started)
- [Running the Python Examples](#running-the-python-examples)
- [How to Use This Repository](#how-to-use-this-repository)
- [Contributing](#contributing)
- [License](#license)

## Purpose

Experienced developers often know a practice is wrong without being able to name it, explain why it causes trouble, or show a better alternative. This repository collects those ideas in one place:

- **Naming the problem:** anti-patterns are described so teams can refer to them in code reviews and design discussions.
- **Explaining the trade-offs:** guides cover why a practice causes harm and when a "bad" pattern might still be acceptable.
- **Showing alternatives:** paired "bad" and "good" examples illustrate the difference in code.
- **Sharing a vocabulary:** a glossary defines common terms so readers and contributors use them consistently.

## Repository Structure

The repository is mostly flat. Files fall into these groups:

```
.
├── LICENSE
├── CONTRIBUTING.md
├── README.md
├── glossary.md
├── feature-flags.md
│
├── *-antipatterns.md              # Anti-pattern catalogs (code, tests, errors, DB, etc.)
├── Clean-Code-V2.4.pdf            # Reference PDF
├── Clean-Architecture-V1.0.pdf    # Reference PDF
│
├── reraise_exceptions_bad.py      # Python example: exception re-raising (anti-pattern)
├── reraise_exceptions_good.py     # Python example: exception re-raising (recommended)
├── exists.py                      # Python example
│
├── 01-modern-javascript.md        # Front-end series, numbered 01–06
├── 02-react.md
├── 03-typescript.md
├── 04-the-browser.md
├── 05-css-html-restart.md
├── 06-front-end-development-practices.md
├── hoisting.html
│
└── *.png, *.jpg, *.jpeg, *.gif    # Diagrams and illustrations
```

Several `README.md` files appear in the listing. They are likely section or directory READMEs, which suggests the repository has subdirectories that the flat listing doesn't show.

## Contents

### Anti-Pattern Catalogs

Each catalog describes common mistakes in one area of software development.

| File | Topic |
|------|-------|
| `code-antipatterns.md` | General code-level mistakes and smells |
| `tests-antipatterns.md` | Common testing mistakes, such as brittle, slow, or misleading tests |
| `error-handling-antipatterns.md` | Problems with exceptions, error propagation, and recovery |
| `database-antipatterns.md` | Schema design, query, and data-access mistakes |
| `sqlalchemy-antipatterns.md` | SQLAlchemy-specific mistakes, such as session misuse and N+1 queries |
| `mvcs-antipatterns.md` | Mistakes in Model-View-Controller/Service structures |
| `scalability-antipatterns.md` | Designs that fail under growth in load, data, or team size |

### Architecture and Clean Code

- **`Clean-Code-V2.4.pdf`**: a reference document on writing readable, maintainable code.
- **`Clean-Architecture-V1.0.pdf`**: a reference document on structuring software around stable abstractions and separating business rules from frameworks and delivery mechanisms.
- **`glossary.md`**: definitions of terms used across the repository.
- **`feature-flags.md`**: guidance on using feature flags to decouple deployment from release, including their lifecycle and the cost of leaving them in place.

### Error Handling Examples

The two Python files show a common exception-handling issue: re-raising exceptions.

- **`reraise_exceptions_bad.py`** shows a pattern that loses information, such as the original traceback or exception chain, or that swallows errors.
- **`reraise_exceptions_good.py`** shows the recommended approach, which preserves context. In Python this usually means a bare `raise` to re-raise the current exception, or `raise NewError(...) from original` to add context while keeping the cause.

Pair these with `error-handling-antipatterns.md` for the reasoning behind them.

- **`exists.py`** is a standalone Python example. Its purpose is not described in the listing, so check the file before relying on it.

### Front-End Development Series

The numbered files form a learning path through modern web development:

1. **`01-modern-javascript.md`**: modern JavaScript language features and idioms.
2. **`02-react.md`**: component-based UI development with React.
3. **`03-typescript.md`**: adding static typing to JavaScript projects.
4. **`04-the-browser.md`**: how browsers work, including rendering, events, and networking.
5. **`05-css-html-restart.md`**: a refresher on HTML and CSS fundamentals.
6. **`06-front-end-development-practices.md`**: team-level practices such as tooling, testing, and code organization.

**`hoisting.html`** is a standalone demonstration of JavaScript hoisting, a frequent source of confusion for newcomers.

### Reference and Process

- **`CONTRIBUTING.md`**: how to propose changes, report issues, and submit pull requests.
- **`LICENSE`**: the terms under which the material may be used and shared.

### Images and Diagrams

The repository includes many illustrations that support the Markdown guides. They cover:

- **Testing:** `test-pyramid.png`, `what to assert.png`
- **Architecture:** `clean-architecture-cone.jpg`, `software_architecture_pasta.png`, `uwe-friedrichsen-resilient-architecture.png`
- **Process and delivery:** `mvp.jpeg`, `how-not-to-build-mvp.jpg`, `waterfall-UX.jpeg`, `decomposing problems.jpg`
- **Optimization and automation:** `premature-optimization-flowchart.png`, `premature automation.png`, `the reality of automation.png`
- **Technical debt and defects:** `tech-debt.jpeg`, `cost-of-defects.jpg`
- **Front-end:** `caniuse.png`, `js-the-good-parts.jpg`, `learning-roadmap.png`, `syntax-highlighting.jpeg`, `hoisting.html`
- **Miscellaneous:** `rewrite.gif`, `us-vs-them.jpeg`, `amazon_writing_rules.jpeg`, `let-your-bugs-teach-you-julia-evans.jpg`

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/<owner>/professional-programming-d3w2l1ll.git
   cd professional-programming-d3w2l1ll
   ```

2. Read the Markdown files in any order. No build step is required.
3. Open the PDFs and images with any standard viewer.

To view the Markdown with rendered diagrams, use a Markdown viewer or a hosting platform that renders relative image links, such as GitHub.

## Running the Python Examples

The Python examples use only the standard library, so no installation is needed beyond Python 3.

```bash
python3 reraise_exceptions_bad.py
python3 reraise_exceptions_good.py
python3 exists.py
```

Compare the output and tracebacks of the "bad" and "good" versions to see how exception context changes.

## How to Use This Repository

- **Learning:** start with the front-end series if you are new to web development, or with `code-antipatterns.md` and the Clean Code and Clean Architecture PDFs for general engineering practice.
- **Code review:** link to a specific anti-pattern section in a review comment to explain why a change should be reconsidered.
- **Team onboarding:** share `glossary.md` and the catalogs so new members learn the team's vocabulary.
- **Reference:** use the catalogs as a checklist when designing a new service, data model, or test suite.

## Contributing

Contributions are welcome, including corrections, new anti-patterns, clearer examples, and better diagrams. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. In general:

1. Fork the repository and create a branch for your change.
2. Keep each anti-pattern entry focused on one idea, with a description, why it is harmful, and a better alternative.
3. Add or update "bad" and "good" examples in code where practical.
4. Open a pull request describing what changed and why.

## License

This project is licensed under the terms in the [LICENSE](LICENSE) file. The bundled PDFs and images may be subject to their own licenses or attribution requirements. Check the original sources before redistributing them.
