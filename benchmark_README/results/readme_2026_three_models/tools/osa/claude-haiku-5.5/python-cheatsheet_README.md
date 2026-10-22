# Comprehensive Python Cheatsheet

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

The Comprehensive Python Cheatsheet is a static, single-page reference for the Python programming language. It presents concise, code-focused explanations and examples organized by topic, covering collections, types, syntax, system interaction, data handling, advanced topics, common libraries, and multimedia. It is primarily intended for Python developers and learners who want a quick reference, and secondarily for maintainers who regenerate the site and its charts. The site is built from source content by build scripts rather than served by a backend, and an alternate PDF output is also produced. To view the site or rebuild its outputs, see the Getting Started section.

---

## Core Features

- **Single-page Python reference:** Covers core Python topics, from collections and syntax to system, data, advanced features, and libraries, with a table of contents linking to each section. Developers can find a topic quickly without leaving the page.
- **Syntax-highlighted code examples:** Embedded snippets are highlighted for readability, so developers can scan and copy examples directly.
- **Light and dark themes:** The theme is selected with a query parameter in the page URL (for example, `?theme=dark3`), letting readers choose a display that suits their environment.
- **Refreshable data charts:** Scripts fetch live COVID case and death data and market price series, then regenerate interactive Plotly charts and PNG images, keeping the reference's charts current.
- **ASCII-to-Unicode table conversion:** A helper converts ASCII tables into Unicode box-drawing tables, giving documentation tables a cleaner appearance.

---

## Installation

No package installation is required to view the cheatsheet.

1. Obtain the repository files and open the repository root directory.
2. To rebuild the site or refresh the charts, follow the steps in the Getting Started section.

---

## Getting Started

This is a static site. Open `index.html` in a web browser to view the cheatsheet. No build step is needed to view it.

**Prerequisites** (only needed to regenerate the site or charts)
- Node.js and npm, for `parse.js`
- Python 3 with `pandas` and `plotly`, for `web/update_plots.py`
- Network access, because `update_plots.py` fetches live data over HTTP

**Quickstart**

1. Open `index.html` in a browser. To use a dark theme, add `?theme=dark3` to the URL, for example `index.html?theme=dark3`.
2. From the project directory, install the Node.js dependencies used by `parse.js`:

```bash
npm install jsdom jquery showdown highlightjs@9.12.0
```

3. Rebuild `index.html` from `web/template.html` and `README.md` (these build inputs were not confirmed in the reviewed file tree; verify they exist before running):

```bash
node parse.js
```

4. Optionally, refresh the chart assets. This requires network access and writes `web/covid_deaths.js`, `web/covid_deaths.png`, `web/covid_cases.js`, and `web/covid_cases.png`:

```bash
python3 web/update_plots.py
```

---

## Contributing

Contribution guidelines are not currently documented in this repository. For changes that affect the generated site, rebuild `index.html` with `node parse.js`. If chart data or scripts are changed, also run `python3 web/update_plots.py` (requires network access).

---

## License

No project-level license is specified in the reviewed repository files. The file [License.txt](./web/OnlineWebFonts_COM_cb7eb796ae7de7195a34c485cacebad1/License.txt) contains the license for the bundled web fonts in the `web/OnlineWebFonts_COM_cb7eb796ae7de7195a34c485cacebad1/` directory.

---

## Citation

Citation details are not yet available for this project.

---