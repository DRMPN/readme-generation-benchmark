# Python Fire

Python Fire is a library for automatically creating command-line interfaces (CLIs) from Python objects. Give Fire a function, class, module, dictionary, or other object, and it turns that object into commands you can run from a terminal.

Fire is useful for quickly building command-line tools, exploring Python code interactively, and making existing functions available without writing a separate argument parser.

## Installation

Install Fire from PyPI:

```bash
pip install fire
```

To install a local checkout of the project:

```bash
pip install .
```

## Quick start

Create a file named `greet.py`:

```python
import fire


def greet(name="World", greeting="Hello"):
    """Greet someone."""
    return f"{greeting}, {name}!"


if __name__ == "__main__":
    fire.Fire(greet)
```

Run it from the terminal:

```bash
python greet.py
```

```text
Hello, World!
```

Pass arguments to the function as command-line arguments:

```bash
python greet.py Ada
```

```text
Hello, Ada!
```

You can also supply keyword arguments:

```bash
python greet.py Ada --greeting=Hi
```

```text
Hi, Ada!
```

Fire converts command-line values to Python values where possible. For example, numeric arguments can be passed as numbers:

```python
import fire


def add(x, y):
    return x + y


if __name__ == "__main__":
    fire.Fire(add)
```

```bash
python add.py 10 20
```

```text
30
```

## Creating a CLI from a module

Pass a module’s functions or classes to `fire.Fire`, or call `fire.Fire()` from the module to expose its available members.

```python
import fire


def greet(name="World"):
    return f"Hello, {name}!"


def add(x, y):
    return x + y


if __name__ == "__main__":
    fire.Fire()
```

With this file saved as `app.py`, you can run its functions by name:

```bash
python app.py greet Ada
python app.py add 10 20
```

Passing an explicit object to `fire.Fire` is often a good choice when you want to make clear which part of your program is the CLI:

```python
if __name__ == "__main__":
    fire.Fire({"greet": greet, "add": add})
```

## Creating a CLI from a class

Fire can expose a class and its methods as commands:

```python
import fire


class Calculator:
    def add(self, x, y):
        return x + y

    def multiply(self, x, y):
        return x * y


if __name__ == "__main__":
    fire.Fire(Calculator)
```

For example:

```bash
python calculator.py add 10 20
```

```text
30
```

```bash
python calculator.py multiply 6 7
```

```text
42
```

Functions and methods can use normal Python parameters and default values. Fire uses those call signatures to determine which arguments the command accepts.

## Working with objects and return values

Fire can create commands from many kinds of Python objects, including dictionaries, lists, modules, classes, and instances. It also lets you continue working with an object returned by a command, so commands can be composed to explore or operate on nested objects.

The result of a command is displayed in the terminal. Fire’s output formatting depends on the type of the returned value; it is not necessarily JSON or another machine-readable format.

## Command-line arguments

A Fire CLI follows the structure of the Python object it wraps:

- A function or method is invoked with arguments from the command line.
- Members of an object can be selected as subcommands.
- Function and method defaults are available when you omit optional arguments.
- Values are interpreted as Python values when possible; values that cannot be interpreted remain strings.
- Use shell quoting when an argument contains spaces or characters that your shell treats specially.

For example, a string containing spaces should generally be quoted:

```bash
python greet.py "Ada Lovelace"
```

Keyword arguments can be written using `--name=value` syntax:

```bash
python greet.py Ada --greeting=Welcome
```

## Help

Fire generates help information for a CLI. Request it from the command line with `--help`:

```bash
python calculator.py --help
```

Help is also available for commands and subcommands. Use it to inspect the commands Fire exposes and the arguments accepted by a particular function or method.

## Interactive mode and shell completion

Fire includes tools for exploring a CLI interactively and for generating shell-completion support. These special options are typically passed after `--` so they are handled by Fire:

```bash
python calculator.py -- --interactive
python calculator.py -- --completion
```

The completion option prints a completion script. Follow the instructions for your shell to install or source that script; setup differs between shells.

## API

The main entry point is `fire.Fire`:

```python
fire.Fire(component=None)
```

Pass the Python object you want to expose as `component`. If you omit it, Fire uses the calling context to build a CLI from the available objects.

A typical script calls Fire from its main block:

```python
if __name__ == "__main__":
    fire.Fire(component)
```

This keeps the CLI from running when the file is imported as a module.

## Tips

- **Start with a small component.** Exposing a specific function, class, or dictionary makes the CLI’s available commands easier to understand.
- **Use docstrings.** Clear docstrings help explain the purpose of functions and methods to people using the CLI.
- **Keep Python APIs usable.** Fire exposes the behavior of your Python objects; thoughtful names, defaults, and return values make for a better command-line interface.
- **Quote shell-sensitive values.** The shell processes a command before Python receives it, so quote arguments containing spaces or special characters.
- **Treat CLI input as untrusted.** Fire is not a sandbox. A CLI can invoke the Python behavior you expose, so do not use it as a security boundary.

## Development

To work from a checkout, install the project locally:

```bash
pip install -e .
```

The repository includes tests alongside the implementation. Run them with the test runner configured for your environment.

## License

Python Fire is distributed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for the full license text.
