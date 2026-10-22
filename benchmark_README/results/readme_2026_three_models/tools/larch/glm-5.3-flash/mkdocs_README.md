# mkdocs-pn1vdzt5

![MkDocs Logo](docs/img/screenshot.png)

**MkDocs** is a fast, simple and downright gorgeous static site generator that's geared towards building project documentation. Documentation source files are written in Markdown, and configured with a single YAML configuration file.

## Features

- **Great themes** — Comes bundled with two beautiful themes (`readthedocs` and `mkdocs`), with support for light and dark color modes, localization, and extensive customization options.
- **Live preview** — The built-in dev server (`mkdocs serve`) with LiveReload reloads your documentation as you save changes.
- **Easy deployment** — One-command deployment to GitHub Pages (`mkdocs gh-deploy`) or any static hosting service.
- **Markdown everywhere** — Write your docs in Markdown with full support for tables, fenced code blocks, and more.
- **Powerful configuration** — Flexible YAML-based configuration with validation, defaults, and sensible error messages (I18n-ready).
- **Theming & plugin system** — A rich theme engine (template overrides, custom CSS/JS, translations) and a plugin architecture with a comprehensive plugin event system.
- **Search** — Built-in client-side search powered by Lunr.js, with support for many languages (Japanese, Chinese, Thai, Hindi, Arabic, European languages, etc.), pre-built indexes, and web workers for performance.
- **PyPI integration** — Standard packaging via `pyproject.toml` and Hatch build hooks, fully typed (`py.typed`).

## Project Structure

```
├── mkdocs/                  # Main package
│   ├── cli.py / __main__.py # Command-line interface
│   ├── commands/            # build, serve, new, gh-deploy, etc.
│   ├── config/              # Configuration loading, defaults, options
│   ├── structure/           # Files, pages, nav handling
│   ├── rendering/           # Markdown/HTML rendering, templates
│   ├── themes/              # Bundled themes (mkdocs, readthedocs)
│   ├── utils/               # YAML, caching, filters, babel helpers
│   └── localization/        # Translations (many locales via gettext)
├── mkdocs/commands/         # CLI command implementations
├── mkdocs/tests/            # Comprehensive test suite
├── docs/                    # Documentation source & theme assets
└── pyproject.toml           # Package metadata & build config
```

## Getting Started

### Installation

```bash
pip install mkdocs
```

Or with optional styling dependencies:

```bash
pip install mkdocs -r requirements-style.txt
```

### Creating a New Project

```bash
mkdocs new my-project
cd my-project
```

This creates a minimal project with a `mkdocs.yml` configuration file and a `docs/` directory containing an `index.md`.

### Previewing Your Docs

```bash
mkdocs serve
```

Starts a development server at `http://127.0.0.1:8000` with auto-reload.

### Building Your Site

```bash
mkdocs build
```

Generates a static site in the `site/` directory.

### Deploying to GitHub Pages

```bash
mkdocs gh-deploy
```

## CLI Commands

| Command | Description |
|---|---|
| `mkdocs new` | Create a new MkDocs project |
| `mkdocs serve` | Start the live-reloading dev server |
| `mkdocs build` | Build the documentation site |
| `mkdocs gh-deploy` | Deploy to GitHub Pages |

## Writing Your Documentation

Documentation pages are plain Markdown files placed in your project's `docs/` directory. Navigation is defined in `mkdocs.yml`:

```yaml
site_name: My Project
nav:
  - Home: index.md
  - User Guide: usage.md
  - API Reference: api.md
```

## Themes

MkDocs ships with two themes:

- **`mkdocs`** — the default theme with light/dark color modes, responsive layout, and search.
- **`readthedocs`** — a three-column layout modeled after the Read the Docs look.

Custom themes can be created by extending an existing theme or writing a new one, with support for custom templates, CSS, JavaScript, and translations (`l10n`).

## Plugins

Extend MkDocs behavior with plugins that hook into build events (page rendering, navigation, template context, etc.). See `docs/user-guide/plugins.md` for the full plugin event list and API.

## Development

### Running the Tests

```bash
pip install -r requirements-docs.txt
python -m pytest mkdocs/tests
```

Or run the full integration suite:

```bash
python mkdocs/tests/integration.py
```

### Contributing

Contributions are welcome! Please read `CONTRIBUTING.md` for guidelines. Translation contributions use GNU gettext — the `.po`/`.pot` message catalogs are in the theme directories (`babel.cfg` defines extraction rules).

## Documentation

Full documentation is included in this repository under `docs/`:

- Getting Started
- Writing Your Docs
- Choosing & Customizing Your Theme
- Localizing Your Theme
- Deploying Your Docs
- Configuration Reference
- CLI Reference
- Theme & Plugin Developer APIs

## License

MIT — see [LICENSE](LICENSE).
