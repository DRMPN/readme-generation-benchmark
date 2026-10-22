# MkDocs

MkDocs is a **fast**, **simple** and **downright gorgeous** static site generator that's geared towards building project documentation. Documentation source files are written in Markdown, and configured with a single YAML configuration file.

## Features

- **Great themes available** — Choose between the built-in themes (`mkdocs` and `readthedocs`), pick one of the many third-party themes, or build your own.
- **Easy to customize** — Customize your theme, install plugins, and modify Markdown's behavior with Markdown extensions.
- **Preview your site as you work** — The built-in dev-server lets you preview your documentation as you're writing it, auto-reloading and refreshing your browser whenever you save your changes.
- **Host anywhere** — MkDocs builds completely static HTML sites that you can host on GitHub Pages, Amazon S3, or anywhere else you choose.

## Requirements

MkDocs requires Python 3.8+ (Python 3.8–3.12 are supported, including PyPy) and `pip`.

## Installation

Install the `mkdocs` package using pip:

```bash
pip install mkdocs
```

Verify the installation:

```console
$ mkdocs --version
mkdocs, version 1.2.0 from /usr/local/lib/python3.8/site-packages/mkdocs (Python 3.8)
```

On Windows, if commands don't work directly, prefix them with `python -m`, e.g. `python -m pip install mkdocs` and `python -m mkdocs`.

Optional extras:

```bash
pip install 'mkdocs[i18n]'   # theme localization support (Babel)
```

## Getting Started

Create a new project:

```bash
mkdocs new my-project
cd my-project
```

This creates a single configuration file, `mkdocs.yml`, and a folder named `docs` containing your documentation source files, starting with a single page, `index.md`.

Start the built-in development server:

```console
$ mkdocs serve
INFO    -  Building documentation...
INFO    -  Documentation built in 0.22 seconds
INFO    -  Serving on http://127.0.0.1:8000/
```

Open <http://127.0.0.1:8000/> in your browser. The dev-server supports auto-reloading and rebuilds whenever the configuration file, documentation directory, or theme directory changes.

Add pages, configure navigation in `mkdocs.yml`:

```yaml
site_name: MkLorum
nav:
  - Home: index.md
  - About: about.md
```

Change the theme:

```yaml
theme: readthedocs
```

Build the static site:

```bash
mkdocs build
```

This creates a `site` directory containing the generated HTML, assets, a `sitemap.xml`, and `mkdocs/search_index.json`. Deploy the contents of that directory anywhere static files can be served, or use the built-in GitHub Pages deployment:

```bash
mkdocs gh-deploy
```

## CLI Commands

Run `mkdocs --help` for a complete list of commands, and `mkdocs <command> --help` for options of a specific command. Available commands:

| Command | Description |
| --- | --- |
| `mkdocs new [dir]` | Create a new MkDocs project. |
| `mkdocs serve` | Run the built-in development server with live reloading. Supports `-a <IP:PORT>`, `-o/--open`, `--dirty`, `-c/--clean`, `--watch`, `--watch-theme`, `--no-livereload`. |
| `mkdocs build` | Build the documentation. Supports `-c/--clean/--dirty`, `-d <site_dir>`, `-s/--strict`, `-t <theme>`, `-f <config-file>`. |
| `mkdocs gh-deploy` | Deploy documentation to GitHub Pages. Supports `-m`, `-b <remote-branch>`, `-r <remote-name>`, `--force`, `--no-history`, `--ignore-version`. |
| `mkdocs get-deps` | Show required PyPI packages inferred from plugins in `mkdocs.yml`. Can be combined with pip: `pip install $(mkdocs get-deps)`. |

Global options include `-v/--verbose`, `-q/--quiet`, and `--color/--no-color`.

## Configuration

The project is configured by default using a YAML file named `mkdocs.yml` in the project directory. The only required setting is `site_name`; everything else is optional. Key settings include:

- `site_name` — required main title of the documentation.
- `site_url`, `repo_url`, `repo_name`, `edit_uri`, `edit_uri_template` — URLs and edit links.
- `nav` — global navigation layout (defaults to a sorted list of all Markdown files).
- `theme` — theme name and theme-specific options (`locale`, `custom_dir`, `static_templates`, etc.).
- `docs_dir` (default `docs`) and `site_dir` (default `site`) — source and output directories.
- `exclude_docs`, `draft_docs`, `not_in_nav` — gitignore-style pattern lists controlling which files are built or shown in the nav.
- `validation` — configure the strictness of link/anchor validation messages.
- `markdown_extensions` — enable and configure Python-Markdown extensions.
- `plugins` — plugins to use when building (the `search` plugin is enabled by default); supports an `enabled` option per plugin.
- `hooks` — plugin-like event handlers loaded from local Python files.
- `extra_css`, `extra_javascript`, `extra_templates`, `extra` — additional assets and template context.
- `use_directory_urls`, `strict`, `dev_addr`, `watch` — preview and build behavior.
- `INHERIT` — deep-merge a parent configuration file for multi-site setups.

Special YAML tags are supported, including `!ENV` to read values from environment variables and `!relative` to express paths relative to the current Markdown file, `docs_dir`, or the config directory.

## Built-in Themes

Two themes ship with MkDocs:

- **mkdocs** — the default, a custom Bootstrap theme. Supports options such as `color_mode` (light/dark/auto), `user_color_mode_toggle`, `nav_style`, `highlightjs`, `hljs_style`, `hljs_languages`, `analytics.gtag`, `shortcuts`, `navigation_depth`, and `locale`.
- **readthedocs** — a clone of the Read the Docs theme. Supports `highlightjs`, `hljs_languages`, `analytics`, `include_homepage_in_sidebar`, `prev_next_buttons_location`, `navigation_depth`, `collapse_navigation`, `titles_only`, `sticky_navigation`, `locale`, and `logo`.

Both built-in themes support localization. To use a locale:

```bash
pip install 'mkdocs[i18n]'
```

```yaml
theme:
  name: mkdocs
  locale: fr
```

Theme localization only translates text within the theme's templates (such as "next"/"previous" links), not the documentation content itself.

## Search

MkDocs ships with a `search` plugin based on [lunr.js], enabled by default. It supports options including `separator`, `min_search_length`, `lang` (with support for many languages via Lunr Languages), `prebuild_index` (requires Node.js), and `indexing` (`full`, `sections`, `titles`).

## Extending MkDocs

- **Plugins** — subclass `mkdocs.plugins.BasePlugin`, register an `mkdocs.plugins` entry point, and handle events such as `on_config`, `on_files`, `on_nav`, `on_page_markdown`, `on_post_build`, and more. Event handlers can be assigned priorities, and MkDocs provides typed configuration schemas, `get_plugin_logger()`, and error classes such as `PluginError`.
- **Themes** — a theme needs at minimum a `main.html` Jinja2 template and, for packaged themes, an `mkdocs_theme.yml` config file and an `mkdocs.themes` entry point. Templates have access to variables such as `config`, `nav`, `page`, and `base_url`, plus custom filters like `url`, `tojson`, and `script_tag`.
- **API Reference** — documentation for `Files`, `File`, `Config`, `TemplateContext`, and `LiveReloadServer` is available in the developer guide.

See the [Developer Guide](https://www.mkdocs.org/dev-guide/) for full details on themes, translations, plugins, and the API.

## Development

The main development tool is [Hatch], which manages dependencies and acts as the command runner. Install it (ideally with `pipx install hatch`), then from a clone of this repository:

```bash
hatch run all          # Run all checks required for MkDocs
```

Individual checks:

```bash
hatch run test:test              # Unit test suite
hatch run integration:test       # Integration tests
hatch run style:fix              # Auto-format (Black, isort) and lint (Ruff)
hatch run types:check            # Type-check with mypy
hatch run lint:check             # Spelling (codespell), markdownlint, jshint, CSS checks
hatch run docs:serve             # Preview MkDocs' own docs locally
```

The unit test suite runs via `python -m unittest discover -s mkdocs -p "*tests.py"` across a matrix of Python versions (3.8–3.12 and PyPy) and dependency modes (default and minimum requirements), with coverage reporting. Integration tests cover various project configurations including complicated configs, sub-pages, and unicode file names.

A local development install is also possible with `pip install --editable .`.

### Translating Themes

Contributions of theme translations are welcome. The workflow uses [Babel]'s `pybabel` commands (`init_catalog`, `update_catalog`, `compile_catalog`, `extract_messages`) on the `messages.pot`/`messages.po` files under `mkdocs/themes/<theme>/locales/`. See the [Translation Guide](https://www.mkdocs.org/dev-guide/translations/) and the [Contributing Guide](https://www.mkdocs.org/about/contributing/) for details.

## Contributing

Contributions are welcome in many forms: code patches via pull requests, documentation improvements, bug reports, and patch reviews. When reporting an issue, please include your platform, MkDocs version, a minimal reproducible `mkdocs.yml`, what you expected, and what happened instead. For large changes, please open an issue first to get early feedback. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

Everyone interacting in the MkDocs project's codebases, issue trackers, chat rooms, and mailing lists is expected to follow the [PyPA Code of Conduct].

## Links

- Documentation: <https://www.mkdocs.org/>
- Source: <https://github.com/mkdocs/mkdocs>
- Issues: <https://github.com/mkdocs/mkdocs/issues>
- Release notes: <https://www.mkdocs.org/about/release-notes/>
- Plugin/theme catalog: <https://github.com/mkdocs/catalog>

## License

Copyright © 2014-present, Tom Christie. All rights reserved.

MkDocs is distributed under the terms of the **BSD 2-Clause License**. Redistribution and use in source and binary forms, with or without modification, are permitted provided that the copyright notice and disclaimer are retained. See [LICENSE](LICENSE) for the full text.

The ReadTheDocs theme is used under license from the ReadTheDocs projects — see [docs/about/license.md](docs/about/license.md) for details.

[Hatch]: https://hatch.pypa.io/
[Babel]: https://babel.pocoo.org/
[lunr.js]: https://lunrjs.com/
[PyPA Code of Conduct]: https://www.pypa.io/en/latest/code-of-conduct/
