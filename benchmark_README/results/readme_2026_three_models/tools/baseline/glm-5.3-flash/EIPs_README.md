# Ethereum Improvement Proposals (EIPs)

This repository hosts the **Ethereum Improvement Proposals (EIPs)** — the canonical collection of specification documents that describe proposed standards and protocol changes for Ethereum. EIPs cover everything from core protocol changes (consensus rules, gas costs, new opcodes) to application-level standards (token interfaces like ERC-20 and ERC-721, wallet and RPC conventions) and networking or process proposals.

The rendered, browsable version of these proposals is published at **eips.ethereum.org** (the `CNAME` file in this repository configures that custom domain). Each proposal lives as a standalone Markdown file in the `EIPS/` directory, named using the pattern `eip-<number>.md` — for example, `EIPS/eip-20.md` (the ERC-20 token standard), `EIPS/eip-155.md`, `EIPS/eip-4844.md`, and so on.

## What is an EIP?

An EIP (Ethereum Improvement Proposal) is a design document providing information to the Ethereum community, or describing a new feature for Ethereum or its processes or environment. Proposals move through a lifecycle of statuses such as **Draft**, **Review**, **Last Call**, **Final**, **Stagnant**, **Withdrawn**, and **Living**. Categories include:

- **Standards Track – Core**: consensus-fork changes to the protocol (e.g., `eip-1559.md`, fee market changes; `eip-4844.md`, blob transactions; `eip-1153.md`, transient storage opcodes).
- **Standards Track – Networking**: network protocol improvements.
- **Standards Track – Interface**: API/RPC and client interface standards (e.g., `eip-1193.md`, the JavaScript provider API; `eip-1102.md`, opt-in account exposure).
- **ERC (Ethereum Request for Comments)**: application-level standards such as `eip-20.md` (fungible tokens) and `eip-721.md` (non-fungible tokens).

Some proposals that were reclassified as ERCs remain in this repository as stub files with `status: Moved`, pointing to the dedicated ERCS repository (e.g., `eip-1077.md`, `eip-1102.md` style stubs).

## Repository structure

```
.
├── EIPS/                     # All EIP documents (eip-<number>.md)
│   ├── eip-1.md              # EIP process document / index of proposals
│   └── eip-<number>.md       # Individual proposals
├── assets/                   # Images referenced from EIP documents
├── .github/
│   ├── CONTRIBUTING.md       # Contribution guidelines
│   ├── CODEOWNERS            # Code ownership rules
│   ├── ISSUE_TEMPLATE/       # Issue templates (bug reports, process changes)
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── ISSUE_TEMPLATE.md
│   ├── renovate.json         # Automated dependency updates
│   └── workflows/            # CI and automation workflows
├── CNAME                     # Custom domain (eips.ethereum.org)
├── 404.html                  # Custom 404 page for the site
└── ...
```

## How EIPs are formatted

Each EIP is a Markdown file with a YAML front matter header followed by the proposal body. A typical header looks like:

```yaml
---
eip: 1108
title: Reduce alt_bn128 precompile gas costs
author: Author Name (@github-handle)
discussions-to: <forum or issue URL>
status: Final
type: Standards Track
category: Core
created: 2018-05-21
requires: 196, 197
---
```

Key front matter fields:

| Field          | Description                                                        |
| -------------- | ------------------------------------------------------------------ |
| `eip`          | The EIP number (assigned via the EIP process)                      |
| `title`        | Human-readable title of the proposal                               |
| `author`       | Author name(s) and GitHub handles                                  |
| `discussions-to` | Where discussion happens (typically Ethereum Magicians)          |
| `status`       | Current lifecycle status (Draft, Review, Final, Stagnant, …)       |
| `type`         | Standards Track, Meta, or Informational                            |
| `category`     | Core, Networking, or Interface (for Standards Track)               |
| `created`      | Date the proposal was first submitted                              |
| `requires`     | EIP numbers this proposal depends on                               |

The body of an EIP conventionally includes sections such as **Abstract**, **Motivation**, **Specification**, **Rationale**, **Backwards Compatibility**, **Test Cases**, **Implementations**, and **Copyright**. See `EIPS/eip-1.md` for the authoritative description of the EIP process, required sections, and formatting rules.

## Contributing an EIP

Before opening a pull request, please read [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md). The general workflow is:

1. **Discuss the idea first.** Post your proposal to the Ethereum Magicians forum (or another appropriate venue) and link it in your EIP's `discussions-to` field. EIPs are expected to have prior community discussion before being merged as drafts.
2. **Create the proposal file.** Add a new file `EIPS/eip-<number>.md` following the front matter format described above. Use the `discussions-to` field to link your forum thread. If your proposal builds on other EIPs, list them in the `requires` field.
3. **Reference assets correctly.** Place images in the `assets/` directory and reference them relative to your EIP file (e.g., `../assets/eip-107/authorization.png`).
4. **Open a pull request.** Follow the pull request template. Continuous integration will validate your document (see [Testing](#testing) below). An auto-review bot and code owners will shepherd your PR through review.
5. **Maintain the proposal.** As community consensus forms, editors will advance your EIP's status. Proposals that go inactive for a long period may be marked **Stagnant** by automation.

Authors submitting ERC-type proposals should be aware that some ERCs have been split out into a separate repository; files with `status: Moved` in this repository redirect readers there.

If you spot a typo, broken link, or formatting problem in an existing EIP, editorial pull requests are welcome. Substantive technical changes should go through the proposal's `discussions-to` channel.

## Issues

Use the repository's issue templates:

- **Bug report** — for problems with the site build, broken EIP documents, or repository tooling.
- **Propose process change** — for suggested changes to the EIP process itself.

Technical debate about a specific EIP should happen in its `discussions-to` thread, not in this repository's issues.

## Setup

This site is built with **Jekyll** and published via GitHub Pages (see the `jekyll.yml` workflow). To build and preview the site locally:

1. Install Ruby and Bundler.
2. Clone this repository:

   ```sh
   git clone https://github.com/ethereum/EIPs.git
   cd EIPs
   ```

3. Install dependencies and serve:

   ```sh
   bundle install
   bundle exec jekyll serve
   ```

4. Open `http://localhost:4000` in your browser to browse the rendered EIPs.

Because the `CNAME` file is present, GitHub Pages serves the site at `eips.ethereum.org` in production; locally you use `localhost`.

## Configuration

- **Jekyll**: The site is rendered by Jekyll; EIP Markdown files in `EIPS/` are processed into HTML pages. The custom `404.html` handles not-found pages.
- **Renovate**: `.github/renovate.json` keeps build dependencies up to date automatically via pull requests.
- **CODEOWNERS**: `.github/CODEOWNERS` defines who must review changes to particular paths (notably EIP editors for proposal files).
- **Domain**: `CNAME` pins the GitHub Pages deployment to the `eips.ethereum.org` domain.

## Development and automation

The `.github/workflows/` directory contains several GitHub Actions workflows that keep the repository healthy:

| Workflow                  | Purpose                                                              |
| ------------------------- | -------------------------------------------------------------------- |
| `ci.yml`                  | Runs checks on pull requests and pushes (including EIP validation)   |
| `jekyll.yml`              | Builds the Jekyll site for GitHub Pages deployment                   |
| `post-ci.yml`             | Post-CI tasks, such as reporting results on pull requests            |
| `auto-review-bot.yml` / `auto-review-trigger.yml` | Automates reviewer assignment and review tracking |
| `auto-stagnate-bot.yml`   | Marks proposals as Stagnant after prolonged inactivity               |
| `stale.yml`               | Marks stale issues and pull requests                                 |
| `jekyll-label-bot.yml`    | Applies labels related to site builds                                |

When contributing, expect CI to run on your pull request. Ensure your new or modified EIP file passes validation (correct front matter, valid status/category/type values, and required sections) before requesting review.

## Testing

Testing this repository consists of two things:

1. **Continuous integration.** The `ci.yml` workflow validates proposed changes — checking document structure, front matter fields, and formatting consistency across EIP files. A green CI run is required before merge. The `post-ci.yml` workflow surfaces results back onto pull requests.
2. **Local site build.** Before submitting, build the site locally with Jekyll (`bundle exec jekyll serve`) and confirm your proposal renders correctly, including any images under `assets/` and any internal links to other EIP files (which should be relative links like `[EIP-1108](./eip-1108.md)`).

There is no application code to unit test; the "source of truth" is the Markdown documents themselves, and correctness means passing the EIP validation checks and rendering properly.

## License

All EIP documents in this repository are **open-source**. Each proposal carries a copyright notice — the standard text states:

> Copyright and related rights waived via [CC0](../LICENSE.md).

Refer to the repository's `LICENSE.md` for the full license terms. Contributions are licensed under the same terms, so content in this repository may be freely reused, modified, and redistributed.

## Additional resources

- **EIP-1** (`EIPS/eip-1.md`) — the meta-document describing the EIP purpose, process, categories, statuses, and editor responsibilities. Read this first if you intend to author a proposal.
- **Ethereum Magicians** — the community forum where most `discussions-to` links point; the primary venue for proposal debate.
- **eips.ethereum.org** — the rendered site built from this repository, the best place to read proposals in their final formatted form.
