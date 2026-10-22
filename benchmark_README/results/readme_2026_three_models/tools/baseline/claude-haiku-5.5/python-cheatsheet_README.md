# Comprehensive Python Cheatsheet

This repository contains the source and build tooling for the Comprehensive Python Cheatsheet, a single-page reference that is rendered as a web page (`index.html`) and can also be exported as a printable PDF. The Python content is written in Markdown, and `parse.js` converts it into the HTML page. The `pdf/` directory holds the scripts, templates, and manual steps for producing print-ready PDF versions.

## Overview

The repository has three main parts:

- **Web build (`parse.js`, `web/`)**: `parse.js` is a Node.js script that creates `index.html` from `web/template.html` and the root `README.md`. The `web/` directory holds the template, stylesheets, JavaScript libraries, fonts, images, and plot data.
- **PDF production (`pdf/`)**: Scripts, HTML variants, Adobe Acrobat header and footer presets, and a manual workflow for generating PDF files.
- **Helper utilities (`web/`)**: `convert_table.py` converts tables between ASCII and Unicode box-drawing formats, and `empty_script.py` is a small Python script that the repository includes for GitHub language detection.

### Repository layout

| Path | Purpose |
|------|---------|
| `index.html` | Generated cheatsheet page |
| `parse.js` | Builds `index.html` from the template and Markdown source |
| `pdf/README.md` | Step-by-step manual for creating PDFs on macOS |
| `pdf/create_index.py` | Prints a grouped alphabetical index of headings from `index.html` |
| `pdf/remove_links.py` | Replaces selected links in `index.html` with page-number references |
| `pdf/index_for_pdf.html`, `pdf/index_for_pdf_print.html` | Replacement index sections for the two PDF variants |
| `pdf/popup.html` | Included HTML file; its purpose is not described in the supplied material |
| `pdf/Acrobat/` | XML header and footer presets for Adobe Acrobat Pro DC |
| `web/template.html` | Template used by `parse.js` |
| `web/convert_table.py` | Converts tables between ASCII and Unicode box-drawing styles |
| `web/covid_cases.js`, `web/covid_deaths.js` | Plotly data files for COVID-19 charts |
| `web/*.css` | Stylesheets, including default and several dark variants |
| `web/update_plots.py` | Present in the repository; its contents are not part of the supplied material |

## Setup

### Requirements for building the web page

`parse.js` is a Node.js script. The comments in the file give these installation steps:

1. Install Node.js and npm. On Debian or Ubuntu:
   ```bash
   sudo apt install nodejs npm
   ```
   On macOS, use Homebrew (`brew install ...`).

2. Install the dependencies. You can install them globally:
   ```bash
   npm install -g jsdom jquery showdown highlightjs@9.12.0
   ```
   Or install them into the project directory, which the file recommends to avoid permission and path problems:
   ```bash
   npm install jsdom jquery showdown highlightjs@9.12.0
   ```

3. If you installed globally on macOS and Node cannot find the modules, add the following line to `~/.bash_profile` or `~/.bashrc`, then run `bash`:
   ```bash
   export NODE_PATH=/usr/local/lib/node_modules
   ```

### Requirements for PDF generation

The PDF workflow in `pdf/README.md` is written for macOS and needs:

- Adobe Acrobat Pro DC
- Chromium version 108.0.5328.0, as the manual states that later versions render the site incorrectly after the index is added
- Python 3, with the `bs4` (BeautifulSoup) package for `pdf/create_index.py`
- The Acrobat header and footer presets from `pdf/Acrobat/`, copied to `/Users/<username>/Library/Preferences/Adobe/Acrobat/DC/HeaderFooter/`

## Usage

### Building the web page

Run the build script from the repository root:

```bash
./parse.js
```

Or with Node directly:

```bash
node parse.js
```

The script writes `index.html`. The file header suggests adding `./parse.js` to a Git `pre-commit` hook in `.git/hooks/`, so the page is rebuilt before every commit.

### Generating the index

`pdf/create_index.py` reads `index.html`, collects level 2 to 4 headings, and prints a Markdown index grouped by first letter. Each entry links to the heading's anchor with a `[1](#id)` link. Output goes to standard output:

```bash
python3 pdf/create_index.py > index_output.md
```

The script's usage comment is incomplete (it reads `Usage: .py`), so this invocation is inferred from the code.

### Preparing the PDF-specific version

`pdf/remove_links.py` edits the root `index.html` in place. It replaces a fixed list of in-text links with plain text and a page reference such as `(p. 16)`, which is needed because links do not work on paper. Run it with:

```bash
./pdf/remove_links.py
```

The PDF manual says to run `./parse.js` before this step, so that the links are regenerated from the source first.

### Converting tables

`web/convert_table.py` reads from standard input and writes to standard output. It detects the input style automatically:

- If the first line starts with `+`, it treats the input as an ASCII table and converts it to Unicode box-drawing characters. In the body rows, `yes` becomes a check mark (✓).
- Otherwise, it converts Unicode box-drawing input back to ASCII.

```bash
python3 web/convert_table.py < table_ascii.txt
```

### Viewing the page

Open `index.html` in a browser. The page loads its scripts and stylesheets from the `web/` directory.

## Configuration

The supplied files show several configurable elements, but no separate configuration file:

- **Stylesheets**: `web/` contains `style.css` and `default.min.css` along with several dark variants (`style_dark.css` through `style_dark3.css`, and `default_dark.min.css` through `default_dark3.min.css`). The supplied files do not show which one the template selects.
- **Module paths**: On macOS, `NODE_PATH` can be set so that `parse.js` finds globally installed modules (see Setup).
- **Print settings**: The PDF manual specifies the settings used for printing from Chromium: A4 paper, default margins (top 10 mm, right 9.5 mm, bottom 8 mm, left 10 mm), default scale, and no headers or footers. The resulting document should be 51 pages long, with an empty last page.
- **Acrobat header and footer**: The manual provides these values if the presets are lost: left-line 0.6, left-text 0.8, top-line 11.4, bottom-text 0.27, right-text-odd 0.57, font Menlo, font size 8. The page crop uses inches, A4 page size, and an X offset of 0.1 in.
- **Document properties**: The manual sets the PDF title to "Comprehensive Python Cheatsheet" and the author to "Jure Šorn".
- **Plot data**: The chart files `web/covid_cases.js` and `web/covid_deaths.js` contain Plotly data and are loaded by the page. Their structure is data-driven, so they are regenerated rather than edited by hand.

## Development

### Editing content

The cheatsheet content lives in the root `README.md`, which `parse.js` converts into `index.html`. Rebuild after each change. Because `pdf/remove_links.py` and the PDF index templates modify or replace parts of `index.html`, avoid committing those temporary changes to the web version. The PDF manual restores the page by re-running `parse.js` after the PDF is generated.

### Code blocks

`parse.js` defines many code snippets as highlighted HTML strings using `highlight.js` class names (for example, `hljs-keyword` and `hljs-string`). The `highlightjs@9.12.0` version matches the bundled `web/highlight.min.js` (v9.12.0).

### Bundled libraries

The `web/` directory includes these third-party files:

- `jquery-3.4.0.min.js` and `jquery-3.4.0.slim.min.js`
- `highlight.min.js` (highlight.js v9.12.0, BSD-3-Clause license per its header)
- `showdown.min.js`, a Markdown-to-HTML converter
- `plotly.min.js`, used for the COVID-19 charts

### Fonts

`web/` includes two font sets from OnlineWebFonts: Menlo Regular and Menlo Bold, in EOT, SVG, TTF, WOFF, and WOFF2 formats. Each set has its own `License.txt` and `Online_Web_Fonts.url` file, which should be consulted before redistributing them.

### Python helpers

- `pdf/create_index.py` depends on BeautifulSoup (`bs4`) and uses Python's standard library otherwise.
- `pdf/remove_links.py` contains a dictionary of link text replacements that must match the current `index.html` exactly. If the source changes, these entries may no longer match, and the script will silently leave the unmatched links in place.
- `web/convert_table.py` has no external dependencies.

### Repository hygiene

The file header of `parse.js` suggests installing it as a pre-commit hook so that `index.html` stays in sync with the source.

## Testing

The supplied file listing contains no test files, test runner configuration, or continuous integration configuration. Verification is manual:

- After building, open `index.html` and confirm that the page renders and the Plotly charts appear. The PDF manual includes a step to check that plots were rendered correctly.
- For PDF output, follow the checklist in `pdf/README.md`: confirm the page count (51 pages, with an empty last page), check header and footer alignment on the first page, and confirm that the bottom line aligns with the text.
- `convert_table.py` can be checked by converting a table to Unicode and back to ASCII and comparing the result with the original.

## License

No top-level license file is included in the supplied file listing, so this README does not state a license for the project's own content or code. The bundled third-party components carry their own terms:

- The Menlo font files include `License.txt` files in their respective directories.
- `highlight.min.js` identifies itself as BSD-3-Clause licensed in its header.
- The jQuery and Showdown files include their own license headers.

Check the license terms for the root of the project before reusing or redistributing the cheatsheet content.

## Notes on the supplied material

- `parse.js` reads the root `README.md`, but that file is not in the supplied listing, so its content could not be verified.
- `pdf/README.md` refers to `pdf/acrobat/`, while the directory in the listing is `pdf/Acrobat/`. Use the path that matches your file system when copying the presets.
- `pdf/remove_links.py` documents its usage as `./remove_links.py`, but the PDF manual invokes it as `./pdf/remove_links.py`. Both work because the script resolves paths relative to its own location.
