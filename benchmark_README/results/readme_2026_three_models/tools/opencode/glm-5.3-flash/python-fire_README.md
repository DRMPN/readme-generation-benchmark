# Python Fire

_Python Fire is a library for automatically generating command line interfaces
(CLIs) from absolutely any Python object._

- Python Fire is a simple way to create a CLI in Python.
- Python Fire is a helpful tool for developing and debugging Python code.
- Python Fire helps with exploring existing code or turning other people's
  code into a CLI.
- Python Fire makes transitioning between Bash and Python easier.
- Python Fire makes using a Python REPL easier by setting up the REPL with the
  modules and variables you'll need already imported and created.

## Installation

To install Python Fire with pip, run: `pip install fire`

To install Python Fire with conda, run: `conda install fire -c conda-forge`

To install Python Fire from source, first clone the repository and then run:
`python setup.py install`. To install from source for development, instead run
`python setup.py develop`.

## Basic Usage

You can call `Fire` on any Python object: functions, classes, modules,
objects, dictionaries, lists, tuples, etc. They all work!

Here's an example of calling Fire on a function.

```python
import fire

def hello(name="World"):
  return "Hello %s!" % name

if __name__ == '__main__':
  fire.Fire(hello)
```

Then, from the command line, you can run:

```bash
python hello.py  # Hello World!
python hello.py --name=David  # Hello David!
python hello.py --help  # Shows usage information.
```

Here's an example of calling Fire on a class.

```python
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
python calculator.py double 10  # 20
python calculator.py double --number=15  # 30
```

## Using a Fire CLI

Every Fire command corresponds to a Python component. You can extend a command
by adding the name of a member of an object, a key of a dict, or the index of
an element of a list or tuple. If your command corresponds to a function, you
can call it with arguments specified positionally or by name (flag syntax).

Flags to Fire should be separated from the Fire command by an isolated `--` in
order to distinguish between flags and named arguments. For example, to enter
interactive mode, append `-- -i` or `-- --interactive` to any command. Help is
an exception; the isolated `--` is optional for getting help.

| Using a CLI     | Command                                 | Notes                                      |
| :-------------- | :-------------------------------------- | :----------------------------------------- |
| Help            | `command --help` or `command -- --help` |                                            |
| REPL            | `command -- --interactive`              | Enters interactive mode.                   |
| Separator       | `command -- --separator=X`              | Sets the separator to `X`.                 |
| Completion      | `command -- --completion [shell]`       | Generates a completion script for the CLI. |
| Trace           | `command -- --trace`                    | Gets a Fire trace for the command.         |
| Verbose         | `command -- --verbose`                  |                                            |

## Reference

| Setup   | Command             | Notes
| :------ | :------------------ | :---------
| install | `pip install fire`  |

| Creating a CLI | Command                | Notes
| :--------------| :--------------------- | :---------
| import         | `import fire`          |
| Call           | `fire.Fire()`          | Turns the current module into a Fire CLI.
| Call           | `fire.Fire(component)` | Turns `component` into a Fire CLI.

## Why is it called Fire?

When you call `Fire`, it fires off (executes) your command.

## Examples

The [`examples/`](examples/) directory contains example Fire CLIs, including:

- `examples/cipher` — a cipher example
- `examples/diff` — a diff example
- `examples/identity` — an identity example
- `examples/widget` — a widget example with a collector

## Documentation

Additional documentation is available in the [`docs/`](docs/) directory:

- [Installation](docs/installation.md)
- [Benefits](docs/benefits.md)
- [The Python Fire Guide](docs/guide.md)
- [Using a Fire CLI](docs/using-cli.md)
- [Troubleshooting](docs/troubleshooting.md)
- [API Reference](docs/api.md)

The docs are built with [MkDocs](https://www.mkdocs.org/) using the
configuration in [`mkdocs.yml`](mkdocs.yml).

## Development

### Requirements

Python Fire requires Python 3.7 or later. Its runtime dependency is
`termcolor`; the test dependencies are `hypothesis` and `levenshtein` (see
[`setup.py`](setup.py)).

### Testing

Python Fire uses GitHub Actions to run tests on each pull request. You can run
these tests yourself as well. To do this, first install the test dependencies
listed in setup.py (e.g. pytest, mock, termcolor, and hypothesis). Then run
the tests by running `pytest` in the root directory of the repository.

### Linting

Please run lint on your pull requests to make accepting the requests easier.
To do this, run `pylint fire` in the root directory of the repository. Note
that even if lint is passing, additional style changes to your submission may
be made during merging.

## Contributing

We'd love to accept your patches and contributions. Please see
[`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines, including the requirement
to sign the [Contributor License Agreement](https://cla.developers.google.com/)
before making your first contribution.

Python Fire follows the guidelines in the
[Google Python Style Guide](http://google.github.io/styleguide/pyguide.html).
In addition, the project follows a convention of:

- Maximum line length: 80 characters
- Indentation: 2 spaces (4 for line continuation)
- PascalCase for function and method names
- Single quotes around strings, three double quotes around docstrings

## Compatibility

Python Fire supports Python 3.7 through 3.13 and is OS independent (see the
classifiers in [`setup.py`](setup.py)).

## License

Licensed under the [Apache 2.0](LICENSE) License.

## Disclaimer

This is not an official Google product.
