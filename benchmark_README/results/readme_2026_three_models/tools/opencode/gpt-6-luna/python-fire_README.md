# Python Fire

Python Fire is a Python library for automatically generating command-line
interfaces (CLIs) from Python components. Call `fire.Fire()` on a function,
class, module, object, dictionary, list, or other component to expose it through
a CLI.

## Installation

Install from PyPI with pip:

```bash
pip install fire
```

Or install from conda-forge:

```bash
conda install fire -c conda-forge
```

This package requires Python 3.7 or newer. Its runtime dependency is
[`termcolor`](https://pypi.org/project/termcolor/).

## Quick start

Save this as `hello.py`:

```python
import fire


def hello(name='World'):
    return 'Hello %s!' % name


if __name__ == '__main__':
    fire.Fire(hello)
```

Run the function from the command line:

```console
$ python hello.py
Hello World!
$ python hello.py David
Hello David!
$ python hello.py --name=David
Hello David!
```

Fire converts command-line arguments to Python values where possible. Functions
can be called with positional arguments or named flags. When Fire is given a
class, constructor arguments are passed by name, for example
`python tool.py --setting=value command`.

## Expose multiple commands

Pass an object or class to `Fire` to expose its members as commands. For
example:

```python
import fire


class Calculator:
    def add(self, x, y):
        return x + y

    def multiply(self, x, y):
        return x * y


if __name__ == '__main__':
    fire.Fire(Calculator)
```

Now commands such as `python calculator.py add 10 20` and
`python calculator.py multiply 10 20` call the corresponding methods. Fire
traverses components as arguments are consumed: a command can select a member,
call a function, instantiate a class, index a list or tuple, or continue on the
result of a call. Pass a dictionary to `Fire` to choose and name the commands
explicitly.

Calling `fire.Fire()` without a component exposes the calling context's local
and global names. Alternatively, pass a specific component to limit what the
CLI exposes. `fire.Fire` also accepts `command`, `name`, and `serialize`
arguments; see the [API reference](docs/api.md).

## Use Fire with an existing module

Fire can turn a module or Python file into a CLI without changing its source:

```bash
python -m fire calendar --help
python -m fire path/to/script.py command --argument=value
```

The first argument can be a dotted Python module name or a path to a `.py`
file.

## CLI flags and help

Use `--help` or `-h` to display generated help and usage information. Fire uses
docstrings in its generated help. The other Fire-specific flags go after an
isolated `--`, which distinguishes them from arguments to the exposed Python
component:

| Flag | Purpose |
| --- | --- |
| `--interactive` or `-i` | Enter an interactive Python session after running the command. If IPython is installed, Fire uses it. |
| `--completion` (optionally `fish`) | Print a completion script for Bash or Fish. |
| `--trace` | Show the steps Fire took to execute the command. |
| `--separator=VALUE` | Change the default `-` separator used to end arguments to a function and continue on its result. |
| `--verbose` or `-v` | Include private members in help and usage information. |

For example, `python hello.py -- --interactive` enters interactive mode, and
`python hello.py -- --trace` prints a trace. Help can also be requested without
the isolated `--`, though `-- --help` makes clear that it is a Fire flag.

## Documentation and examples

- [The guide](docs/guide.md) covers command construction, argument parsing,
  chaining, and more.
- [Using a Fire CLI](docs/using-cli.md) explains command behavior and flags.
- [API quick reference](docs/api.md) documents `fire.Fire` arguments.
- [Benefits](docs/benefits.md) describes common uses for Fire.
- Runnable examples are in [`examples/`](examples/).

## Development

To install this checkout locally, run `python setup.py install`. To run the
test suite, install the test dependencies listed in `setup.py` and run
`pytest` from the repository root. See [CONTRIBUTING.md](CONTRIBUTING.md) for
contribution guidelines and linting instructions.

## License

Python Fire is licensed under the [Apache License, Version 2.0](LICENSE).

Python Fire is not an official Google product.
