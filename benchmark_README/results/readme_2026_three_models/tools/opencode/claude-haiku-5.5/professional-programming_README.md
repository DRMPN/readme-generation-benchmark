# Professional programming

A collection of Markdown notes, training material, antipattern catalogs, cheatsheets, and images on software engineering practice, mostly aimed at back-end and web developers.

## Contents

| Path | Description |
| --- | --- |
| [`antipatterns/`](./antipatterns/README.md) | Catalogs of code, error-handling, test, database, scalability, and ORM (SQLAlchemy) antipatterns, with examples. |
| [`training/web-dev/`](./training/web-dev/README.md) | An opinionated ramp-up program for web developers: principles, roadmap, approach, and topic-specific reading and exercises. |
| [`training/front-end/`](./training/front-end/README.md) | An introduction to front-end programming for back-end developers, covering modern JavaScript, React, TypeScript, the browser, CSS/HTML, and front-end practices. |
| [`training/learning-python/`](./training/learning-python/README.md) | A pointer to a separate Python learning repository. |
| [`cheatsheets/`](./cheatsheets) | PDF cheatsheets: `Clean-Architecture-V1.0.pdf` and `Clean-Code-V2.4.pdf`. |
| [`feature-flags.md`](./feature-flags.md) | Notes on why and when to use feature flags, with references. |
| [`glossary.md`](./glossary.md) | Short definitions of software engineering terms such as conceptual integrity, reliability, the Two Generals' Problem, and the Law of Demeter. |
| [`images/`](./images) | Illustrations referenced by the notes. |
| [`CONTRIBUTING.md`](./CONTRIBUTING.md) | Setup instructions for contributors (pre-commit hooks). |
| [`LICENSE`](./LICENSE) | MIT License. |

### Antipatterns

The `antipatterns/` directory contains:

- `code-antipatterns.md`
- `error-handling-antipatterns.md`
- `tests-antipatterns.md`
- `database-antipatterns.md`
- `scalability-antipatterns.md`
- `sqlalchemy-antipatterns.md`
- `mvcs-antipatterns.md`
- `sqlalchemy-examples/` and `python-examples/`: Python code examples referenced by the notes.

The index in `antipatterns/README.md` also links to a `python-antipatterns.md` file, which is not present in this repository.

### Web development training

`training/web-dev/README.md` is organized as:

- **Principles**: focus on the essentials, treat best practices as part of programming, and learn by doing.
- **Roadmap**: start with one programming language, do a first pass at the development environment (HTTP, Git, Docker and `docker-compose`, command line, text editor), write and get review on a full exercise, then move to advanced topics.
- **Approach**: learn a text editor deeply, and learn one language in depth (Python or TypeScript are suggested).
- **Topic-specific materials**: best practices, code architecture and design patterns, databases and SQL, the command line and Linux, distributed systems, networking and HTTP, project management, security, and Git.

### Front-end training

`training/front-end/` is a sequence of sessions:

1. `01-modern-javascript.md`
2. `02-react.md`
3. `03-typescript.md`
4. `04-the-browser.md`
5. `05-css-html-restart.md`
6. `06-front-end-development-practices.md`

It also includes `examples/hoisting.html` and an image of a learning roadmap.

## Feature flags

`feature-flags.md` lists the benefits of feature flags: faster rollback, a forcing function for testing, smaller and safer code iterations, and gradual rollout. It also gives guidance on when not to use them (simple copy or logging changes, changes that are quick to roll back, and safe asynchronous jobs) and when they are useful (large refactors, changes to integration points, performance optimization, and new flows).

## Glossary

`glossary.md` defines terms including blackbox and whitebox monitoring, conceptual integrity, the end-to-end principle, NIHITO, stability, reliability, the Two Generals' Problem, the Law of Demeter, and the second-system effect.

## Contributing

Contributions use [pre-commit](https://pre-commit.com/). The `.pre-commit-config.yaml` file configures these hooks:

- `check-yaml`, `end-of-file-fixer`, and `trailing-whitespace` from `pre-commit-hooks`
- `black` for Python formatting
- `doctoc` to generate the tables of contents at the top of Markdown files (the `## Table of Contents` title is set in the config)

To set up the hooks:

```bash
pip install pre-commit   # or: pipx install pre-commit
pre-commit install
```

Sections between the `<!-- START doctoc generated TOC ... -->` and `<!-- END doctoc generated TOC ... -->` markers are generated; re-run `doctoc` rather than editing them by hand.

## License

Released under the [MIT License](./LICENSE). Copyright (c) 2017 Charles-Axel Dein.
