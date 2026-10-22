# 30 Days of Python

A 30-day Python programming course, with lessons in English, Chinese, and Korean, plus practice exercises, example scripts, sample datasets, and small projects. It covers Python from basic syntax through data analysis, web scraping, databases, and building APIs.

> **Note:** This README was written from the file listing alone. Folder placement is inferred from file names, and some details (such as the exact contents of `app.py` or `requirements.txt`) should be checked against the source files.

---

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Course Curriculum](#course-curriculum)
- [Languages](#languages)
- [Getting Started](#getting-started)
- [How to Use This Course](#how-to-use-this-course)
- [Example Scripts](#example-scripts)
- [Projects](#projects)
- [Data Files](#data-files)
- [Images and Assets](#images-and-assets)
- [Contributing](#contributing)
- [License and Acknowledgments](#license-and-acknowledgments)

---

## Overview

This repository is organized as a day-by-day course. Each day has a Markdown lesson that explains a topic, shows code examples, and usually ends with an exercise. Supporting Python scripts, sample datasets, and a small web application are included so that learners can run code and work with real data.

The course is suited to:

- Complete beginners who have never programmed
- Developers from other languages who want a structured introduction to Python
- Learners who want practical exposure to data analysis, web scraping, databases, and APIs

---

## Repository Structure

The listing suggests the following layout. Some files appear to be duplicated across folders (for example, `09_conditionals.md` and `17_exception_handling.md` each appear twice), which is likely because each lesson exists in more than one folder or language.

```
30-Days-Of-Python/
├── README.md                     # Main project overview
├── readme*.md                    # Per-range readme files (readme1-3, readme4-6, ..., readme28-30)
│
├── 01–30 lesson files (.md)      # English lessons, one per day
├── *_cn.md                       # Chinese lessons
├── *_ko.md                       # Korean lessons (Days 4, 7, 10, and readme)
│
├── Example and exercise scripts  # day-3.py, day_4.py, day_5.py, helloworld.py, variables.py, etc.
├── Module examples               # arithmetic.py, arithmetics.py, greet.py, mymodule.py, __init__.py, main.py
├── Data-processing scripts       # countries.py, countries-data.py, stop_words.py
│
├── Datasets                      # CSV, JSON, TXT, XLSX, XML files
├── Web application               # app.py, templates, static assets, Procfile, requirements.txt
│
└── Images                        # PNG screenshots used in lessons
```

### Key Components

| Component | Purpose |
|---|---|
| Lesson Markdown files | Core course content, one per day |
| `*_cn.md` files | Chinese translations of lessons |
| `*_ko.md` files | Korean translations of selected lessons |
| `day_*.py`, `day-3.py` | Practice scripts for specific days |
| `arithmetic.py`, `greet.py`, `mymodule.py`, `__init__.py` | Examples for modules and packages |
| `countries.py`, `countries-data.py` | Scripts for working with country data |
| `stop_words.py` | Stop-word list used in text analysis |
| Datasets | Used in the data analysis, pandas, statistics, and web scraping lessons |
| Web app files | A small Flask-style web application with templates and deployment files |

---

## Course Curriculum

| Day | Topic | Description |
|:---:|---|---|
| 1 | Getting Started | Installing Python, setting up the environment, running the first program |
| 2 | Variables and Built-in Functions | Naming variables, data types, and common built-in functions |
| 3 | Operators | Arithmetic, comparison, logical, and assignment operators |
| 4 | Strings | String creation, methods, formatting, and indexing |
| 5 | Lists | Creating and manipulating ordered collections |
| 6 | Tuples | Immutable sequences and their uses |
| 7 | Sets | Unique unordered collections and set operations |
| 8 | Dictionaries | Key-value data structures |
| 9 | Conditionals | `if`, `elif`, `else`, and decision logic |
| 10 | Loops | `for` and `while` loops, `break`, and `continue` |
| 11 | Functions | Defining and calling functions, parameters, and return values |
| 12 | Modules | Importing and creating modules |
| 13 | List Comprehension | Concise syntax for building lists |
| 14 | Higher-Order Functions | `map`, `filter`, `reduce`, and functions as arguments |
| 15 | Python Type Errors | Common type errors and how to handle them |
| 16 | Python Datetime | Working with dates and times |
| 17 | Exception Handling | `try`, `except`, `finally`, and raising errors |
| 18 | Regular Expressions | Pattern matching with the `re` module |
| 19 | File Handling | Reading and writing text, CSV, JSON, and other files |
| 20 | Python Package Manager | Using `pip` to install and manage packages |
| 21 | Classes and Objects | Object-oriented programming basics |
| 22 | Web Scraping | Extracting data from websites |
| 23 | Virtual Environment | Creating and managing isolated Python environments |
| 24 | Statistics | Statistical calculations with Python |
| 25 | Pandas | Data analysis with `Series` and `DataFrame` |
| 26 | Python Web | How the web works and building web pages with Python |
| 27 | Python with MongoDB | Connecting Python to a MongoDB database |
| 28 | API | Understanding and consuming APIs |
| 29 | Building an API | Creating your own API |
| 30 | Conclusions | Review and next steps |

Day 1 has no separate lesson file in the listing. Its content is likely covered in `readme.md` or the first `readme` file.

---

## Languages

Lessons are available in multiple languages:

- **English:** `01`–`30` `.md` files (the primary version)
- **Chinese (中文):** Files ending in `_cn.md`, covering Days 15–30 and including the conclusion
- **Korean (한국어):** Files ending in `_ko.md` for Days 4, 7, and 10, plus `readme_ko.md`

The English lessons are the most complete. Other languages may cover fewer days.

---

## Getting Started

### Prerequisites

- Python 3.7 or newer (3.8+ is recommended for the data and web lessons)
- A code editor such as VS Code
- A terminal or command prompt
- Git (to clone the repository)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd 30-Days-Of-Python-2o8b90rx
   ```

2. **Check your Python version**

   ```bash
   python --version
   # or
   python3 --version
   ```

3. **Create a virtual environment** (recommended, see Day 23)

   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate         # Windows
   ```

4. **Install the dependencies**

   The web application and some lessons need additional packages. Install them from the requirements file:

   ```bash
   pip install -r requirements.txt
   ```

   Lessons on pandas, statistics, web scraping, MongoDB, and APIs may need extra packages such as `pandas`, `numpy`, `requests`, `beautifulsoup4`, `pymongo`, and `openpyxl` (for the Excel file). Install them with `pip` as needed.

---

## How to Use This Course

1. **Read the lesson** for the day you are working on (for example, `05_lists.md`).
2. **Run the examples** in a Python shell or a script file.
3. **Try the exercises** at the end of each lesson.
4. **Check the related scripts** (such as `day_4.py` or `day_5.py`) for extra practice.
5. **Use the datasets** in the data lessons to apply what you have learned to real data.

Suggested learning path:

- **Days 1–10:** Core syntax and data structures
- **Days 11–17:** Functions, modules, and error handling
- **Days 18–24:** Regular expressions, file handling, OOP, web scraping, and statistics
- **Days 25–30:** Data analysis, web development, databases, and APIs

---

## Example Scripts

| File | Likely Purpose |
|---|---|
| `helloworld.py` | First program, printing a message |
| `variables.py` | Variable and data type examples |
| `day-3.py`, `day_4.py`, `day_5.py` | Practice code for Days 3, 4, and 5 |
| `arithmetic.py` / `arithmetics.py` | Arithmetic examples, likely for the modules lesson |
| `greet.py` | A simple function or module example |
| `mymodule.py` | A custom module that can be imported |
| `__init__.py` | Marks a folder as a Python package |
| `main.py` | Entry point that imports other modules |
| `countries.py` / `countries-data.py` | Work with country data from JSON or CSV |
| `stop_words.py` | Common stop words for text processing |

---

## Projects

### Web Application

The web application uses HTML templates and static assets and includes deployment files. It appears to be a small Flask-style site.

| File | Purpose |
|---|---|
| `app.py` | Main application file that defines routes |
| `layout.html` | Base template shared by pages |
| `home.html`, `about.html`, `post.html` | Page templates |
| `result.html` | Template for displaying results |
| `main.css` | Stylesheet |
| `Procfile` | Tells a hosting platform (such as Heroku) how to start the app |
| `requirements.txt` | Lists the Python packages the app needs |

**Running the application locally** (assuming a Flask app):

```bash
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000` in your browser. Check `app.py` for the actual port and startup command.

**Deploying:** The `Procfile` suggests the app can be deployed to Heroku or a similar service. Check the file for the exact start command.

---

## Data Files

The datasets support several lessons. Each file is listed below with its likely use.

### Structured Data (CSV)

| File | Likely Use |
|---|---|
| `weight-height.csv` | Statistics and pandas exercises |
| `fortune_500_companies_2017.csv`, `F500.csv`, `fortune1000_final.csv` | Pandas and data analysis (company rankings) |
| `hacker_news.csv`, `HN_posts_year_to_Sep_26_2016.csv` | Data analysis of Hacker News posts |
| `csv_example.csv` | Reading and writing CSV files (Day 19) |
| `result.csv` | Output file from a script |

### Structured Data (JSON and XML)

| File | Likely Use |
|---|---|
| `countries_data.json`, `countries_data_long.json` | Working with country data |
| `cats.json` | JSON parsing practice |
| `json_example.json` | JSON file handling (Day 19) |
| `scrapped_data.json` | Output from a web scraping exercise (Day 22) |
| `xml_example.xml` | XML parsing practice |

### Excel

| File | Likely Use |
|---|---|
| `excel_example.xlsx` | Reading Excel files with Python |

### Text Files

| File | Likely Use |
|---|---|
| `romeo_and_juliet.txt` | Text analysis and string processing |
| `obama_speech.txt`, `michelle_obama_speech.txt`, `melina_trump_speech.txt`, `donald_speech.txt` | Text analysis, word counting, and comparison |
| `email_exchanges.txt`, `email_exchanges_big.txt` | Pattern matching with regular expressions |
| `example.txt`, `reading_file_example.txt` | File handling examples (Day 19) |

---

## Images and Assets

The PNG files are screenshots and diagrams used in the Markdown lessons. They illustrate:

- Installing Python on Windows, macOS, and Linux
- Using VS Code and the Python shell
- Operator and data type diagrams (comparison, identity, and logical operators)
- Indexing diagrams for strings, lists, and tuples
- Exception handling flow (`try_except.png`)
- Pandas `Series` and `DataFrame` examples
- MongoDB Atlas setup steps (sign-up, cluster creation, user setup, and IP access)
- API and HTTP request/response diagrams
- Postman usage for API testing
- Regular expressions (`regex.png`)

---

## Contributing

Contributions are welcome. You can help by:

1. **Fixing errors** in lessons or code
2. **Adding translations** to a language that is missing a lesson
3. **Improving exercises** or adding new examples
4. **Reporting issues** you find while working through a lesson

To contribute:

1. Fork the repository.
2. Create a branch for your change (`git checkout -b fix/day-10-loops`).
3. Make your changes and test any code you modify.
4. Commit with a clear message and open a pull request.

Please keep translations consistent with the English version, and place each translated file next to the original with the matching suffix (`_cn` or `_ko`).

---

## License and Acknowledgments

Check the repository for a `LICENSE` file for the terms of use. This project appears to be based on the *30 Days of Python* course by Asabeneh Yetayeh. The original course has been translated into several languages by community contributors.

Thank you to everyone who wrote, translated, reviewed, and contributed to these lessons.

---

Happy coding!
