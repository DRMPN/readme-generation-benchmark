# python-fire-pcyk6w3x

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

Python Fire is a Python library for automatically generating command-line interfaces from virtually any Python object—functions, classes, modules, and more—often with a single call. It is aimed at developers building command-line tools in Python who want to expose existing code as a CLI without writing argument-parsing boilerplate. The library can be used programmatically or invoked directly from the command line on an existing module, and it provides help text, interactive REPL mode, and shell completion for generated CLIs. See the Getting Started section for runnable steps.

---

## Core Features

- **Automatic CLI generation from any Python object** — wrap functions, classes, modules, dicts, lists, and more into a runnable command-line interface with a single call, eliminating boilerplate argument parsing.
- **Run CLIs on code without modifying it** — invoke Fire against third-party or existing modules directly from the command line, by module name or file path, so you can expose tools you don't own.
- **Automatic argument parsing and member traversal** — command arguments are consumed to access members, call functions, and instantiate classes, turning chained commands into simple, predictable CLI calls.
- **Built-in help, tracing, and interactive REPL mode** — every generated CLI gets help and usage flags, a trace for debugging commands, and an optional interactive session with your components loaded (using IPython if available).
- **Shell completion script generation** — generate Bash or Fish completion scripts for your CLI, giving users tab-completion out of the box.

---

## Installation

Install python-fire-pcyk6w3x using one of the following methods:

**Using PyPi:**

```sh
pip install fire
```

---

## Getting Started

### Installation
To get started, install Python Fire from PyPI:

```bash
pip install fire
```

### Quickstart
Fire allows you to turn any Python component into a CLI with a single function call. Here is a minimal "Hello World" example using `fire.Fire()`.

Create a file (e.g., `example.py`) with the following content:

```python
import fire

def hello(name):
  return f'Hello {name}!'

if __name__ == '__main__':
  fire.Fire()
```

You can then run the function from the command line:

```bash
$ python example.py hello World
Hello World!
```

---

## API Reference

The public API of Python Fire is small and centered on a single entrypoint.

## `fire` (top-level package)

Exported via `fire/__init__.py` (`__all__ = ['Fire']`):

| Symbol | Purpose |
| --- | --- |
| `fire.Fire(component=None, command=None, name=None, serialize=None)` | Main entrypoint. Turns any Python object (function, class, module, etc.) into a CLI. Executes a command from the `command` argument or `sys.argv`, traversing the target component's members, calling functions, and instantiating classes. Returns the result of executing the command. |
| `fire.__version__` | Library version string (currently `'0.7.0'`). |

`Fire` parameters:
- `component`: The initial target component for the CLI.
- `command`: Optional command to execute (string or list of strings); defaults to `sys.argv`.
- `name`: Optional name of the command as entered at the command line; used in interactive mode and completion script generation.
- `serialize`: Optional callable used to serialize all objects to text.

`Fire` raises `ValueError` if `command` is not a string or sequence of arguments, and raises `FireExit` on errors (code 2) or when help/trace flags are used (code 0).

## Exceptions (`fire.core`)

| Symbol | Purpose |
| --- | --- |
| `FireError` | Exception used by Fire when a Fire command cannot be executed; caught internally and added to the Fire trace. |
| `FireExit(SystemExit)` | Exception raised to the client in the case of a `FireError`; the Fire program trace is available on its `trace` property. |

## Decorators (`fire.decorators`)

These decorators attach metadata telling Fire how to parse command line arguments for the decorated function:

| Symbol | Purpose |
| --- | --- |
| `SetParseFn(fn, *arguments)` | Sets the function Fire uses to parse args when calling the decorated function. With no `arguments`, sets the default parse function; otherwise applies it to the named arguments listed. |
| `SetParseFns(*positional, **named)` | Sets parse functions for positional and named arguments. Each parse function accepts a single string and returns the value to use in its place. |
| `GetMetadata(fn)` | Returns the metadata dict attached to a function (e.g. `ACCEPTS_POSITIONAL_ARGS`). |
| `GetParseFns(fn)` | Returns the parse-function metadata dict (`default`, `positional`, `named`) for a function. |

## Interactive mode (`fire.interact`)

| Symbol | Purpose |
| --- | --- |
| `Embed(variables, verbose=False)` | Drops into a Python REPL with the given `variables` available as local variables. Uses IPython's REPL when installed; otherwise falls back to the builtin `code.InteractiveConsole`. `verbose` controls whether hidden members (names starting with `_`) are shown. |

## CLI usage as a module (`fire/__main__.py`)

Fire can also be used without modifying target code via `python -m fire [module]`. The module's public functions:

| Symbol | Purpose |
| --- | --- |
| `import_module(module_or_filename)` | Imports a module by name or by `.py` file path, returning `(module, module_name)`. Raises `OSError`/`ValueError` for invalid files or modules. |
| `import_from_file_path(path)` | Imports a module given a file path. |
| `import_from_module_name(module_name)` | Imports a module by dotted module name. |
| `main(args)` | Entrypoint when invoked as `python -m fire`; imports the target and calls `fire.Fire` on it. |

Other helpers in `fire.core` (e.g. `Display`, `CompletionScript`) are used internally by Fire's flag handling (`--help`, `--trace`, `--completion`, `--interactive`) and are not part of the primary intended API surface.

---

## Examples

Examples of how this should work and how it should be used are available [here](./examples).

---

## Documentation

A detailed python-fire-pcyk6w3x description is available [here](./docs).

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to python-fire-pcyk6w3x.

---

## License

This project is protected under the Apache 2.0. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). python-fire-pcyk6w3x repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{python-fire-pcyk6w3x,

        author = {README Benchmark},

        title = {python-fire-pcyk6w3x repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---