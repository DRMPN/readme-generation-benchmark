# Comprehensive Python Cheatsheet

Exhaustive, simple, beautiful and concise. A truly Pythonic cheat sheet about the Python programming language.

Author: Jure Šorn ([gto76](https://github.com/gto76))

The published version of this cheat sheet is hosted at [gto76.github.io/python-cheatsheet](https://gto76.github.io/python-cheatsheet/).

## About the Project

This project is a static, single-page website that documents the Python programming language. Its content covers a wide range of topics, including:

*   **Collections:** List, Dictionary, Set, Tuple, Range, Enumerate, Iterator, Generator.
*   **Types:** Type, String, Regular Expression, Format, Numbers, Combinatorics, Datetime.
*   **Syntax:** Function, Inline, Imports, Decorator, Class, Duck Type, Enum, Exceptions.
*   **System:** Exit, Print, Input, Command Line Arguments, Open, Path, OS Commands.
*   **Data:** JSON, Pickle, CSV, SQLite, Bytes, Struct, Array, Memory View, Deque.
*   **Advanced:** Operator, Match Statement, Logging, Introspection, Threading, Coroutines.
*   **Libraries:** Progress Bar, Plot, Table, Console App, GUI, Scraping, Web, Profile.
*   **Multimedia:** NumPy, Image, Animation, Audio, Synthesizer, Pygame, Pandas, Plotly.

The site is styled with a custom CSS theme (with multiple dark mode variations) and syntax highlighting for Python code examples. It also includes interactive Plotly charts.

## Directory Structure

```
.
├── README.md           # The source content (Markdown) for the entire cheatsheet.
├── parse.js            # Node.js script to build index.html from README.md.
├── index.html          # The generated static website.
├── pdf/
│   ├── README.md       # Instructions for generating PDFs (requires Acrobat Pro & Chromium).
│   ├── create_index.py # Creates a page-number index for the PDF.
│   ├── remove_links.py # Replaces hyperlinks with static page numbers for printing.
│   ├── index_for_pdf.html
│   ├── index_for_pdf_print.html
│   └── Acrobat/        # Header/footer XML presets for Adobe Acrobat.
└── web/
    ├── template.html   # HTML template used by parse.js.
    ├── style.css       # Main styles for the website.
    ├── style_dark*.css # Variations for dark mode.
    ├── update_plots.py # Updates the Plotly charts with the latest external data.
    ├── convert_table.py# Converts plain text tables into fancy Unicode borders.
    ├── jquery-3.4.0.min.js
    ├── showdown.min.js # Markdown converter library.
    ├── highlight.min.js
    └── plotly.min.js
```

## Build & Deployment

The site is compiled locally using Node.js. 

### 1. Prerequisites

To install Node.js and npm, run:
```bash
# On Debian/Ubuntu
$ sudo apt install nodejs npm
# On macOS
$ brew install nodejs
```

Install the required global dependencies:
```bash
$ npm install -g jsdom jquery showdown highlightjs@9.12.0
```

*Note: If you are running on macOS and modules can't be found after installation, export the Node path:*
```bash
$ export NODE_PATH=/usr/local/lib/node_modules
```

### 2. Build the Website

To compile the cheatsheet, run the parser script from the project root. It reads `README.md`, injects it into `web/template.html`, and writes the result to `index.html`:
```bash
$ node parse.js
```

Alternatively, you can set up a git hook to run this script automatically before every commit. Create a file named `.git/hooks/pre-commit` containing the following line and make it executable:
```bash
./parse.js
```

## Updating Charts

The website includes interactive charts rendered via Plotly. The data for these charts is periodically refreshed from external sources.

To update the COVID-19 charts (deaths and confirmed cases) with the latest available data, run the following Python script from the `web/` directory:
```bash
$ cd web/
$ ./update_plots.py
```
This requires the `pandas` and `plotly` Python libraries.

## Generating a PDF

This repository includes a workflow for converting the website into a print-optimized PDF file. This is a multi-step process that involves specific external applications and manual layout adjustments.

The tools and instructions for this process are detailed in [`pdf/README.md`](pdf/README.md).
