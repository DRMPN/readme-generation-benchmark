# 30 Days of Python

A 30-day Python programming course in Markdown, with accompanying code samples, datasets, images, a small Flask web application, and translations into Chinese, Korean, and Portuguese.

![30 Days of Python banner](images/30DaysOfPython_banner3@2x.png)

## Contents

- [About](#about)
- [Repository Layout](#repository-layout)
- [Course Outline](#course-outline)
- [Translations](#translations)
- [Code Samples](#code-samples)
- [Web Application (`python_for_web`)](#web-application-python_for_web)
- [Datasets](#datasets)
- [Getting Started](#getting-started)
- [Known Issues](#known-issues)
- [Credits](#credits)

## About

The course covers Python 3 from first steps through web development, data work, and APIs. Each day is a Markdown lesson that explains a topic, includes examples, and ends with exercises. The Day 30 conclusion notes that, after completing the exercises and projects, learners can move toward data analysis, data science, machine learning, or web development.

The course is written for beginners and for experienced programmers who want to learn Python.

## Repository Layout

| Path | Contents |
| --- | --- |
| `01_Day_Introduction/` ... `30_Day_Conclusions/` | English lesson files, one folder per day, each with a `.md` lesson (Day 1 has only a code sample, see [Known Issues](#known-issues)) |
| `Chinese/` | Chinese translation of the lessons, with its own `README.md` |
| `Korean/`, `korean/` | Korean translation (`Korean/` holds more files; `korean/` contains `readme.md` and one lesson) |
| `Portuguese/` | Portuguese translation, with its own `README.md` |
| `old_files/` | Earlier single-file and multi-part versions of the course README |
| `python_for_web/` | Flask web application used in Day 26 |
| `mypackage/` | Small example package (`greet.py`, `arithmetics.py`, `__init__.py`) |
| `20_Day_Python_package_manager/` | Day 20 lesson with `greet.py`, `arithmetic.py`, and `__init__.py` example files |
| `mymodule.py`, `12_Day_Modules/` | Module examples used in the Day 12 lesson |
| `data/` | Sample datasets and text files used in the lessons |
| `files/` | Sample CSV, JSON, XML, Excel, and text files for file-handling examples |
| `images/` | Images referenced by the lessons |
| `numpy.md`, `numpy_files/` | NumPy material and PNG images |
| `test_files/` | PNG images |

## Course Outline

Each day links to its English lesson file.

| Day | Topic |
| --- | --- |
| 01 | [Introduction](01_Day_Introduction/helloworld.py) (code sample only) |
| 02 | [Variables and built-in functions](02_Day_Variables_builtin_functions/02_variables_builtin_functions.md) |
| 03 | [Operators](03_Day_Operators/03_operators.md) |
| 04 | [Strings](04_Day_Strings/04_strings.md) |
| 05 | [Lists](05_Day_Lists/05_lists.md) |
| 06 | [Tuples](06_Day_Tuples/06_tuples.md) |
| 07 | [Sets](07_Day_Sets/07_sets.md) |
| 08 | [Dictionaries](08_Day_Dictionaries/08_dictionaries.md) |
| 09 | [Conditionals](09_Day_Conditionals/09_conditionals.md) |
| 10 | [Loops](10_Day_Loops/10_loops.md) |
| 11 | [Functions](11_Day_Functions/11_functions.md) |
| 12 | [Modules](12_Day_Modules/12_modules.md) |
| 13 | [List comprehension](13_Day_List_comprehension/13_list_comprehension.md) |
| 14 | [Higher-order functions](14_Day_Higher_order_functions/14_higher_order_functions.md) |
| 15 | [Python type errors](15_Day_Python_type_errors/15_python_type_errors.md) |
| 16 | [Python date and time](16_Day_Python_date_time/16_python_datetime.md) |
| 17 | [Exception handling](17_Day_Exception_handling/17_exception_handling.md) |
| 18 | [Regular expressions](18_Day_Regular_expressions/18_regular_expressions.md) |
| 19 | [File handling](19_Day_File_handling/19_file_handling.md) |
| 20 | [Python package manager (pip)](20_Day_Python_package_manager/20_python_package_manager.md) |
| 21 | [Classes and objects](21_Day_Classes_and_objects/21_classes_and_objects.md) |
| 22 | [Web scraping](22_Day_Web_scraping/22_web_scraping.md) |
| 23 | [Virtual environments](23_Day_Virtual_environment/23_virtual_environment.md) |
| 24 | [Statistics](24_Day_Statistics/24_statistics.md) |
| 25 | [Pandas](25_Day_Pandas/25_pandas.md) |
| 26 | [Python for the web](26_Day_Python_web/26_python_web.md) |
| 27 | [Python with MongoDB](27_Day_Python_with_mongodb/27_python_with_mongodb.md) |
| 28 | [APIs](28_Day_API/28_API.md) |
| 29 | [Building an API](29_Day_Building_API/29_building_API.md) |
| 30 | [Conclusions](30_Day_Conclusions/30_conclusions.md) |

Some lessons install third-party packages, as shown in their install commands: `numpy` (Day 20 and Day 24), `pandas` (Day 20 and Day 25), `requests` and `beautifulsoup4` (Day 22), `virtualenv` and `Flask` (Day 23 and Day 26), and `pymongo` and `dnspython` (Day 27).

## Translations

The lessons are available in these languages:

- **Chinese** (`Chinese/`): see [`Chinese/README.md`](Chinese/README.md). Its table of contents links to the translated lessons.
- **Korean** (`Korean/` and `korean/`): see [`Korean/readme_ko.md`](Korean/readme_ko.md) and [`korean/readme.md`](korean/readme.md).
- **Portuguese** (`Portuguese/`): see [`Portuguese/README.md`](Portuguese/README.md).

The translated folders do not cover all 30 days. The Chinese folder has files for most days, with Day 1 in its `README.md`. The Korean and Portuguese folders have fewer files. Check each folder for the days you need.

## Code Samples

Several folders include runnable `.py` files, including:

- `01_Day_Introduction/helloworld.py`
- `02_Day_Variables_builtin_functions/variables.py`
- `03_Day_Operators/day-3.py`
- `04_Day_Strings/day_4.py`
- `05_Day_Lists/day_5.py`
- `12_Day_Modules/main.py` and `12_Day_Modules/mymodule.py`: `main.py` imports from `mymodule`, so run it from `12_Day_Modules/`.
- `20_Day_Python_package_manager/`: `greet.py`, `arithmetic.py`, and `__init__.py`
- `mypackage/`: `greet_person(firstname, lastname)` in `greet.py`, and `add_numbers`, `subtract`, `multiple`, `division`, `remainder`, and `power` in `arithmetics.py`

Run scripts with a Python 3 interpreter, for example:

```shell
python 01_Day_Introduction/helloworld.py
```

## Web Application (`python_for_web`)

`python_for_web/` is a small Flask application for the Day 26 lesson.

Routes defined in `app.py`:

| Route | Methods | Behavior |
| --- | --- | --- |
| `/` | GET | Renders the home page listing the technologies used (HTML, CSS, Flask, Python). |
| `/about` | GET | Renders the about page. |
| `/post` | GET, POST | GET renders a text-input form titled "Text Analyzer". POST reads the `content` field and redirects to `/result`. |
| `/result` | GET | Renders the result page. |

The `/post` route currently does not analyze the submitted text. The result page only displays a heading. The text-analysis step is not implemented in the code, despite what the home page describes.

Files:

- `app.py`: Flask application. It reads the port from the `PORT` environment variable and defaults to `5000`. It runs with `debug=True` and host `0.0.0.0`.
- `requirements.txt`: pinned dependencies (`Flask==1.1.1`, `Werkzeug==0.16.0`, `Jinja2==2.10.3`, `MarkupSafe==1.1.1`, `itsdangerous==1.1.0`, `Click==7.0`).
- `Procfile`: `web: python app.py`, for platforms that use Procfiles.
- `templates/`: `layout.html`, `home.html`, `about.html`, `post.html`, and `result.html`.
- `static/css/main.css`: stylesheet.

To run it locally:

```shell
cd python_for_web
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:5000`.

The pinned versions are old (Flask 1.1.1 dates from 2019). They may not install on recent Python versions. This has not been tested here.

## Datasets

`data/` and `files/` contain sample data used in the lessons, including:

- CSV: `data/hacker_news.csv`, `data/HN_posts_year_to_Sep_26_2016.csv`, `data/F500.csv`, `data/fortune1000_final.csv`, `data/fortune_500_companies_2017.csv`, `data/weight-height.csv`, `data/result.csv`, `files/csv_example.csv`
- JSON: `data/countries_data.json`, `data/countries_data_long.json`, `data/cats.json`, `files/json_example.json`, `22_Day_Web_scraping/scrapped_data.json`
- Text: `data/romeo_and_juliet.txt`, `data/obama_speech.txt`, `data/donald_speech.txt`, `data/michelle_obama_speech.txt`, `data/melina_trump_speech.txt`, `data/email_exchanges.txt`, `data/email_exchanges_big.txt`, `files/example.txt`, `files/reading_file_example.txt`
- Other: `files/xml_example.xml`, `files/excel_example.xlsx`
- Python helpers: `data/countries.py`, `data/countries-data.py`, `data/stop_words.py`

Check each lesson for the file paths it expects.

## Getting Started

1. Install Python 3 from [python.org](https://www.python.org/).
2. Clone or download this repository.
3. Open a lesson, such as [`02_Day_Variables_builtin_functions/02_variables_builtin_functions.md`](02_Day_Variables_builtin_functions/02_variables_builtin_functions.md), and work through its examples and exercises.
4. Run the matching code in a Python shell or as a `.py` file.

The lessons suggest Visual Studio Code as an editor, but any editor works.

## Known Issues

Problems found while writing this README:

- **No English Day 1 lesson file.** `01_Day_Introduction/` contains only `helloworld.py`. The Day 1 lesson text appears in the Chinese and Portuguese `README.md` files, and the older combined `old_files/readme.md` covers Days 1 to 3.
- **Chinese README Day 1 link is broken.** The Chinese `README.md` links Day 1 to `./readme.md`, which does not exist in `Chinese/`.
- **Duplicate Korean folders.** Both `Korean/` and `korean/` exist and differ only in case.
- **Unimplemented text analysis.** The web application's `/post` route does not analyze text, and the `/result` page only shows a heading (see [Web Application](#web-application-python_for_web)).
- **Outdated `old_files/`.** These older versions contain outdated instructions and typos, such as `area_of_width` in `old_files/readme.md`. Treat them as archives.
- **Typo in example code.** `12_Day_Modules/main.py` passes `'Asabneh'` to `fullname`.

## Credits

The course is by Asabeneh Yetayeh. The lessons link to the author's [LinkedIn](https://www.linkedin.com/in/asabeneh/) and [Twitter](https://twitter.com/Asabeneh) accounts and a [PayPal](https://www.paypal.me/asabeneh) donation page. The repository's `.github/FUNDING.yml` lists `Asabeneh` as the GitHub sponsor.

The lessons also point to the Telegram community, [30DaysOfPython challenge](https://t.me/ThirtyDaysOfPython).

This repository does not include a license file, so check with the author before reusing the material.
