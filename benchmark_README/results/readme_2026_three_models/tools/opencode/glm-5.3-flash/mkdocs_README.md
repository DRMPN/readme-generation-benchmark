# MkDocs

Project documentation with Markdown.

MkDocs is a **fast**, **simple** and **downright gorgeous** static site
generator that's geared towards building project documentation. Documentation
source files are written in Markdown, and configured with a single YAML
configuration file. Start by reading the [introductory tutorial], then check the
[User Guide] for more information.

## Features

- **Great themes available** — Choose between the built-in themes,
  [`mkdocs`](https://www.mkdocs.org/user-guide/choosing-your-theme/#mkdocs) and
  [`readthedocs`](https://www.mkdocs.org/user-guide/choosing-your-theme/#readthedocs),
  select one of the third-party themes (see the
  [MkDocs Themes](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Themes) wiki page
  as well as the [MkDocs Catalog](https://github.com/mkdocs/catalog#-theming)),
  or [build your own](https://www.mkdocs.org/dev-guide/themes/).
- **Easy to customize** — Get your project documentation looking just the way
  you want it by
  [customizing your theme](https://www.mkdocs.org/user-guide/customizing-your-theme/)
  and/or installing some
  [plugins](https://www.mkdocs.org/user-guide/configuration/#plugins). Modify
  Markdown's behavior with
  [Markdown extensions](https://www.mkdocs.org/user-guide/configuration/#markdown_extensions).
  Many [configuration options](https://www.mkdocs.org/user-guide/configuration/)
  are available.
- **Preview your site as you work** — The built-in dev-server allows you to
  preview your documentation as you're writing it. It will even auto-reload and
  refresh your browser whenever you save your changes.
- **Host anywhere** — MkDocs builds completely static HTML sites that you can
  host on GitHub Pages, Amazon S3, or
  [anywhere](https://www.mkdocs.org/user-guide/deploying-your-docs/) else you
  choose.

## Installation

Install MkDocs with pip:

```bash
pip install mkdocs
```

Optional localization support for the built-in themes is available via the
`i18n` extra:

```bash
pip install 'mkdocs[i18n]'
```

MkDocs requires Python 3.8 or newer. For more details, see the
[Installation Guide](https://www.mkdocs.org/user-guide/installation/).

## Quick start

Create a new project and preview it with the built-in dev-server:

```bash
mkdocs new my-project
cd my-project
mkdocs serve
```

Then open <http://127.0.0.1:8000/> in your browser. The dev-server rebuilds
your documentation whenever the configuration file, documentation directory, or
theme directory changes.

A new project contains a single configuration file named `mkdocs.yml` and a
folder named `docs` containing your documentation source files. The
`site_name` option is the only required setting in the configuration file.

Build the static site with:

```bash
mkdocs build
```

This creates a `site` directory containing the generated HTML, plus extras
such as `sitemap.xml` and `mkdocs/search_index.json`.

## Commands

MkDocs provides the following commands (use `mkdocs --help` for a complete
list, or `mkdocs COMMAND --help` for the options of a given command):

- `mkdocs new` — Create a new MkDocs project.
- `mkdocs serve` — Run the development server with live reload.
- `mkdocs build` — Build the documentation site.
- `mkdocs gh-deploy` — Deploy your documentation to GitHub Pages.
- `mkdocs get-deps` — Inspect the Markdown extensions and themes required by
  your configuration.

## Documentation

The complete documentation is available at [www.mkdocs.org](https://www.mkdocs.org/).

- [Getting Started](https://www.mkdocs.org/getting-started/) — An introductory
  tutorial.
- [User Guide](https://www.mkdocs.org/user-guide/) — Complete documentation of
  MkDocs' features.
- [Release Notes](https://www.mkdocs.org/about/release-notes/) — Project
  history.

## Getting help

To get help with MkDocs, please use the
[GitHub discussions](https://github.com/mkdocs/mkdocs/discussions) or
[GitHub issues](https://github.com/mkdocs/mkdocs/issues).

## Contributing

Contributions are welcome in the form of code patches via pull requests,
documentation improvements, and bug reports. For details on how to set up a
development environment and run the checks, see
[CONTRIBUTING.md](CONTRIBUTING.md).

In summary, the project uses [Hatch](https://hatch.pypa.io/) to manage
dependencies and run tasks. The main checks can be run with:

```bash
hatch run all
```

This encompasses the individual checks:

- `hatch run test:test` and `hatch run integration:test` — Run the test suite.
- `hatch run style:fix` — Check and format the code with Isort, Black, and
  Ruff.
- `hatch run types:check` — Type-check the code with mypy.
- `hatch run lint:check` — Run the remaining checks, such as spelling and JS
  style.

Everyone interacting in the MkDocs project's codebases, issue trackers, chat
rooms, and mailing lists is expected to follow the
[PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).

## License

MkDocs is licensed under the [BSD-2-Clause](LICENSE) license.

Copyright © 2014-present, Tom Christie. All rights reserved.

[introductory tutorial]: https://www.mkdocs.org/getting-started/
[User Guide]: https://www.mkdocs.org/user-guide/
