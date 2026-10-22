# Python Cheatsheet

> **Note:** This README was written from the file listing alone, without reading the file contents. Descriptions of behavior are inferred from file names and should be checked against the actual source code. Items marked **(verify)** are particularly uncertain.

## Overview

**python-cheatsheet-1b55ga8l** is a static web and print resource for Python. It appears to combine a browsable HTML cheatsheet with a printable PDF-ready version. The content is organized into numbered XML chapters, which are converted into HTML pages with a table of contents, search-friendly index, styling, and social sharing metadata.

The project includes:

- **Content** stored as XML chapters (`Chapter_1.xml` to `chapter_8.xml`), plus `odd_pages.xml`, `even_pages.xml`, and `bottom_line.xml` for page-layout content.
- **Build tooling** in JavaScript and Python for parsing, indexing, converting, and cleaning content.
- **Web front end** with HTML pages, CSS themes (light and several dark variants), and JavaScript for syntax highlighting and charts.
- **Embedded assets** including images, social cards, bundled fonts, and third-party libraries.

## Features

- Eight-chapter Python reference covering the core language and common tasks.
- Separate **print** and **web** index pages (`index_for_pdf.html`, `index_for_pdf_print.html`, `index.html`).
- Multiple **color themes** (`style.css`, `style_dark.css`, `style_dark1.css`, `style_dark2.css`, `style_dark3.css`) with matching highlight.js themes.
- Syntax highlighting via **highlight.js** and Markdown rendering via **showdown**.
- **Interactive charts** (`covid_cases.js`, `covid_deaths.js`) rendered with **Plotly**, using data from `covid_cases.png`, `covid_deaths.png`, and `continents.csv`.
- A **popup** and **FAQ** page for supplementary information.
- Social media preview images in several sizes (Twitter card, Open Graph).
- Bundled **Menlo** monospace fonts in multiple formats for offline and web use.

## Repository Structure

### Content (XML)

| File | Purpose (inferred) |
|---|---|
| `Chapter_1.xml` … `chapter_8.xml` | Main cheatsheet chapters. Note the mixed capitalization (`Chapter_1.xml` vs. `chapter_2.xml`). |
| `odd_pages.xml` / `even_pages.xml` | Content arranged for odd and even pages in a printed, two-sided layout. |
| `bottom_line.xml` | Closing or summary content, possibly a footer or final section. |

### Build and Processing Scripts

| File | Language | Purpose (inferred) |
|---|---|---|
| `parse.js` | JavaScript | Parses the XML chapters into HTML or another intermediate format. |
| `create_index.py` | Python | Generates index pages from the parsed content. |
| `remove_links.py` | Python | Strips links, likely for the print version. |
| `convert_table.py` | Python | Converts tables between formats. **(verify)** |
| `update_plots.py` | Python | Regenerates chart data or chart output. |
| `empty_script.py` | Python | Placeholder or stub script. |
| `script_2.js` | JavaScript | Client-side behavior for the web pages. |
| `covid_cases.js`, `covid_deaths.js` | JavaScript | Plotly chart definitions for the COVID charts. |

### HTML Pages

| File | Purpose (inferred) |
|---|---|
| `index.html` | Main web version of the cheatsheet. |
| `index_for_pdf.html` | Version prepared for PDF export. |
| `index_for_pdf_print.html` | Print-optimized variant. |
| `template.html` | Base template used to generate pages. |
| `faq.html` | Frequently asked questions. |
| `popup.html` | Popup content, possibly a notice or help dialog. |
| `Demo.html` (×3) | Font demonstration pages bundled with web font kits. Not part of the cheatsheet itself. |

### Stylesheets

| File | Purpose (inferred) |
|---|---|
| `style.css` | Default light theme and layout. |
| `style_dark.css`, `style_dark1.css`, `style_dark2.css`, `style_dark3.css` | Dark theme variants. |
| `default.min.css`, `default_dark.min.css`, `default_dark1.min.css`, `default_dark2.min.css`, `default_dark3.min.css` | highlight.js code-highlighting themes matching the page themes. |

### JavaScript Libraries

| File | Library |
|---|---|
| `jquery-3.4.0.min.js`, `jquery-3.4.0.slim.min.js` | jQuery 3.4.0 (full and slim builds) |
| `highlight.min.js` | highlight.js, for syntax highlighting |
| `showdown.min.js` | Showdown, for Markdown-to-HTML conversion |
| `plotly.min.js` | Plotly.js, for charts |

### Data

| File | Purpose |
|---|---|
| `continents.csv` | Mapping of countries to continents, used for grouping chart data. **(verify)** |
| `covid_cases.png`, `covid_deaths.png` | Static chart images, likely fallbacks or previews for the interactive charts. |

### Images

| File(s) | Purpose (inferred) |
|---|---|
| `descripitive_image_final.png`, `descripitive_image_final-01.png` | Illustrative images for the content. The file name contains a typo ("descripitive"), which is preserved here. |
| `mario_bros.png` | Example or illustration image. |
| `image_orig.jpeg`, `image_orig_blue6.png` | Original source images. |
| `image_720.jpeg`, `image_960.jpeg`, `image_888.jpeg` | Resized variants. |
| `image_social.jpeg`, `image_social_2.png`, `image_social_3.png`, `image_social_4.png`, `image_social_bckp.png` | Social sharing images. `_bckp` suggests a backup. |
| `image_twitter_card.jpeg`, `image_twitter_card_2.jpeg`, `twitter_card_large.jpeg`, `twitter_card_large_bckp.jpeg` | Twitter/X card images. |
| `favicon.png` | Site favicon. |

### Fonts

The font folders are web font kits for **Menlo**, a monospace font, in multiple formats (`.woff`, `.woff2`, `.ttf`, `.eot`, `.svg`).

- **Menlo Regular** and **Menlo Bold** are provided with `License.txt` and `Online_Web_Fonts.url`, which point to the font's source.
- Three hash-named kits (`a6ffc5d72a96b65159e710ea6d258ba4.*`, `9f94dc20bb2a09c15241d3a880b7ad01.*`, and one more) are generated web font packages, each with its own `Demo.html`, license, and source URL. **(verify)** Their exact fonts should be checked before redistribution.

Menlo is a proprietary font from Microsoft/Apple. Confirm that you have the right to redistribute the font files before publishing this repository.

## How the Pieces Fit Together

The project appears to follow this workflow (inferred from file names):

1. **Author content** in the XML chapter files (`Chapter_1.xml` to `chapter_8.xml`), with page-layout files for printing.
2. **Parse** the XML using `parse.js` into HTML fragments.
3. **Assemble pages** from `template.html` and generate indexes with `create_index.py`, producing `index.html`, `index_for_pdf.html`, and `index_for_pdf_print.html`.
4. **Post-process** for print with `remove_links.py` and other converters.
5. **Update data-driven content** such as charts with `update_plots.py`, `covid_cases.js`, and `covid_deaths.js`.
6. **Serve or export** the result. The HTML can be opened directly in a browser, or the print-ready index can be converted to PDF.

## Getting Started

### Prerequisites

- **Python 3.x** for the `.py` scripts.
- **Node.js** for `parse.js`. **(verify)** Check whether it has npm dependencies.
- A modern web browser for viewing the output.

### Viewing the Cheatsheet

No build is needed to view the static site. Open `index.html` in a browser:

```bash
open index.html        # macOS
xdg-open index.html    # Linux
start index.html       # Windows
```

### Rebuilding the Content (verify)

The exact commands are not documented in the listing. A likely sequence is:

```bash
node parse.js
python3 create_index.py
python3 remove_links.py
python3 update_plots.py
```

Check each script's source for required arguments, input and output paths, and dependencies before running them.

### Exporting to PDF

1. Open `index_for_pdf_print.html` in a browser.
2. Print to PDF, using the browser's print dialog with background graphics enabled.

## Customization

- **Themes:** Copy one of the `style_dark*.css` files as a starting point, and pair it with a matching `default_dark*.min.css` highlight theme.
- **Content:** Edit the chapter XML files, then rerun the parser and index generator.
- **Social previews:** Replace the `image_social*` and `twitter_card*` images to change link previews.
- **Charts:** Update `continents.csv` or the chart scripts to change the COVID visualizations.

## Third-Party Components

| Component | Version / Notes | License |
|---|---|---|
| jQuery | 3.4.0 | MIT **(verify)** |
| highlight.js | Bundled minified build | BSD-3-Clause **(verify)** |
| Showdown | Bundled minified build | BSD-3-Clause **(verify)** |
| Plotly.js | Bundled minified build | MIT **(verify)** |
| Menlo fonts | Bundled web font kits | See `License.txt` in each font folder |

## Known Issues and Notes

- **Inconsistent naming:** `Chapter_1.xml` uses a capital C, while the other chapters use lowercase. The build may depend on this exact casing, which can fail on case-sensitive file systems.
- **Typo in file name:** `descripitive_image_final.png` should probably be `descriptive_image_final.png`. Renaming it requires updating any references.
- **Backup files:** `image_social_bckp.png` and `twitter_card_large_bckp.jpeg` may be unused and can be removed if not referenced.
- **Duplicate font kits:** Multiple hash-named font folders and `Demo.html` files may be leftovers from downloading font kits. Remove any that the site does not use.
- **Placeholder script:** `empty_script.py` contains no logic, so it can be removed or implemented.
- **Font licensing:** Confirm redistribution rights for Menlo before publishing.

## Contributing

1. Fork the repository and create a branch.
2. Edit the XML chapters or scripts.
3. Rebuild the HTML and verify the output in a browser, including the dark themes and the print version.
4. Open a pull request describing the change.

## License

See the project's license file. The bundled fonts are covered by their own licenses in `License.txt`. Third-party libraries retain their original licenses.
