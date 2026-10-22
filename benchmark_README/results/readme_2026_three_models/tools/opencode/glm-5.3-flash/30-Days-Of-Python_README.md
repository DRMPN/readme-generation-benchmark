# 30 Days Of Python

![30DaysOfPython](./images/30DaysOfPython_banner3@2x.png)

**30 Days Of Python** is a step-by-step Python programming challenge. The material is broken down into 30 days, where each day covers several topics with explanations, real-world examples, and hands-on exercises, and each lesson ends with a set of exercises. The course teaches Python 3 and is designed for beginners as well as professionals who want to learn the language.

- **Author:** [Asabeneh Yetayeh](https://www.linkedin.com/in/asabeneh/)
- **Edition:** Second Edition, July 2021

## Contents

| # | Day | Topic |
|---|-----|-------|
| 01 | Introduction | [Lesson notes¹](./old_files/readme.md) · [helloworld.py](./01_Day_Introduction/helloworld.py) |
| 02 | Variables, builtin functions | [Lesson notes](./02_Day_Variables_builtin_functions/02_variables_builtin_functions.md) · [variables.py](./02_Day_Variables_builtin_functions/variables.py) |
| 03 | Operators | [Lesson notes](./03_Day_Operators/03_operators.md) · [day-3.py](./03_Day_Operators/day-3.py) |
| 04 | Strings | [Lesson notes](./04_Day_Strings/04_strings.md) · [day_4.py](./04_Day_Strings/day_4.py) |
| 05 | Lists | [Lesson notes](./05_Day_Lists/05_lists.md) · [day_5.py](./05_Day_Lists/day_5.py) |
| 06 | Tuples | [Lesson notes](./06_Day_Tuples/06_tuples.md) |
| 07 | Sets | [Lesson notes](./07_Day_Sets/07_sets.md) |
| 08 | Dictionaries | [Lesson notes](./08_Day_Dictionaries/08_dictionaries.md) |
| 09 | Conditionals | [Lesson notes](./09_Day_Conditionals/09_conditionals.md) |
| 10 | Loops | [Lesson notes](./10_Day_Loops/10_loops.md) |
| 11 | Functions | [Lesson notes](./11_Day_Functions/11_functions.md) |
| 12 | Modules | [Lesson notes](./12_Day_Modules/12_modules.md) · [mymodule.py](./12_Day_Modules/mymodule.py) · [main.py](./12_Day_Modules/main.py) |
| 13 | List comprehension | [Lesson notes](./13_Day_List_comprehension/13_list_comprehension.md) |
| 14 | Higher order functions | [Lesson notes](./14_Day_Higher_order_functions/14_higher_order_functions.md) |
| 15 | Python type errors | [Lesson notes](./15_Day_Python_type_errors/15_python_type_errors.md) |
| 16 | Python date time | [Lesson notes](./16_Day_Python_date_time/16_python_datetime.md) |
| 17 | Exception handling | [Lesson notes](./17_Day_Exception_handling/17_exception_handling.md) |
| 18 | Regular expressions | [Lesson notes](./18_Day_Regular_expressions/18_regular_expressions.md) |
| 19 | File handling | [Lesson notes](./19_Day_File_handling/19_file_handling.md) |
| 20 | Python package manager | [Lesson notes](./20_Day_Python_package_manager/20_python_package_manager.md) |
| 21 | Classes and objects | [Lesson notes](./21_Day_Classes_and_objects/21_classes_and_objects.md) |
| 22 | Web scraping | [Lesson notes](./22_Day_Web_scraping/22_web_scraping.md) |
| 23 | Virtual environment | [Lesson notes](./23_Day_Virtual_environment/23_virtual_environment.md) |
| 24 | Statistics (incl. NumPy) | [Lesson notes](./24_Day_Statistics/24_statistics.md) · [numpy.md](./numpy.md) |
| 25 | Pandas | [Lesson notes](./25_Day_Pandas/25_pandas.md) |
| 26 | Python for web (Flask) | [Lesson notes](./26_Day_Python_web/26_python_web.md) · [Flask example app](./python_for_web/) |
| 27 | Python with MongoDB | [Lesson notes](./27_Day_Python_with_mongodb/27_python_with_mongodb.md) |
| 28 | API | [Lesson notes](./28_Day_API/28_API.md) |
| 29 | Building an API | [Lesson notes](./29_Day_Building_API/29_building_API.md) |
| 30 | Conclusions | [Lesson notes](./30_Day_Conclusions/30_conclusions.md) |

¹ The Day 1 lesson notes live in `old_files/readme.md`, which also contains the Day 2–3 material from the previous edition layout.

The course concludes (Day 30) by pointing graduates toward data analysis, data science, machine learning, and web development paths.

## Getting started

1. Install Python 3 from [python.org](https://www.python.org/). You can verify the installation with:

   ```shell
   python --version
   ```

2. Choose a code editor. The course uses and recommends [Visual Studio Code](https://code.visualstudio.com/).

3. Work through the days in order. Each day folder contains the lesson notes, and several days also include example or exercise scripts you can run with `python <file>.py`.

### Additional requirements for specific days

Some later days use third-party tools and packages. Install what you need for the day you are studying:

- **Day 19 (File handling):** sample files to read and write are provided in [`files/`](./files/) (TXT, CSV, JSON, XML, and Excel examples).
- **Day 22 (Web scraping):** `pip install requests beautifulsoup4`
- **Day 24 (Statistics):** uses the `statistics` module and NumPy (`numpy.md`).
- **Day 25 (Pandas):** `pip install pandas`
- **Day 26 (Python for web):** a complete Flask example app is provided in [`python_for_web/`](./python_for_web/); its `requirements.txt` pins Flask 1.1.1 and related packages. The lesson also covers deploying to Heroku with a `Procfile`.
- **Day 27 & 29 (MongoDB and building an API):** `pip install pymongo dnspython`, a running MongoDB instance, and an HTTP client such as [Postman](https://www.getpostman.com/) or [Insomnia](https://insomnia.rest/download) to exercise the API endpoints.

## Repository layout

```
├── 01_Day_Introduction/          # Day folders, one per day (lesson notes + example scripts)
├── ...
├── 30_Day_Conclusions/
├── Chinese/                      # Chinese translation (README + Day 02–30 notes)
├── Korean/, korean/              # Partial Korean translation
├── Portuguese/                   # Partial Portuguese translation (README + Day 02)
├── old_files/                    # Previous-edition READMEs (readme.md = Days 1–3, readme4-6.md … readme28-30.md)
├── data/                         # Datasets used in the exercises (JSON, CSV, TXT)
├── files/                        # Sample files for the Day 19 file-handling lesson
├── images/                       # Images referenced by the lesson notes
├── numpy_files/, test_files/     # Generated figures referenced by the Day 24 / NumPy notes
├── mypackage/, mymodule.py       # Example modules used in the modules/packages lessons
├── numpy.md                      # Day 24 lesson notes, extended with the NumPy section
├── python_for_web/               # Day 26 Flask example app (app.py, templates/, static/, Procfile)
└── .github/                      # Repository configuration (funding)
```

### Data files

The [`data/`](./data/) folder holds the datasets referenced by the exercises, including:

- `countries_data.json`, `countries.py`, `countries-data.py` — country data used in the file-processing exercises
- Speech transcripts: `obama_speech.txt`, `michelle_obama_speech.txt`, `melina_trump_speech.txt`, `donald_speech.txt`
- `romeo_and_juliet.txt`, `email_exchanges.txt`, `email_exchanges_big.txt`
- CSV files: `F500.csv`, `fortune_500_companies_2017.csv`, `fortune1000_final.csv`, `hacker_news.csv`, `HN_posts_year_to_Sep_26_2016.csv`, `weight-height.csv`, `result.csv`
- `cats.json`, `stop_words.py`

## Translations

Community translations are available inside this repository, though not all of them cover every day:

- **Chinese** — [`Chinese/`](./Chinese/): a full set of notes for Days 02–30 plus a README that includes Day 1.
- **Korean** — [`Korean/`](./Korean/) and [`korean/`](./korean/): a partial set covering several early days.
- **Portuguese** — [`Portuguese/`](./Portuguese/): a README plus the Day 02 notes.

## Community and support

- [Join the Telegram channel for help](https://t.me/ThirtyDaysOfPython)
- The author accepts support through [PayPal](https://www.paypal.com/paypalme/asabeneh) and [GitHub Sponsors](https://github.com/sponsors/Asabeneh) (see `.github/FUNDING.yml`).
- Feedback and testimonials links are listed in the [Day 30 notes](./30_Day_Conclusions/30_conclusions.md).

## Credits

All lesson content was written by **Asabeneh Yetayeh**. The per-day notes carry the header "Second Edition: July, 2021". The original challenge is published at [github.com/Asabeneh/30-Days-Of-Python](https://github.com/Asabeneh/30-Days-Of-Python).
