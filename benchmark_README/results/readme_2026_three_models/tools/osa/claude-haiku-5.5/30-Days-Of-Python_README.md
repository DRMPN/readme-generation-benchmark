# 30 Days Of Python Programming

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Examples](#examples)
- [Documentation](#documentation)
- [Citation](#citation)

---

## Overview

This repository is a beginner-oriented Python course titled "30 Days Of Python Programming." It is organized as day-by-day lessons, each covering a specific Python topic and accompanied by example programs that use the standard library. It is intended primarily for novice programmers learning Python, and secondarily for instructors and translators, since the material is available in multiple language editions. The repository also includes a small Flask web application, a "Text Analyzer" demo, that serves as a secondary resource for learners exploring web development. New readers should start with the lessons for the core learning path, and see Getting Started for runnable steps.

---

## Core Features

- **Step-by-step Python lessons:** Day-by-day Markdown lessons paired with runnable example scripts let developers learn Python progressively from fundamentals onward.
- **Translated editions:** Parallel language editions of the lessons let learners study the material in their preferred language.
- **Module and package examples:** Working examples of importing functions, data, and packages show beginners how to organize and reuse Python code.
- **Small Flask web demo:** A minimal Flask web app, a Text Analyzer, gives web-development learners a working reference for serving pages with Flask.

---

## Installation

Install 30-Days-Of-Python-9kiwk0ga from the current local checkout:

1. Open the repository root:

```sh
   cd path/to/30-Days-Of-Python-9kiwk0ga
```

2. Install the Flask demo's dependencies as described in [Getting Started](#getting-started).

---

## Getting Started

This repository contains Python lessons and a small Flask demo app.

**Prerequisites**

- Python installed on your machine
- `pip` available in your terminal

**Quickstart: run the Flask demo**

1. Get the repository files on your machine.
2. Install the Flask app's pinned dependencies:

```bash
pip install -r python_for_web/requirements.txt
```

3. Start the app:

```bash
python python_for_web/app.py
```

4. Optionally, set the `PORT` environment variable before starting. The app reads it with `os.environ.get("PORT")`.
5. Open the URL shown in the terminal output.

---

## Examples

The day-by-day lessons are Markdown files with paired Python example scripts. For example, `12_Day_Modules/mymodule.py` defines functions and values used in the Day 12 modules lesson. Read the lesson Markdown alongside its scripts.

---

## Documentation

The lessons are written in Markdown, with one lesson per day. The material is also available in multiple language editions, so learners can study it in their preferred language.

---

## Citation

### APA format:

```text
README Benchmark (2026). 30-Days-Of-Python-9kiwk0ga repository [Computer software].
```

### BibTeX format:

```bibtex
@misc{30-Days-Of-Python-9kiwk0ga,
    author = {README Benchmark},
    title = {30-Days-Of-Python-9kiwk0ga repository},
    year = {2026}
}
```

---