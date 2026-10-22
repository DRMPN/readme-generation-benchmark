# Python Cheatsheet

![Screenshot of the website](descripitive_image_final.png)

A comprehensive Python cheatsheet — an interactive, single-page reference covering the whole Python language, its standard library, and the most useful third-party packages. It is available online at:

**https://python-cheatsheet-3muyjnl6.glitch.me/** (mirror of the main site)

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Contents](#contents)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Scripts](#scripts)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [Credits & License](#credits--license)

---

## About

This project is a **Python cheatsheet for experienced programmers**. Instead of tutorials, it offers dense, annotated code examples that follow the official style guide (PEP 8). Every snippet runs with Python **3.10+**.

The entire cheatsheet lives on one web page so that everything can be searched quickly with `Ctrl+F`, and it is rendered directly in the browser from a Markdown source — no build step or server required.

---

## Features

- **Single-page, self-contained site** — plain HTML/CSS/JS, hosted as static files.
- **Searchable** — use `Ctrl+F` (or `Cmd+F`) to jump between any of the 25 sections.
- **Syntax highlighting** for all Python code blocks via `highlight.min.js`.
- **Markdown rendering in the browser** via `showdown.min.js`.
- **Interactive charts** — Plotly-powered graphs of COVID-19 cases and deaths (`plotly.min.js`, `covid_cases.js`, `covid_deaths.js`).
- **Dark mode themes** — multiple dark stylesheet variants (`default_dark*.min.css`, `style_dark*.css`) alongside the default light theme (`default.min.css`, `style.css`).
- **Custom monospace font** — Menlo Regular and Bold bundled in all web formats (woff, woff2, ttf, svg, eot).
- **Print-friendly layout** — `index_for_pdf.html` / `index_for_pdf_print.html` for generating a PDF version.
- **Social / SEO cards** — Open Graph and Twitter card images (`image_social*.png`, `image_twitter_card*.jpeg`, `twitter_card_large.jpeg`).
- **Responsive design** — different pre-sized social and preview images (`image_720.jpeg`, `image_888.jpeg`, `image_960.jpeg`, etc.).

---

## Contents

The cheatsheet is organized into the following sections (each chapter is also stored as its own XML file, e.g. `Chapter_1.xml` … `chapter_8.xml`, plus `odd_pages.xml` / `even_pages.xml` for the paginated PDF export):

1. **Main** — syntax at a glance, numeric types, operators, integer sizes, strings, format specifiers, statements, comprehension syntax, classes, dataclasses, enum, exceptions.
2. **Libraries** — package managers (`pip`, `poetry`, `virtualenv`, `venv`, `pipx`), main and third-party libraries, Plotly charts, Pygame, Pandas examples.
3. **Types** — immutable and mutable types, type annotations, generics, operators and their methods.
4. **Classes** — class basics, inheritance, properties, dataclasses, slots and locks, duck typing, ABC.
5. **Data Structures** — operators, methods, comparison of structures, comprehensions.
6. **Exceptions** — catching, raising, and re-raising exceptions, built-in exception hierarchy.
7. **Numbers** — basics, float problems, math module functions and constants, random numbers.
8. **Strings** — basic operations, string module, formatting, escape sequences, Unicode.
9. **Bytes** — encoding and decoding, slicing, bytearray.
10. **Datetime** — creating and parsing dates, arithmetic, timezones.
11. **Structs** — packing/unpacking binary data with the `struct` module.
12. **Generators** — generators, comprehensions, generator expressions, coroutines, async/await.
13. **File Handling** — reading/writing files, CSV, JSON, pickle, file and directory operations.
14. **CSV** — reading and writing CSV files.
15. **JSON** — encoding, decoding, and pretty-printing JSON.
16. **Pickle** — serializing objects.
17. **SQLite** — database basics, parameterized queries.
18. **Statistics** — `statistics` and `numpy` functions.
19. **Bytes and String** — conversions between text and binary.
20. **Audio** — generating tones with the `wave` and `math` modules.
21. **Keyboard Shortcuts** — productivity tips.
22. **Terms** — terminology reference.
23. **Packages** — popular third-party libraries.
24. **Frequently Asked Questions** — see also `faq.html`.
25. **Useful Libraries** — curated list of packages worth knowing.

---

## How It Works

The site is built entirely from client-side JavaScript, so it works from any static host (GitHub Pages, Glitch, Netlify, or a local file):

1. **`index.html`** contains the page shell, navigation, and the full cheatsheet text stored as Markdown inside `<script type="text/plain">` blocks.
2. **`showdown.min.js`** converts the embedded Markdown into HTML at load time.
3. **`highlight.min.js`** applies Python syntax highlighting to the generated `<code>` blocks.
4. **`script_2.js`** and **`empty_script.js`** drive the UI: sidebar navigation, section scrolling, theme switching, and keyboard shortcuts.
5. **`plotly.min.js`** + **`covid_cases.js`** / **`covid_deaths.js`** render interactive COVID-19 charts (data in `continents.csv`).
6. **`style.css`** and the bundled **Menlo** font provide the monospaced, cheat-sheet look; the `*_dark*.css` files provide dark themes.
7. **`popup.html`** provides a small browser popup view of the cheatsheet.
8. **`faq.html`** and **`Demo.html`** contain standalone pages (FAQ and a font demo).

---

## Project Structure

```
.
├── index.html                      # Main cheatsheet page (source of truth, Markdown-embedded)
├── index_for_pdf.html              # HTML used to produce the PDF version
├── index_for_pdf_print.html        # Print-optimized version for PDF export
├── faq.html                        # Frequently asked questions page
├── popup.html                      # Compact popup view
├── Demo.html                       # Font/webfont demo page
├── template.html                   # HTML template used by the build scripts
│
├── JavaScript
│   ├── showdown.min.js             # Markdown → HTML converter
│   ├── highlight.min.js            # Syntax highlighter
│   ├── plotly.min.js               # Charting library
│   ├── script_2.js                 # Site logic (nav, themes, search)
│   ├── empty_script.js             # Placeholder script
│   ├── covid_cases.js              # COVID-19 case data & chart code
│   ├── covid_deaths.js             # COVID-19 death data & chart code
│   └── jquery-3.4.0.slim.min.js / jquery-3.4.0.min.js
│
├── Styles
│   ├── style.css                   # Main stylesheet
│   ├── style_dark1/2/3.css         # Dark theme variants
│   ├── default.min.css             # Default (light) highlight theme
│   └── default_dark1/2/3.min.css   # Dark highlight themes
│
├── Fonts
│   ├── Menlo Regular.* / Menlo Bold.*   # Custom monospaced font (all web formats)
│   └── 9f94dc20bb2a09c15241d3a880b7ad01.* / a6ffc5d72a96b65159e710ea6d258ba4.*
│
├── Data
│   ├── continents.csv              # Continent data for the charts
│   ├── covid_cases.js / covid_deaths.js
│   └── Chapter_1.xml … chapter_8.xml, odd_pages.xml, even_pages.xml, bottom_line.xml
│                                    # Chapter content used for the paginated PDF export
│
├── Images
│   ├── descripitive_image_final.png / descripitive_image_final-01.png
│   ├── image_720.jpeg, image_888.jpeg, image_960.jpeg, image_orig.jpeg,
│   │   image_orig_blue6.png, image_social_*.png, image_twitter_card*.jpeg,
│   │   twitter_card_large.jpeg, twitter_card_large_bckp.jpeg
│   ├── covid_cases.png, covid_deaths.png, mario_bros.png, favicon.png
│
├── Python scripts
│   ├── parse.js                    # Node script for parsing/generating chapter XML
│   ├── create_index.py             # Generates the index.html from chapter files
│   ├── update_plots.py             # Fetches COVID data and regenerates the Plotly charts
│   ├── convert_table.py            # Converts tabular data for the cheatsheet
│   ├── remove_links.py             # Strips links for the print/PDF version
│   └── empty_script.py             # Placeholder
│
└── README.md                       # This file
```

---

## Scripts

### `create_index.py`
Assembles `index.html` from the individual chapter sources (`Chapter_1.xml` … `chapter_8.xml`, `bottom_line.xml`), wrapping the content in `template.html`.

### `update_plots.py`
Pulls the latest COVID-19 data, processes it against `continents.csv`, and regenerates `covid_cases.js` / `covid_deaths.js` used by the Plotly charts.

### `convert_table.py`
Converts tabular/CSV content into the Markdown tables used inside the cheatsheet.

### `remove_links.py`
Produces a link-free variant of the page content for the printable/PDF versions (`index_for_pdf_print.html`).

### `parse.js`
Node.js helper that parses chapter markup and generates the XML page files used by the PDF pipeline.

Run them with:

```bash
python create_index.py
python update_plots.py
python convert_table.py
python remove_links.py
node parse.js
```

---

## Getting Started

### View locally

No build step needed — just open the page in a browser:

```bash
# Option 1: open directly
open index.html

# Option 2: serve locally
python -m http.server 8000
# then visit http://localhost:8000/index.html
```

> Note: some browsers restrict `file://` requests; a local server is the most reliable option.

### Generate the PDF version

1. Run `python remove_links.py` to strip hyperlinks.
2. Rebuild with `python create_index.py` if chapters changed.
3. Open `index_for_pdf_print.html` in a browser and print to PDF.

---

## Contributing

Contributions are welcome! The easiest ways to help:

- **Fix typos or clarify examples** — edit the relevant chapter file and re-run `create_index.py`.
- **Add a new section** — add a chapter file, register it in the table of contents, and rebuild the index.
- **Improve the charts** — extend `update_plots.py`.

When contributing code snippets, please ensure they:

- Run on Python 3.10+,
- Conform to PEP 8,
- Include a short, self-explanatory comment above each block,
- Keep each section compact — this is a cheatsheet, not a tutorial.

---

## Credits & License

- **Author:** Jovito — based on the widely used [python-cheatsheet](https://gto76.github.io/python-cheatsheet/) project.
- **Fonts:** Menlo (Regular & Bold), obtained via Online Web Fonts — see `Online_Web_Fonts.url` and `License.txt`.
- **Libraries used:** jQuery, Showdown.js, Highlight.js, Plotly.js.

This repository is distributed for educational purposes. Check `License.txt` files accompanying the bundled fonts for their redistribution terms, and respect the licenses of the JavaScript libraries (`showdown.min.js`, `highlight.min.js`, `plotly.min.js`, `jquery`).

---

## Quick Preview

```python
>>> a = "Python"
>>> b = [1, 2, 3]
>>> f"{a} has {len(b)} items"
'Python has 3 items'
>>> [x * 2 for x in b if x > 1]
[4, 6]
>>> dict(sorted({"c": 3, "a": 1, "b": 2}.items()))
{'a': 1, 'b': 2, 'c': 3}
```

Happy Pythoning! 🐍
