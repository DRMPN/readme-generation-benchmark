# devops-exercises-sztbje1t

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This repository is a knowledge base for preparing for DevOps, SRE, and production engineering interviews. It provides a large collection of question-and-answer material, hands-on exercises with solutions, and preparation guides spanning topics such as cloud platforms, containers, infrastructure as code, CI/CD, Linux, programming, security, and observability. It is aimed at job candidates preparing for interviews as well as practitioners self-studying these areas. Beyond the written content, it includes a small set of helper scripts for self-quizzing and content maintenance, and contributors can follow a documented format for adding new material. See Getting Started for runnable steps and ways to navigate the material.

---

## Core Features

- **Extensive DevOps/SRE question bank** — Interview questions and answers spanning Kubernetes, AWS/Azure/GCP, Terraform, Ansible, Linux, Python, Git, security, and more, letting candidates quickly review and self-assess their technical knowledge.
- **Hands-on exercises with solutions** — Practice real-world scenarios through exercises that include sample applications, CI pipelines, and infrastructure-as-code examples, many with solutions to check your work.
- **Interactive self-quiz mode** — A command-line quiz that randomly presents questions, reveals answers on demand, and can skip questions without documented answers for focused practice.
- **Structured interview preparation guide** — Opinionated guidance on required skills, converting job requirements into practice scenarios, building personal DevOps projects, and handling the interview process itself.
- **Automated content maintenance** — Helper scripts that count questions and exercises and keep the displayed totals up to date, so contributors can extend the content without manual bookkeeping.

---

## Installation

**Using the current local checkout:**

1. Open the repository root:

```sh
cd path/to/devops-exercises-sztbje1t
```

No further setup is required at the repository root: the quiz script uses only the Python 3 standard library, and the learning material is plain Markdown. Note that any `requirements.txt` files found inside `exercises/` belong to those exercises' sample applications and are not needed to use the repository itself.

---

## Getting Started

**Prerequisites**

- Python 3 for the quiz script (it uses only the standard library, so no extra packages are required)
- Git, to clone the repository

**Quickstart**

1. Clone this repository and change into its directory.

2. Browse the content: `README.md` contains the main question/answer list, and `topics/` holds per-subject material (e.g., Linux, Kubernetes, Terraform, AWS). Many exercises include a `solutions/` directory. The repository also includes `faq.md` (frequently asked questions) and `credits.md` (project credits).

3. Optional: read `prepare_for_interview.md` for an opinionated guide on preparing for DevOps/SRE interviews.

4. Quiz yourself with randomly selected questions:

```bash
python scripts/random_question.py        # one question at a time, drawn from README.md
python scripts/random_question.py -s     # skip questions without a documented answer
```

Run the script from the repository root (it reads `README.md` from the current directory). Press Enter to reveal each answer and Ctrl-C to exit.

5. Optional: practice the challenges in `exercises/` and the exercise sections of each `topics/*/README.md`, then compare your work with the provided solutions.

---

## Testing

Verification for this repository combines a local CI script, a small Python test suite, and hosted CI.

- **Local checks:** Before submitting a pull request, test your changes locally with the `run_ci.sh` script in the `scripts/` directory, as described in [CONTRIBUTING.md](CONTRIBUTING.md).
- **Test suite:** The `tests/` directory contains:
  - `syntax_checker_unittest.py` and `syntax_lint.py` — validation of question/content formatting.
  - `scripts_question_utils_unittest.py` — tests for the question helper utilities in `scripts/question_utils.py`.
  - `testcases/` — test case files used by these checks.
- **Doctests:** `scripts/question_utils.py` executes its doctests when run directly (`doctest.testmod()` under `__main__`).
- **CI:** Automated CI is configured via `.travis.yml` and `.github/workflows/`.
- **Content consistency:** After adding questions, `scripts/count_questions.sh` recounts questions/exercises and updates the count in `README.md`, and `scripts/update_question_number.py` refreshes the question counter — both help keep content stats accurate.

Note: this project is a content knowledge base, so testing focuses mainly on question formatting and helper scripts rather than a runnable application. Exact invocation syntax for the individual files in `tests/` is not documented here; use `scripts/run_ci.sh` for the supported local check.

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to devops-exercises-sztbje1t.

---

## License

The project's licensing terms are defined in the [LICENSE](./LICENSE) file. Refer to that file for full details.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). devops-exercises-sztbje1t repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{devops-exercises-sztbje1t,

        author = {README Benchmark},

        title = {devops-exercises-sztbje1t repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---