# Python Cheatsheet

A single-page, searchable Python cheatsheet, published as a website and as a printable PDF. The site is built from a Markdown source file and an HTML template by a Node.js script.

The project is by Jure Šorn ([gto76](https://github.com/gto76)). The published site is at <https://gto76.github.io/python-cheatsheet/>.

## Contents

- [What is in the repository](#what-is-in-the-repository)
- [Using the cheatsheet](#using-the-cheatsheet)
- [Topics covered](#topics-covered)
- [Building the site](#building-the-site)
- [Other scripts](#other-scripts)
- [Creating the printable PDF](#creating-the-printable-pdf)
- [License](#license)

## What is in the repository

| Path | Purpose |
| --- | --- |
| `index.html` | Generated single-page cheatsheet (the published site). |
| `parse.js` | Node.js build script that generates `index.html` from the Markdown source and `web/template.html`. |
| `web/template.html` | HTML template with the page layout, metadata, and placeholder for the content. |
| `web/` | Static assets used by the site: CSS (light and dark themes), JavaScript libraries (jQuery, Plotly, Showdown, highlight.js), images, the COVID and Plotly data files, and bundled web fonts. |
| `web/update_plots.py` | Python script that regenerates the COVID and market plots in `web/` from online data. |
| `web/convert_table.py` | Converts ASCII box tables to Unicode box-drawing tables, and back, via standard input and output. |
| `web/empty_script.py` | A placeholder Python file. Its comments say it exists so GitHub detects the project as Python. |
| `pdf/` | Files and instructions for producing a printable PDF (see [Creating the printable PDF](#creating-the-printable-pdf)). |

## Using the cheatsheet

Open the published site or `index.html` in a browser.

- Use Ctrl+F (or ⌘F on macOS) to search the page.
- Search for `#<title>` to limit the search to section titles.
- Click a title's `#` to get a link to that section.
- Use the links in the page menu to download the Markdown text file or to switch themes. The page links to a `?theme=dark3` variant for the dark theme and `?theme=light` for the light theme.

## Topics covered

The table of contents in the cheatsheet is grouped into these sections:

1. **Collections**: List, Dictionary, Set, Tuple, Range, Enumerate, Iterator, Generator
2. **Types**: Type, String, Regular Expressions, Format, Numbers, Combinatorics, Datetime
3. **Syntax**: Function, Inline, Import, Decorator, Class, Duck Types, Enum, Exceptions
4. **System**: Exit, Print, Input, Command Line Arguments, Open, Path, OS Commands
5. **Data**: JSON, Pickle, CSV, SQLite, Bytes, Struct, Array, Memory View, Deque
6. **Advanced**: Operator, Match Statement, Logging, Introspection, Threading, Coroutines
7. **Libraries**: Progress Bar, Plot, Table, Console App, GUI, Scraping, Web, Profile
8. **Multimedia**: NumPy, Image, Animation, Audio, Synthesizer, Pygame, Pandas, Plotly

## Building the site

`parse.js` reads the Markdown source file `README.md` and the template `web/template.html`, converts the Markdown to HTML, applies the page modifications in the script, and writes the result to `index.html`.

> **Note:** `parse.js` expects the root `README.md` to contain the cheatsheet's Markdown source. If you replace that file with other content, running the build will overwrite `index.html` with the output built from that content.

### Requirements

- Node.js and npm. On Debian/Ubuntu: `sudo apt install nodejs npm`. On macOS: `brew install node`.
- The npm packages used by the script: `jsdom`, `jquery`, `showdown`, and `highlightjs` (version 9.12.0).

### Steps

```bash
npm install jsdom jquery showdown highlightjs@9.12.0
node parse.js
```

The script's header comments suggest installing the packages into the project directory, as above, to avoid permission and path problems. They also describe an optional `pre-commit` Git hook that runs `./parse.js` before each commit.

## Other scripts

Run these from the repository root unless noted.

### `web/update_plots.py`

Regenerates the plot data and images used in the Plotly section. Its usage line is `./update_plots.py`. It:

- Downloads COVID-19 data from `covid.ourworldindata.org`, and country-to-continent data from a GitHub gist.
- Downloads Bitcoin, gold, and Dow Jones price history from Yahoo Finance.
- Writes `web/covid_deaths.js`, `web/covid_cases.js`, and the matching PNG images.

The script needs network access and the Python packages `pandas` and `plotly`. Writing PNG images uses Plotly's `write_image`, which requires an image export backend to be installed.

### `web/convert_table.py`

Converts a text table between ASCII form and Unicode box-drawing form. It reads lines from standard input and prints the result:

```bash
python3 web/convert_table.py < table.txt
```

If the first line starts with `+`, the table is converted from ASCII to Unicode. Otherwise it is converted from Unicode to ASCII.

## Creating the printable PDF

The `pdf/` directory contains the notes and helper scripts for producing a printable PDF. The instructions in `pdf/README.md` are written for macOS and use:

- Adobe Acrobat Pro DC, with the header and footer presets in `pdf/Acrobat/`.
- Chromium version 108.0.5328.0, which the instructions say is needed for correct rendering.

The helper scripts are:

- `pdf/remove_links.py`: Replaces the internal links in `index.html` with plain text and page numbers, for the print-optimized version. It opens `../index.html`, so run it from inside the `pdf/` directory.
- `pdf/create_index.py`: Reads `index.html` with BeautifulSoup and prints an alphabetical index of section titles in Markdown form. It reads `index.html` from the current directory, so run it from the repository root. It needs the `beautifulsoup4` package.
- `pdf/index_for_pdf.html` and `pdf/index_for_pdf_print.html`: Replacement index and footer sections used when preparing the PDF.

See `pdf/README.md` for the full step-by-step process.

## License

No license file is included in this repository. Check with the author before reusing or redistributing the content.
