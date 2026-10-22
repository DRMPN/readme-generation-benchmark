# Python Fire

> A Python library for automatically generating command-line interfaces (CLIs) from any Python object, module, function, or class.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
  - [Turning Objects into CLIs](#turning-objects-into-clis)
  - [Arguments and Types](#arguments-and-types)
  - [Accessing Members and Chaining Calls](#accessing-members-and-chaining-calls)
  - [Built-in Flags](#built-in-flags)
  - [Help Screens](#help-screens)
  - [Separators](#separators)
  - [Interactive Mode](#interactive-mode)
  - [Tracing Execution](#tracing-execution)
  - [Shell Completion](#shell-completion)
  - [Customizing Help and Descriptions](#customizing-help-and-descriptions)
- [Project Structure](#project-structure)
- [Development](#development)
  - [Setting Up a Development Environment](#setting-up-a-development-environment)
  - [Running Tests](#running-tests)
  - [Fuzz Tests](#fuzz-tests)
  - [Building the Documentation](#building-the-documentation)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

Python Fire is a library that generates command-line interfaces from almost any Python object with no boilerplate code. You call `fire.Fire()` with the object you want to expose, and Fire inspects it and builds a CLI for it. Functions become commands, classes become command groups with constructor arguments, dictionaries, lists, and other containers can be navigated by key or index, and the arguments you pass on the command line are parsed into Python values.

Fire is useful for:

- Quickly exposing an existing function, class, or module as a CLI during development.
- Building admin and maintenance tools without writing argument parsers.
- Exploring and debugging code interactively from the shell.
- Wrapping libraries so their functionality is accessible from the terminal.

Unlike `argparse` or `click`, you do not declare arguments, options, or commands. Fire derives them from the signatures, attributes, and docstrings of your code.

## Features

- **Zero-boilerplate CLIs** from functions, classes, modules, dictionaries, lists, tuples, and most other Python objects.
- **Automatic argument parsing** with type inference. Values such as `1`, `1.5`, `True`, `[1,2,3]`, and `{"a": 1}` are parsed as Python literals when possible; otherwise they are passed as strings.
- **Automatic help screens** generated from function signatures and docstrings.
- **Method chaining** across objects, for example `command obj method1 arg method2`.
- **Interactive mode** that drops you into a Python REPL with your component and the results already loaded.
- **Execution tracing** to see exactly how Fire resolved a command line.
- **Shell completion** for bash, zsh, and fish.
- **Separator control** so that the `-` token can be used to split flags from positional arguments in chained calls.
- **Pager and console utilities** for formatted, readable output in the terminal.

## Installation

Install the latest release from PyPI:

```bash
pip install fire
```

Install from source:

```bash
git clone https://github.com/google/python-fire.git
cd python-fire
pip install .
```

Install in editable mode for development:

```bash
pip install -e .
```

Check the installation:

```bash
python -c "import fire; print(fire.__file__)"
```

## Quick Start

Create a file named `calculator.py`:

```python
import fire


def add(x, y):
    """Return the sum of x and y."""
    return x + y


def multiply(x, y, power=1):
    """Return x * y, optionally raised to a power."""
    return (x * y) ** power


if __name__ == '__main__':
    fire.Fire()
```

Run it from the shell:

```bash
$ python calculator.py add 10 20
30

$ python calculator.py multiply 3 4 --power=2
144

$ python calculator.py add --help
```

Fire's `Fire()` with no arguments exposes the current module. Every function becomes a subcommand, and the function's parameters become positional arguments or flags.

## Usage Guide

### Turning Objects into CLIs

`fire.Fire(component=None, command=None, name=None, serialize=None)` is the main entry point. The most common forms are:

```python
import fire

# 1. Expose the current module.
fire.Fire()

# 2. Expose a specific function.
def hello(name='World'):
    return f'Hello {name}!'

fire.Fire(hello)

# 3. Expose a class. Its constructor arguments become flags,
#    and its methods become subcommands.
class Greeter:
    def __init__(self, greeting='Hello'):
        self.greeting = greeting

    def greet(self, name):
        return f'{self.greeting}, {name}!'

fire.Fire(Greeter)

# 4. Expose a dictionary, list, or other container.
fire.Fire({'apple': 'red', 'banana': 'yellow'})
```

Running the `Greeter` example:

```bash
$ python greeter.py greet World
Hello, World!

$ python greeter.py --greeting=Hi greet Alice
Hi, Alice!
```

Use `command` to run a single command from a larger object without going through the command-line arguments first:

```python
fire.Fire(Greeter, command=['greet', 'World'])
```

### Arguments and Types

Fire parses each argument as a Python literal when it can. This means you usually do not need to specify types.

| Command-line input | Parsed value |
|---|---|
| `42` | `int` 42 |
| `3.14` | `float` 3.14 |
| `True` / `False` | `bool` |
| `None` | `None` |
| `[1,2,3]` | `list` |
| `"{'a': 1}"` | `dict` |
| `hello` | `str` "hello" |

Keyword arguments can be given as flags:

```bash
python tool.py command --name=Alice --verbose
python tool.py command --name Alice --verbose
```

Boolean flags can be negated with `--no` prefixes:

```bash
python tool.py command --noverbose
```

Positional arguments and flags can be mixed:

```python
def send(to, subject='', body=''):
    ...
```

```bash
python mail.py send alice@example.com --subject="Hi" --body="Hello there"
```

Use `--` to explicitly end flag parsing, which is useful when a value begins with a dash:

```bash
python tool.py echo -- --not-a-flag
```

### Accessing Members and Chaining Calls

Fire can traverse attributes, dictionary keys, and list indices as part of the command:

```python
class Config:
    database = {'host': 'localhost', 'port': 5432}
    servers = ['alpha', 'beta']
```

```bash
python config.py database host       # localhost
python config.py servers 1           # beta
```

Calls can be chained. The return value of one command becomes the object for the next:

```python
class Builder:
    def __init__(self):
        self.parts = []

    def add(self, part):
        self.parts.append(part)
        return self

    def build(self):
        return ' '.join(self.parts)
```

```bash
python builder.py add hello add world build
# hello world
```

When a method's arguments belong to the method being called rather than the next one, use the `-` separator described below.

### Built-in Flags

Fire adds the following flags to every CLI it generates:

| Flag | Short | Description |
|---|---|---|
| `--help` | `-h` | Show the help screen for the current component. |
| `--interactive` | `-i` | Enter an interactive Python REPL after the command runs. |
| `--trace` | `-t` | Print a trace of how the command was resolved. |
| `--verbose` | `-v` | Include private and additional members in help output. |
| `--completion` | | Print a shell completion script. |
| `--separator=SEP` | | Change the separator token (default `-`). |

Flags placed before the command apply to the top-level component. Flags placed after a command apply to that command.

### Help Screens

Fire generates help automatically from signatures and docstrings:

```bash
$ python calculator.py multiply --help
NAME
    calculator.py multiply - Return x * y, optionally raised to a power.

SYNOPSIS
    calculator.py multiply X Y <flags>

POSITIONAL ARGUMENTS
    X
    Y

FLAGS
    --power=POWER
        Default: 1
```

Help for the whole component is available by running it with no command or with `--help`:

```bash
python calculator.py --help
```

Docstrings are parsed in Google, NumPy, and Sphinx styles, so `Args:` and `Returns:` sections are reflected in the generated help.

### Separators

Fire uses the separator `-` to mark where the arguments of one call end and the next command begins. This is needed when a method has arguments and you want to call another method afterward:

```bash
python builder.py add hello - build
```

Without the separator, Fire would interpret `build` as a second argument to `add`. You can change the separator if `-` conflicts with your data:

```bash
python builder.py --separator=: add hello : build
```

Setting `--separator` to an empty value disables separator handling.

### Interactive Mode

Add `--interactive` (or `-i`) to drop into a Python REPL after the command runs. The component and the result are available as variables:

```bash
$ python calculator.py add 2 3 -- --interactive
5
Fire is starting a Python REPL with the following variables:
  Fire: fire
  component: <module 'calculator'>
  result: 5
>>> component.multiply(result, 4)
20
```

This is useful for exploring a library or debugging state without writing a separate script.

### Tracing Execution

Use `--trace` to see each step Fire takes:

```bash
$ python calculator.py add 1 2 --trace
```

The trace lists which component was accessed, which arguments were consumed, how each value was parsed, and which function was finally called. It is the fastest way to diagnose why an argument went to an unexpected place, particularly in chained commands.

### Shell Completion

Generate a completion script for your CLI:

```bash
python calculator.py -- --completion > calculator_completion.sh
source calculator_completion.sh
```

Fire supports bash, zsh, and fish. After sourcing the script, pressing Tab completes command names, method names, and flags.

### Customizing Help and Descriptions

Fire reads docstrings and signatures by default. You can override these behaviors:

- Define a `__fire_components__` or use `fire.core.Fire` options such as `name=` to change how the program appears in help output.
- Use `fire.Fire(..., serialize=func)` to control how the final result is printed. For example, `serialize=json.dumps` prints results as JSON.

```python
import json
import fire

def data():
    return {'name': 'Fire', 'version': 1}

if __name__ == '__main__':
    fire.Fire(data, serialize=json.dumps)
```

```bash
$ python data_tool.py
{"name": "Fire", "version": 1}
```

## Project Structure

The repository is organized as follows. Paths are inferred from the file listing.

```
python-fire/
├── README.md                  # Project overview
├── LICENSE                    # Apache License 2.0
├── CONTRIBUTING.md            # Contribution guidelines
├── setup.py                   # Packaging and installation
├── setup.cfg                  # Packaging and tool configuration
├── MANIFEST.in                # Extra files included in source distributions
├── requirements.txt           # Runtime and development dependencies
├── pylintrc                   # Lint configuration
├── mkdocs.yml                 # Documentation site configuration
├── docs/                      # Documentation sources (Markdown)
│   ├── index.md
│   ├── benefits.md
│   ├── guide.md
│   ├── installation.md
│   ├── using-cli.md
│   ├── troubleshooting.md
│   └── api.md
└── fire/                      # Main package
    ├── __init__.py            # Public API (exports Fire)
    ├── __main__.py            # Module entry point
    ├── core.py                # Fire() entry point and command execution
    ├── parser.py              # Argument parsing and type conversion
    ├── helptext.py            # Help screen generation
    ├── formatting.py          # Text formatting utilities
    ├── formatting_windows.py  # Windows-specific formatting
    ├── docstrings.py          # Docstring parsing
    ├── inspectutils.py        # Signature and member introspection
    ├── decorators.py          # Decorators for customizing behavior
    ├── completion.py          # Shell completion script generation
    ├── interact.py            # Interactive REPL mode
    ├── trace.py               # Execution tracing
    ├── value_types.py         # Value type handling
    ├── custom_descriptions.py # Custom help descriptions
    ├── test_components.py     # Sample components used by tests
    ├── test_components_py3.py # Python 3-specific test components
    ├── test_components_bin.py # Binary-related test components
    ├── testutils.py           # Shared test helpers
    ├── console/               # Terminal utilities
    │   ├── console_attr.py    # Terminal attributes and capabilities
    │   ├── console_attr_os.py # OS-specific terminal attributes
    │   ├── console_io.py      # Console input/output helpers
    │   ├── console_pager.py   # Pager support for long output
    │   ├── encoding.py        # Encoding helpers
    │   ├── files.py           # File utilities
    │   ├── platforms.py       # Platform detection
    │   └── text.py            # Text utilities
    └── tests/                 # Test modules (*_test.py, *_fuzz_test.py)
```

The listing also includes several modules that are not part of the core Fire package: `diff.py`, `difffull.py`, `widget.py`, `collector.py`, `identity.py`, and `cipher.py`, along with their tests and `__init__.py` files. These appear to be auxiliary or supporting components. Their purpose is not described in the repository files provided, so check their source before relying on them.

### Key Modules

- **`core.py`**: Implements `Fire()`. It takes the component, walks the command-line arguments, calls the target, and prints or serializes the result.
- **`parser.py`**: Converts strings from the command line into Python values and matches them to function parameters.
- **`helptext.py`**: Builds the NAME, SYNOPSIS, ARGUMENTS, and FLAGS sections of help screens.
- **`inspectutils.py`**: Wraps Python's `inspect` module to get signatures, members, and defaults in a uniform way.
- **`docstrings.py`**: Extracts summaries and argument descriptions from docstrings.
- **`completion.py`**: Produces shell completion scripts.
- **`trace.py`**: Records the steps Fire takes, for `--trace` output.
- **`interact.py`**: Starts the interactive REPL for `--interactive`.

## Development

### Setting Up a Development Environment

```bash
git clone https://github.com/google/python-fire.git
cd python-fire
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
pip install -e .
pip install -r requirements.txt
```

### Running Tests

Tests are written with the standard `unittest` framework and are named `*_test.py`. Run the whole suite with:

```bash
python -m unittest discover -p "*_test.py"
```

Run a single test module:

```bash
python -m unittest fire.core_test
python -m unittest fire.parser_test
python -m unittest fire.completion_test
```

Some tests depend on the components in `test_components*.py`. Keep those files in sync with test expectations when you change them.

### Fuzz Tests

Modules ending in `_fuzz_test.py` (for example `parser_fuzz_test.py` and `docstrings_fuzz_test.py`) feed randomized or unusual inputs to the parser and docstring code to find crashes. Run them as regular tests. For deeper runs, use a fuzzing tool such as Atheris if your environment supports it.

### Building the Documentation

The documentation is written in Markdown and built with MkDocs using `mkdocs.yml`:

```bash
pip install mkdocs
mkdocs serve       # Live preview at http://127.0.0.1:8000
mkdocs build       # Static site in ./site
```

### Linting and Style

A `pylintrc` file is provided at the repository root:

```bash
pip install pylint
pylint fire
```

Follow the style of surrounding code. Keep lines reasonably short and include docstrings for public functions.

### Building a Distribution

```bash
pip install build
python -m build
```

This creates source and wheel archives in `dist/`.

## Contributing

Contributions are welcome. Before opening a pull request:

1. Read [CONTRIBUTING.md](CONTRIBUTING.md).
2. Open an issue to discuss significant changes.
3. Add or update tests for any behavior you change.
4. Run the full test suite and linter.
5. Keep commits focused and write clear commit messages.

Bug reports should include the Python version, the Fire version, the operating system, a minimal reproduction, and the output of `--trace` when relevant.

## Troubleshooting

**The wrong argument is passed to a method in a chain.**
Use the separator `-` to end the current call's arguments before the next command, or run with `--trace` to see how Fire assigned each token.

**A value is interpreted as a number or boolean when I want a string.**
Quote the value so the shell preserves it, and wrap it in additional quotes so Fire sees a string literal, for example `--name="'123'"`.

**Help output is missing private members.**
Add `--verbose` to show additional members.

**A value starting with `-` is treated as a flag.**
Place `--` before the value: `python tool.py echo -- -value`.

**Tab completion does not work.**
Confirm the generated script has been sourced in the current shell, and that your shell is one Fire supports (bash, zsh, or fish).

**Output is hard to read for long results.**
Use `serialize=` to format the output, for example with `json.dumps` or `pprint.pformat`.

For more detail, see the documentation in `docs/troubleshooting.md`.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for the full text.

---

*This README was written from the repository file listing. Command examples reflect Fire's documented behavior. Verify any flag or option against the installed version with `python -m fire --help` or the source in `fire/core.py` before relying on it in production.*
