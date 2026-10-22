# delPezzo

A Sagemath module for studying the flexibility of affine cones over del Pezzo surfaces. It provides tools for working with (possibly weak) del Pezzo surfaces as blowups of $\mathbb{P}^2$, their negative curves and Néron–Severi cones, and collections of cylinders on them. It can search for cylinder coverings that establish generic flexibility for ample divisor classes.

The project is described in `pyproject.toml` as "a Sagemath module for studying flexibility of affine cones over del Pezzo surfaces." It is version `2025.1` and was written by Alexander Perepechko.

## Overview

The package `delPezzo` (in `src/delPezzo/`) builds on Sage's toric lattices, cones, and quadratic forms. Its main components are:

- **`Surface`** (`surface.py`): a del Pezzo surface of degree `d`, represented as the blowup of $\mathbb{P}^2$ at `9 - d` points. It exposes the lattice basis `L` and `E`, the canonical class `K`, the intersection form `dot`, the lists of $(-1)$- and $(-2)$-curves, the Ample cone, and methods such as `blowups()`, `contractions_P2()`, and `standard_contraction()`. Weak surfaces are described with `WeakDependencies`, which records collinear triples, infinitesimal chains, six-point conics, and cuspidal cubics.
- **`Contraction`** (`surface.py`): a blowdown from a surface to $\mathbb{P}^2$, with projection and the induced line and conic classes.
- **`Cylinder`, `CylinderList`, `CylinderGenerator`** (`cylinder.py`): constructions of cylinders (for example, lines, lines through two pairs of points, tangents to conics, $\mathbb{P}^1\times\mathbb{P}^1$-type pairs, and cuspidal cubics), together with checks for polarity, completeness, transversality, and generic flexibility on a given cone.
- **`NE_SubdivisionCone`** (`cone.py`): cones obtained by subdividing the Mori cone $\overline{NE}$ of the surface, with named types such as `B(i)`, `C(i)`, `B(i)-P1xP1`, and `C(i)-P1xP1`. It also provides helper functions `relint_contains_relint` and `relints_intersect`.
- **`Finder`** and **`ConeCovering`** (`finder.py`): an iterative search that starts from the full cone of effective curves, collects polar cylinders, and subdivides cones where generic flexibility is not yet established.
- **Lubbes list parsing** (`Lubbes_parse.py`, `Lubbes_list.txt`): a bundled table of 176 weak del Pezzo surface types. Each row gives an index, a rank (the number of blown-up points), a list of basis labels, and a singularity type. The parser turns rows into `Surface` objects.

The test suite, `bibliography.rst`, and the docstrings cite the following works: Cheltsov–Park–Won (two papers), Kim–Park, Lubbes (two papers), Park–Won, Perepechko (three papers, including the arXiv preprint on Sagemath), and Won.

## Repository Layout

```
.devcontainer/devcontainer.json   Dev container configuration (Sage image)
bibliography.rst                  Reference entries used in docstrings
pyproject.toml                    Project metadata and pytest options
src/delPezzo/                     Package source
  __init__.py                     Public exports
  surface.py                      Surface, Contraction, Curve, Point, WeakDependencies
  cone.py                         NE_SubdivisionCone and cone helpers
  cylinder.py                     Cylinder, CylinderList, CylinderGenerator
  finder.py                       Finder, ConeCovering
  Lubbes_parse.py                 Parsing of the Lubbes list
  Lubbes_list.txt                 Table of weak del Pezzo surface types
tests/                            pytest modules and tests.ipynb notebook
```

## Requirements

- **Sagemath.** Every module in the package imports from `sage`, so the package cannot run under a plain Python interpreter.
- **Python.** `pyproject.toml` declares `requires-python = ">=3.9"`. However, the source uses `match` statements (Python 3.10 and later), so Python 3.10 or newer is needed in practice.
- **Packages used by the development environment.** The dev container installs `tqdm` and `pytest` into Sage's Python.

## Setup

### Option 1: Dev container

The file `.devcontainer/devcontainer.json` defines a container named "Sage" based on the `sagemath/sagemath:latest` image. On creation, it runs:

```
sudo apt update && sudo apt install ca-certificates && sage --pip install tqdm pytest
```

It sets the VS Code default interpreter to `sage -python` and installs the extensions `ms-python.python`, `ms-toolsai.jupyter`, and `Codeium.codeium`.

### Option 2: Existing Sage installation

`pyproject.toml` does not contain a `[build-system]` table, so the supplied files do not describe a packaged installation. The notebook `tests/tests.ipynb` makes the package importable by adding the source directory to the path:

```python
import sys
sys.path.insert(0, '../src')
```

Use the same approach in your own scripts, or set `PYTHONPATH` to `src` when running Sage's Python.

## Usage

The examples below use names that appear in the test files.

### Creating a surface

```python
from delPezzo import Surface

S = Surface(5)            # the blowup of P^2 at 4 points
print(S.minus_one_curves) # the (-1)-curves
print(S.minus_two_curves) # empty for a smooth surface
```

For a smooth surface of degree $d$, `Surface(d)` blows up `9 - d` points. Degree 1 to 9 is accepted, but `blowups()` raises `NotImplementedError` for degrees 3 and below.

### Weak surfaces from the Lubbes list

```python
from delPezzo import generate_surface, generate_surfaces

S = generate_surface("18 5 [23, 45] 2A1")
print(S.singularity_type())   # singularity type of the surface

surfaces_deg4 = list(generate_surfaces(4))   # 16 surfaces of degree 4
```

`generate_surfaces(degree)` returns the rows whose rank is `9 - degree`. The labels in brackets are converted to zero-based point indices.

### Cylinders and coverings

```python
from delPezzo import Surface, CylinderGenerator, CylinderList, NE_SubdivisionCone

S = Surface(5)
constructions = ['P1xP1', 'lines', 'tangent', 'lines2']
cylinders = list(CylinderGenerator.all_cylinders(S, constructions))

cone = NE_SubdivisionCone.representative(S, 'B(0)').cone
covering = CylinderList(cylinders).get_polar_on(cone).reduce()
print(len(covering))
```

Here `get_polar_on` keeps the cylinders that are polar on the cone, and `reduce` removes redundant cylinders.

### Automated search

```python
from delPezzo import Surface, Finder

F = Finder(S=Surface(5), constructions=['lines', 'lines2', 'tangent'])
F.iterate()                    # subdivide cones where flexibility is not yet shown
print(F.all_coverings_are_genflex())
```

`Finder.iterate()` returns `True` when every polarization cone has been shown to be covered.

### Weak surfaces with explicit dependencies

```python
from delPezzo import Surface, WeakDependencies

deps = WeakDependencies(collinear_triples=[[1, 2, 0]])
S = Surface(6, dependencies=deps)
```

Point indices start at 0. The tests in `test_weak_deg6.py` build cylinders with `Cylinder.make(...)` on such surfaces.

## Configuration

The supplied files define only a small amount of configuration:

- **`pyproject.toml`** sets the project name, version, author, Python requirement, and the README used as the long description. It also sets pytest options:
  ```toml
  [tool.pytest.ini_options]
  addopts = "--import-mode importlib -p no:warnings"
  ```
- **`Surface` arguments.** `dependencies` takes a `WeakDependencies` object. `extra` is a dictionary. For degree 2, the key `tacnodal_curves` (an even integer from 0 to 24) sets the number of tacnodal curves, and it defaults to 0.
- **`.devcontainer/devcontainer.json`** controls the container image, the setup command, and the VS Code interpreter.

No environment variables are read by the package source.

## Development

- Package code lives in `src/delPezzo/`. Public names are exported from `src/delPezzo/__init__.py`.
- Several source files contain `TODO` notes and commented-out code that mark unfinished work. Examples include the `relative_volume` method in `NE_SubdivisionCone`, which raises `NotImplementedError`, and the unfinished `reduce` logic for double points, which raises `NotImplementedError` when `keep_double_points=True`.
- `Surface.blowups()` and `CylinderGenerator` contain notes saying which constructions are suitable for weak surfaces and which need work.
- `test_deg2_KimPark.py` is marked in its docstring as abandoned and is to be moved to a `txt/` directory.
- `test_deg2_B2.py` contains a `__main__` block that writes a TikZ file to `../local/B2_CPW.tex` if `tikzplotlib` is installed. Otherwise it prints a message.

## Testing

Tests use pytest and are located in `tests/`. From a Sage environment with `src` on the path, a typical invocation is:

```
sage -python -m pytest tests
```

The `pytest` options in `pyproject.toml` apply automatically. The test modules cover:

| Module | Focus |
|---|---|
| `test_Lubbes.py` | Parsing of the Lubbes list and counts per degree |
| `test_blowups.py` | Blowups, contractions to $\mathbb{P}^2$ |
| `test_contraction.py` | Chains of contracted curves, valid contractions |
| `test_deg2.py`, `test_deg3.py`, `test_deg4.py`, `test_deg5.py` | Cylinder coverings following the cited papers |
| `test_deg2_B2.py` | Polar subsets on the cone $B(2)$ for degree 2 |
| `test_finder.py` | The iterative `Finder` in degrees 5 and 6 |
| `test_surface.py` | Disjoint subsets and curve naming |
| `test_various.py` | Cone types and coverings in degrees 3 and 5 |
| `test_weak_deg6.py` | Cylinders on weak surfaces of degree 6 |

Some tests are not active:

- `test_deg1.py::test_deg1` is skipped with the reason "needs a rewrite."
- `test_deg4.py::test_ParkWon_C` is skipped as "not implemented."

`tests/tests.ipynb` runs many of these test functions interactively. It inserts `../src` into `sys.path` and imports the test modules.

## References

The docstrings and test modules follow the following works, listed in `bibliography.rst`:

- [CPW13] I. Cheltsov, J. Park, J. Won. *Affine cones over smooth cubic surfaces*. J. Eur. Math. Soc. 18(7), 2016.
- [CPW15] I. Cheltsov, J. Park, J. Won. *Cylinders in del Pezzo surfaces*. IMRN 2017(4), 2017.
- [KimPark21] J. Kim, J. Park. *Generic flexibility of affine cones over del Pezzo surfaces of degree 2*. Int. J. Math. 32(14), 2021.
- [Lub-min] N. Lubbes. *Minimal families of curves on surfaces*. J. Symbolic Comput. 65, 2014.
- [Lub-algo] N. Lubbes. *Algorithms for singularities and real structures of weak del Pezzo surfaces*. J. Algebra Appl. 13(05), 2014.
- [PW16] J. Park, J. Won. *Flexible affine cones over del Pezzo surfaces of degree 4*. Eur. J. Math. 2(1), 2016.
- [Pe13] A. Yu. Perepechko. *Flexibility of affine cones over del Pezzo surfaces of degree 4 and 5*. Funct. Anal. Appl. 47(4), 2013.
- [Pe20] A. Perepechko. *Affine cones over cubic surfaces are flexible in codimension one*. Forum Math. 33(2), 2021.
- [Pe23] A. Perepechko. *Generic flexibility of affine cones over del Pezzo surfaces in Sagemath*. arXiv:2305.06462.
- [Won22] J. Won. *Flexibility of affine cones over singular del Pezzo surfaces with degree 4*. East Asian Math. J. 38(3), 2022.

## License

No license file appears in the supplied repository files, and no license is named in `pyproject.toml`. The license for this project is therefore not specified here. Check with the author before reusing or redistributing the code.
