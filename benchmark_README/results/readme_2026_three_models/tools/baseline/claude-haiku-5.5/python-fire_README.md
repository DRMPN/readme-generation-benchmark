# Python Fire

[![PyPI](https://img.shields.io/pypi/pyversions/fire.svg?style=plastic)](https://github.com/google/python-fire)

Python Fire is a library for automatically generating command line interfaces (CLIs) from almost any Python object. You pass it a function, class, object, module, dictionary, list, or tuple, and it builds a CLI for that object. The library is named "Fire" because calling `fire.Fire()` fires off your command.

This project is not an official Google product.

## Overview

The library's documentation describes these main uses:

- **Creating CLIs:** Write the functionality you want on the command line as a function, module, or class, then add one call to `fire.Fire`.
- **Developing and debugging:** Run parts of a library from the command line without editing a main method for each experiment. The `--interactive` flag opens a REPL with your variables already defined.
- **Exploring existing code:** Call `Fire` on an existing module, including one whose source you do not have, to see what it exposes. The documentation gives `difflib` as an example.
- **Bridging Bash and Python:** Call Python functions from shell pipelines alongside tools such as `grep`, `xargs`, and `wc`.

Here is a minimal example. Save it as `hello.py`:

```python
import fire

def hello(name="World"):
  return "Hello %s!" % name

if __name__ == '__main__':
  fire.Fire(hello)
```

Then run:

```bash
python hello.py  # Hello World!
python hello.py --name=David  # Hello David!
python hello.py --help  # Shows usage information.
```

A class works the same way. Each public method becomes a command:

```python
import fire

class Calculator(object):
  """A simple calculator class."""

  def double(self, number):
    return 2 * number

if __name__ == '__main__':
  fire.Fire(Calculator)
```

```bash
python calculator.py double 10  # 20
python calculator.py double --number=15  # 30
```

### Package contents

The `fire` package contains the core implementation:

- `fire/core.py` implements `Fire`, the command execution logic, and the flag handling.
- `fire/completion.py` generates Bash and Fish completion scripts.
- `fire/helptext.py` produces help and usage screens.
- `fire/docstrings.py` parses Google, NumPy, and reST style docstrings for help text.
- `fire/decorators.py` provides `SetParseFn` and `SetParseFns` for customizing argument parsing.
- `fire/__main__.py` implements `python -m fire`.
- `fire/console/` contains a vendored copy of the console package from `googlecloudsdk`.

The `examples/` directory contains sample packages named `cipher`, `diff`, `identity`, and `widget`.

## Installation

Install the released package from PyPI:

```bash
pip install fire
```

Or install from conda-forge:

```bash
conda install fire -c conda-forge
```

To install from source, clone the repository and run:

```bash
python setup.py install
```

For development, use an editable install instead:

```bash
python setup.py develop
```

The package metadata in `setup.py` declares `requires_python='>=3.7'` and lists Python 3.7 through 3.13 as supported classifiers. Its runtime dependency is `termcolor`. The `requirements.txt` file contains only `.`, which installs the project itself.

## Usage

### Calling `Fire` on different components

`Fire` accepts any Python object as its first argument. The `fire.Fire()` call with no argument uses the calling context, meaning the module's globals and locals, as the component.

```python
import fire

english = 'Hello World'
spanish = 'Hola Mundo'
fire.Fire()
```

```bash
python example.py english   # Hello World
python example.py spanish   # Hola Mundo
```

Passing a dictionary exposes only the keys you choose:

```python
import fire

def add(x, y):
  return x + y

def multiply(x, y):
  return x * y

if __name__ == '__main__':
  fire.Fire({
      'add': add,
      'multiply': multiply,
  })
```

### Command syntax

A Fire command is a sequence of arguments that Fire consumes from left to right. Each step can:

- access a member of the current object, such as an attribute, method, or dictionary key;
- index into a list or tuple;
- call a function;
- instantiate a class;
- call a callable object.

Arguments can be positional or named with flag syntax. Hyphens and underscores are interchangeable in names, and the `=` in `--name=value` is optional:

```bash
python example.py --name="Sherrerd Hall" --stories=3 climb_stairs 10
python example.py --name="Sherrerd Hall" climb_stairs --stairs-per-story 10
```

Methods can be chained. If a method returns `self`, later commands apply to that object. The documentation shows a `BinaryCanvas` class whose `move`, `on`, and `off` methods chain together to draw a figure.

Results are printed according to their type. If the result has a custom `__str__` method, Fire prints `str(result)`. If the result is a list, set, or generator, each item is printed on its own line. Otherwise, Fire shows the help screen for the result.

### Argument parsing

Fire determines argument types from their values, not from function annotations. Python literals such as numbers, strings, tuples, lists, and dictionaries are parsed. Bare words become strings.

```bash
python example.py 10          # int
python example.py 10.0        # float
python example.py hello       # str
python example.py '(1,2)'     # tuple
python example.py True        # bool
```

Because Bash processes quotes before Fire sees the arguments, quoting matters. The guide shows that `'{"name": "David Bieber"}'` is parsed as a dict, while `{"name":"David Bieber"}` is parsed as a string.

Boolean flags can be written as `--name`, which sets `True`, or `--noname`, which sets `False`.

### Separator

The default separator is `-`. Arguments after a separator are applied to the result of the preceding call instead of being passed to the function:

```bash
python example.py dog cat elephant - upper
```

To pass `-` as a literal argument, change the separator with `--separator`:

```bash
python example.py dog cat elephant X upper -- --separator=X
```

### Async functions

When Fire encounters a coroutine function, it runs the coroutine to completion before continuing. The implementation in `fire/core.py` uses `asyncio.get_event_loop().run_until_complete`.

### Running a module without modifying it

The `python -m fire` entry point runs Fire on an existing module or file:

```bash
python -m fire calendar -h
python -m fire example hello --name=World
python -m fire example.py hello --name=World
```

## Flags

Flags for Fire itself must follow an isolated `--` argument. Arguments before the final `--` belong to the Fire command.

| Flag | Purpose |
| --- | --- |
| `--help`, `-h` | Show help and usage information. The isolated `--` is optional for help. |
| `--interactive`, `-i` | Open a Python REPL with the component and related variables already defined. |
| `--separator=X` | Change the separator from `-` to `X`. |
| `--completion [shell]` | Print a completion script for the CLI. Bash is the default; `fish` is supported. |
| `--trace`, `-t` | Print a Fire trace of how the command was executed. |
| `--verbose`, `-v` | Include private members in help and usage output. |

Examples:

```bash
python example.py -- --help
python example.py -- --interactive
python example.py -- --completion > ~/.example-completion
```

The interactive mode uses IPython if it is installed, according to the documentation. Otherwise it uses the standard Python REPL.

## Configuration

`fire.Fire` accepts these keyword arguments:

- `component`: the object to expose. If omitted, the calling context is used.
- `command`: a string or a list of arguments. If omitted, `sys.argv[1:]` is used. Strings are split with `shlex`.
- `name`: the CLI name shown in help text, and used in interactive mode and completion scripts. If omitted, it is inferred from `sys.argv[0]`.
- `serialize`: a callable that converts results to text before they are printed.

```python
import fire

fire.Fire(component, command=['hello', '--name=5'], name='tool')
```

Argument parsing can be customized with decorators from `fire/decorators.py`:

- `@decorators.SetParseFn(fn, *arguments)` sets a parsing function for the listed arguments, or the default for all arguments if none are listed.
- `@decorators.SetParseFns(*positional, **named)` sets parsing functions by position or by name.

Other behavior is controlled through the flags listed above. On Windows, `fire/formatting_windows.py` initializes ANSI color handling. If `colorama` is not installed, it sets the `ANSI_COLORS_DISABLED` environment variable to `1`.

Lists and tuples accept index access. Dicts accept key access, and Fire also tries matching keys by their string form.

## Development

### Repository layout

- `fire/`: library source and tests. Test files end in `_test.py`.
- `examples/`: example packages.
- `docs/`: Markdown documentation, including the guide, the API reference, and troubleshooting notes.
- `mkdocs.yml`: MkDocs site configuration for `docs/`.
- `setup.py` and `setup.cfg`: packaging and tool configuration.
- `.github/`: GitHub Actions workflow, a build script, and Dependabot configuration.
- `pylintrc`: lint configuration.

### Continuous integration and dependencies

The repository includes `.github/workflows/build.yml` and `.github/scripts/build.sh`, and `.github/scripts/requirements.txt` pins development tools: `setuptools`, `pip`, `pylint`, `pytest`, `pytest-pylint`, `pytest-runner`, `termcolor`, `hypothesis`, and `levenshtein`. Dependabot checks the pip requirements in `.github/scripts/` and GitHub Actions monthly.

### Code style

According to `CONTRIBUTING.md`, the project follows the Google Python Style Guide, with these additions:

- Maximum line length of 80 characters.
- Two-space indentation, with four spaces for continuation lines.
- PascalCase for function and method names.
- Single quotes for strings and triple double quotes for docstrings.

### Changes to `fire/console`

`fire/console/README.md` states that the console package comes from the upstream `googlecloudsdk` project. Python Fire does not accept pull requests that modify it. Changes should go to the upstream project.

## Testing

Run the test suite from the repository root with `pytest`:

```bash
pip install -e .
pip install pytest hypothesis levenshtein
pytest
```

`CONTRIBUTING.md` says the test dependencies include pytest, mock, termcolor, and hypothesis. `setup.py` lists `hypothesis` and `levenshtein` as test dependencies. The `setup.cfg` file configures pytest to skip two files by default: `fire/test_components_py3.py` and `fire/parser_fuzz_test.py`.

The repository includes fuzz tests built with Hypothesis, such as `fire/docstrings_fuzz_test.py`, which runs `docstrings.parse` on generated text.

Linting uses pylint:

```bash
pylint fire
```

The contributing guide notes that passing lint does not guarantee that a pull request will be accepted without style changes.

## Documentation

The `docs/` directory contains:

- `index.md`: the overview and quick start.
- `installation.md`: installation options.
- `benefits.md`: use cases.
- `guide.md`: a long tutorial covering functions, classes, grouping, properties, chaining, argument parsing, and flags.
- `using-cli.md`: how to use a Fire CLI and its flags.
- `api.md`: a quick reference.
- `troubleshooting.md`: known issues.

`mkdocs.yml` sets the site name to "Python Fire", uses the `readthedocs` theme, and defines the navigation.

The troubleshooting page notes that a module should not share a name with a builtin module such as `cmd`, `os`, `re`, or `sys`. Doing so can cause Fire to import the wrong module.

## Contributing

Contributions are accepted through GitHub pull requests. According to `CONTRIBUTING.md`:

1. Open an Issue to state your intent before making changes.
2. Fork the project and make your changes in your copy.
3. Open a pull request.
4. Sign the Contributor License Agreement if this is your first contribution. The CLA page is at <https://cla.developers.google.com/>.

All submissions, including those from project members, go through code review.

## License

Python Fire is licensed under the Apache License, Version 2.0. The full text is in the `LICENSE` file. The `LICENSE` file has the copyright line "Copyright 2017 Google Inc. All rights reserved." The source files carry a 2018 copyright header. `setup.py` lists the license as "Apache Software License."
