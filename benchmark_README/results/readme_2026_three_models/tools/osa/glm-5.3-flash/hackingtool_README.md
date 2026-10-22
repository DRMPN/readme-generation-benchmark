# Hackingtool

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

Hackingtool is an all-in-one toolkit that aggregates a wide range of security and penetration-testing utilities behind a single interactive, menu-driven terminal interface, saving practitioners from managing dozens of separate tools. It is aimed at security researchers, penetration testers, and ethical hackers working on Linux systems (Debian-based distributions and Arch), with an explicit emphasis on lawful use. The project offers an interactive menu-based CLI for launching and managing tools, a Docker-based deployment option, and a modular structure for organizing tools by category. Newcomers should consult the Getting Started section for setup and run steps.

---

## Core Features

- Aggregates a broad set of security and pentesting utilities (information gathering, wireless attacks, SQL injection, XSS, phishing, web attacks, forensics, steganography, reverse engineering, and more) into a single interactive terminal menu, so you can browse and launch tools without hunting for each one separately.
- Manages the full lifecycle of each bundled tool — install, run, and uninstall — from the same interface, reducing manual setup and cleanup work.
- Organizes tools into categorized, nested menus via a plugin-style framework, making it easy to navigate by attack category or task.
- Includes a built-in tool manager for updating the system, updating Hackingtool itself, and cleanly uninstalling it.
- Runs on Linux (Kali/Parrot via apt, Arch via pacman) or in a ready-to-use Docker container, giving flexible deployment options for security workflows.

---

## Installation

Install Hackingtool using one of the following methods, depending on your environment:

**Recommended System Installation (Linux):**

This method handles system dependencies (APT/Pacman) and sets up the necessary environment via the included installer script.

1. Clone the repository:
```bash
   git clone https://github.com/Z4nzu/hackingtool.git
   cd hackingtool
```

2. Run the installer as root. It updates packages, installs system dependencies, clones the project to `/usr/share/hackingtool`, creates a Python virtual environment, and installs the Python requirements:

```bash
   sudo chmod +x install.sh
   sudo ./install.sh
```

   Choose `[1]` for Kali Linux / Parrot OS (apt) or `[2]` for Arch Linux (pacman), or pass the choice directly, e.g. `sudo ./install.sh 1`.

**Local Checkout (Development/Testing):**

For testing or development, you can install dependencies directly from the local checkout:

1. Open the repository root:
```sh
   cd path/to/hackingtool
```

2. Install the project dependencies:

```sh
   pip install -r requirements.txt
```

**Docker Container:**

A Kali-based `Dockerfile` and `docker-compose.yml` are provided for containerized usage.

---

## Getting Started

**Prerequisites**

- Linux only: Kali Linux / Parrot OS (apt-based) or Arch Linux (pacman-based); Windows is not supported.
- Python 3 with pip. Required system packages are installed by the installer; Python dependencies are listed in `requirements.txt`.
- Root privileges and an internet connection (the installer checks both).

**Quickstart**

1. Clone the repository:

```bash
   git clone https://github.com/Z4nzu/hackingtool.git
   cd hackingtool
```

2. Run the installer as root. It updates packages, installs system dependencies, clones the project to `/usr/share/hackingtool`, creates a Python virtual environment, and installs the Python requirements:

```bash
   sudo chmod +x install.sh
   sudo ./install.sh
```

   Choose `[1]` for Kali Linux / Parrot OS (apt) or `[2]` for Arch Linux (pacman), or pass the choice directly, e.g. `sudo ./install.sh 1`.

3. Start the interactive menu:

```bash
   python3 hackingtool.py
```

   Run it from the installed copy at `/usr/share/hackingtool` or from your local clone.

4. On first launch, choose where tools will be installed: `[1]` to enter a path manually or `[2]` for the default (`/home/hackingtool/`). The choice is saved to `~/hackingtoolpath.txt` and reused on later runs.

5. Pick a category from the menu and use the `Install` / `Run` options shown for each tool.

---

## Contributing

Contributions are welcome! Please review the issue templates and documentation guidelines before submitting bug reports or feature requests. We encourage you to submit pull requests, following our contribution guidelines.

---

## License

This project is released under the terms defined in the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). Hackingtool repository [Computer software]. https://github.com/Z4nzu/hackingtool

### BibTeX format:

    @misc{hackingtool-td6hyvax,

        author = {README Benchmark},

        title = {Hackingtool repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }