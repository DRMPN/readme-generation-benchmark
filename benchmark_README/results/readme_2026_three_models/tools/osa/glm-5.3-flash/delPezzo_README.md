# delPezzo-2b5uu04x

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Contributing](#contributing)
- [Citation](#citation)

---

## Overview

This project is a Python research library for computational algebraic geometry, focused on (weak) del Pezzo surfaces: it models the Picard lattice, (-1)- and (-2)-curves, subdivisions of the NE cone, and cylinders on surfaces. It is built on top of SageMath and is intended for researchers in algebraic geometry and computational mathematicians studying del Pezzo surfaces, cylinders, and related flexibility questions. Surfaces can be generated from an embedded published classification, and computations are exposed through object-oriented APIs that largely return generator-based results for cone subdivisions and cylinder collections. Newcomers should consult the Getting Started section for setup instructions and runnable examples.

---

## Core Features

- Models generic and weak del Pezzo surfaces of degrees 1–9 in the Picard lattice, including blowup-point dependencies such as collinear triples, infinitely near chains, and points on a conic, so researchers can work with concrete surfaces without manual lattice bookkeeping.
- Enumerates subdivisions of the NE (Mori) cone of a surface, tracking parent faces and subdividing rays, which supports systematic exploration of ample cones and birational contractions.
- Constructs cylinders on (weak) del Pezzo surfaces via several geometric constructions (lines, tangent-and-conic pencils, and their weak variants), recording complement, support, fiber, and transversality data for each cylinder.
- Searches for cone coverings by polar cylinders, enabling automated verification of cylinder (and hence potential fibration) existence on a given surface.
- Generates surfaces and their blowup configurations from an embedded classification of del Pezzo surfaces, letting users reproduce known examples programmatically instead of entering data by hand.

---

## Installation

**Prerequisites:**

- Python 3.10 or newer.
- SageMath — the package depends on it directly: every module imports from `sage.all_cmdline`, so all code must run in a Python environment where SageMath is available.

Install delPezzo-2b5uu04x using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/delPezzo-2b5uu04x
```

2. Install the project in editable mode:

```sh
pip install -e .
```

---

## Getting Started

**Prerequisites**

- Python 3.10 or newer.
- SageMath — the package depends on it directly: every module imports from `sage.all_cmdline`, so all code must run in a Python environment where SageMath is available.
- Packaging metadata and dependencies are defined in `pyproject.toml` in the repository root; a `.devcontainer` configuration is also provided.

**Quickstart**

1. Install the package from the repository root (see `pyproject.toml` for the exact dependencies).
2. Start a Python session with SageMath available, e.g. from within SageMath.
3. Run a first example — create a degree-5 del Pezzo surface, enumerate its cylinders, and compute a covering against a subdivision cone:

```python
    from delPezzo import Surface, NE_SubdivisionCone, CylinderList

    S = Surface(5)
    cylinders = [c for c in S.all_cylinders(['P1xP1', 'lines', 'tangent'])]
    cone = NE_SubdivisionCone.representative(S, 'B(0)')  # 1-d cone in 5-d lattice N
    collection = CylinderList(cylinders)
    covering = collection.get_polar_on(cone).reduce()
```

4. More runnable examples and further documentation resources are listed in the [Documentation](#documentation) section.

---

## Documentation

- **Doctest examples:** Sage-style `EXAMPLES` blocks in the module docstrings across `src/delPezzo` serve as runnable usage examples.
- **Notebook:** a supplementary Jupyter notebook is available at `tests/tests.ipynb`.
- **Bibliography:** `bibliography.rst` — a bibliography file included in the repository.

---

## API Reference

The package `delPezzo` (`src/delPezzo/`, SageMath required) exposes the following public interface; all symbols below are re-exported from the package root (`src/delPezzo/__init__.py`).

**Surfaces — `delPezzo.surface`**

- `Surface(degree, dependencies=None, extra=None)` — generic (possibly weak) del Pezzo surface, degree 1–9; attributes `degree`, `N` (Picard lattice), `K`, `E` (exceptional curves of the blowup from `P^2`), `L`, `Q`, `NE`, `minus_one_curves`, `minus_two_curves`; `all_cylinders([...])` iterates cylinders for given construction names (e.g. `['P1xP1', 'lines', 'tangent']`).
- `WeakDependencies` — dataclass of blowup-point dependencies for weak surfaces (`collinear_triples`, `infinitesimal_chains`, `sixs_on_conic`, `cusp_cubics`, 0-based point indices); methods `is_trivial()`, `degree_estimate()`, `is_valid()`.
- `Curve`, `Point`, `Contraction` — curve/point classes and contractions to `P^2` used across the package.

**Cones — `delPezzo.cone`**

- `NE_SubdivisionCone` — subdivision cone of the NE cone keeping creation info (`cone`, `S`, `parent`, `parent_face`, `parent_ray`). Key members:
  - `NE(S)` / `from_face_and_ray(parent, face, ray)` — base NE cone of a surface / child cone from a face plus subdividing ray (classmethods).
  - `children(subdivision_ray=None)` / `ample_children(subdivision_ray=None)` — generators of subdivision cones / of cones whose relative interiors contain ample divisors.
  - `make_child(face, subdivision_ray=None)` — child cone for a specific face; raises `ValueError` on invalid input.
  - `rays()`, `subdivision_faces(ray)`, `type()`, `Ample()`, `print()` — ray access, faces not containing a ray, cone-type label, ample-class cone, debug output.
  - `representative(S, ...)` — representative subdivision cone used in doctests (e.g. `NE_SubdivisionCone.representative(S, 'B(0)')`).
- `relint_contains_relint(supercone, cone)` / `relints_intersect(cone1, cone2)` — relative-interior containment / intersection predicates for Sage cones.

**Cylinders — `delPezzo.cylinder`**

- `Cylinder` — frozen dataclass for a cylinder (`complement` and `support`: (-1)-curve lists; `fiber`, `basepoint`, `transversal`, `dimension`, construction metadata). Classmethod builders:
  - `make(S, complement, support, fiber=None, basepoint=None, ...)` — general constructor.
  - `make_type_lines(S, E, e)` — lines through the image of `e` and members of `E`; not suitable for weak surfaces.
  - `make_type_lines2(S, E, e1, e2, e3, e4)` — pencil-of-lines construction (Perepechko-2013, Sec. 3.1).
  - `make_type_tangent(S, E, E_on_conic, E_on_tangent, E_on_fibers=None)` — conic-plus-tangent construction.
  - `make_type_tangent_weak(S, contraction, E_on_conic, E_on_tangent, E_on_fibers=None)` — weak-surface variant taking a `Contraction`.
- `CylinderList`, `CylinderGenerator` — cylinder collection/generator helpers; e.g. `CylinderList(cylinders).get_polar_on(cone).reduce()` (see the `Surface` doctest).

**Search and classification data**

- `Finder`, `ConeCovering` — search utilities in `delPezzo.finder` (see `src/delPezzo/finder.py`).
- `generate_surfaces`, `generate_surface`, `Lubbes_lines` — build `Surface` objects from the Lubbes classification data bundled with `delPezzo.Lubbes_parse`.

---

## Testing

All tests live in the `tests/` directory at the repository root, organized as Python modules following the `test_*.py` naming convention.

**Scope of the suite**

- Core modules: `test_surface.py`, `test_contraction.py`, `test_blowups.py`, `test_finder.py`, `test_Lubbes.py`
- Degree-specific behavior for del Pezzo degrees 1–6, including weak surfaces and named special cases: `test_deg1.py`, `test_deg2.py`, `test_deg2_B2.py`, `test_deg2_KimPark.py`, `test_deg3.py`, `test_deg4.py`, `test_deg5.py`, `test_weak_deg6.py`
- Cross-cutting checks: `test_various.py`
- A supplementary Jupyter notebook: `tests/tests.ipynb`

**Environment**

The package depends on SageMath throughout, so tests must be run in a Python environment where the `sage` library is importable. A `.devcontainer` configuration is included in the repository for setting up a development environment.

**Running the tests**

The repository contains no CI configuration or documented test command. The `test_*.py` modules follow the conventional layout recognized by standard Python test runners and can be executed from the repository root. Additionally, docstrings across `src/delPezzo` contain Sage-style `EXAMPLES` doctest blocks that serve as executable usage examples.

---

## Contributing

No dedicated contribution guidelines are documented in the repository. When contributing changes, keep the following repository conventions in mind:

- Run all code in a Python environment where SageMath is available, since every module imports from `sage.all_cmdline`.
- Packaging metadata and dependencies are defined in `pyproject.toml` in the repository root; a `.devcontainer` configuration is provided for setting up a development environment.
- Tests live in `tests/` and follow the `test_*.py` naming convention; docstrings across `src/delPezzo` contain Sage-style `EXAMPLES` doctest blocks that should be kept consistent with any behavior changes.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). delPezzo-2b5uu04x repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{delPezzo-2b5uu04x,

        author = {README Benchmark},

        title = {delPezzo-2b5uu04x repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---