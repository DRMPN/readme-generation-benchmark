# python-spider-7puiop5s

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [Citation](#citation)

---

## Overview

This repository is a collection of standalone Python web-scraping scripts and small utilities that download online media, crawl site content, and automate tasks such as querying a university academic system. It is aimed primarily at developers and hobbyists learning web-scraping techniques, with code and comments written in an educational, tutorial style. The tools are organized as independent subprojects rather than a single installable package: most run from the command line, one provides a desktop GUI, and one is structured as a multi-page crawler project. Because each subproject is self-contained, refer to Getting Started for per-project setup and runnable steps.

---

## Core Features

- **Multi-platform video downloading** — search Bilibili by keyword across multiple result pages and download video streams with real-time console progress, while companion scripts cover other platforms such as Douyin, so media can be collected directly from the terminal.
- **Danmaku capture and subtitle conversion** — downloads a video's bullet-comment XML and converts it into ASS subtitle files, letting saved videos keep on-screen comments as synchronized subtitles.
- **Comic scraping pipeline** — a complete Scrapy project enumerates comic chapters, resolves image URLs on each page, and downloads them through the item pipeline, providing a working template for paginated image-site crawling.
- **University system automation** — logs into the Zhengfang educational administration system and parses grade tables into structured records, demonstrating session-based login together with HTML table extraction.
- **Graphical playback assistant** — a tkinter desktop app offers selectable playback channels for mainstream video sites, playback of a pasted link, and QR codes for switching to mobile viewing, giving non-command-line users an accessible entry point.

---

## Installation

This repository is not an installable package: it is a flat collection of standalone scripts, and there is no `requirements.txt` at the repository root. There is no separate installation step beyond obtaining the code — clone or copy the repository, then follow the per-project setup in [Getting Started](#getting-started).

---

## Getting Started

This repository is a flat collection of standalone Python scripts: there is no shared package, root `requirements.txt`, or unified entry point, so each tool is run directly from its own folder.

**Prerequisites**

- Python with `pip` available on your `PATH`.
- Dependencies vary per tool. Only `video_downloader/` and `zhengfang_system_spider/` ship a `requirements.txt`; other scripts need their imported libraries (`requests`, `bs4`, `lxml`, Scrapy, Pillow) installed separately.

**Quickstart: `video_downloader` (tkinter GUI)**

1. Clone the repository and enter the tool's folder:

```bash
cd video_downloader
```

2. Install its dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
python video_downloader.py
```

4. In the window titled `VIP视频破解助手`, select a channel (通道一/通道二), paste a video URL, then click 播放 to play or 手机观看 to get a QR code for mobile viewing.

**Other tools**

- `cartoon/` is a Scrapy project; with Scrapy installed, run `scrapy crawl comic` from the directory containing `scrapy.cfg`.
- `zhengfang_system_spider/` ships its own `requirements.txt`; install it with `pip install -r requirements.txt` from that folder, then run the spider script from there.
- Per-folder READMEs with usage details exist for `bilibili/`, `bilibili_luckyman/`, `dingdong/`, `douyin/`, `zhengfang_system_spider/`, and `2020/`. Consult each folder's README for its exact entry point and run instructions.

---

## Contributing

There is no dedicated contribution guide or issue template in this repository. If you would like to propose changes, open an issue or submit a pull request against the canonical repository, keeping in mind that each subproject is self-contained and changes should be scoped to the relevant folder.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). python-spider-7puiop5s repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{python-spider-7puiop5s,

        author = {README Benchmark},

        title = {python-spider-7puiop5s repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }