# Ethereum Improvement Proposals (EIPs)

This repository contains the source for [eips.ethereum.org](https://eips.ethereum.org) and the canonical collection of **Ethereum Improvement Proposals (EIPs)**. EIPs describe standards for the Ethereum platform, including core protocol specifications, client APIs, and contract standards. They are the primary mechanism for proposing new features, collecting community technical input, and documenting design decisions that have gone into Ethereum.

Network upgrades are discussed separately in the [Ethereum Project Management](https://github.com/ethereum/pm) repository.

## Repository layout

| Path | Contents |
| --- | --- |
| `EIPS/` | One Markdown file per EIP (e.g. `eip-1.md`), each with a YAML front-matter preamble |
| `assets/` | Per-EIP asset folders (e.g. `assets/eip-1/`) used for images, test data, and other supporting files |
| `eip-template.md` | The suggested template for new EIPs |
| `_config.yml`, `_layouts/`, `_includes/`, `_data/` | [Jekyll](https://jekyllrb.com/) site configuration and templates |
| `index.html`, `core.html`, `erc.html`, … | Jekyll-generated index pages for each EIP type and category |
| `rss/` | Jekyll-generated RSS feeds (all EIPs, Last Call, non-ERC, and ERC variants) |
| `config/` | CI tool configuration: `eipw.toml` (EIP Walidator), `eip-editors.yml`, `.markdownlint.yaml`, `.codespell-whitelist`, `.jekyll-labels.yml`, `mlc_config.json` |
| `.github/` | GitHub Actions workflows, issue/PR templates, and `CONTRIBUTING.md` |
| `LICENSE.md` | [CC0 1.0 Universal](LICENSE.md) — all EIPs are placed in the public domain |

The published site combines this repository with the [ethereum/ercs](https://github.com/ethereum/ercs) repository (see [Building the site](#building-the-site)).

## Reading EIPs

The rendered proposals are available at [eips.ethereum.org](https://eips.ethereum.org), organized by type and category. RSS feeds (all EIPs, Last Call, non-ERC, and ERC variants) and an email alert subscription are linked from the homepage.

Every EIP has a **type** and, during its life cycle, a **status**:

- **Types** — Standards Track (subdivided into **Core**, **Networking**, **Interface**, and **ERC**), **Meta** (processes and guidelines), and **Informational** (general guidelines; not consensus recommendations).
- **Statuses** — `Draft`, `Review`, `Last Call`, `Final`, `Stagnant`, `Withdrawn`, and `Living` (continually updated proposals such as EIP-1). Ideas that have not yet been drafted are not tracked in this repository.

The authoritative description of this process is [EIP-1](EIPS/eip-1.md).

## Contributing a new EIP

1. **Vet the idea.** Discuss it on the [Ethereum Magicians forum](https://ethereum-magicians.org/) before writing a formal proposal, to avoid duplicating prior work and to gauge community interest.
2. **Review [EIP-1](EIPS/eip-1.md).** It defines the required format, style rules, and process.
3. **Write the EIP.** Copy [`eip-template.md`](eip-template.md), fill in the preamble fields, and complete the required sections.
4. **Submit a pull request** to this repository. An EIP editor assigns the EIP number; drafts are initially named `eip-draft_title_abbrev.md`.

A bot automatically merges pull requests that meet all of the following criteria (see the [PR template](.github/PULL_REQUEST_TEMPLATE.md)):

- The PR edits only existing draft PRs.
- The build passes.
- Your GitHub username or email address is listed in the `author` preamble header of every affected proposal, inside triangular brackets (`< >`). If matching on email, it must be the address publicly listed on your GitHub profile.

> **ERC-related pull requests** (application-level standards such as token standards) belong in the [ethereum/ercs](https://github.com/ethereum/ercs) repository, not here.

### EIP format

Each EIP is a Markdown file beginning with an RFC 822-style front-matter preamble. Headers must appear in the order: `eip`, `title`, `description`, `author`, `discussions-to`, `status`, `last-call-deadline`, `type`, `category`, `created`, `requires`, `withdrawal-reason` (optional fields — `last-call-deadline`, `category`, `requires`, and `withdrawal-reason` — are omitted when not applicable). Notable constraints enforced by the linters:

- The `title` is 2–44 characters and must not repeat the EIP number; the `description` is 2–140 characters and must not contain `:`.
- `discussions-to` must be an [Ethereum Magicians](https://ethereum-magicians.org/) thread URL.
- Proposals must be referenced as `EIP-N` or `ERC-N` (never `EIPN` or `EIP N`).
- Sections must appear in the order: Abstract, Motivation, Specification, Rationale, Backwards Compatibility, Test Cases, Reference Implementation, Security Considerations, Copyright. Motivation, Backwards Compatibility, Test Cases, and Reference Implementation may be omitted when not applicable.
- The Copyright section must use the wording: *Copyright and related rights waived via [CC0](LICENSE.md).*

### Minimum content requirements

- **Abstract** — a terse, human-readable technical summary of the specification.
- **Specification** — syntax and semantics detailed enough for interoperable implementations across Ethereum clients.
- **Rationale** — the design decisions behind the specification and the alternatives considered.
- **Security Considerations** — required; proposals missing this section will be rejected, and an EIP cannot reach `Final` without a security discussion deemed sufficient by reviewers.
- **Copyright** — the CC0 waiver described above.

## Building the site

The site is built with Jekyll via the `github-pages` gem (Jekyll 3.9.3 with the Minima theme, kramdown, and Rouge syntax highlighting):

```sh
bundle install
bundle exec jekyll serve
```

Continuous integration uses Ruby 3.1. Note that `.gitattributes` enforces LF line endings on all files, which is required to run the EIP Walidator locally.

In CI, the [ethereum/ercs](https://github.com/ethereum/ercs) repository is merged into a copy of this repository (`erc-*.md` files are renamed to `eip-*.md`), and the combined site is built. This is why ERC pages appear on eips.ethereum.org even though their source lives elsewhere.

## Continuous integration and automation

Pull requests run several checks (defined in `.github/workflows/ci.yml`):

- **EIP Walidator** (`eipw`) — validates preamble fields and section structure using `config/eipw.toml`.
- **HTMLProofer** — builds the merged EIPs + ERCs site and verifies internal links, images, scripts, and Open Graph metadata; also runs the GitHub Pages DNS health check.
- **Link Check** — [markdown-link-check](https://github.com/gaurav-nelson/github-action-markdown-link-check) on modified files, configured via `config/mlc_config.json`.
- **CodeSpell** — spell checking of changed files, with exceptions listed in `config/.codespell-whitelist`.
- **Markdown Linter** — [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) using `config/.markdownlint.yaml`.

When CI fails, the [Post CI workflow](.github/workflows/post-ci.yml) posts a comment on the PR and applies a `w-ci` label, which is removed once CI passes.

Additional automation:

- **Auto Review Bot** — runs [eip-review-bot](https://github.com/ethereum/eip-review-bot) with `config/eip-editors.yml` to request reviews from the relevant editors based on a proposal's category.
- **Auto Stagnant Bot** — runs weekly and moves inactive Draft/Review/Last Call proposals to `Stagnant`.
- **Stale Bot** — marks issues and PRs inactive for 183 days as stale and closes them after 190 days.
- **Jekyll Label Bot** — applies type/status/classification labels to PRs based on front-matter changes (`config/.jekyll-labels.yml`).
- **Renovate** — a Renovate configuration exists at `.github/renovate.json`, but dependency updates are currently disabled (`"enabled": false`).

The current EIP editors are listed in [`config/eip-editors.yml`](config/eip-editors.yml).

## License

All contents of this repository are released under [CC0 1.0 Universal](LICENSE.md) (public domain). Every EIP must include a copyright waiver linking to this license.
