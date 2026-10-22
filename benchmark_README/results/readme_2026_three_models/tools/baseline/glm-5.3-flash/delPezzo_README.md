# delPezzo

A [SageMath](https://www.sagemath.org/) module for studying the flexibility of affine cones over (weak) del Pezzo surfaces.

**Version:** 2025.1
**Author:** Alexander Perepechko ([a@perep.ru](mailto:a@perep.ru))

---

## Overview

This package provides computational tools for working with smooth and weak del Pezzo surfaces, their Picard lattices, contractions, and cylinders. Its main purpose is to verify and search for coverings of ample cone regions by polar cones of cylinder collections, which establishes (generic) flexibility of the corresponding affine cones over del Pezzo surfaces.

The module represents a del Pezzo surface of degree `d` as a blowup of `P^2` in `9 - d` points (possibly infinitely near, i.e. a weak del Pezzo surface). Curve classes live in a toric lattice endowed with the standard intersection form, and cylinders are described combinatorially via their polar and forbidden cones in the Picard lattice. Generic flexibility is checked by determining whether a collection of cylinders is polar, complete, and transversal over a given cone of polarization classes.

The mathematical background and the underlying algorithms are described in the references listed in the [References](#references) section below, most notably [Pe23].

## Features

- **`Surface`** (`delPezzo.surface`) — a generic (possibly weak) del Pezzo surface of degree 1–9, with:
  - Picard lattice `N`, canonical class `K`, standard line class `L`, and the exceptional basis `E` of the blowup from `P^2`;
  - enumeration of all `(-1)`- and `(-2)`-curves (`minus_one_curves`, `minus_two_curves`);
  - disjoint subsets of curves, double/triple intersection points;
  - blowups (`Surface.blowups()`) and contractions to `P^2` (`Surface.contractions_P2()`), including the `Contraction` class with chains of contracted curves, line and conic classes;
  - the ample cone (`Surface.Ample`) and the Mori cone `NE`.
- **`WeakDependencies`** — encodes configurations of blown-up points: collinear triples, chains of infinitely near points, six-tuples on conics, and cuspidal cubics (relevant for degree 1).
- **`Cylinder` and `CylinderList`** (`delPezzo.cylinder`) — constructions of standard cylinder types on del Pezzo surfaces (`lines`, `lines2`, `tangent`, `tangent_weak`, `P1xP1`, `cuspcubic`, and more), with checks for polarity, completeness, and transversality, and a test for generic flexibility (`is_generically_flexible_on`).
- **`NE_SubdivisionCone`** (`delPezzo.cone`) — cones obtained by subdividing the Mori cone, classified by Fujita types such as `B(i)`, `C`, `C(i)`, and their `-P1xP1` variants; provides representatives and subdivision children.
- **`Finder` and `ConeCovering`** (`delPezzo.finder`) — an automated search for cylinder collections achieving generic flexibility over the ample cone, by iteratively subdividing cones where flexibility is not yet established.
- **Lubbes' list of weak del Pezzo surfaces** (`delPezzo.Lubbes_parse`) — parsing and generation of all 176 weak del Pezzo surfaces from `Lubbes_list.txt`, classified by singularity root type.

## Requirements

- Python **≥ 3.9**
- **SageMath** (the module imports from `sage.all_cmdline`, `sage.geometry`, `sage.combinat`, etc.)
- `tqdm` and `pytest` (used in the development environment; see below)

## Installation

The package follows the `src` layout and can be installed into a SageMath environment with pip:

```bash
sage --pip install .
```

There is no setup required beyond having SageMath available, since the package relies on the Sage library at import time.

Alternatively, the repository ships a VS Code **devcontainer** configuration (`.devcontainer/devcontainer.json`) based on the `sagemath/sagemath:latest` Docker image. Opening the repository in VS Code with the Dev Containers extension will:

- create a container with SageMath installed;
- run `sage --pip install tqdm pytest` on creation;
- configure the default Python interpreter to `sage -python`;
- recommend the Python, Jupyter, and Codeium extensions.

## Usage

Import the module and start exploring:

```python
from delPezzo import Surface, CylinderList, Cylinder, CylinderGenerator
from delPezzo import NE_SubdivisionCone, Finder
from delPezzo import generate_surfaces, generate_surface
```

### Creating surfaces

```python
# The generic del Pezzo surface of degree 5
S = Surface(5)

# A weak del Pezzo surface of degree 6 with one collinear triple of points
from delPezzo import WeakDependencies
S = Surface(6, dependencies=WeakDependencies(collinear_triples=[[1, 2, 0]]))
```

### Enumerating curves and contractions

```python
S = Surface(5)
S.minus_one_curves   # all (-1)-curves
S.disjoint_subsets(S.minus_one_curves)   # pairwise disjoint subsets
list(S.contractions_P2())                # all contractions to P^2
```

### Constructing cylinders and checking flexibility

Cylinders can be built directly:

```python
S = Surface(3)
U = CylinderList([Cylinder.make_type_tangent(S, S.E, E_on_conic=S.E[1:], E_on_tangent=[S.E[0]])])
U.is_generically_flexible_on('B(1)')   # types such as 'B(i)', 'C', 'C(i)-P1xP1'
```

or generated over all contractions and constructions:

```python
S = Surface(5)
constructions = ['P1xP1', 'lines', 'tangent', 'lines2']
cylinders = list(CylinderGenerator.all_cylinders(S, constructions))
collection = CylinderList(cylinders)
```

Supported construction names include `'lines'`, `'lines2'`, `'tangent'`, `'P1xP1'`, `'cuspcubic'`, `'LL'`, and `'QT'`.

### Searching for coverings

```python
from delPezzo import Finder, Surface

S = Surface(5)
F = Finder(S=S, constructions=['lines', 'lines2', 'tangent'])
F.iterate()                       # subdivide cones where flexibility is not yet achieved
F.all_coverings_are_genflex()     # True if generic flexibility holds for all polarizations
F.coverings                       # list of ConeCovering objects
```

### Working with Lubbes' classification

`Lubbes_list.txt` contains 176 weak del Pezzo surfaces with their ranks and singularity types. Surfaces can be generated by degree or parsed from a line of the list:

```python
for S in generate_surfaces(4):
    print(S)   # 16 weak del Pezzo surfaces of degree 4

S = generate_surface("18 5 [23, 45] 2A1")   # a degree 5 surface with 2A1 singularities
```

The exact command-line interface is not provided; the `Lubbes_parse` module also exposes a `__main__` block that prints all surfaces of a given degree.

## Configuration

There are no runtime configuration files. Behavior is controlled through constructor arguments:

- `Surface(degree, dependencies=..., extra=...)` — `dependencies` is a `WeakDependencies` instance describing the blowup configuration; `extra` supports keys such as `'tacnodal_curves'` (degree 2 only).
- `Finder(S, constructions=..., recommended_coverings=...)` — controls which cylinder constructions are used in the search and allows supplying known coverings.
- `CylinderList.is_generically_flexible_on(cone, exclude=..., restrict_to_ample=...)` — the `exclude` cone restricts the completeness check; `restrict_to_ample` limits checks to ample divisor classes.

## Project Structure

```
├── .devcontainer/
│   └── devcontainer.json        # VS Code dev container (SageMath image)
├── bibliography.rst             # bibliographic entries for the references
├── pyproject.toml               # project metadata and pytest configuration
├── src/
│   └── delPezzo/
│       ├── __init__.py          # public API
│       ├── surface.py           # Surface, Contraction, Curve, Point, WeakDependencies
│       ├── cylinder.py          # Cylinder, CylinderList, CylinderGenerator
│       ├── cone.py              # NE_SubdivisionCone and cone-utility functions
│       ├── finder.py            # Finder, ConeCovering
│       ├── Lubbes_parse.py      # parsing Lubbes' classification
│       └── Lubbes_list.txt      # data: 176 weak del Pezzo surfaces
└── tests/
    ├── test_*.py                # pytest test modules
    └── tests.ipynb              # Jupyter notebook running key tests
```

## Testing

The project uses [pytest](https://pytest.org). The pytest options are configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "--import-mode importlib -p no:warnings"
```

Run the full test suite from the repository root (inside a SageMath-enabled environment):

```bash
sage --pytest tests
```

or, if pytest is installed in the Sage Python environment:

```bash
sage -python -m pytest
```

The test suite includes:

- `test_Lubbes.py` — generation of surfaces from Lubbes' list (e.g., 16 surfaces of degree 4, 2 of degree 7);
- `test_blowups.py`, `test_contraction.py` — blowups, contractions, and validity checks;
- `test_deg1.py` … `test_deg5.py`, `test_weak_deg6.py` — flexibility results for specific degrees, checking coverings from the literature ([CPW15], [Pe13], [Pe20], [PW16], [KimPark21], [Pe23]);
- `test_deg2_KimPark.py`, `test_deg2_B2.py` — degree 2 case studies (the latter also contains plotting helpers using `tikzplotlib`);
- `test_finder.py` — automated covering search;
- `test_surface.py` — lattice utilities and curve naming;
- `test_various.py` — miscellanea, cone types, and coverings.

Some tests are marked `pytest.mark.skip` (e.g., `test_deg1`, `test_ParkWon_C`) because they need a rewrite or are not implemented. A Jupyter notebook `tests/tests.ipynb` runs representative tests interactively; it inserts `../src` into `sys.path` so it can be used without installing the package.

## Development

- The package imports Sage at module level; run all scripts with the Sage Python interpreter (`sage -python`).
- The devcontainer provides a ready-to-use SageMath environment for VS Code, including Jupyter support for the notebook in `tests/`.
- The codebase uses Python dataclasses, `functools.cache`/`cached_property` for lattice-heavy computations, and relies heavily on Sage's toric lattice and polyhedral cone facilities.
- `pyproject.toml` declares the package name `delPezzo`, version `2025.1`, and the README as the project description source.

## References

The algorithms and constructions implemented here are based on the following works (see `bibliography.rst` for full citations):

- **[CPW13]** I. Cheltsov, J. Park, J. Won — *Affine cones over smooth cubic surfaces*, J. Eur. Math. Soc. 18 (2016).
- **[CPW15]** I. Cheltsov, J. Park, J. Won — *Cylinders in del Pezzo surfaces*, Int. Math. Res. Not. 2017.
- **[KimPark21]** J. Kim, J. Park — *Generic flexibility of affine cones over del Pezzo surfaces of degree 2*, Int. J. Math. 32 (2021).
- **[Lub-min]** N. Lubbes — *Minimal families of curves on surfaces*, J. Symbolic Comput. 65 (2014).
- **[Lub-algo]** N. Lubbes — *Algorithms for singularities and real structures of weak Del Pezzo surfaces*, J. Algebra Appl. 13 (2014).
- **[PW16]** J. Park, J. Won — *Flexible affine cones over del Pezzo surfaces of degree 4*, Eur. J. Math. 2 (2016).
- **[Pe13]** A. Yu. Perepechko — *Flexibility of affine cones over del Pezzo surfaces of degree 4 and 5*, Funct. Anal. Appl. 47 (2013).
- **[Pe20]** A. Perepechko — *Affine cones over cubic surfaces are flexible in codimension one*, Forum Math. 33 (2021).
- **[Pe23]** A. Perepechko — *Generic flexibility of affine cones over del Pezzo surfaces in Sagemath*, arXiv:2305.06462.
- **[Won22]** J. Won — *Flexibility of affine cones over singular del Pezzo surfaces with degree 4*, East Asian Math. J. 38 (2022).

## License

This repository does not contain an explicit license file. All rights are reserved by the author, Alexander Perepechko, unless otherwise specified. If you intend to reuse or redistribute this code, please contact the author.
