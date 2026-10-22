# Comprehensive Python Cheatsheet

This repository contains a concise, example-driven reference to Python and commonly used Python libraries. The rendered cheatsheet is [`index.html`](index.html), with its styles, scripts, images, and data files in [`web/`](web/).

## Read the cheatsheet

- Open `index.html` in a web browser to browse the local copy.
- Visit the [hosted cheatsheet](https://gto76.github.io/python-cheatsheet/) for the published web version.
- Use your browser’s Find feature (`Ctrl+F` or `⌘F`) to locate a topic. The page has linked sections and a table of contents.
- The page supports light and dark themes. Dark variants can be selected with `?theme=dark`, `?theme=dark1`, `?theme=dark2`, or `?theme=dark3`; `?theme=light` selects light mode. Without an explicit theme, the page can follow the browser’s dark-mode preference.

The examples use placeholders such as `<list>` and `<str>` to indicate the kind of value expected or produced. This is a quick reference rather than a step-by-step Python course; consult the [Python documentation](https://docs.python.org/3/) when you need fuller explanations.

## Topics

The contents are organized into these broad groups:

1. **Collections** — lists, dictionaries, sets, tuples, ranges, iteration, and generators.
2. **Types** — types and abstract base classes, strings, regular expressions, formatting, numbers, combinatorics, and dates and times.
3. **Syntax** — functions, inline expressions, imports, decorators, classes, duck types, enums, and exceptions.
4. **System** — program exit, input and output, command-line arguments, files, paths, and operating-system commands.
5. **Data** — JSON, pickle, CSV, SQLite, bytes, structs, arrays, memory views, and deques.
6. **Advanced** — operators, pattern matching, logging, introspection, threads, and coroutines.
7. **Libraries** — examples using third-party libraries for progress bars, plotting, tables, console and GUI applications, scraping, web applications, and profiling.
8. **Multimedia** — NumPy, images, animation, audio, synthesizers, Pygame, pandas, and Plotly.

The page also includes an appendix with Cython and installation-related notes.

## Repository contents

- `index.html` — the checked-in rendered cheatsheet.
- `web/` — page template, styling, browser scripts, images, chart data and assets, plus helper scripts.
- `web/faq.html` — FAQ content covering version assumptions, notation, and usage.
- `pdf/` — HTML files, scripts, and Acrobat settings used in the documented PDF preparation workflow. The workflow is described in [`pdf/README.md`](pdf/README.md); it requires software and manual steps described there.
- `parse.js` — a Node.js script that converts Markdown in the root `README.md` into `index.html`, using `web/template.html` and additional page transformations.

## Rebuilding the web page

`parse.js` reads the root `README.md` and writes over `index.html`. Its comments list these Node.js modules: `jsdom`, `jquery`, `showdown`, and `highlightjs` (the script’s setup notes specify `highlightjs@9.12.0`). For example, after installing Node.js and those modules, run:

```sh
node parse.js
```

**Caution:** this repository snapshot does not include the full cheatsheet Markdown that corresponds to the checked-in `index.html` as a separate source file. The `README.md` here is project documentation; running `parse.js` will regenerate `index.html` from this document and therefore replace the rendered cheatsheet. Do not run it unless that replacement is intended.

Other helpers include `web/convert_table.py`, which converts between ASCII and Unicode table borders, and `web/update_plots.py`, which refreshes the Plotly examples and image files from external data sources. The latter requires network access and Python packages; its source imports pandas and Plotly.

## Related links

- [Frequently Asked Questions](https://github.com/gto76/python-cheatsheet/wiki/Frequently-Asked-Questions)
- [Repository on GitHub](https://github.com/gto76/python-cheatsheet)
- [Hosted cheatsheet](https://gto76.github.io/python-cheatsheet/)
