# HackingTool

A Python-based, menu-driven launcher that collects security, penetration testing, and digital forensics tools in one place. Instead of installing and configuring each utility separately, you can browse categories and install or run tools from a single interface.

> **Disclaimer:** This project is intended for educational purposes, authorized security testing, CTF competitions, and research. Only use these tools against systems you own or have explicit written permission to test. Unauthorized access to computer systems is illegal in most jurisdictions. The authors and contributors accept no liability for misuse.

---

## Table of Contents

- [Features](#features)
- [Repository Structure](#repository-structure)
- [Tool Categories](#tool-categories)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Native Installation](#native-installation)
  - [Docker Installation](#docker-installation)
- [Usage](#usage)
- [Architecture Overview](#architecture-overview)
- [Adding a New Tool](#adding-a-new-tool)
- [Updating](#updating)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Single entry point:** Launch all tools from one interactive menu.
- **Categorized tools:** Tools are grouped by function, such as web attacks, wireless, forensics, and OSINT.
- **Automated installation:** Tools can be installed and updated from within the menu.
- **Anonymity support:** An `anonsurf` module provides routing of traffic through anonymizing networks.
- **Docker support:** A `Dockerfile` and `docker-compose.yml` allow an isolated, reproducible environment.
- **Extensible design:** A central tool manager makes it straightforward to add new categories or tools.
- **Automatic README generation:** `generate_readme.py` helps keep documentation in sync with the tool list.

---

## Repository Structure

```
hackingtool-6m0usg5r/
├── hackingtool.py              # Main entry point (interactive menu)
├── core.py                     # Core utilities shared across modules
├── tool_manager.py             # Installs, tracks, and launches tools
├── install.sh                  # Native installation script
├── update.sh                   # Updates the repository and installed tools
├── Dockerfile                  # Container image definition
├── docker-compose.yml          # Container orchestration configuration
├── requirements.txt            # Python dependencies
├── generate_readme.py          # Helper script for generating documentation
├── LICENSE                     # Project license
├── A0.png, A1.png, A2.png, A4.png, A00.png   # Screenshots / images
├── demo/                       # Demo assets
│
├── Tool category modules:
│   ├── webattack.py
│   ├── xss_attack.py
│   ├── sql_tools.py
│   ├── wireless_attack_tools.py
│   ├── wifi_jamming.py
│   ├── ddos.py
│   ├── exploit_frameworks.py
│   ├── payload_creator.py
│   ├── payload_injection.py
│   ├── post_exploitation.py
│   ├── remote_administration.py
│   ├── android_attack.py
│   ├── reverse_engineering.py
│   ├── forensic_tools.py
│   ├── steganography.py
│   ├── hash_crack.py
│   ├── wordlist_generator.py
│   ├── information_gathering_tools.py
│   ├── web_crawling.py
│   ├── email_verifier.py
│   ├── socialmedia.py
│   ├── socialmedia_finder.py
│   ├── phising_attack.py
│   ├── homograph_attacks.py
│   ├── anonsurf.py
│   ├── other_tools.py
│   └── mix_tools.py
```

### Key Files

| File | Purpose |
|------|---------|
| `hackingtool.py` | Starts the application and displays the main menu. |
| `core.py` | Shared helper functions such as colored output, command execution, and input handling. |
| `tool_manager.py` | Handles tool metadata, installation, updates, and launching. |
| `install.sh` | Installs system dependencies and sets up the application natively. |
| `update.sh` | Pulls the latest changes and refreshes tools. |
| `generate_readme.py` | Generates or refreshes documentation from the tool definitions. |
| `Dockerfile` | Builds a container image with the required environment. |
| `docker-compose.yml` | Defines how the container is run, including volumes and networking. |

---

## Tool Categories

Each category maps to a module in the repository.

| Category | Module(s) | Description |
|----------|-----------|-------------|
| **Information Gathering** | `information_gathering_tools.py` | Reconnaissance and host, domain, and network information collection. |
| **Web Attacks** | `webattack.py` | Tools for testing web application security. |
| **XSS Attacks** | `xss_attack.py` | Cross-site scripting detection and testing. |
| **SQL Injection** | `sql_tools.py` | SQL injection detection and testing utilities. |
| **Web Crawling** | `web_crawling.py` | Crawling and enumerating web content. |
| **Wireless Attacks** | `wireless_attack_tools.py`, `wifi_jamming.py` | Wireless network auditing tools. |
| **DDoS Testing** | `ddos.py` | Stress-testing tools for availability assessment. |
| **Exploit Frameworks** | `exploit_frameworks.py` | Wrappers and launchers for exploitation frameworks. |
| **Payload Creation** | `payload_creator.py`, `payload_injection.py` | Generation and injection of test payloads. |
| **Post Exploitation** | `post_exploitation.py` | Tools used after initial access during authorized assessments. |
| **Remote Administration** | `remote_administration.py` | Remote access and administration tools. |
| **Android Attacks** | `android_attack.py` | Mobile security testing for Android. |
| **Reverse Engineering** | `reverse_engineering.py` | Disassemblers, debuggers, and binary analysis tools. |
| **Forensics** | `forensic_tools.py` | Disk, memory, and file forensics. |
| **Steganography** | `steganography.py` | Hiding and extracting data within files. |
| **Hash Cracking** | `hash_crack.py` | Hash identification and cracking for password auditing. |
| **Wordlist Generation** | `wordlist_generator.py` | Creation of custom wordlists for authorized testing. |
| **Phishing Simulation** | `phising_attack.py`, `homograph_attacks.py` | Social engineering simulations for security awareness training. |
| **Social Media Tools** | `socialmedia.py`, `socialmedia_finder.py` | OSINT for social media profiles. |
| **Email Verification** | `email_verifier.py` | Checking email validity and related metadata. |
| **Anonymity** | `anonsurf.py` | Routing traffic through anonymizing networks. |
| **Miscellaneous** | `other_tools.py`, `mix_tools.py` | Additional and combined utilities. |

---

## Requirements

### System

- **Operating system:** Linux is recommended (Debian/Ubuntu/Kali/Parrot). Termux on Android is supported for some tools.
- **Python:** 3.x
- **Privileges:** Some tools, especially wireless and network tools, require root or `sudo`.
- **Git:** Required for cloning and updating repositories.
- **Internet connection:** Required for installing tools and dependencies.

### Python Dependencies

Listed in `requirements.txt`. Install them with:

```bash
pip3 install -r requirements.txt
```

### Optional

- **Docker** and **Docker Compose**, for the containerized setup.

---

## Installation

### Native Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/<your-username>/hackingtool-6m0usg5r.git
   cd hackingtool-6m0usg5r
   ```

2. **Run the installer:**

   ```bash
   sudo bash install.sh
   ```

   The script installs system packages, Python dependencies, and sets up the launcher.

3. **Start the tool:**

   ```bash
   python3 hackingtool.py
   ```

### Docker Installation

1. **Build and start the container:**

   ```bash
   docker-compose up --build
   ```

2. **Or build the image manually:**

   ```bash
   docker build -t hackingtool .
   docker run -it hackingtool
   ```

Running inside a container gives you an isolated environment. Some tools that need direct hardware access, such as wireless adapters, may not work in a container without additional configuration (device passthrough, privileges, or host networking).

---

## Usage

Launch the main menu:

```bash
python3 hackingtool.py
```

Navigation generally works as follows:

1. Select a **category** from the main menu by entering its number.
2. Select a **tool** within that category.
3. Choose to **install**, **update**, or **run** the tool.
4. Follow the on-screen prompts. Enter `0` or `back` to return to the previous menu, and use the exit option to quit.

Screenshots of the interface are included in the repository (`A0.png`, `A1.png`, `A2.png`, `A4.png`, `A00.png`).

---

## Architecture Overview

```
           ┌──────────────────┐
           │  hackingtool.py  │   Main menu / entry point
           └────────┬─────────┘
                    │
        ┌───────────┴────────────┐
        ▼                        ▼
┌───────────────┐       ┌──────────────────┐
│   core.py     │◄──────│ tool_manager.py  │
│ shared helpers│       │ install / launch │
└───────────────┘       └────────┬─────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
      ┌────────────────────┐         ┌───────────────────────┐
      │ Category modules   │         │ Install / update      │
      │ (webattack.py, …)  │         │ scripts (install.sh,  │
      └────────────────────┘         │ update.sh)            │
                                     └───────────────────────┘
```

- **Entry point** (`hackingtool.py`) renders menus and dispatches user choices.
- **Category modules** define the tools in each group.
- **Tool manager** handles cloning, installing, updating, and launching tools.
- **Core utilities** provide shared functionality such as output formatting and command execution.

---

## Adding a New Tool

1. Open the module for the relevant category (for example, `webattack.py`).
2. Add an entry describing the tool, including its name, description, repository URL, install command, and run command. Follow the format used by existing entries in the file.
3. If the tool needs a new category, create a new module, register it in `hackingtool.py`, and add it to the menu.
4. Add any new Python dependencies to `requirements.txt`.
5. Test the installation and launch from the menu on a clean environment.
6. Optionally run `generate_readme.py` to refresh the documentation.

---

## Updating

To update the repository and its tools:

```bash
sudo bash update.sh
```

Or pull the latest changes manually and reinstall the launcher:

```bash
git pull
sudo bash install.sh
```

---

## Troubleshooting

| Problem | Possible Cause | Solution |
|---------|----------------|----------|
| `ModuleNotFoundError` | Python dependencies missing | Run `pip3 install -r requirements.txt`. |
| Permission denied when installing | Insufficient privileges | Run with `sudo`. |
| A tool fails to install | Missing system package or network issue | Check the error output, install the missing package, and retry. |
| Wireless tools do not detect adapters | Running in Docker or without root | Run natively as root and confirm the adapter supports monitor mode. |
| Docker container cannot access hardware | No device passthrough | Add the device to `docker-compose.yml` or use native installation. |
| Menu displays garbled characters | Terminal encoding or color support | Use a terminal with UTF-8 and ANSI color support. |

---

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-tool`
3. Commit your changes: `git commit -m "Add my-tool to <category>"`
4. Push the branch: `git push origin feature/my-tool`
5. Open a pull request describing the change.

Please make sure that:

- New tools are relevant to security testing, research, or education.
- Installation is tested on at least one supported platform.
- Descriptions are accurate and concise.
- Code follows the existing style in the repository.

---

## License

This project is distributed under the terms described in the [LICENSE](LICENSE) file.

---

*This README was written from the repository file listing. Command names, URLs, and tool details should be verified against the actual source code before publishing. Running `generate_readme.py` can help keep the tool list accurate.*
