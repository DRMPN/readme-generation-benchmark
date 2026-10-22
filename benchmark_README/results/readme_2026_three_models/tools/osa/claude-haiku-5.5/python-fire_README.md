# python-fire-ws_i3wns

---

[![PyPi](https://badge.fury.io/py/fire.svg)](https://badge.fury.io/py/fire)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

Python Fire is a Python library that generates command-line interfaces from existing Python objects, such as functions, classes, modules, and instances, with a single call to `Fire()`. It is intended for Python developers who want to expose existing code as a command-line tool without writing argument-parsing logic. The library can also be run against an existing Python module from the command line, so code can be used as a CLI without modifying it. For runnable steps and usage details, see the Getting Started section and the linked documentation.

---

## Core Features

- **Turns existing Python code into a CLI:** A single call to Fire can expose functions, classes, modules, and objects as command-line interfaces. Developers can reuse existing code without rewriting it for the command line.
- **Dispatches nested commands:** Command arguments are consumed in order to access members, call functions, or instantiate classes. Developers can expose nested behavior through one command string.
- **Generates help and usage output:** The --help flag shows usage for any command, and --verbose includes private members. Developers can discover available commands and arguments without reading the source.
- **Parses arguments as Python values:** Arguments that are Python literals or containers, such as lists and dicts, are converted to those types. Unquoted words are treated as strings, so developers can pass structured input directly.
- **Generates completion scripts:** Fire can produce completion scripts for a CLI, so commands and flags can be completed in the terminal.

---

## Installation

Install python-fire-ws_i3wns using one of the following methods:

**Using PyPi:**

```sh
pip install fire
```

---

## Getting Started

Python Fire requires Python 3.7 or later.

1. Install Python Fire from PyPI:

```bash
pip install fire
```

2. Create a file named `example.py` with the following content:

```python
import fire

def hello(name):
  return f'Hello {name}!'

if __name__ == '__main__':
  fire.Fire()
```

3. Run the `hello` command:

```bash
python example.py hello World
```

Expected output:

```text
Hello World!
```

4. Show the help screen for the CLI:

```bash
python example.py --help
```

---

## API Reference

Python Fire is used through one public entrypoint, `fire.Fire`. The symbols below are the ones present in the provided key files.

### Package entrypoint (`fire`)

| Symbol | Purpose |
|---|---|
| `fire.Fire(component=None, command=None, name=None, serialize=None)` | Builds a CLI from `component` and runs `command` (a string or list of strings), or `sys.argv[1:]` if `command` is omitted. Defined in `fire/core.py` and exported via `__all__`. |
| `fire.__version__` | Package version string (`'0.7.0'`). |

`Fire` behavior from its docstring:
- Raises `ValueError` if `command` is not a string or a sequence of arguments.
- Raises `FireExit` with code `2` when a `FireError` occurs.
- Raises `FireExit` with code `0` when the help or trace flags are used and succeed.

### Core helpers (`fire.core`)

| Symbol | Purpose |
|---|---|
| `Display(lines, out)` | Writes the joined `lines` to `out` through `console_io.More`. |
| `CompletionScript(name, component, shell)` | Returns the completion script text for a Fire CLI. |
| `FireError` | Exception used internally by Fire; it is caught and recorded in the trace rather than raised by `Fire`. |
| `FireExit` | `SystemExit` subclass raised to the caller on Fire errors or on help/trace output. Its trace is exposed on the `trace` property. |

### Argument parsing (`fire.parser`)

These functions are defined in `fire/parser.py` and are not re-exported from the `fire` package.

| Symbol | Purpose |
|---|---|
| `CreateParser()` | Returns the `argparse` parser for Fire flags (`--verbose`, `--interactive`, `--separator`, `--completion`, `--help`, `--trace`). |
| `SeparateFlagArgs(args)` | Splits arguments at the last `--` into Fire args and flag args. |
| `DefaultParseValue(value)` | Parses a command-line string as a Python literal, or returns it as a string. |

### Module entrypoint (`fire.__main__`)

Run with `python -m fire [module]`, where `module` is a dotted module name or a path to a `.py` file.

| Symbol | Purpose |
|---|---|
| `main(args)` | Entrypoint used by `python -m fire`; imports the target and calls `fire.Fire`. |
| `import_module(module_or_filename)` | Imports a module by name or from a `.py` file path. |

### Example usage

`examples/widget/widget.py` defines a `Widget` class with `whack(n=1)` and `bang(noise='bang')` methods. Its `main()` calls `fire.Fire(Widget(), name='widget')`.

---

## Examples

Examples of how this should work and how it should be used are available [here](./examples).

---

## Documentation

A detailed python-fire-ws_i3wns description is available [here](./docs).

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to python-fire-ws_i3wns.

---

## License

This project is protected under the Apache 2.0. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). python-fire-ws_i3wns repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{python-fire-ws_i3wns,

        author = {README Benchmark},

        title = {python-fire-ws_i3wns repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---