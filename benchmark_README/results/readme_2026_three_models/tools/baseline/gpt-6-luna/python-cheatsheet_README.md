# Comprehensive Python Cheatsheet

This repository contains a web-based Python reference and supporting files for generating and preparing its printable PDF editions. The cheatsheet is organized into linked topics and includes Python examples, syntax-highlighted code, plots, images, and library references. The repository also includes static web assets, helper scripts, and PDF production materials.

## Overview

The site is assembled from `web/template.html` and a Markdown source file named `README.md` by the root-level `parse.js` script. The generated site is `index.html`. The topic navigation in the parser covers eight broad areas:

1. Collections
2. Types
3. Syntax
4. System
5. Data
6. Advanced
7. Libraries
8. Multimedia

The `web/` directory contains the site’s stylesheets, JavaScript libraries, fonts, images, and supporting data. It includes light and dark style resources, syntax highlighting, and Plotly assets and chart data. The `pdf/` directory contains Acrobat header and footer resources, alternate print-oriented HTML files, and instructions for creating PDFs.

## Requirements

To regenerate the web page, install Node.js and npm, then install the modules used by `parse.js`:

- `jsdom`
- `jquery`
- `showdown`
- `highlightjs` version `9.12.0`

The parser’s comments document both global and project-local dependency installation. The project-local option is:

```sh
npm install jsdom jquery showdown highlightjs@9.12.0
```

Alternatively, install globally:

```sh
npm install -g jsdom jquery showdown highlightjs@9.12.0
```

On macOS, if globally installed modules cannot be found, the parser comments suggest setting `NODE_PATH` to the global module directory, for example:

```sh
export NODE_PATH=/usr/local/lib/node_modules
```

The repository also contains Python helper scripts. The supplied files do not define a Python dependency installation procedure for all helpers. In particular, `pdf/create_index.py` imports BeautifulSoup.

## Setup and Usage

Run commands from the repository root. To generate the site:

```sh
node parse.js
```

The parser’s usage comment describes this command as creating `index.html` from `web/template.html` and the Markdown source. Open the resulting `index.html` in a browser to view the cheatsheet. The repository includes local web assets such as stylesheets, fonts, JavaScript libraries, and images.

The root parser has no documented command-line options. Its comments show `node parse.js` as the intended invocation. If you are updating the cheatsheet source, regenerate the page after making changes so that the generated HTML reflects them.

Several auxiliary scripts are available:

- `web/convert_table.py` converts between ASCII and Unicode table borders. It reads table lines from standard input and prints the converted result. For example:

  ```sh
  python3 web/convert_table.py < table.txt
  ```

- `pdf/create_index.py` reads `index.html` and prints an alphabetical index of headings from levels 2 through 4.
- `pdf/remove_links.py` makes a set of predefined substitutions in the root `index.html`, replacing selected links with plain text and page references. It is intended for the print-optimized PDF workflow; it changes `index.html` in place.

The `web/` directory also contains plotting-related scripts and data, including `update_plots.py`, chart JavaScript files, and `continents.csv`. Their precise options and external data requirements are not documented in the supplied text.

## Configuration and Assets

There is no general configuration file or documented settings interface in the supplied files. The web presentation is supported by CSS files in `web/`, including `style.css`, multiple dark-style variants, and corresponding bundled `default` stylesheets. The directory also includes local copies of jQuery, Showdown, Highlight.js, and Plotly, as well as Menlo font files in several web font formats.

The parser includes hard-coded HTML fragments used for navigation and selected code examples. The PDF workflow uses separate print HTML files: `pdf/index_for_pdf.html` and `pdf/index_for_pdf_print.html`. The repository also contains XML files under `pdf/Acrobat/` for Acrobat header and footer presets.

The bundled font directories include `License.txt` files. Third-party JavaScript files also contain their own license notices. These notices apply to those components; they do not establish a license for the project as a whole.

## Development

Edit the cheatsheet source and the relevant template or assets, then run `node parse.js` to rebuild `index.html`. The parser comments recommend optionally adding a Git pre-commit hook that runs:

```sh
./parse.js
```

That suggestion assumes the script is executable and that its Node dependencies are available to the hook.

For changes involving the PDF edition, consult [`pdf/README.md`](pdf/README.md). Its documented process is specifically for macOS and calls for Adobe Acrobat Pro DC. The instructions describe two PDF variants: a normal PDF and one optimized for laser color printing. They also specify opening the generated site in Chromium version `108.0.5328.0`; the document warns that later versions render the site incorrectly after the print index is added. The workflow includes manual browser styling adjustments, printing to A4 PDF, applying Acrobat presets, and checking that plots render correctly. This is a manual publishing procedure, not an automated build step.

## Testing and Validation

The supplied files do not show a dedicated automated test suite or test command. After regenerating the site, open `index.html` in a browser and check that the content, navigation links, code formatting, images, and plots appear as expected.

For PDF work, follow the checks in `pdf/README.md`: verify plot rendering, confirm the expected page count during production, inspect header and footer alignment, and remove the final blank page when instructed. The PDF guide describes a 51-page intermediate document with a blank last page before that page is removed.

## PDF Production

The PDF instructions describe setup of Acrobat header and footer presets by copying files from `pdf/Acrobat/` into the user’s Adobe Acrobat preferences directory. They then provide separate steps for normal and print-optimized PDFs, followed by shared Acrobat finishing instructions.

The print-optimized workflow runs the parser and `pdf/remove_links.py` before using the print-specific HTML. Follow the source instructions carefully: they include manual color adjustments, paper and margin settings, metadata values, and optimization steps. These are production instructions rather than requirements for viewing the web version.

## License

No project-level license is identified in the supplied files. The repository does include license files and notices for bundled components, including font packages and JavaScript libraries. Review those component-specific terms before redistributing the bundled assets; do not assume they define the license for the cheatsheet or the repository as a whole.
