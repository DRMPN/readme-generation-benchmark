# Software Engineering Resources

A curated collection of software engineering resources maintained by Charles-Axel Dein (`charlax`). The repository gathers documented anti-patterns with runnable Python and SQLAlchemy examples, training curricula for front-end and web development, PDF cheat sheets, and reference material such as a glossary and an essay on feature flags.

Several documents are companion material to related repositories by the same author, including [professional-programming](https://github.com/charlax/professional-programming), [python-education](https://github.com/charlax/python-education), and [engineering-management](https://github.com/charlax/engineering-management).

## Repository layout

```
.
├── antipatterns/        # Documented anti-patterns, with Python/SQLAlchemy examples
│   ├── python-examples/ # Bad vs. good exception re-raising demos
│   └── sqlalchemy-examples/
├── cheatsheets/         # PDF cheat sheets (Clean Architecture, Clean Code)
├── training/            # Training curricula (front-end, web dev, Python)
├── feature-flags.md     # Essay: why and when to use feature flags
├── glossary.md          # Glossary of software engineering terms
└── images/              # Illustrations used across the documents
```

## Anti-patterns

The [`antipatterns/`](antipatterns/README.md) directory collects anti-patterns encountered in real codebases, each illustrated with bad and good code samples. The index page also links a Python anti-patterns page; the documents included here are:

- **[Code anti-patterns](antipatterns/code-antipatterns.md)** — mostly Python-focused but largely generic: strict email validation (why sending a validation email is stronger), late returns, "hacks" comments vs. proper `TODO` comments, redundant argument/class/function names in identifiers and docstrings, unreadable response construction, non-deterministic tests, unbalanced boilerplate, inconsistent `get`/`find` verb conventions, opaque function arguments (`*args`/`**kwargs`, dict params), hiding formatting behind helpers, returning `None` instead of raising a `NotFound` exception, and bloated catch-all `utils`/`lib` modules.
- **[Database anti-patterns](antipatterns/database-antipatterns.md)** — why to prefer `TEXT` over `VARCHAR`/`CHAR(n)` in PostgreSQL.
- **[Error handling anti-patterns](antipatterns/error-handling-antipatterns.md)** — hiding or silencing exceptions ("the most diabolical Python antipattern"), raising unrelated or overly broad exceptions, unconstrained defensive programming, and useless catch-and-re-raise chains. Advocates logging plus metrics with alerting, catching exceptions at the outermost layers (the end-to-end principle), and re-raising with a bare `raise` to preserve the traceback.
- **[MVCS anti-patterns](antipatterns/mvcs-antipatterns.md)** — creating entities for association tables. Drawing on Domain-Driven Design (Eric Evans), it argues association tables are persistence details that should not leak into the domain layer; put association attributes on real entities and filtering logic in repositories.
- **[Scalability anti-patterns](antipatterns/scalability-antipatterns.md)** — placeholder (TODO) sections on not paging database queries and returning whole objects where primary keys would suffice.
- **[SQLAlchemy anti-patterns](antipatterns/sqlalchemy-antipatterns.md)** — abusing lazily loaded relationships instead of SQL `EXISTS` queries, explicit session passing, implicit transaction handling, loading full objects just to check existence, using the identity operator (`is`) in filters instead of `.is_(None)`, and returning `None` instead of raising `NoResultFound`.
- **[Tests anti-patterns](antipatterns/tests-antipatterns.md)** — over-reliance on centralized fixtures, over-reliance on replaying external requests, inefficient query testing, assertions in loops (which pass vacuously on empty lists), and the inverted testing pyramid, with references to Martin Fowler's test pyramid and related reading.

### Runnable examples

- `antipatterns/python-examples/reraise_exceptions_bad.py` and `reraise_exceptions_good.py` demonstrate the difference between replacing an exception with a new one (losing the original root cause) and logging plus re-raising with a bare `raise`.
- `antipatterns/sqlalchemy-examples/exists.py` compares two ways of checking whether a row exists — loading the full entity via `.first()` versus asking the database with `query.exists()` — using an in-memory SQLite database with SQL echo enabled.

## Training

### Front-end (`training/front-end/`)

*Introduction to front-end programming for back-end developers*: a six-module curriculum built for back-end and infrastructure developers, intended as support for an oral presentation and explicitly an introduction rather than expert material. Prerequisites: basics of HTTP, the browser (DOM, developer console), HTML/CSS, general programming, and some JavaScript experience. Before starting, readers are directed to [grab/front-end-guide](https://github.com/grab/front-end-guide). The curriculum:

1. **Modern JavaScript** — quirks and casting, `===` vs. `==`, prototypes, object/array destructuring, `let`/`const` and hoisting, arrow functions, classes, template literals, loops, promises and async functions, modules, optional chaining, plus a self-assessment. Code can be run quickly on CodeSandbox; an `examples/hoisting.html` demo and reference images are included.
2. **React** — DOM manipulation refresher, the official React tutorial, setting up React in a Vanilla JS CodeSandbox, an exercise, and self-assessment questions.
3. **TypeScript** — the official handbook introductions (for JS, OOP, and FP developers), structural vs. nominal typing, and TypeScript exercises.
4. **The browser** — reading and manipulating the DOM; events.
5. **CSS & HTML: restart** — modern technologies and methodologies; accessibility.
6. **Front-end development practices** — building a professional web app: dependency management (npm/yarn), testing (Jest), code style (Prettier, ESLint), security (HTTPS, CORS, XSS, CSP, OWASP), state management (Redux, MobX, hooks), backend interaction (GraphQL/Apollo), error boundaries, CSS-in-JS (styled-components, Emotion) and frameworks (Material UI, Tailwind CSS), developer experience (Storybook), bundling/compiling/deploying (webpack, Parcel, Rollup, Babel; SSR vs. CSR vs. SSG), monitoring (Sentry), performance (Lighthouse, DevTools), and PWAs.

A learning-roadmap image (from kamranahmedse/developer-roadmap) and further resources round out the track.

### Web development (`training/web-dev/`)

*Learning web development*: an opinionated ramp-up program for web developers requiring little more than general knowledge of computers and the Internet. Principles: focus on the main stuff, treat best practices as part of programming, go wide and deep, learn by doing through exercises, and lean on videos. The roadmap is: (1) pick a programming language, (2) make a first pass at the web environment (HTTP, Git, Docker and `docker-compose`, command line, text editor), (3) write a full-fledged exercise and get it reviewed, (4) tackle advanced topics. Advice includes mastering a powerful text editor (VSCode or Vim) and achieving deep proficiency in one language (Python or TypeScript recommended), with exercises (Exercism, build-your-own-x) and topic-specific reading lists covering best practices, code architecture and design patterns, databases and SQL, dev environment and Linux, distributed systems, network/HTTP, project management, security, and Git. The selection is drawn from [charlax/professional-programming](https://github.com/charlax/professional-programming).

### Python (`training/learning-python/`)

A pointer to the separate [python-education](https://github.com/charlax/python-education) repository.

## Cheat sheets (`cheatsheets/`)

- `Clean-Architecture-V1.0.pdf`
- `Clean-Code-V2.4.pdf`

## Essays and reference

### `feature-flags.md`

Makes the case for feature flags: **velocity** (disable features faster than re-deploying), **testing** (flags force owners to exercise the flow), **code iterations** (smaller, safer pull requests), and **gradual rollout** (per-city or per-group activation, A/B testing). It also discusses judgment calls: skip flags for simple copy/log changes, fast rollbacks, or safe asynchronous jobs; use them for large refactors, changing integration points, performance optimizations, and new flows. References Martin Fowler's *FeatureToggle*, Flickr's *Flipping Out*, and a Travis CI post.

### `glossary.md`

Definitions with sources, including conceptual integrity (Fred Brooks), the end-to-end principle, NIHITO, stability and reliability (ISO/IEC 9126), the Two Generals' Problem, the Law of Demeter, blackbox/whitebox monitoring, and the second-system effect.

## Development

The repository is primarily Markdown documents and PDFs, plus a handful of Python example scripts. Development tooling is handled with [pre-commit](https://pre-commit.com/).

### Setup

Install `pre-commit` (e.g. with pipx), then install the hooks:

```bash
pre-commit install
```

### Configured hooks

Defined in `.pre-commit-config.yaml`:

- `pre-commit-hooks` (v2.3.0): `check-yaml`, `end-of-file-fixer`, `trailing-whitespace`
- `black` (19.3b0): formats the Python example files
- `doctoc` (v1.4.0): regenerates the `## Table of Contents` blocks at the top of most documents

Because most Markdown files start with a doctoc-generated table of contents, do not edit those sections by hand — re-run doctoc (the hook does this) to update them instead.

## Testing

There is no automated test suite; the repository consists mostly of documentation. The Python examples can be executed directly to observe the behavior they illustrate:

```bash
python antipatterns/sqlalchemy-examples/exists.py            # requires SQLAlchemy
python antipatterns/python-examples/reraise_exceptions_good.py
python antipatterns/python-examples/reraise_exceptions_bad.py  # intentionally raises
```

`exists.py` creates an in-memory SQLite table and prints the SQL produced by the "bad" (`SELECT ... LIMIT 1`) and "good" (`SELECT EXISTS (...)`) existence checks. The "bad" re-raise example raises on purpose, showing how the original `NameError` traceback is replaced by a generic `ToastException`, while the "good" version logs and re-raises the original error.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The main requirement is enabling the pre-commit hooks (see Development above) so formatting, whitespace, YAML checks, and table-of-contents generation stay consistent.

## License

Released under the [MIT License](LICENSE). Copyright (c) 2017 Charles-Axel Dein.
