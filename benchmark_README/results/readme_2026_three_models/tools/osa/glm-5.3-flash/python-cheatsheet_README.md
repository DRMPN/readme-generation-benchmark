# python-cheatsheet-f429caxu

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

This repository maintains a static documentation/reference website whose pages combine long-form reference content with embedded, interactive charts, including up-to-date COVID-19 and financial-market plots, multiple CSS themes (including dark variants), and print/PDF-oriented page variants. It is primarily aimed at readers of the published reference pages, with a secondary audience of maintainers who keep the chart data current. The site itself is fully self-contained, with all JavaScript, CSS, and fonts vendored so it works without a package manager or build step. For maintainers, small Python 3 utility scripts fetch live external data and regenerate the embedded chart data and index listings; see Getting Started for runnable steps.

---

## Core Features

- Comprehensive Python reference content presented as a static website, so readers can look up topics without installing anything.
- Interactive Plotly charts (COVID-19 cases/deaths, Bitcoin/Gold/Dow Jones comparisons) that visualize live-reference data directly in the browser.
- Multiple CSS themes, including dark-mode variants, letting readers choose a comfortable viewing style.
- Python maintenance scripts that fetch fresh data and regenerate charts, keeping the published figures up to date.
- Fully self-contained assets (vendored JavaScript libraries, CSS, and self-hosted fonts), so the site works without a package manager or external CDN.

---

## Installation

Install python-cheatsheet-f429caxu using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/python-cheatsheet-f429caxu
```

---

## Getting Started

**Prerequisites**

- Python 3 with `pandas`, `Plotly`, and `BeautifulSoup` (`bs4`) available — these are the libraries imported by the maintenance scripts. The repository contains no dependency manifest, so install them manually.
- Internet access: the data-update script fetches live data from OWID (covid.ourworldindata.org) and Yahoo Finance.

**Quickstart**

1. **View the site.** Open `index.html` in a browser. All JavaScript libraries, CSS themes, and fonts are vendored in the repository, so no build step or package manager is required.

2. **Refresh the chart data.** From the `web/` directory, run the update script:

```bash
cd web
./update_plots.py
```

This downloads the latest OWID COVID-19 data and Yahoo Finance series, then regenerates `covid_deaths.js`, `covid_cases.js`, and the PNG exports `covid_deaths.png` and `covid_cases.png`.

3. **Regenerate the PDF heading index.** From the `pdf/` directory:

```bash
cd pdf
python3 create_index.py
```

The script parses the `index.html` in the current directory (h2–h4 headings) and prints a Markdown heading index to stdout.

`web/convert_table.py` is an optional helper that converts tables between ASCII and Unicode box-drawing formats; it is not part of the core data-update flow.

---

## Contributing

---

## License

This project is protected under the License. For more details, refer to the [LICENSE](./web/OnlineWebFonts_COM_cb7eb796ae7de7195a34c485cacebad1/License.txt) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). python-cheatsheet-f429caxu repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{python-cheatsheet-f429caxu,

        author = {README Benchmark},

        title = {python-cheatsheet-f429caxu repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---