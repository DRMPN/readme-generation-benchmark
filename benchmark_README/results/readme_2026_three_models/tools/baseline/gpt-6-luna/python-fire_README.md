# Python Fire

Python Fire is a Python library for automatically generating command-line interfaces (CLIs) from Python objects. Call `fire.Fire()` on a module, class, object, function, dictionary, list, or other component to expose its functionality through the command line.

Fire can help you create CLIs with little additional code, try library functionality from a terminal, or explore existing Python modules. It also provides generated help, command tracing, interactive mode, and shell completion.

> Python Fire is not an official Google product.

## Installation

Python Fire requires Python 3.7 or later. Install the published package with pip:

```bash
pip install fire
```

The project documentation also lists a conda installation:

```bash
conda install fire -c conda-forge
```

To install from a source checkout, run:

```bash
python setup.py install
```

For development against the checkout, use:

```bash
python setup.py develop
```

## Quick start

Create a Python file such as `hello.py`:

```python
import fire

def hello(name='World'):
  return f'Hello {name}!'

if __name__ == '__main__':
  fire.Fire(hello)
```

Run the exposed function from a terminal:

```bash
python hello.py
# Hello World!

python hello.py David
# Hello David!
```

You can also pass named arguments and request help:

```bash
python hello.py --name=David
python hello.py --help
```

Calling `fire.Fire()` without a component exposes the calling context. This is useful for making several functions or values in a module available as commands:

```python
import fire

def add(x, y):
  return x + y

def multiply(x, y):
  return x * y

if __name__ == '__main__':
  fire.Fire()
```

For example, `python calculator.py add 10 20` calls `add` and prints its result. You can instead pass a selected component, such as a dictionary of commands, a class, or an object.

## Using a Fire CLI

A Fire command begins with the component passed to `Fire`. Additional command-line tokens can access its members, call functions, instantiate classes, or index into lists and tuples. For example, a command can select a method and supply its arguments:

```bash
python calculator.py double 10
python calculator.py double --number=15
```

Function arguments can generally be positional or named. Named arguments use flag syntax, such as `--name=value` or `--name value`; hyphens and underscores are interchangeable in member and flag names. Class constructor arguments must be supplied by name. Fire parses values from their command-line representation, including common Python literals such as numbers, strings, lists, tuples, and dictionaries.

A separator divides arguments for the current call from arguments to apply to its result. The default separator is `-`. This is useful with functions that accept variable arguments or when chaining operations. To change it, put Fire’s `--separator` flag after an isolated `--`:

```bash
python example.py items - upper
python example.py items X upper -- --separator=X
```

Fire-specific flags are normally placed after the final standalone `--`, which distinguishes them from arguments to your component. Help is an exception and can also be requested directly with `--help` or `-h`.

| Flag | Purpose |
| --- | --- |
| `--help`, `-h` | Show help and usage information for the current command. |
| `--interactive`, `-i` | Enter a Python REPL with useful context available. |
| `--separator=X` | Use `X` instead of the default `-` separator. |
| `--completion [shell]` | Print a completion script; Bash is the default, and `fish` is supported. |
| `--trace` | Show the steps Fire took to execute the command. |
| `--verbose`, `-v` | Include private members in help and usage output. This is primarily a debugging aid. |

For example:

```bash
python hello.py -- --trace
python hello.py -- --interactive
python hello.py -- --completion fish
```

Interactive mode uses IPython when it is installed; otherwise, Fire starts a regular Python REPL. Completion scripts can be saved and sourced in the relevant shell. If the commands exposed by a CLI change, regenerate its completion script.

For more examples and details on command behavior, see the [guide](docs/guide.md) and [Using a Fire CLI](docs/using-cli.md).

## Running Fire without changing a module

Fire can expose a module or Python file without adding a `fire` import or `Fire` call to it:

```bash
python -m fire calendar -h
python -m fire path/to/example.py hello --name=World
```

The first form accepts a module name; the second accepts a `.py` file path. See [the API quick reference](docs/api.md) for the `python -m fire` syntax and `Fire()` arguments.

## Configuration and customization

`fire.Fire()` accepts these arguments:

- `component`: The object to expose. If omitted, Fire uses the calling context.
- `command`: A command string or a list or tuple of argument strings. If omitted, Fire uses `sys.argv[1:]`.
- `name`: The CLI name shown in help and used for completion generation. If omitted, Fire infers it.
- `serialize`: A callable that converts results to text. Without one, Fire uses a component’s custom `__str__` when available and otherwise applies its standard output behavior.

The command separator defaults to `-`; change it with the `-- --separator=VALUE` Fire flag. For customized argument conversion, the `fire.decorators` module provides `SetParseFn` and `SetParseFns` decorators for specifying parsing functions.

## Development

The repository includes the library under `fire/`, tests alongside the implementation, and example CLIs under `examples/`. Documentation pages are in `docs/` and are configured with `mkdocs.yml`.

Install the project for development and add the test and lint tools. The package’s test dependencies include Hypothesis and Levenshtein; the CI requirements also list pytest, pylint, and pytest-related packages. Then run the test suite and lint from the repository root:

```bash
pytest
pylint fire
```

The pytest configuration in `setup.cfg` excludes `fire/test_components_py3.py` and `fire/parser_fuzz_test.py` from the default test run. Contribution guidance asks contributors to state their intent in an issue before making changes, fork the repository, and open a pull request for review. Contributions require a Contributor License Agreement. The project follows the Google Python Style Guide, with an 80-character line limit and two-space indentation; see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Troubleshooting

Avoid naming your own modules after standard-library modules such as `sys`, `linecache`, `cmd`, `bdb`, `repr`, `os`, `re`, `pprint`, or `traceback`. A name collision can cause Fire to import your module instead of the standard-library module and lead to errors. See [the troubleshooting guide](docs/troubleshooting.md).

## Documentation

- [Overview and basic usage](docs/index.md)
- [Installation](docs/installation.md)
- [Benefits](docs/benefits.md)
- [The Python Fire guide](docs/guide.md)
- [Using a Fire CLI](docs/using-cli.md)
- [API quick reference](docs/api.md)
- [Troubleshooting](docs/troubleshooting.md)

## License

Python Fire is distributed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for the license text.
