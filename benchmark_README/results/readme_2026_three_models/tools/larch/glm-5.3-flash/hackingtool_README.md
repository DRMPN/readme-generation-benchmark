# Hackingtool

![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Docker-lightgrey)

**Hackingtool** is an all-in-one penetration testing and ethical hacking toolkit. It aggregates a wide collection of security tools into a single, easy-to-use menu-driven interface so penetration testers, security researchers, and CTF players can quickly find and launch the right tool for the job.

> ⚠️ **Disclaimer:** This project is intended **for educational purposes and authorized security testing only**. Using these tools against systems without explicit permission is illegal. The developers assume no liability for misuse.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tool Categories](#-tool-categories)
- [Installation](#-installation)
- [Docker Installation](#-docker-installation)
- [Usage](#-usage)
- [Updating the Toolkit](#-updating-the-toolkit)
- [Generating the README](#-generating-the-readme)
- [Screenshots](#-screenshots)
- [Requirements](#-requirements)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- 🎯 **All-in-one menu** — access dozens of hacking tools from a single interactive interface
- 🛠️ **Automatic tool installation** — installs missing dependencies and clones required repositories
- 🕵️ **Wide coverage** — from information gathering to post-exploitation
- 🐳 **Docker support** — run everything in an isolated, portable container
- 🔄 **Self-updating** — one-command update mechanism (`update.sh`)

---

## 🗂️ Tool Categories

Hackingtool is organized into the following modules:

| Module | Description |
|---|---|
| `information_gathering_tools.py` | OSINT, whois, DNS enumeration, subdomain discovery |
| `webattack.py` | Web application attack frameworks |
| `xss_attack.py` | Cross-Site Scripting (XSS) scanners and payloads |
| `sql_tools.py` | SQL injection tools and database exploitation |
| `web_crawling.py` | Web crawlers and directory bruteforcers |
| `homograph_attacks.py` | Homograph / IDN spoofing attack generators |
| `phising_attack.py` | Phishing page generators and credential capture simulations |
| `ddos.py` | DoS/DDoS testing tools (for load-testing your own systems) |
| `wireless_attack_tools.py` | Wi-Fi auditing and attack tools |
| `wifi_jamming.py` | Deauthentication / Wi-Fi jamming tools |
| `payload_creator.py` | Payload generation (msfvenom wrappers and similar) |
| `payload_injection.py` | Payload delivery and injection helpers |
| `post_exploitation.py` | Post-exploitation modules and privilege escalation |
| `reverse_engineering.py` | Reverse engineering and binary analysis tools |
| `forensic_tools.py` | Digital forensics and incident response utilities |
| `hash_crack.py` | Password and hash cracking tools |
| `wordlist_generator.py` | Custom wordlist generation for bruteforcing |
| `android_attack.py` | Android / APK attack and analysis tools |
| `remote_administration.py` | Remote administration tool (RAT) frameworks |
| `exploit_frameworks.py` | Exploit frameworks and database search tools |
| `socialmedia.py` / `socialmedia_finder.py` | Social media OSINT and account discovery |
| `email_verifier.py` | Email validation and verification tools |
| `steganography.py` | Steganography hiding/extraction tools |
| `anonsurf.py` | Anonymity tools (Tor routing, MAC spoofing) |
| `mix_tools.py` | Miscellaneous utilities |
| `other_tools.py` | Additional community tools |

---

## 🚀 Installation

### Requirements

- Linux (Kali / Parrot / Ubuntu recommended)
- Python 3.x
- `pip`, `git`, and `sudo` privileges

### One-line install

```bash
git clone https://github.com/<owner>/hackingtool-7vg8sj8i.git
cd hackingtool-7vg8sj8i
chmod +x install.sh
sudo ./install.sh
```

The `install.sh` script will:

1. Install Python dependencies from `requirements.txt`
2. Clone and set up external tool repositories
3. Add the `hackingtool` command to your system

### Manual install

```bash
pip install -r requirements.txt
python hackingtool.py
```

---

## 🐳 Docker Installation

Run Hackingtool in a fully isolated container:

```bash
git clone https://github.com/<owner>/hackingtool-7vg8sj8i.git
cd hackingtool-7vg8sj8i

# Using docker-compose (recommended)
docker-compose up -d
docker-compose exec hackingtool python hackingtool.py

# Or build manually
docker build -t hackingtool .
docker run -it --net=host hackingtool
```

The included `Dockerfile` and `docker-compose.yml` handle all dependencies, so nothing pollutes your host system.

---

## 🖥️ Usage

Launch the toolkit:

```bash
sudo hackingtool
# or
sudo python hackingtool.py
```

You'll be greeted with a numbered menu. Simply enter the number of the category you want, then pick a specific tool. The toolkit will automatically install any missing tool on first use.

**Tip:** Some tools require **root privileges** and/or **monitor-mode wireless adapters**, so run as `sudo` where needed.

---

## 🔄 Updating the Toolkit

Keep everything up to date with:

```bash
chmod +x update.sh
./update.sh
```

This pulls the latest version of the repository and refreshes all integrated external tools.

---

## 🧾 Generating the README

The project includes `generate_readme.py`, a utility to auto-generate/update the tool documentation from the source files:

```bash
python generate_readme.py
```

---

## 📸 Screenshots

| | |
|---|---|
| ![Main Menu](A0.png) | ![Tools](A1.png) |
| ![Categories](A2.png) | ![Output](A4.png) |

---

## 📦 Requirements

All Python dependencies are listed in `requirements.txt`. External tools (like Nmap, sqlmap, Metasploit, etc.) are installed automatically on demand by the toolkit.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-tool`)
3. Add your tool to the appropriate category module
4. Submit a pull request

---

## ⚖️ License

This project is licensed under the terms of the [LICENSE](LICENSE) file.

---

## 🔗 Credits

Built for the infosec community — use responsibly. 💀
