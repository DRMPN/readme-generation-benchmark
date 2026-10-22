# gpt-engineer-dvhu31wz

---

[![PyPi](https://badge.fury.io/py/gpt-engineer.svg)](https://badge.fury.io/py/gpt-engineer)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![openai](https://img.shields.io/badge/OpenAI-412991.svg?style={0}&logo=OpenAI&logoColor=white)
![python](https://img.shields.io/badge/Python-3776AB.svg?style={0}&logo=Python&logoColor=white)
![toml](https://img.shields.io/badge/TOML-9C4121.svg?style={0}&logo=TOML&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Testing](#testing)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

gpt-engineer helps developers generate new code projects or improve existing ones from prompts using language models. It is intended for developers working with AI-assisted code generation and refinement. The project provides a command-line workflow that can generate code and optionally process it in an execution environment; see Getting Started for runnable steps.

---

## Installation

**Prerequisites:** requires Python >=3.10,<3.13

Install gpt-engineer-dvhu31wz using one of the following methods:

**Using PyPi:**

```sh
pip install gpt-engineer
```

---

## Getting Started

Prerequisite: an OpenAI API key.

Set `OPENAI_API_KEY` in your environment or add it to a `.env` file in the working directory. The CLI loads the key from either location.

---

## Architecture

- The CLI accepts generation or improvement requests and coordinates the agent workflow.
- The agent uses memory and an execution environment during code generation and improvement; execution can be part of the workflow.
- Memory and execution-environment modules provide the corresponding storage and code-processing roles.
- A separate benchmarking module is included; its interactions with the agent workflow are not established by the available context.

---

## Testing

The repository includes tests for the CLI, core functionality (including agents, execution, file handling, and token usage), and benchmark configuration. No test-run command is documented in the provided context.

---

## Examples

Examples of how this should work and how it should be used are available [here](./docs/examples).

---

## Documentation

A detailed gpt-engineer-dvhu31wz description is available [here](./docs).

---

## Contributing

- **[Submit Pull Requests](./.github/CONTRIBUTING.md)**: To learn more about making a contribution to gpt-engineer-dvhu31wz.

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this software, please cite it as it is written in the [CITATION](./citation.cff) file.

---