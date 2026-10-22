# 30 Days of Python

A hands-on Python learning repository organized as a 30-day challenge. It combines lesson notes, small runnable scripts, exercises, data files, and supporting images to help learners progress from Python basics to topics such as data analysis and web development.

## Overview

The main English-language lessons are grouped into numbered day folders, from `01_Day_Introduction` through `30_Day_Conclusions`. Many lessons are Markdown tutorials that include explanations, code examples, and exercises; some folders also contain Python scripts to run or study. The topics span:

- Python fundamentals: variables, built-in functions, operators, strings, and collections
- Program flow and reusable code: conditionals, loops, functions, modules, and comprehensions
- Further language features: higher-order functions, errors, date and time, exceptions, regular expressions, files, and classes
- Applied topics: package management, web scraping, virtual environments, statistics, pandas, web development, MongoDB, and APIs

The repository also includes translated lesson material in `Chinese/`, `Korean/`, `korean/`, and `Portuguese/`. Translation coverage varies; use the English day folders as the main lesson sequence.

Additional materials include sample datasets in `data/`, file-format examples in `files/`, lesson images in `images/`, a NumPy tutorial in `numpy.md`, and a small Flask application in `python_for_web/`.

The lesson pages identify Asabeneh Yetayeh as the author and describe the material as the second edition, dated July 2021.

## Getting started

You need a Python 3 installation to run the Python examples. The lessons use modern Python syntax, including f-strings; the strings lesson identifies f-strings as a Python 3.6+ feature. The repository does not provide a single top-level dependency file for all lessons, so requirements depend on which material you choose to run.

1. Obtain the repository and open it in a terminal or editor.
2. Start with the introduction and proceed through the numbered day folders. Read the Markdown lesson before trying its exercises.
3. Run an individual script with Python. For example:

   ```sh
   python 01_Day_Introduction/helloworld.py
   python 02_Day_Variables_builtin_functions/variables.py
   python 03_Day_Operators/day-3.py
   ```

   If your system uses `python3` for Python 3, substitute `python3` in these commands.

The lessons are also useful without running the scripts: their Markdown files contain explanations, examples, and exercises that can be worked through in the Python interactive shell.

## Usage

### Follow the lessons

Read the day files in order. Lesson links within the Markdown connect neighboring days, and many lessons end with exercises. For example, Day 2 introduces variables, built-in functions, data types, and casting; later lessons build on those ideas with strings, collections, conditionals, loops, and functions.

Some lesson folders contain runnable examples. Day 12 includes `main.py` and `mymodule.py` to demonstrate imports and aliases. Run the example with:

```sh
python 12_Day_Modules/main.py
```

### Use the supporting files

The `data/` directory contains sample material in formats including CSV, JSON, and plain text. The `files/` directory contains examples such as CSV, JSON, XML, text, and Excel files. Some lessons refer to these resources for practice. `images/` contains illustrations used by the tutorials.

`numpy.md` is a separate tutorial covering NumPy arrays, operations, statistics, and linear algebra examples. It documents installing NumPy with `pip install numpy`; examples in the tutorial also import other scientific and plotting libraries. Those extra packages are not listed in a repository-wide requirements file.

### Run the Flask example

The web example lives in `python_for_web/`. Its requirements file pins Flask and its related packages. From that directory, install the listed dependencies and start the app:

```sh
cd python_for_web
python -m pip install -r requirements.txt
python app.py
```

The app defines `/`, `/about`, `/result`, and `/post` routes and renders templates from `templates/`. The `/post` route accepts GET and POST requests; on POST it reads the submitted `content` field and redirects to the result route. The app binds to `0.0.0.0` and uses the `PORT` environment variable when set, otherwise port `5000`.

## Configuration and dependencies

Most examples use Python’s standard library and require no package installation. Dependencies are specific to optional topics:

- `python_for_web/requirements.txt` lists pinned versions of Click, Flask, itsdangerous, Jinja2, MarkupSafe, and Werkzeug.
- `numpy.md` documents NumPy installation and includes examples using NumPy, Matplotlib, Seaborn, and SciPy. There is no supplied requirements file for these tutorial examples.

The Flask application sets `SEND_FILE_MAX_AGE_DEFAULT` to `0`, disabling caching of static files. Its run configuration takes the port from `PORT` or defaults to `5000`. The app is configured with `debug=True` in its run block.

## Development

For learning or contributing, make changes in the relevant day folder and keep examples consistent with their lesson. The course is organized as instructional material rather than as one installable Python package. To explore module examples, note that the repository contains module and package demonstrations in locations including `12_Day_Modules/`, `20_Day_Python_package_manager/`, `mypackage/`, and the project root.

The Flask example’s templates and static stylesheet are under `python_for_web/templates/` and `python_for_web/static/`. Run the app from `python_for_web/` so its relative template and static paths resolve as expected.

## Testing

The supplied files do not define a project-wide automated test suite or test command. Verify changes by running the relevant lesson script or Flask example and working through its documented exercises. For the web example, start the app and visit its routes in a browser. The `test_files/` directory contains PNG images referenced by the NumPy tutorial; it is not identified as an automated test suite.

## License

No license file or license terms are included in the supplied repository tree. Check the repository’s current license information or contact the project owner before redistributing or reusing its material.
