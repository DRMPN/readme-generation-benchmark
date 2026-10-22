# Python Fire

---

[![PyPi](https://badge.fury.io/py/fire.svg)](https://badge.fury.io/py/fire)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Python Fire is a library that generates command-line interfaces from Python objects and programs, helping developers expose existing code for command-line use. It is intended for Python developers and can be used as a library or through a command-line entry point. See Usage for runnable steps and an introduction to using Fire.

---

## Installation

Python Fire requires Python 3.7 or later. Install Python Fire using the following method:

**Using PyPi:**

```sh
pip install fire
```

---

## Usage

Expose a Python component by calling `fire.Fire()` from your program. Pass a component to expose only that object:

```python
import fire

def hello(name):
  return f'Hello {name}!'

if __name__ == '__main__':
  fire.Fire(hello)
```

Run the script with its arguments:

```bash
python example.py World
```

You can also run Fire against an existing module or `.py` file without modifying it:

```bash
python -m fire packageA.packageB.module
python -m fire packageA/packageB/module.py
```

Extend a command with member names and arguments to access and call components. Add `--help` to inspect a command; Fire flags such as `--interactive` are separated from command arguments with `--` (for example, `command -- --interactive`).

---

## Examples

Examples of how this should work and how it should be used are available [here](./examples).

---

## Documentation

A detailed Python Fire description is available [here](./docs).

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to Python Fire.

---

## License

For licensing details, refer to the [LICENSE](./LICENSE) file.