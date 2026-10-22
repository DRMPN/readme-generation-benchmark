# Ethereum Improvement Proposals (EIPs)

This repository hosts the **Ethereum Improvement Proposals (EIPs)** — the official specifications that describe standards for the Ethereum platform, including core protocol changes, networking protocols, client APIs, and application-level contract standards (ERCs). The repository contains both the proposal documents themselves and the Jekyll-based static site that renders and publishes them to **[eips.ethereum.org](https://eips.ethereum.org)**.

EIPs stand for *Ethereum Improvement Proposals* and are modeled after Bitcoin's BIPs and Python's PEPs. Each proposal is a design document providing information to the Ethereum community, describing a new feature, its processes, or its environment.

---

## Table of Contents

- [What is an EIP?](#what-is-an-eip)
- [EIP Types](#eip-types)
- [EIP Workflow & Statuses](#eip-workflow--statuses)
- [Repository Structure](#repository-structure)
- [Contributing an EIP](#contributing-an-eip)
- [Required Preamble Headers](#required-preamble-headers)
- [Local Development](#local-development)
- [Linting & Validation](#linting--validation)
- [Utility Scripts & Reference Code](#utility-scripts--reference-code)
- [Automation & CI](#automation--ci)
- [RSS Feeds](#rss-feeds)
- [EIP Editors](#eip-editors)
- [Citation Format](#citation-format)
- [License](#license)
- [Additional Resources](#additional-resources)

---

## What is an EIP?

An EIP is a design document that:

1. Describes a proposed standard or protocol change for Ethereum,
2. Provides a precise technical specification of the feature,
3. Captures community consensus around the proposal.

The EIP process — including who may author proposals, how they are reviewed, and what statuses they move through — is itself defined in **[EIP-1](eip-1.md)** (*EIP Purpose and Guidelines*), which is the canonical reference for everything in this repository.

Two common examples of well-known EIPs hosted here:

| EIP | Title | Type |
|-----|-------|------|
| [EIP-20](eip-20.md) | Token Standard | ERC |
| [EIP-721](eip-721.md) | Non-Fungible Token Standard | ERC |
| [EIP-1155](eip-1155.md) | Multi Token Standard | ERC |
| [EIP-155](eip-155.md) | Simple replay attack protection | Core |
| [EIP-1559](eip-1559.md) | Fee market change | Core |
| [EIP-4844](eip-4844.md) | Shard Blob Transactions | Core |
| [EIP-4361](eip-4361.md) | Sign-In with Ethereum | ERC |

---

## EIP Types

Every EIP has a **type**, declared in its preamble:

| Type | Sub-types | Description |
|------|-----------|-------------|
| **Standards Track** | `Core` | Consensus forks, EVM changes, block/transaction validity rules |
| | `Networking` | devp2p, network protocol specifications |
| | `Interface` | Client API/RPC specifications and language-level standards |
| | `ERC` | Application-level conventions and standards (tokens, name registries, wallet behavior, etc.) |
| **Meta** | — | Proposals about the process surrounding Ethereum or EIPs themselves |
| **Informational** | — | General guidelines or information; does **not** propose a new feature and does not represent community consensus |

---

## EIP Workflow & Statuses

An EIP moves through the following lifecycle:

```text
                   ┌─────────────┐
        Idea ────▶ │    Draft    │
                   └──────┬──────┘
                          │
                   ┌──────▼──────┐
                   │   Review    │◀────┐
                   └──────┬──────┘     │ (revisions)
                          │            │
                   ┌──────▼──────┐     │
                   │  Last Call  │─────┘
                   └──────┬──────┘
                          │
                   ┌──────▼──────┐
                   │    Final    │
                   └─────────────┘

    Any non-final status may become ─▶ Stagnant (inactive > 6 months)
    An author may retire a proposal  ─▶ Withdrawn
    Continuously updated documents   ─▶ Living
```

| Status | Meaning |
|--------|---------|
| **Idea** | An idea pre-approved for drafting (tracked outside this repo) |
| **Draft** | The proposal is being iterated on and is open for discussion |
| **Review** | The proposal is formally being reviewed by the community |
| **Last Call** | The proposal is considered final and ready; a minimum review window (typically 14 days) applies before promotion |
| **Final** | The standard is accepted and finalized |
| **Stagnant** | The proposal has had no activity for 6+ months and may be resurrected by authors or editors |
| **Withdrawn** | The proposal has been withdrawn by the author(s) |
| **Living** | A continually updated EIP (e.g., EIP-1 itself) |

Category/status listing pages in this repository are rendered per type and status: [`core.html`](core.html), [`erc.html`](erc.html), [`interface.html`](interface.html), [`networking.html`](networking.html), [`informational.html`](informational.html), [`meta.html`](meta.html), and [`all.html`](all.html).

---

## Repository Structure

```text
.
├── eip-1.md                     # The EIP process specification (start here!)
├── eip-<number>.md              # One markdown file per proposal (e.g. eip-20.md, eip-721.md, ...)
├── eip-template.md              # Template used when drafting a new proposal
│
├── _config.yml                  # Jekyll site configuration
├── Gemfile / Gemfile.lock       # Ruby dependencies for the static site
├── CNAME                        # Custom domain (eips.ethereum.org)
├── index.html                   # Landing page
├── 404.html                     # Not-found page
│
├── eip.html / erc.html          # Jekyll layouts that render individual proposals
├── core.html / erc.html / interface.html /
│   networking.html / informational.html / meta.html /
│   all.html                     # Category & status listing pages
├── statuses.yaml                # Status metadata for the listing pages
│
├── head.html / header.html / social.html /
│   toc.html / anchor_headings.html /
│   eiptable.html / eipnums.html / authorlist.html   # Jekyll includes (site chrome,
│                                                     # auto-generated tables, author lists)
│
├── style.scss / override.css    # Site styling
│
├── eip-editors.yml              # Current roster of EIP editors
├── eipw.toml                    # eipw (EIP-Watch) linter configuration
├── mlc_config.json              # markdown-link-check configuration
│
├── all.xml / erc.xml / nonerc.xml /
│   last-call.xml / erc-last-call.xml /
│   nonerc-last-call.xml         # RSS feeds (all / ERC / non-ERC / Last Call variants)
│
├── LICENSE.md                   # Repository licensing information
├── README.md                    # This file
│
└── (assets)                     # Images, diagrams, PDFs, datasets, reference code and
                                 # test vectors referenced by individual EIPs
```

### Notable asset groups

Assets accompanying specific proposals include, for example:

- **EIP-1155 reference implementation** — `IERC1155.sol`, `ERC1155.sol`, `ERC1155TokenReceiver.sol`, `ERC1155WithTotals.sol`, plus example dapp contracts (`BidOnAddresses.sol`, `Salary.sol`, ...).
- **EIP-4881 deposit snapshot tooling** — `eip_4881.py`, `deposit_snapshot.py`, `test_deposit_snapshot.py`, `deposit_tree_evolution.svg`.
- **EIP-2537 (BLS12-381) test vectors** — `add_G1_bls.json`, `mul_G2_bls.json`, `pairing_check_bls.json`, `msm_G1_bls.json`, `map_fp2_to_G2_bls.json` and the corresponding `fail-*.json` negative-test suites, plus supporting research PDFs.
- **EIP-1559 fee-market analysis** — `base_fee_1.png`, `base_fee_225.png`, `fee_analysis.md`, gas cost estimation reports.
- **EIP-7702 / account-abstraction material** — `auth-msg.png`, `auth-msg-multi-call.png`, delegation diagrams.
- **General research papers** — arXiv and IACR eprints underpinning various consensus-layer proposals.

---

## Contributing an EIP

> **Read [EIP-1](eip-1.md) first.** It defines the entire process described below.

### Before you write

1. **Discuss your idea first.** Ideas should be vetted publicly — e.g., on the [Ethereum Magicians forum](https://ethereum-magicians.org/) or the relevant fellowship/core-dev call — *before* a pull request is opened. A well-socialized idea is far more likely to advance.
2. **Check for prior work.** Search the repository and closed issues/PRs; your idea may already exist as a Draft, Final EIP, or Withdrawn proposal.
3. **Choose the right type & category.** Core changes to the protocol go through the AllCoreDevs process; application standards (ERCs) go through the ERC review process.

### Submitting

1. **Fork** this repository and create a branch.
2. **Copy** [`eip-template.md`](eip-template.md) to `eip-XXXX.md` (a free number will be confirmed/assigned by the editors).
3. **Complete the preamble** (see [Required Preamble Headers](#required-preamble-headers)).
4. **Write the specification.** Be precise, self-contained, and complete — the *Specification* section must be implementable without reference to external material.
5. **Validate locally** (see [Linting & Validation](#linting--validation)) and build the site.
6. **Open a pull request** containing exactly one proposal (one EIP per PR). Editors will check formatting, move it to `Draft`/`Review` as appropriate, and merge. **Merging does not equal acceptance** — it merely starts the formal process.

### Ground rules

- ✅ High-quality, technically rigorous, community-reviewed documents.
- ❌ Plagiarism, unsolicited self-promotion, or proposals without prior public discussion.
- An EIP must be **atomic**: one proposal per EIP; small, focused changes fare best.
- Editors may move stale proposals to **Stagnant** and can be petitioned to revive them.

---

## Required Preamble Headers

Each `eip-XXXX.md` begins with a YAML front-matter block. The key fields:

```yaml
---
eip: 1234
title: A short title (max 44 characters)
description: One-or-two sentence summary
author: Name <email>, Name2 <email2>
discussions-to: https://ethereum-magicians.org/t/topic/1234
status: Draft
type: Standards Track
category: ERC            # Core | Networking | Interface | ERC (Standards Track only)
created: 2024-01-31
requires: 155            # optional, EIPs this depends on
license: CC0-1.0         # see eip-1 for allowed licenses
---
```

Full details, including `layer` (consensus proposals), `withdrawal-reason`, and license rules, are specified in [EIP-1](eip-1.md).

---

## Local Development

The published site is built with **Jekyll**.

### Prerequisites

- **Ruby** (≥ 2.7) and **Bundler**
- **Python 3.x** for the utility scripts (optional)
- **Go** for the Go-based reference utilities (optional)
- [`eipw`](https://github.com/ethereum/eipw) for linting proposals (optional but recommended)

### Building the site

```bash
# Install Ruby dependencies
bundle install

# Serve the site locally with live reload
bundle exec jekyll serve --incremental

# Site will be available at http://localhost:4000
```

The listing pages (e.g., `core.html`, `erc.html`) are generated from the EIP front-matter, using the includes in `eiptable.html`, `eipnums.html`, and `authorlist.html`.

---

## Linting & Validation

Two automated validators guard proposal quality:

### eipw (EIP-Watch)

The primary linter for EIP documents. Behavior is configured in [`eipw.toml`](eipw.toml) — it checks preamble correctness, required sections, markdown structure, and more:

```bash
cargo install eipw        # or download a release binary
eipw lint
```

### Markdown link checker

Internal links are checked using [`mlc_config.json`](mlc_config.json):

```bash
npx markdown-link-check --config mlc_config.json eip-XXXX.md
```

> CI runs both tools on every pull request. Please make sure your proposal passes locally before submitting.

---

## Utility Scripts & Reference Code

The repository also carries reference implementations, scripts, and test data that accompany specific EIPs:

| Language | Examples | Purpose |
|----------|----------|---------|
| **Python** | `eip_4881.py`, `deposit_snapshot.py`, `test_deposit_snapshot.py` | Generate & verify execution-layer deposit tree snapshots (EIP-4881) |
| **Python** | `convert.py`, `convert_tests.py`, `rlp_types.py`, `ssz_types.py`, `transactions.py`, `generate_test_cases.py` | Test-vector generation and serialization tooling |
| **Python** | `optional.py`, `tests.py`, `progressive.py` | Prototype/analysis utilities for various proposals |
| **Go** | `decimal_float.go`, `decimal_float_test.go`, `gasEVMPlusEmulate.go`, `uint256_wrapped.go` | Reference code and EVM cost simulations |
| **Yul** | `BlackScholes.yul`, `Neuron.yul` | Benchmark workloads used in gas-cost studies |
| **Solidity** | `IERC1155.sol` et al., `Extsload.sol`, `BaseSalary.sol` et al. | Reference contracts for ERC/Interface EIPs |
| **JSON** | `*_bls.json`, `test-vectors-*.json`, `precompile.json` | Formal conformance test vectors |

Example usage:

```bash
# Regenerate / verify an EIP-4881 deposit snapshot
python3 eip_4881.py

# Run the accompanying tests
python3 -m unittest test_deposit_snapshot.py
```

---

## Automation & CI

- **eipw** linting runs automatically on proposals in pull requests, posting results inline.
- A merge bot (EIP-Bot) labels, comments on, and tracks the state of proposal PRs.
- The markdown link checker validates that referenced resources exist.
- On merge to `master`, the site is rebuilt and published to **eips.ethereum.org**, and the RSS feeds are regenerated.

---

## RSS Feeds

Subscribe to proposal activity via the generated feeds:

| Feed | Contents |
|------|----------|
| [`all.xml`](all.xml) | All EIPs |
| [`erc.xml`](erc.xml) | ERCs only |
| [`nonerc.xml`](nonerc.xml) | Non-ERC (Core/Networking/Interface/Meta/Informational) |
| [`last-call.xml`](last-call.xml) | All proposals in Last Call |
| [`erc-last-call.xml`](erc-last-call.xml) | ERCs in Last Call |
| [`nonerc-last-call.xml`](nonerc-last-call.xml) | Non-ERCs in Last Call |

---

## EIP Editors

The current list of EIP editors is maintained in [`eip-editors.yml`](eip-editors.yml). Editors are responsible for:

- Checking formatting and process compliance,
- Assigning EIP numbers and merging proposal PRs,
- Guiding proposals through status transitions (but *not* judging technical merit — that is the community's and reviewers' job).

To reach the editors, open an issue on this repository or post on the Ethereum Magicians forum.

---

## Citation Format

When referencing a proposal, cite it in this style:

```text
EIP-20: Token Standard. V. Buterin, F. Vogelsteller.
Status: Final. Type: Standards Track. Created: 2015-11-19.
https://eips.ethereum.org/EIPS/eip-20
```

---

## License

Licensing for this repository is described in [`LICENSE.md`](LICENSE.md). Each individual EIP declares its own license in its preamble (commonly **CC0-1.0** or **Apache-2.0**, per the rules in [EIP-1](eip-1.md)). By contributing, you agree that your contributions are licensed accordingly.

---

## Additional Resources

- 📖 [EIP-1 — EIP Purpose and Guidelines](eip-1.md)
- 🌐 [eips.ethereum.org](https://eips.ethereum.org) — the rendered, canonical site
- 💬 [Ethereum Magicians](https://ethereum-magicians.org/) — community discussion forum
- 🔧 [eipw — the EIP linter](https://github.com/ethereum/eipw)
- 🗳️ [Ethereum Cat Herders](https://ethereumcatherders.com/) — process support for EIPs and network upgrades

> **TL;DR:** Read [EIP-1](eip-1.md), discuss your idea publicly, copy the template, fill in the preamble, validate with `eipw`, and open a pull request with exactly one proposal. 🚀
