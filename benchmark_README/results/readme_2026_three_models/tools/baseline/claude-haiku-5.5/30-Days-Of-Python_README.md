# 30 Days of Python

This repository is a 30-day Python programming course. Each day covers one topic, from variables and operators through data structures, functions, and modules to exception handling, date and time, file handling, package management, web development, MongoDB, and APIs. The lessons are written in Markdown, with runnable example scripts and exercises. The author is Asabeneh Yetayeh, and the lessons are labeled "Second Edition: July, 2021."

## Overview

The course is organized as one folder per day, numbered `01_Day_...` through `30_Day_...`. Most days contain a Markdown lesson, such as `02_Day_Variables_builtin_functions/02_variables_builtin_functions.md`. Some days also include Python scripts that demonstrate the lesson, such as `03_Day_Operators/day-3.py` or `12_Day_Modules/main.py`.

The lessons follow a consistent pattern. Each one introduces a topic with code examples, explains the concepts, and ends with exercises at one or more difficulty levels. Several lessons use the same running example, a `person` dictionary describing a fictional person with fields such as `first_name`, `country`, and `skills`.

The repository also contains:

- **Translations:** `Chinese/` holds Chinese versions of Days 2 through 30 with a `README.md`. `Korean/` and `korean/` hold partial Korean translations. `Portuguese/` holds Portuguese versions of Day 2 and a `README.md`.
- **Supporting data:** `data/` contains CSV, JSON, and text files, plus Python modules such as `countries.py` and `countries-data.py`. Exercises refer to these files.
- **Sample files:** `files/` contains example CSV, Excel, JSON, XML, and text files for the file-handling material.
- **Images:** `images/` holds the screenshots and diagrams used in the lessons, including MongoDB setup screenshots under `images/mongoDB/`.
- **NumPy notes:** `numpy.md` is a Day 24 document covering NumPy arrays, mathematical operations, slicing, random numbers, and basic statistics. It is linked to the statistics material.
- **Archived readmes:** `old_files/` contains older combined readme files for the course days.
- **Flask application:** `python_for_web/` contains a small web app, described below.

### Repository Structure

| Path | Contents |
| --- | --- |
| `01_Day_Introduction/` through `30_Day_Conclusions/` | Daily lessons and example scripts |
| `Chinese/`, `Korean/`, `korean/`, `Portuguese/` | Translated lessons |
| `data/` | Datasets and data-related Python modules |
| `files/` | Sample files for file handling |
| `images/`, `numpy_files/`, `test_files/` | Images used in lessons and notebook outputs |
| `mypackage/` | A small package with `__init__.py`, `arithmetics.py`, and `greet.py` |
| `python_for_web/` | Flask web application |
| `old_files/` | Archived readme files |
| `.github/FUNDING.yml` | GitHub funding configuration |
| `.gitignore` | Git ignore rules |

## Setup

The supplied files do not specify a required Python version. The lessons assume Python 3 and use features such as f-strings, which the Day 4 lesson notes require Python 3.6 or later.

### Course Lessons

1. Clone or download the repository.
2. Install Python 3. The lessons include installation screenshots for Windows and macOS under `images/`, but the instructions themselves are not included in the supplied text.
3. Use VS Code or a Python shell to run the examples. The Day 2 lesson describes opening the Python shell, and the Day 1 lesson presents the `helloworld.py` example.
4. Starting with Day 24, the NumPy lesson recommends Jupyter Notebook and suggests installing [Anaconda](https://www.anaconda.com/), which includes many common packages. Alternatively, install NumPy directly:

   ```sh
   pip install numpy
   ```

The Day 23 lesson covers virtual environments, and the Day 20 lesson covers the Python package manager. Consult those lessons for environment setup.

### Flask Web Application

The application in `python_for_web/` has pinned dependencies in `requirements.txt`:

```text
Click==7.0
Flask==1.1.1
itsdangerous==1.1.0
Jinja2==2.10.3
MarkupSafe==1.1.1
Werkzeug==0.16.0
```

To set it up:

```sh
cd python_for_web
pip install -r requirements.txt
```

## Usage

### Running Example Scripts

Most example scripts can be run directly with Python. For example, the Day 12 module demo imports from `mymodule.py`, so both files must be in the same directory:

```sh
cd 12_Day_Modules
python main.py
```

`main.py` imports `generate_full_name`, `sum_two_nums`, `person`, and `gravity` from `mymodule`, then prints results. The contents of `mymodule.py` are not included in the supplied text.

The Day 12 lesson also shows a command-line example using `sys.argv`:

```sh
python script.py Asabeneh 30DaysOfPython
```

### Running the Flask Application

`app.py` defines the following routes:

| Route | Methods | Behavior |
| --- | --- | --- |
| `/` | GET | Renders `home.html` with a list of technologies (`HTML`, `CSS`, `Flask`, `Python`) |
| `/about` | GET | Renders `about.html` |
| `/result` | GET | Renders `result.html` |
| `/post` | GET, POST | GET renders `post.html` for the "Text Analyzer" page. POST reads the `content` form field and redirects to `/result`. |

The application runs when `app.py` is executed directly:

```sh
cd python_for_web
python app.py
```

The `__main__` block starts the server on host `0.0.0.0`, using the port from the `PORT` environment variable or port 5000 by default.

The POST handler reads the submitted `content` value but does not use it before redirecting. The result page therefore does not display any analysis.

Templates are in `python_for_web/templates/` (`layout.html`, `home.html`, `about.html`, `post.html`, `result.html`), and styles are in `python_for_web/static/css/main.css`. The `Procfile` exists in the same directory, but its contents are not included in the supplied text.

## Configuration

The supplied files contain only a small amount of configuration:

- **`PORT` environment variable:** `app.py` reads the server port from `PORT` and defaults to `5000`.
- **Static file caching:** `app.py` sets `SEND_FILE_MAX_AGE_DEFAULT` to `0` to stop caching of static files.
- **Debug mode:** `app.run` is called with `debug=True`. This should be disabled in production.
- **Host binding:** The server binds to `0.0.0.0`, making it reachable from other machines on the network.
- **Dependencies:** The versions of Flask, Werkzeug, Jinja2, and related packages are pinned in `python_for_web/requirements.txt`.
- **Git ignore rules:** `.gitignore` at the root and `python_for_web/.gitignore` list files excluded from version control. Their contents are not included in the supplied text.

## Development

Contributions can take several forms.

- **Lessons:** Each day's content is a Markdown file. Edit the lesson in its day folder, keeping the existing structure with a title header, navigation links, a table of contents, exercises, and a closing congratulations section.
- **Examples:** Day folders may include `.py` example files. Keep them in the same folder as the lesson they support.
- **Translations:** Translated lessons live in `Chinese/`, `Korean/`, `korean/`, and `Portuguese/`. The supplied text does not describe a translation workflow.
- **Package example:** `mypackage/` and `20_Day_Python_package_manager/` contain small package examples. Their contents are not included in the supplied text.
- **Data:** Datasets are in `data/` and sample files in `files/`. The Day 22 web scraping lesson has a `scrapped_data.json` file alongside its Markdown lesson.

The supplied files do not include a contributing guide, code of conduct, or development environment file.

## Testing

The supplied file tree contains no automated test files, such as `test_*.py` modules or a test configuration file. The `test_files/` directory contains three PNG images named `test_121_0.png`, `test_141_0.png`, and `test_143_0.png`. These appear to be plot outputs from the NumPy material, not test scripts.

The lessons include exercises and example code, and the Day 15 lesson encourages readers to run the examples in the Python interactive shell. The supplied text does not describe a test command or CI pipeline.

## License

The supplied files do not include a LICENSE file, and no license is stated in the supplied text. Check the repository for license information before reusing or redistributing the content.

The `.github/FUNDING.yml` file exists, but its contents are not included in the supplied text. The lessons link to the author's LinkedIn and Twitter profiles, and the Day 11 lesson links to an external testimonial page.

## Acknowledgements

The lessons credit the author, Asabeneh Yetayeh. Several lessons cite external references, including the Python documentation, W3Schools, Programiz, and strftime.org, for reference material and tables.
