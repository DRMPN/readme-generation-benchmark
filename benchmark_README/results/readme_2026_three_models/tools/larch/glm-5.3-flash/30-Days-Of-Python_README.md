# 🐍 30 Days Of Python

![30 Days of Python banner](./30DaysOfPython_banner3@2x.png)

> 🎯 **30 Days Of Python** — a step-by-step challenge to learn the Python programming language from scratch in 30 days. Each day covers a new topic with explanations, code examples, and hands-on exercises using real datasets.

---

## 📖 About

This repository contains a complete **30-day Python programming curriculum**. It starts with the absolute basics — installing Python, the shell, and variables — and progressively builds up to advanced topics such as file handling, regular expressions, object-oriented programming, web scraping, data analysis with **Pandas**, web development with **Flask**, working with **APIs**, and **MongoDB**.

Each day has its own markdown lesson (`NN_topic.md`) with theory, code snippets, exercises, and mini-projects. Supporting datasets (speeches, CSVs, JSON files) are included so all exercises can be completed offline.

**Who is this for?**
- Beginners with no prior programming experience
- Developers coming from other languages who want to pick up Python
- Anyone following the "learn one topic per day" challenge format

---

## 🗂️ Repository Structure

```
30-Days-Of-Python-s42zrgdq
│
├── 02_variables_builtin_functions.md   # Daily lessons (Day 2 – Day 30)
├── ...
├── 30_conclusions.md
│
├── helloworld.py, variables.py, day_3.py ...   # Code written during lessons
├── mymodule.py, arithmetic.py, greet.py        # Module / package examples
├── app.py, requirements.txt, Procfile          # Flask web app (Day 26+)
├── home.html, layout.html, about.html ...      # Flask templates
├── main.css                                    # Stylesheet
│
├── countries.py, stop_words.py                 # Data helper modules
├── obama_speech.txt, romeo_and_juliet.txt ...  # Text corpora for exercises
├── countries_data.json, cats.json ...          # JSON datasets
├── weight-height.csv, hacker_news.csv ...      # CSV datasets
├── excel_example.xlsx, xml_example.xml         # Other formats
│
├── *.png                                       # Screenshots & diagrams used in lessons
├── readme.md + readme4-6.md ...                # Grouped day summaries
└── *_cn.md / *_ko.md                           # Chinese / Korean translations
```

---

## 📅 Table of Contents — The 30 Days

| Day | Topic | Lesson File |
|:---:|-------|-------------|
| 1 | Introduction & Getting Started (Hello, World!) | `readme.md` |
| 2 | Variables & Built-in Functions | [02_variables_builtin_functions.md](./02_variables_builtin_functions.md) |
| 3 | Operators | [03_operators.md](./03_operators.md) |
| 4 | Strings | [04_strings.md](./04_strings.md) |
| 5 | Lists | [05_lists.md](./05_lists.md) |
| 6 | Tuples | [06_tuples.md](./06_tuples.md) |
| 7 | Sets | [07_sets.md](./07_sets.md) |
| 8 | Dictionaries | [08_dictionaries.md](./08_dictionaries.md) |
| 9 | Conditionals | [09_conditionals.md](./09_conditionals.md) |
| 10 | Loops | [10_loops.md](./10_loops.md) |
| 11 | Functions | [11_functions.md](./11_functions.md) |
| 12 | Modules | [12_modules.md](./12_modules.md) |
| 13 | List Comprehension | [13_list_comprehension.md](./13_list_comprehension.md) |
| 14 | Higher Order Functions | [14_higher_order_functions.md](./14_higher_order_functions.md) |
| 15 | Python Type Errors | [15_python_type_errors.md](./15_python_type_errors.md) |
| 16 | Python DateTime | [16_python_datetime.md](./16_python_datetime.md) |
| 17 | Exception Handling | [17_exception_handling.md](./17_exception_handling.md) |
| 18 | Regular Expressions | [18_regular_expressions.md](./18_regular_expressions.md) |
| 19 | File Handling | [19_file_handling.md](./19_file_handling.md) |
| 20 | Python Package Manager (pip) | [20_python_package_manager.md](./20_python_package_manager.md) |
| 21 | Classes and Objects | [21_classes_and_objects.md](./21_classes_and_objects.md) |
| 22 | Web Scraping | [22_web_scraping.md](./22_web_scraping.md) |
| 23 | Virtual Environments | [23_virtual_environment.md](./23_virtual_environment.md) |
| 24 | Statistics | [24_statistics.md](./24_statistics.md) |
| 25 | Pandas | [25_pandas.md](./25_pandas.md) |
| 26 | Python Web (Flask) | [26_python_web.md](./26_python_web.md) |
| 27 | Python with MongoDB | [27_python_with_mongodb.md](./27_python_with_mongodb.md) |
| 28 | APIs | [28_API.md](./28_API.md) |
| 29 | Building an API | [29_building_API.md](./29_building_API.md) |
| 30 | Conclusions | [30_conclusions.md](./30_conclusions.md) |

> 🌍 **Translations included:** several lessons are also available in **Chinese (`_cn.md`)** and **Korean (`_ko.md`)**.

> 📚 **Grouped summaries:** `readme4-6.md`, `readme7-9.md`, `readme10-12.md`, `readme13-15.md`, `readme16-18.md`, `readme19-21.md`, `readme22-24.md`, `readme25-27.md`, `readme28-30.md` provide condensed recaps per three-day block.

---

## 📊 Datasets & Resources

The lessons come with real-world datasets used for the exercises:

**📝 Text / Speeches**
- `obama_speech.txt`, `michelle_obama_speech.txt`
- `donald_speech.txt`, `melina_trump_speech.txt`
- `romeo_and_juliet.txt`
- `email_exchanges.txt`, `email_exchanges_big.txt`
- `reading_file_example.txt`, `example.txt`
- `stop_words.py` — list of English stop words for text processing

**🧾 JSON**
- `countries_data.json`, `countries_data_long.json` — country population, languages, currencies
- `cats.json`, `json_example.json`, `scrapped_data.json`

**📈 CSV / Excel / XML**
- `weight-height.csv` — statistics & Pandas exercises
- `hacker_news.csv`, `HN_posts_year_to_Sep_26_2016.csv` — filtering & aggregation practice
- `fortune_500_companies_2017.csv`, `F500.csv`, `fortune1000_final.csv`, `result.csv`
- `csv_example.csv`, `excel_example.xlsx`, `xml_example.xml`

**🐍 Python data modules**
- `countries.py` — country helper functions
- `stop_words.py` — stop word list for regex/text-cleaning tasks

---

## 🖥️ Code Samples

Example scripts created throughout the challenge:

- **Basics:** `helloworld.py`, `variables.py`, `day_3.py`, `day_4.py`, `day_5.py`
- **Modules:** `mymodule.py`, `arithmetic.py` / `arithmetics.py`, `greet.py`, `__init__.py` — demonstrating imports and packages
- **Flask app (Day 26):**
  - `app.py` — main application
  - `requirements.txt` — dependencies
  - `Procfile` — deployment configuration (Heroku-ready)
  - Templates: `layout.html`, `home.html`, `about.html`, `post.html`, `result.html`
  - Static assets: `main.css`

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.6+** installed — [download here](https://www.python.org/downloads/)
- A code editor — [VS Code](https://code.visualstudio.com/) is recommended
- Git (optional, for cloning)

### Setup

```bash
# 1. Clone the repository
git clone <repository-url>
cd 30-Days-Of-Python-s42zrgdq

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies (needed from Day 20 onward)
pip install -r requirements.txt
```

### Running the Lessons

Open any day's markdown file and follow along. Run the example scripts directly:

```bash
python helloworld.py
python day_5.py
```

### Running the Flask App (Day 26)

```bash
python app.py
# Open http://127.0.0.1:5000 in your browser
```

---

## 🗓️ Suggested Learning Path

| Phase | Days | Focus |
|:-----:|:----:|-------|
| 🌱 Foundations | 1–8 | Syntax, data types, built-in data structures |
| 🔀 Control Flow | 9–12 | Conditionals, loops, functions, modules |
| ⚡ Intermediate | 13–18 | Comprehensions, HOFs, errors, datetime, regex |
| 💾 Working with Data | 19–25 | Files, packages, OOP, scraping, statistics, Pandas |
| 🌐 Real-World Python | 26–30 | Flask, MongoDB, APIs, building your own API |

**Tips for success:**
1. ✅ Complete **one day per day** — don't rush ahead
2. ✍️ Type out all the examples yourself instead of copy-pasting
3. 🧪 Do the exercises at the end of each lesson
4. 💾 Keep a notebook or journal of what you learned each day

---

## 🙏 Credits

This repository is based on the well-known **30 Days of Python** challenge originally created by **[Asabeneh Yetayeh](https://github.com/Asabeneh/30-Days-Of-Python)**, including community translations (Chinese, Korean).

---

## 📄 License

Educational content — free to use for learning purposes. See the original project for licensing details.

---

<div align="center">

**Happy Coding! 🚀** — *30 days from zero to building APIs with Python.*

</div>
