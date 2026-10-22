# Eco2AI-_5zwipdl

---

[![PyPi](https://badge.fury.io/py/eco2ai.svg)](https://badge.fury.io/py/eco2ai)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

eco2ai is a Python library for tracking energy use and estimating CO₂ emissions during CPU and GPU computations, including machine-learning workloads. It is intended for developers and ML or data science practitioners who want to monitor the computational impact of their work. The library provides a Python tracking workflow, and Getting Started is the place to find runnable steps.

---

## Installation

**Prerequisites:** requires Python *

Install Eco2AI-_5zwipdl using one of the following methods:

**Using PyPi:**

```sh
pip install eco2ai
```

---

## Getting Started

Prerequisite: a Python environment. The TensorFlow tutorial also lists its framework and notebook dependencies; see `examples/Eco2AI tutorial tensorflow.ipynb` for that example.

1. Install eco2ai:

```bash
   pip install eco2ai
```

2. In your Python code, create a tracker and start it before your computation:

```python
   import eco2ai

   tracker = eco2ai.Tracker(project_name="my-project")
   tracker.start()
```

3. Run your computation, then call `tracker.stop()` to finish tracking.

---

## API Reference

- `Tracker` (`eco2ai/emission_track.py`) — tracks CO₂ emissions during CPU or GPU computations; the documented usage calls `start()` before the work and `stop()` afterward.

---

## Examples

Examples of how this should work and how it should be used are available [here](./examples).

---

## Contributing

---

## License

This project is protected under the Apache 2.0. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). Eco2AI-_5zwipdl repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{Eco2AI-_5zwipdl,

        author = {README Benchmark},

        title = {Eco2AI-_5zwipdl repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---