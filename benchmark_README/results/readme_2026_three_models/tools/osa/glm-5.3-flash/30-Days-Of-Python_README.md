# 30-Days-Of-Python-bpiiz7cp

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [Citation](#citation)

---

## Overview

30 Days Of Python is a beginner-oriented, self-study curriculum that teaches Python from first steps through functions, file handling, data analysis, and building a web application. It is written for learners new to Python, as well as educators who want to reuse or translate the material. The repository is organized as a day-by-day sequence of written lessons paired with small runnable example scripts, sample datasets, and a self-contained demo web application at the end of the course. Translated versions of the lessons are available in several languages. See Getting Started for how to begin with Day 1.

---

## Core Features

- A structured 30-day Python curriculum that takes learners from basics like variables and functions to OOP, file handling, and web/database topics.
- Small, runnable Python example scripts accompanying each day's lesson, so concepts can be practiced immediately.
- A sample Flask web application with templates and static assets, demonstrating web development with Python.
- Reusable teaching materials, including custom packages and modules plus sample datasets for hands-on data exercises.
- Community translations in Chinese, Korean, and Portuguese, making the curriculum accessible to non-English learners.

---

## Installation

Most lesson examples run with a standard Python installation and require no additional packages. The Day 26 Flask demo has its own dependency manifest:

```sh
cd python_for_web
pip install -r requirements.txt
```

---

## Getting Started

**Prerequisites**

- Python installed on your machine. The lesson examples run with the standard interpreter; the only pinned dependencies in the repo belong to the Day 26 Flask demo (`python_for_web/requirements.txt`).

**Steps**

1. Clone or download this repository.
2. Open `01_Day_Introduction/` and follow the lesson Markdown inside. Work through the numbered day folders in order, from `01_Day_Introduction` to `30_Day_Conclusions`.
3. Run the example scripts shipped with each day, for example with `python <script>.py` from the corresponding day folder.
4. Use the practice datasets in `data/` (for example, `countries-data.py`) for the lesson exercises.
5. Optionally, run the sample Flask app from Day 26:

```bash
   cd python_for_web
   pip install -r requirements.txt
   python app.py
```

   Then open `http://localhost:5000` in your browser (the app serves on port 5000 by default).

---

## Contributing

Contributions to improve or extend the lessons are welcome. Translated versions of the curriculum already exist in several languages; if you would like to add a new translation or fix lesson content, open an issue or submit a pull request.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). 30-Days-Of-Python-bpiiz7cp repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{30-Days-Of-Python-bpiiz7cp,

        author = {README Benchmark},

        title = {30-Days-Of-Python-bpiiz7cp repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---