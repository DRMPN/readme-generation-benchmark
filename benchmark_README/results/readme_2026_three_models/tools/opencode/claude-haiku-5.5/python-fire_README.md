# Python Fire

[![PyPI](https://img.shields.io/pypi/pyversions/fire.svg?style=plastic)](https://github.com/google/python-fire)

Python Fire is a library for automatically generating command line interfaces (CLIs) from Python objects. You pass any Python component (a function, class, object, module, dict, list, or tuple) to `fire.Fire()`, and Fire exposes it as a CLI with no argument-parsing code.

Python Fire is not an official Google product.

## Installation

Install from PyPI:

```bash
pip install fire
```

Install with conda:

```bash
conda install fire -c conda-forge
```

Install from source:

```bash
git clone https://github.com/google/python-fire.git
cd python-fire
python setup.py install
```

For development, use `python setup.py develop` instead.

Python Fire declares support for Python 3.7 and later (`requires_python='>=3.7'`). Its only runtime dependency is `termcolor`.

## Quick Start

Call `fire.Fire()` on any function:

```python
import fire

def hello(name="World"):
  return "Hello %s!" % name

if __name__ == '__main__':
  fire.Fire(hello)
```

```bash
python hello.py                # Hello World!
python hello.py --name=David   # Hello David!
python hello.py --help         # Shows usage information.
```

Call `fire.Fire()` on a class. Its methods become subcommands:

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
python calculator.py double 10          # 20
python calculator.py double --number=15 # 30
```

If you call `fire.Fire()` with no component, Fire uses the module's locals and globals, so every function defined in the module becomes a command:

```python
import fire

def add(x, y):
  return x + y

def multiply(x, y):
  return x * y

if __name__ == '__main__':
  fire.Fire()
```

```bash
python example.py add 10 20       # 30
python example.py multiply 10 20  # 200
```

Fire parses arguments by their values, so `10` is an `int` and `10.0` is a `float`. Bare words are treated as strings.

## Usage

### Core API

| Call | Description |
| :--- | :--- |
| `fire.Fire()` | Turns the current module into a Fire CLI. |
| `fire.Fire(component)` | Turns `component` into a Fire CLI. |

`fire.Fire()` accepts these optional arguments:

| Argument | Description |
| :--- | :--- |
| `component` | The object to expose. If omitted, Fire uses a dict of the calling context's locals and globals. |
| `command` | A string or a list of arguments to run instead of `sys.argv[1:]`. A string is split into arguments. |
| `name` | The CLI name shown in help screens. If omitted, Fire infers it from `sys.argv[0]`. |
| `serialize` | A callable that converts the result to text. If omitted, simple types use `str()`, and objects with a custom `__str__` use that method. |

### Running a module without modifying it

You can use Fire on a module without changing its source:

```bash
python -m fire <module> <arguments>
python -m fire <filepath> <arguments>
```

For example, `python -m fire calendar -h` shows help for the standard library `calendar` module.

### Commands for Fire objects

A Fire command maps onto a Python object, and each argument extends that mapping:

- **Object members:** Add a method or property name to access it. Hyphens and underscores are interchangeable, so `high-score` and `high_score` both work.
- **Dict keys:** Add a key name to access that value.
- **List and tuple indexes:** Add an index to access that element.
- **Functions:** Add arguments by position (`command 5`) or by flag (`command --value 5`).
- **Classes:** Add the `__init__` arguments as flags, such as `--name=...`. Constructor arguments must use flag syntax.
- **Callable objects:** Arguments to `__call__` must use flag syntax.

Example, using a class with a constructor and a method:

```python
class Building(object):

  def __init__(self, name, stories=1):
    self.name = name
    self.stories = stories

  def climb_stairs(self, stairs_per_story=10):
    for story in range(self.stories):
      for stair in range(1, stairs_per_story):
        yield stair
      yield 'Phew!'
    yield 'Done!'

if __name__ == '__main__':
  fire.Fire(Building)
```

```bash
python example.py --name="Sherrerd Hall" --stories=3 climb_stairs 10
python example.py --name="Sherrerd Hall" climb_stairs --stairs_per_story=10
python example.py climb-stairs --stairs-per-story 10 --name="Sherrerd Hall"
```

Fire also works with dicts, lists, `*args`/`**kwargs` functions, and `async` functions. For async functions, Fire runs the coroutine and blocks until it completes.

### Chaining

Fire applies commands from left to right, so each step operates on the result of the previous one. For example, `python example.py --code=ALB city upper` looks up a city and then calls `upper()` on the result.

To build chainable methods, have each method return `self`.

### Separator

A separator (default `-`) ends the arguments for a function call. Arguments after the separator apply to the function's result, not to the function itself:

```bash
python example.py dog cat elephant - upper    # CAT DOG ELEPHANT
python example.py dog cat elephant upper      # without a separator, "upper" becomes an argument
```

Change the separator with `--separator`. Flags always come after an isolated `--`:

```bash
python example.py dog cat elephant X upper -- --separator=X
```

### Serialization

If the final result has a custom `__str__` method, Fire prints the serialized object. If it does not, Fire shows the object's help screen instead.

### Booleans

`True` and `False` parse as booleans. Flag forms `--name` and `--noname` set `name` to `True` and `False`. A boolean flag followed by a plain token takes that token as its value. To avoid this, put a separator after the flag, write the value explicitly (`--obj=True`), or follow the flag with another flag.

### Quoting

Your shell processes quotes before Fire sees the arguments. To pass the string `"10"` rather than the integer `10`, use `'"10"'` or `\"10\"`. To pass a dict, wrap it in single quotes:

```bash
python example.py '{"name": "David Bieber"}'
```

## Flags

Fire flags go after an isolated `--` argument. Everything after the last `--` is treated as a flag, and everything before it is part of the Fire command:

```bash
python widget.py bang --noise=boom -- --verbose
```

`--help` is the only exception: `python example.py --help` and `python example.py -h` also work without the `--`.

| Flag | Usage | Description |
| :--- | :--- | :--- |
| [`--help` / `-h`](docs/using-cli.md#help-flag) | `command -- --help` | Show help and usage information for the command. |
| [`--interactive` / `-i`](docs/using-cli.md#interactive-flag) | `command -- --interactive` | Enter a Python REPL with the Fire component and the calling context's variables available. Uses IPython if it is installed. |
| [`--separator`](docs/using-cli.md#separator-flag) | `command -- --separator=X` | Set the separator to `X`. The default is `-`. |
| [`--completion`](docs/using-cli.md#completion-flag) | `command -- --completion [shell]` | Print a completion script for the CLI. Bash is the default. Use `fish` for the Fish shell. |
| [`--trace`](docs/using-cli.md#trace-flag) | `command -- --trace` | Print a step-by-step trace of how Fire resolved the command. |
| [`--verbose` / `-v`](docs/using-cli.md#verbose-flag) | `command -- --verbose` | Include private members in help and usage output. This is intended as a debugging aid and is not fully supported. |

Example of saving a Bash completion script:

```bash
widget -- --completion > ~/.widget-completion
```

Source the file from your `.bashrc`. Regenerate it if the CLI's commands change.

## Documentation

- [Overview](docs/index.md)
- [Installation](docs/installation.md)
- [Benefits](docs/benefits.md)
- [The Python Fire Guide](docs/guide.md)
- [Using a Fire CLI](docs/using-cli.md)
- [Troubleshooting](docs/troubleshooting.md)
- [API Reference](docs/api.md)

Examples are in the [`examples/`](examples/) directory, including `cipher`, `diff`, `identity`, and `widget`.

## Troubleshooting

Do not name your module after a standard-library module that Fire imports, such as `sys`, `os`, `re`, `cmd`, `traceback`, or `pprint`. If you do, Fire may import your module instead of the built-in one, which can cause errors such as `AttributeError`. See [docs/troubleshooting.md](docs/troubleshooting.md) for details.

## Development

Python Fire's tests run with GitHub Actions on each pull request. To run them locally:

```bash
python setup.py develop
pip install pytest hypothesis levenshtein termcolor
python -m pytest
```

The `setup.cfg` file ignores `fire/test_components_py3.py` and `fire/parser_fuzz_test.py` by default. To run lint:

```bash
pylint fire
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution process, the Contributor License Agreement requirement, and code style guidelines.

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
