# Python Fire

Python Fire is a library for automatically generating command line interfaces (CLIs) from absolutely any Python object.

It will turn any Python module, class, object, function, etc. (any Python component will work!) into a CLI. It's called Fire because when you call `Fire()`, it fires off your command.

## Benefits of Python Fire

- **Create CLIs in Python** — Simply write the functionality you want exposed at the command line as a function, module, or class, and then call Fire. With this addition of a single-line call to Fire, your CLI is ready to go.
- **Develop and debug Python code** — You can run all of your library's functionality from the command line without having to keep making changes to a main method. The `--interactive` flag enters an IPython REPL with your modules and variables already loaded.
- **Explore existing code; turn other people's code into a CLI** — Call `Fire` on an existing module—even one without available source code—and see the functionality it exposes through auto-generated help strings. Call `Fire` on the difflib library and you get a powerful diffing tool.
- **Transition between Bash and Python** — Call Python directly from Bash and mix your Python functions with the unix tools you know and love, like `grep`, `xargs`, `wc`, etc.
- **Explore code in a Python REPL** — The `--interactive` flag starts an IPython REPL with the modules and variables you'll need already imported and created.

## Installation

To install Python Fire with pip, run:

```
pip install fire
```

To install Python Fire with conda, run:

```
conda install fire -c conda-forge
```

To install Python Fire from source, first clone the repository and then run:

```
python setup.py install
```

To install from source for development, instead run:

```
python setup.py develop
```

Python Fire requires Python 3.7 or later and supports Python 3.7–3.13. Its only runtime dependency is `termcolor`. Test dependencies include `hypothesis` and `levenshtein`.

## Basic Usage

You can call `Fire` on any Python object: functions, classes, modules, objects, dictionaries, lists, tuples, etc. They all work!

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

### Hello World Variants

The easiest way to use Fire is to take any Python program and simply call `fire.Fire()` at the end of the program. This will expose the full contents of the program to the command line:

```python
import fire

def hello(name):
  return f'Hello {name}!'

if __name__ == '__main__':
  fire.Fire()
```

```bash
$ python example.py hello World
Hello World!
```

Calling `fire.Fire(hello)` exposes only the `hello` function, so you can run `python example.py World` directly.

You can also write a main function:

```python
import fire

def hello(name):
  return f'Hello {name}!'

def main():
  fire.Fire(hello)

if __name__ == '__main__':
  main()
```

Or, if you're using entry points, simply:

```python
import fire

def hello(name):
  return f'Hello {name}!'

def main():
  fire.Fire(hello)
```

### Using Fire Without Modifying Any Code

You can use Python Fire on a module without modifying the code of the module. The syntax is:

```
python -m fire <module> <arguments>
```

or

```
python -m fire <filepath> <arguments>
```

For example:

```bash
$ python -m fire example hello --name=World
Hello World!
$ python -m fire example.py hello --name=World
Hello World!
```

You can also run it on built-in modules, e.g. `python -m fire calendar -h` treats the built-in `calendar` module as a CLI and provides its help.

### Exposing Multiple Commands

The simplest way to expose multiple commands is to write multiple functions and call `Fire()`. You can also selectively expose functions with a dict, or use an object or a class:

```python
import fire

class Calculator(object):

  def add(self, x, y):
    return x + y

  def multiply(self, x, y):
    return x * y

if __name__ == '__main__':
  fire.Fire(Calculator)
```

```bash
$ python example.py add 10 20
30
$ python example.py multiply 10 20
200
```

When you pass a class, you can also pass arguments for constructing the class:

```python
import fire

class BrokenCalculator(object):

  def __init__(self, offset=1):
      self._offset = offset

  def add(self, x, y):
    return x + y + self._offset

  def multiply(self, x, y):
    return x * y + self._offset

if __name__ == '__main__':
  fire.Fire(BrokenCalculator)
```

```bash
$ python example.py add 10 20
31
$ python example.py add 10 20 --offset=0
30
```

Unlike calling ordinary functions, which can be done both with positional arguments and named arguments (`--flag` syntax), arguments to `__init__` functions must be passed with the `--flag` syntax.

### Grouping Commands

Commands can be nested in arbitrarily complex ways:

```python
class IngestionStage(object):

  def run(self):
    return 'Ingesting! Nom nom nom...'

class DigestionStage(object):

  def run(self, volume=1):
    return ' '.join(['Burp!'] * volume)

  def status(self):
    return 'Satiated.'

class Pipeline(object):

  def __init__(self):
    self.ingestion = IngestionStage()
    self.digestion = DigestionStage()

  def run(self):
    ingestion_output = self.ingestion.run()
    digestion_output = self.digestion.run()
    return [ingestion_output, digestion_output]

if __name__ == '__main__':
  fire.Fire(Pipeline)
```

```bash
$ python example.py run
Ingesting! Nom nom nom...
Burp!
$ python example.py ingestion run
Ingesting! Nom nom nom...
$ python example.py digestion status
Satiated.
```

### Chaining Function Calls

When you run a Fire command, you can take all the same actions on the result of the call that you can take on the original object passed in:

```bash
$ python example.py --code=ALB city upper
ALBANY-SCHENECTADY-TROY
```

If you want to set up your functions to chain nicely, have a class whose methods return `self`.

### Custom Serialization

You can determine how a component will be serialized by defining its `__str__` method. If a custom `__str__` method is present on the final component, the object is serialized and printed. If there's no custom `__str__` method, then the help screen for the object is shown instead.

Alternatively, pass a `serialize` argument to `fire.Fire()`; if specified, all objects are serialized to text via the provided method.

## Using a Fire CLI

Every Fire command corresponds to a Python component. Given a Fire command that corresponds to a Python object, you can extend that command to:

- **Access a member of an object** — add the name of a member of that object as a new argument to the command.
- **Access a member of a dict** — add one of the dict's keys as an argument.
- **Access a member of a list or tuple** — add the index of an element as an argument (e.g. `widget function-that-returns-list 2`).
- **Call a function** — add the arguments of the function, specified positionally or by name using flag syntax.

### Calling Functions

Arguments to a constructor are passed by name using flag syntax `--name=value`. Arguments to other functions may be passed positionally or by name.

```bash
$ python example.py --name="Sherrerd Hall" --stories=3 climb_stairs 10
$ python example.py --name="Sherrerd Hall" climb_stairs --stairs_per_story=10
$ python example.py --name="Sherrerd Hall" climb_stairs --stairs-per-story 10
$ python example.py climb-stairs --stairs-per-story 10 --name="Sherrerd Hall"
```

Note that hyphens and underscores (`-` and `_`) are interchangeable in member names and flag names, and the equal sign between the flag name and its value is optional.

Fire also supports functions with `*varargs` and `**kwargs`, and async functions — whenever Fire encounters a coroutine function, it runs it, blocking until it completes.

You can use a separator to indicate that you're done providing arguments to a function. All arguments after the separator will be used to process the result of the function, rather than being passed to the function itself:

```bash
$ python example.py dog cat elephant - upper
CAT DOG ELEPHANT
```

### Argument Parsing

The types of the arguments are determined by their values, rather than by the function signature where they're used. You can pass any Python literal from the command line: numbers, strings, tuples, lists, dictionaries (sets are only supported in some versions of Python). You can also nest the collections arbitrarily as long as they only contain literals.

```bash
$ python example.py 10
int
$ python example.py 10.0
float
$ python example.py hello
str
$ python example.py '(1,2)'
tuple
$ python example.py [1,2]
list
$ python example.py True
bool
$ python example.py {name:David}
dict
```

Bare-words are automatically replaced with strings. Be careful with your quotes — Bash processes your arguments first, and then Fire parses the result of that.

### Boolean Arguments

The tokens `True` and `False` are parsed as boolean values. You may also specify booleans via flag syntax `--name` and `--noname`, which set `name` to `True` and `False` respectively.

Be careful with boolean flags! If a token other than another flag immediately follows a flag that's supposed to be a boolean, the flag will take on the value of the token rather than the boolean value. You can resolve this by putting a separator after your last flag, by explicitly stating the value of the boolean flag (as in `--obj=True`), or by making sure there's another flag after any boolean flag argument.

## Fire Flags

Fire CLIs all come with a number of flags. These flags should be separated from the Fire command by an isolated `--`. If there is at least one isolated `--` argument, then arguments after the final isolated `--` are treated as flags, whereas all arguments before the final isolated `--` are considered part of the Fire command.

| Setup   | Command             | Notes
| :------ | :------------------ | :---------
| install | `pip install fire`  |

| Creating a CLI | Command                | Notes
| :--------------| :--------------------- | :---------
| import         | `import fire`          |
| Call           | `fire.Fire()`          | Turns the current module into a Fire CLI.
| Call           | `fire.Fire(component)` | Turns `component` into a Fire CLI.

| Using a CLI    | Command                    | Notes
| :------------- | :------------------------- | :---------
| Help           | `command -- --help` | Show help and usage information for the command.
| REPL           | `command -- --interactive` | Enter interactive mode.
| Separator      | `command -- --separator=X` | This sets the separator to `X`. The default separator is `-`.
| Completion     | `command -- --completion [shell]` | Generate a completion script for the CLI.
| Trace          | command `-- --trace` | Gets a Fire trace for the command.
| Verbose        | `command -- --verbose` | Include private members in the output.

_Note that flags are separated from the Fire command by an isolated `--` arg. Help is an exception; the isolated `--` is optional for getting help._

You can add the help flag to any command to see help and usage information. Fire incorporates your docstrings into the help and usage information that it generates, including type annotations and default values where available.

## Arguments for Calling fire.Fire()

| Argument  | Usage                     | Notes                                |
| --------- | ------------------------- | ------------------------------------ |
| component | `fire.Fire(component)`    | If omitted, defaults to a dict of all locals and globals. |
| command   | `fire.Fire(command='hello --name=5')` | Either a string or a list of arguments. If a string is provided, it is split to determine the arguments. If a list or tuple is provided, they are the arguments. If `command` is omitted, then `sys.argv[1:]` (the arguments from the command line) are used by default. |
| name      | `fire.Fire(name='tool')`  | The name of the CLI, ideally the name users will enter to run the CLI. This name will be used in the CLI's help screens. If the argument is omitted, it will be inferred automatically.|
| serialize | `fire.Fire(serialize=custom_serializer)` | If omitted, simple types are serialized via their builtin str method, and any objects that define a custom `__str__` method are serialized with that. If specified, all objects are serialized to text via the provided method. |

## Examples

The `examples/` directory contains additional example programs, including:

- `examples/cipher` — a cipher example
- `examples/diff` — a diff example (with `difffull.py`)
- `examples/identity` — an identity example
- `examples/widget` — a widget example with a collector

Each example includes a corresponding `_test.py` file demonstrating testing practices.

## Documentation

The `docs/` directory contains extensive documentation, including:

- `docs/index.md` — overview and quick reference
- `docs/guide.md` — The Python Fire Guide, with detailed walkthroughs of Fire's features
- `docs/using-cli.md` — How to use a Fire CLI
- `docs/installation.md` — Installation instructions
- `docs/api.md` — Quick reference
- `docs/benefits.md` — Benefits of Python Fire
- `docs/troubleshooting.md` — Known issues

Documentation is built with MkDocs (see `mkdocs.yml`).

## Troubleshooting

### Don't name your module "cmd"

If you have a module name that conflicts with the name of a builtin module, then when Fire goes to import the builtin module, it will import your module instead. This will result in an error, possibly an `AttributeError`. Specifically, do not name your module any of the following: `sys`, `linecache`, `cmd`, `bdb`, `repr`, `os`, `re`, `pprint`, `traceback`.

If you have an issue not resolved in the troubleshooting docs, consider opening a [GitHub Issue](https://github.com/google/python-fire/issues).

## Development

### Contributing

We'd love to accept your patches and contributions to this project. There are just a few small guidelines you need to follow:

1. Read the guidelines in `CONTRIBUTING.md`.
2. Before you begin making changes, state your intent to do so in an Issue.
3. Fork the project. Make changes in your copy of the repository.
4. Open a pull request once your changes are ready.
5. If this is your first contribution, sign the [Contributor License Agreement](https://cla.developers.google.com/). Contributions to this project must be accompanied by a CLA. You (or your employer) retain the copyright to your contribution; this simply gives us permission to use and redistribute your contributions as part of the project.

You generally only need to submit a CLA once, so if you've already submitted one (even if it was for a different project), you probably don't need to do it again.

### Code Reviews

All submissions, including submissions by project members, require review. For changes introduced by non-Googlers, GitHub pull requests are used for this purpose. Consult [GitHub Help](https://help.github.com/articles/about-pull-requests/) for more information on using pull requests.

### Code Style

In general, Python Fire follows the guidelines in the [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html). In addition, the project follows a convention of:

- Maximum line length: 80 characters
- Indentation: 2 spaces (4 for line continuation)
- PascalCase for function and method names
- Single quotes around strings, three double quotes around docstrings

Lint configuration is provided in `pylintrc`.

### Testing

Python Fire uses [GitHub Actions](https://github.com/google/python-fire/actions) to run tests on each pull request. You can run these tests yourself as well. To do this, first install the test dependencies listed in `setup.py` (e.g. pytest, mock, termcolor, and hypothesis). Then run the tests by running:

```
pytest
```

in the root directory of the repository.

Note that `setup.cfg` configures pytest to ignore `fire/test_components_py3.py` and `fire/parser_fuzz_test.py` by default. Fuzz tests (`fire/parser_fuzz_test.py`, `fire/docstrings_fuzz_test.py`) use the `hypothesis` library.

### Linting

Please run lint on your pull requests to make accepting the requests easier. To do this, run:

```
pylint fire
```

in the root directory of the repository. Note that even if lint is passing, additional style changes to your submission may be made during merging.

The project also includes `pytype` configuration in `setup.cfg` for static type checking.

## Repository Layout

- `fire/` — the Python Fire library itself
  - `fire/core.py` — the core Fire functionality
  - `fire/__main__.py` — enables using Fire via `python -m fire` on third-party libraries without modifying their code
  - `fire/console/` — an interactive console (see `fire/console/README.md`)
  - Supporting modules for completion, docstring parsing, help text generation, formatting, interaction, tracing, and argument parsing
- `examples/` — example programs with tests
- `docs/` — MkDocs documentation
- `.github/` — GitHub Actions workflows, build scripts, and Dependabot configuration

## License

Python Fire is licensed under the Apache Software License (Apache 2.0). See the `LICENSE` file for details:

> Copyright 2017 Google Inc. All rights reserved.
>
> Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

## Disclaimer

Python Fire is not an official Google product.
