# Professional Programming

A collection of resources and materials for professional programming: curated lists of quality articles, training materials for developers, and notes on software engineering practices such as antipatterns and feature flags.

This repository was created by Charles-Axel Dein and is licensed under the MIT license (see [LICENSE](./LICENSE)).

## Contents

- [`antipatterns/`](./antipatterns/) — a list of antipatterns:
  - [Code antipatterns](./antipatterns/code-antipatterns.md)
  - [SQLAlchemy antipatterns](./antipatterns/sqlalchemy-antipatterns.md) (with Python examples in [`antipatterns/python-examples/`](./antipatterns/python-examples/) and [`antipatterns/sqlalchemy-examples/`](./antipatterns/sqlalchemy-examples/))
  - [Error handling antipatterns](./antipatterns/error-handling-antipatterns.md)
  - [Tests antipatterns](./antipatterns/tests-antipatterns.md)
  - [MVCs antipatterns](./antipatterns/mvcs-antipatterns.md)
  - [Database antipatterns](./antipatterns/database-antipatterns.md)
  - [Scalability antipatterns](./antipatterns/scalability-antipatterns.md)
  - Related images, such as the test pyramid ([`antipatterns/images/`](./antipatterns/images/))
- [`training/`](./training/) — training materials:
  - [Learning web development](./training/web-dev/README.md) — an opinionated ramp-up program for web developers, with prerequisites of little more than general knowledge about computers and the Internet
  - [Introduction to front-end programming for back-end developers](./training/front-end/README.md) — a course covering modern JavaScript, React, TypeScript, the browser, CSS/HTML, and front-end development practices
  - [Learning Python](./training/learning-python/README.md) — points to the related repository [charlax/python-education](https://github.com/charlax/python-education)
- [`cheatsheets/`](./cheatsheets/) — PDF cheatsheets:
  - [Clean Architecture (V1.0)](./cheatsheets/Clean-Architecture-V1.0.pdf)
  - [Clean Code (V2.4)](./cheatsheets/Clean-Code-V2.4.pdf)
- [`images/`](./images/) — diagrams and illustrations referenced by the materials (MVP, cost of defects, tech debt, clean architecture cone, premature optimization, and more)
- [`feature-flags.md`](./feature-flags.md) — why use feature flags (velocity, testing, code iterations, gradual rollout) and when *not* to use them
- [`glossary.md`](./glossary.md) — definitions of terms such as conceptual integrity, the end-to-end principle, stability and reliability (per ISO/IEC 9126), the Law of Demeter, and the second-system effect

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](./CONTRIBUTING.md).

### Development setup

The repository uses [pre-commit](https://pre-commit.com/) hooks to check YAML, fix end-of-file and trailing-whitespace issues, run [Black](https://github.com/psf/black) on the Python examples, and regenerate the tables of contents with [doctoc](https://github.com/thlorenz/doctoc).

```bash
# install pre-commit (e.g. with pipx), then:
pre-commit install
```
