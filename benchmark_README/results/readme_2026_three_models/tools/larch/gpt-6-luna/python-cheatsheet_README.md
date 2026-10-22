# Python Cheatsheet

A static, browser-based Python cheatsheet with chapter pages, reference material, images, and supporting scripts. The repository also includes files for PDF-oriented indexes, interactive examples, and COVID-19 visualizations.

## Browse the cheatsheet

Open `index.html` in a web browser to view the main site. For a local web server—useful if a browser restricts access to local files—run this command from the repository root:

```bash
python -m http.server 8000
```

Then visit <http://localhost:8000>.

Other HTML pages include:

- `faq.html` — frequently asked questions
- `popup.html` — a popup-oriented page
- `index_for_pdf.html` and `index_for_pdf_print.html` — PDF-related index pages
- `template.html` and `Demo.html` — template or demo pages

The chapter content is also represented by XML files, including `Chapter_1.xml` and `chapter_2.xml` through `chapter_8.xml`. Additional XML files include `odd_pages.xml`, `even_pages.xml`, and `bottom_line.xml`.

## Repository contents

### Pages and styling

- `index.html` is the main entry point.
- `style.css` and `style_dark*.css` provide site styling, including dark-theme variants.
- `default*.css` files provide additional styles, including highlighted or dark-themed variants.
- `highlight.min.js` and `default*.min.css` support syntax highlighting.
- `jquery-3.4.0.min.js` and `jquery-3.4.0.slim.min.js` are bundled jQuery builds.
- `showdown.min.js` provides Markdown-to-HTML support.
- `plotly.min.js` supports interactive charts.
- `script_2.js` and `parse.js` provide additional JavaScript functionality.

### Images and data

The repository contains images used by the site, including social-media cards, descriptive images, and `mario_bros.png`. It also includes:

- `covid_cases.png` and `covid_deaths.png` — chart images
- `covid_cases.js` and `covid_deaths.js` — chart-related JavaScript data or code
- `continents.csv` — a CSV data file

### Fonts and licenses

Several font files are bundled in formats such as WOFF, WOFF2, TTF, EOT, and SVG. The repository includes `License.txt` files alongside some font assets; consult those files for the applicable font licensing terms.

### Python utilities

The repository includes these Python scripts:

- `create_index.py` — related to generating an index
- `remove_links.py` — related to removing links
- `update_plots.py` — related to updating plots
- `convert_table.py` — related to converting tables
- `empty_script.py` — an otherwise empty or placeholder script

The exact inputs, options, and outputs for these utilities are not documented here. Review each script before running it, especially if it modifies files.

## Requirements

The site is primarily static and can be viewed in a modern web browser. A local Python installation is only needed if you want to serve the files with `python -m http.server` or run the Python utilities.

No dependency manifest, such as `requirements.txt` or `pyproject.toml`, is listed. Check the individual scripts for any additional Python dependencies before using them.

## Notes

- Keep the bundled HTML, JavaScript, CSS, font, and image files together when copying or hosting the site; pages may rely on relative paths to those assets.
- No build or test configuration is listed. To check the site, open `index.html` and verify that its pages, images, and interactive features load as expected.
- The repository listing does not identify a root project license. Check the project source and bundled asset licenses before redistributing the material.
