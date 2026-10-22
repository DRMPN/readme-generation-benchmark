# Python Fire

**Python Fire is a library for automatically generating command line interfaces (CLIs) from absolutely any Python object.**

- Python Fire is a simple way to create a CLI in Python. [1]
- Python Fire is a helpful tool for developing and debugging Python code. [2]
- Python Fire helps with exploring existing code or turning other people's code into a CLI. [3]
- Python Fire makes transitioning between Bash and Python easier. [4]
- Python Fire makes using a Python REPL easier by setting up the REPL with the modules and variables you'll need already imported and created. [5]

[1] Part of the magic is that Python Fire automatically runs your code at the command line. Instead of writing a `main` method with argument parsing logic, you simply expose your functions and classes, and Fire turns them into CLI commands.

[2] Fire includes features like interactive mode (`--interactive`), verbose tracing (`--trace`), and automatic completion, which are invaluable when developing or debugging Python code.

[3] Fire can generate a CLI for any Python object: functions, classes, modules, objects, dictionaries, lists, and more. It inspects the object automatically and generates help and usage text.

[4] Fire handles flags, arguments, and quoting conventions so you can call Python code from Bash naturally, and pipe data between the two.

[5] Running a command with the `--interactive` flag drops you into an interactive Python REPL with the result of your command, along with any other modules and variables from your script, already loaded.

---

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Examples](#examples)
- [Benefits](#benefits-of-using-python-fire)
- [Using the CLI](#using-the-cli)
- [Guide](#guide)
- [Troubleshooting](#troubleshooting)
- [API Reference](#api-reference)
- [Development](#development)
- [License](#license)

---

## Installation

Install Python Fire from PyPI:

```bash
pip install fire
```

To install Python Fire with `conda`:

```bash
conda install fire
```

To install Python Fire from source:

```bash
git clone https://github.com/google/python-fire.git
cd python-fire
python setup.py install
```

---

## Basic Usage

Python Fire can be used with any Python object: functions, classes, modules, objects, dictionaries, lists, etc.

### Running a function

```python
# example.py
import fire


def hello(name="World"):
  return "Hello {name}!".format(name=name)


if __name__ == '__main__':
  fire.Fire(hello)
```

Then, from the command line, you can run:

```bash
python example.py hello
# Hello World!

python example.py hello David
# Hello David!

python example.py hello --name=Kevin
# Hello Kevin!
```

### Running a class

```python
# example.py
import fire


class Calculator(object):
  """A simple calculator class."""

  def double(self, number):
    return 2 * number


if __name__ == '__main__':
  fire.Fire(Calculator)
```

Then, from the command line, you can run:

```bash
python example.py double 10
# 20
```

### Running a module

You can also use Fire on an entire module, and Fire will automatically use all the public functions and classes in that module as commands:

```python
# example.py
import fire


def hello(name):
  return "Hello {name}!".format(name=name)


if __name__ == '__main__':
  fire.Fire()
```

```bash
python example.py hello World
# Hello World!
```

---

## Examples

Exposing multiple commands:

```python
# example.py
import fire


class BrokenCalculator(object):

  def __init__(self, offset=0):
    self._offset = offset

  def add(self, x, y):
    return x + y + self._offset

  def multiply(self, x, y):
    return x * y + self._offset


if __name__ == '__main__':
  fire.Fire(BrokenCalculator)
```

```bash
python example.py add 10 20
# 30

python example.py multiply 10 20 --offset=1
# 201

python example.py multiply 10 20
# 200
```

You can also use Fire for a group of commands by passing a dictionary:

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

```bash
python example.py add 2 3
# 5

python example.py multiply 2 3
# 6
```

---

## Benefits of Using Python Fire

Python Fire offers several benefits for building and working with CLIs:

1. **Simplicity**: Automatically generate a CLI without writing any argument parsing or help text boilerplate.
2. **Development tool**: Debug and develop code quickly from the command line using flags like `--interactive` and `--trace`.
3. **Code exploration**: Expose an existing codebase or third-party library as a CLI without modifying it.
4. **Bash/Python interop**: Fire handles type conversions and quoting, making it easier to mix Bash and Python.
5. **REPL convenience**: The `--interactive` flag starts a Python REPL pre-loaded with your modules, variables, and results.
6. **Automatic help**: Fire generates `--help` and usage documentation automatically from your code's docstrings and signatures.
7. **Completion**: Bash completion scripts can be generated for your CLI with `-- --completion`.

---

## Using the CLI

Python Fire CLIs support the following built-in flags:

| Flag | Description |
|------|-------------|
| `-h`, `--help` | Show help for the command. |
| `-v`, `--verbose` | Include more detail in the output. |
| `--interactive` | Start an interactive Python REPL after running the command. |
| `--trace` | Show a trace of the Fire execution, including each step taken. |
| `--verbose-trace` | Show a full trace with additional detail. |
| `--separator` | Change the separator used to split positional arguments (default is `-`). |
| `--completion` | Generate a script for Bash completion for the CLI. |
| `--help` | Show help for the command, and exit. |

**Separators**: Python Fire uses a hyphen `-` as a separator to separate positional arguments from other arguments. For example:

```bash
python example.py - arg1 arg2
```

You can change the separator with the `--separator` flag.

**Flags and arguments**: Functions can be called with positional arguments, named arguments, or flags:

```bash
python example.py hello --name=David
python example.py hello David
python example.py hello --name David
```

**Dashes and underscores**: Fire treats dashes and underscores interchangeably in member names and flag names, so `--name-flag` and `--name_flag` both work.

---

## Guide

### Calling Fire on various objects

| Object | Behavior |
|--------|----------|
| Function | Fire runs the function, using its arguments as CLI arguments. |
| Class | Fire runs the class's `__init__`, then the resulting object's members become subcommands. |
| Module | Fire uses the module's public members as subcommands. |
| Object | Fire uses the object's properties and methods as subcommands. |
| Dict | Fire uses the dict's keys as subcommands. |
| List / Tuple | Fire uses the indices as subcommands (e.g. `list 0`). |
| Other value | Fire simply prints the value. |

### Accessing properties

If you expose an object, its properties can be accessed from the command line:

```python
import fire


class City(object):

  def __init__(self, name, population):
    self.name = name
    self.population = population


if __name__ == '__main__':
  fire.Fire(City)
```

```bash
python example.py --name="New York" --population=8400000 name
# New York
```

### Chained function calls

Fire allows you to chain calls to the results of commands:

```bash
python example.py add 2 3 multiply 2
# (2 + 3) * 2 = 10
```

When you access a member of a returned object, Fire calls that member on the result. This makes it possible to compose powerful command chains.

### Argument parsing

Fire handles parsing of arguments, including automatic type conversion:

- Numeric strings become numbers (int or float).
- `True`/`False` become booleans.
- `{...}` is parsed as a dict, `[...]` as a list.
- Quoted strings are treated as strings.

To force a value to remain a string, use quotes:

```bash
python example.py hello --name='"123"'
```

### Variable args

Functions accepting `*args` can consume any number of positional arguments:

```python
import fire


def total(*args):
  return sum(args)


if __name__ == '__main__':
  fire.Fire(total)
```

```bash
python example.py 1 2 3 4
# 10
```

### Testing CLIs

The `testutils` module included with Fire provides helpers for testing Fire CLIs in your own test suites.

---

## Troubleshooting

Common issues and solutions:

- **Command not found**: Check that the member you're calling is exposed. Fire exposes public members of modules, classes, and objects (those not starting with a single underscore). Use `--verbose` or `--trace` to see how Fire is resolving your command.
- **Wrong argument types**: Fire parses arguments to numbers, booleans, lists, and dicts automatically. Quote arguments to force them to be treated as strings.
- **Conflicts with Bash flags**: Prefix Fire's built-in flags with `--` (e.g. `command -- --help`) to ensure they're passed to Fire rather than interpreted by your shell or script.
- **Errors in trace mode**: Use `--trace` to see exactly how Fire interpreted your command and which function was called with which arguments.
- **Need to explore interactively**: Add `--interactive` to your command to drop into a REPL with the state of your program loaded.

For more details, see the [troubleshooting documentation](troubleshooting.md).

---

## API Reference

### `fire.Fire(component=None, command=None, name=None)`

- **component**: The component to turn into a CLI. Can be a function, class, module, object, dict, list, or other value. If omitted, Fire uses the calling module.
- **command**: An optional Bash-style command string to execute instead of reading arguments from the command line.
- **name**: The name of the CLI, used in help text and completion scripts.

### Other modules

| Module | Description |
|--------|-------------|
| `fire.core` | The core Fire engine that parses commands and executes components. |
| `fire.parser` | The parser that tokenizes command-line arguments into Fire's command grammar. |
| `fire.decorators` | Decorators like `fire.decorators.SetParseFn` for customizing how Fire handles components. |
| `fire.helptext` | Generates help text and usage documentation from docstrings and signatures. |
| `fire.docstrings` | Parses docstrings (Google style and others) for use in generated help. |
| `fire.custom_descriptions` | Determines and customizes component descriptions shown in help output. |
| `fire.inspectutils` | Utilities for inspecting Python objects and getting their signatures. |
| `fire.completion` | Generates Bash completion scripts for Fire CLIs. |
| `fire.trace` | Records the trace of a Fire execution, used by `--trace`. |
| `fire.console` | Console I/O, text formatting, and paging used for rich terminal output (platform-dependent, including Windows support via `formatting_windows`). |
| `fire.parser_fuzz_test` / `fire.docstrings_fuzz_test` | Fuzz tests validating the parser and docstring handling. |
| `fire.testutils` | Utilities for testing CLIs built with Fire. |
| `fire.interact` | Implements the `--interactive` REPL mode. |
| `fire.value_types` | Logic for recognizing and parsing special value types on the command line. |
| `fire.files` | Utilities for working with files, e.g. locating the calling module. |
| `fire.encoding` | Encoding utilities for terminal output. |

---

## Development

To run the test suite locally:

```bash
pip install -r requirements.txt
python -m pytest
```

Linting is configured via `.pylintrc`, and package metadata lives in `setup.py` and `setup.cfg`. Documentation for this project is built with MkDocs, configured in `mkdocs.yml`, with sources in `index.md`, `guide.md`, `benefits.md`, `using-cli.md`, `installation.md`, `api.md`, and `troubleshooting.md`.

To build the documentation:

```bash
mkdocs build
```

---

## License

This project is licensed under the terms of the [LICENSE](LICENSE) file included in the repository.
