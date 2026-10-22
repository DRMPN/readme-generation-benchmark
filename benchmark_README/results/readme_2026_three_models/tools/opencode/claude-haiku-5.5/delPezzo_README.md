# delPezzo

`delPezzo` is a [SageMath](https://www.sagemath.org/) Python module for studying the flexibility of affine cones over del Pezzo surfaces. It models (possibly weak) del Pezzo surfaces of degree 1 to 9 through their Picard lattices, enumerates their negative curves and cones of curves, constructs families of cylinders, and searches for cylinder coverings that certify generic flexibility of the cone over an ample polarization.

The package is version `2025.1` and is described in `pyproject.toml` as "a Sagemath module for studying flexibility of affine cones over del Pezzo surfaces". The author listed in `pyproject.toml` is Alexander Perepechko.

## Background

Flexibility of an affine variety means that its special automorphism group acts transitively on its smooth locus. The module focuses on affine cones over del Pezzo surfaces, following the constructions and results in the works listed under [References](#references). The code implements several of the constructions from those papers (for example, "lines", "lines2", "tangent", "P1xP1", "cuspcubic" and the generic "LL" and "QT" searches), but the README does not claim that every theorem in those papers is formalized in code.

## Features

- **Surfaces** (`Surface`): constructs a del Pezzo surface of a given degree from `P^2` by blowing up `9 - degree` points. Degrees from 1 to 9 are accepted. Weak del Pezzo surfaces are described with `WeakDependencies` (collinear triples, infinitely near chains, six points on a conic, and cuspidal cubics).
- **Curves and cones**: computes the (-1)- and (-2)-curves, the cone of curves `NE`, and the ample cone; `NE_SubdivisionCone` subdivides `NE` into cones of named types such as `B(k)`, `C(k)`, and `*-P1xP1` (see `NE_SubdivisionCone.cone_types`).
- **Contractions** (`Contraction`): enumerates valid contractions of a surface to `P^2` (`Surface.contractions_P2`), including chains of infinitely near (-2)-curves, and computes the induced conic and line linear systems.
- **Cylinders** (`Cylinder`, `CylinderList`, `CylinderGenerator`): builds cylinders of several types, with polarity and completeness checks against a given cone.
- **Coverings** (`Finder`, `ConeCovering`): starts from the whole `NE` cone, reduces cylinder collections on each cone, and subdivides cones where generic flexibility is not yet established (`Finder.iterate`).
- **Lubbes data** (`generate_surfaces`, `generate_surface`, `Lubbes_lines`): reads the list of weak del Pezzo surfaces of a given degree from `src/delPezzo/Lubbes_list.txt`, the list is labelled with Lubbes-style type strings (for example `2A1`, `A2+ A1`). The repository's `bibliography.rst` includes [Lub-min]_ and [Lub-algo]_ by Niels Lubbes, but the repository does not state explicitly which paper the data file comes from.

## Repository layout

```
.
├── .devcontainer/devcontainer.json   # Dev container based on the sagemath/sagemath image
├── bibliography.rst                  # Bibliography entries for the module's docstrings
├── pyproject.toml                    # Package metadata and pytest configuration
├── src/delPezzo/
│   ├── __init__.py                   # Public API re-exports
│   ├── surface.py                    # Surface, WeakDependencies, Contraction, Curve, Point, BubbleClass
│   ├── cone.py                       # NE_SubdivisionCone and cone helper functions
│   ├── cylinder.py                   # Cylinder, CylinderList, CylinderGenerator
│   ├── finder.py                     # Finder and ConeCovering
│   ├── Lubbes_parse.py               # Parser for the Lubbes list of weak del Pezzo surfaces
│   └── Lubbes_list.txt               # Data file used by Lubbes_parse.py
└── tests/                            # pytest test files, and tests.ipynb
```

`src/delPezzo/__init__.py` re-exports the main public names: `WeakDependencies`, `Surface`, `Contraction`, `Curve`, `Point`, `Cylinder`, `CylinderList`, `CylinderGenerator`, `Finder`, `ConeCovering`, `NE_SubdivisionCone`, `relint_contains_relint`, `relints_intersect`, `generate_surfaces`, `generate_surface`, and `Lubbes_lines`.

## Requirements

- **SageMath.** Several modules start with `from sage.all_cmdline import *` or import from `sage.geometry`, `sage.matrix`, `sage.quadratic_forms`, and related Sage packages. The package cannot be used outside a Sage environment.
- **Python 3.10 or newer, in practice.** `pyproject.toml` declares `requires-python = ">=3.9"`, but the source uses `match` statements (for example in `surface.py`, `cone.py`, and `cylinder.py`) and `X | None` annotations evaluated at definition time, which require Python 3.10 or newer.
- **pytest** to run the test suite. `pyproject.toml` configures pytest with `--import-mode importlib`.
- **tqdm** is installed in the dev container's `onCreateCommand`, but no module in `src/` imports it.

The development container `.devcontainer/devcontainer.json` uses the `sagemath/sagemath:latest` image and runs `sage --pip install tqdm pytest` on creation. It also sets the VS Code Python interpreter to `sage -python`.

## Installation

The repository does not include installation instructions beyond the dev container. To use the module from a Sage session, make the `src` directory importable, for example by setting `PYTHONPATH` to the `src` directory of a clone:

```bash
git clone <repository-url> delPezzo
cd delPezzo
export PYTHONPATH="$PWD/src:$PYTHONPATH"
sage -python -c "import delPezzo; print(delPezzo.Surface)"
```

The `pyproject.toml` file has a `[project]` table but no `[build-system]` table, so this README does not claim that `pip install .` has been verified.

## Usage

The following example is taken from the tests in `tests/test_deg5.py`. It checks the covering of a degree 5 surface given in Perepechko (2013), cited as [Pe13]_ in `bibliography.rst`:

```python
from delPezzo import Surface, CylinderList, CylinderGenerator

S = Surface(5)
cylinders = CylinderList(list(CylinderGenerator.all_cylinders(S, ['lines2'])))
assert cylinders.is_generically_flexible_on(S.Ample)
```

The `Surface` class docstring shows another workflow for degree 5, using the `P1xP1`, `lines`, and `tangent` constructions together with a cone of type `B(0)`:

```python
S = Surface(5)
cylinders = [c for c in S.all_cylinders(['P1xP1', 'lines', 'tangent'])]
cone = NE_SubdivisionCone.representative(S, 'B(0)')
collection = CylinderList(cylinders)
covering = collection.get_polar_on(cone).reduce()
```

Note that this snippet is written in the docstring style and calls `S.all_cylinders`, which does not exist as a method on `Surface`; the working entry point in the code is `CylinderGenerator.all_cylinders(S, constructions)`. Treat it as illustrative until it is checked.

To search for a covering over the whole `NE` cone and subdivide until generic flexibility holds or the iteration returns, use `Finder`:

```python
from delPezzo import Finder, Surface

S = Surface(5)
F = Finder(S=S, constructions=['lines', 'lines2', 'tangent'])
done = F.iterate()  # True once generic flexibility holds for all polarizations
```

`Finder` defaults to the `'LL'` construction if `constructions` is not given. `Finder.iterate` subdivides the cones of coverings that are not yet generically flexible and returns `True` when all coverings are generically flexible.

To enumerate the weak del Pezzo surfaces from the Lubbes list of a given degree:

```python
from delPezzo import generate_surfaces

for S in generate_surfaces(4):
    print(S)
```

## Running tests

From the repository root, with SageMath and pytest available and the package importable (see [Installation](#installation)):

```bash
pytest
```

The test files are in `tests/`. They include tests for surfaces, contractions, Lubbes parsing, finder coverings, and cylinder coverings in degrees 1 to 6 and some weak surfaces. Some test files are minimal, and `tests/test_deg2_KimPark.py` states in its header that the file is abandoned.

## Status and limitations

- The code and docstrings contain `TODO` notes and commented-out code, for example in `surface.py` (`contractions`, `is_valid_contraction` variants), `cylinder.py` (a `latex` method and some unfinished `reduce` logic), and `cone.py` (`relative_volume` raises `NotImplementedError`). Parts of the API may be incomplete.
- `Surface.blowups` raises `NotImplementedError` for degree 3 or less. `WeakDependencies.is_valid` raises `NotImplementedError` when the estimated degree is 2 or less.
- `Surface.Ample` is computed from the dual of `NE`. The author notes in a `TODO` that `NE` is preferable because the ample cone has many more rays.
- `CylinderList.insert` contains a leftover `print` call.
- `Finder` and `CylinderList` rely on Sage cone computations, so runtime can be significant in some degrees; a `cone.py` comment notes that the representative construction is slow in degree 1.

## References

The references used in the docstrings are listed in `bibliography.rst`:

- [CPW13] Ivan Cheltsov, Jihun Park, and Joonyeong Won. *Affine cones over smooth cubic surfaces*. Journal of the European Mathematical Society, 18(7):1537–1564, 2016. doi:10.4171/jems/622.
- [CPW15] Ivan Cheltsov, Jihun Park, and Joonyeong Won. *Cylinders in del Pezzo surfaces*. International Mathematics Research Notices, 2017(4):1179–1230, 2017. doi:10.1093/imrn/rnw063.
- [KimPark21] Jaehyun Kim and Jihun Park. *Generic flexibility of affine cones over del Pezzo surfaces of degree 2*. International Journal of Mathematics, 32(14):2150104, 2021. doi:10.1142/S0129167X21501044.
- [Lub-min] Niels Lubbes. *Minimal families of curves on surfaces*. Journal of Symbolic Computation, 65:29–48, 2014. doi:10.1016/j.jsc.2014.01.003.
- [Lub-algo] Niels Lubbes. *Algorithms for singularities and real structures of weak Del Pezzo surfaces*. Journal of Algebra and Its Applications, 13(05):1350158, 2014. doi:10.1142/S0219498813501582.
- [PW16] Jihun Park and Joonyeong Won. *Flexible affine cones over del Pezzo surfaces of degree 4*. European Journal of Mathematics, 2(1):304–318, 2016. doi:10.1007/s40879-015-0054-4.
- [Pe13] A. Yu. Perepechko. *Flexibility of affine cones over del Pezzo surfaces of degree 4 and 5*. Functional Analysis and Its Applications, 47(4):284–289, 2013. doi:10.1007/s10688-013-0035-7.
- [Pe20] Alexander Perepechko. *Affine cones over cubic surfaces are flexible in codimension one*. Forum Mathematicum, 33(2):339–348, 2021. doi:10.1515/forum-2020-0191.
- [Pe23] Alexander Perepechko. *Generic flexibility of affine cones over del Pezzo surfaces in Sagemath*. arXiv:2305.06462.
- [Won22] Joonyeong Won. *Flexibility of affine cones over singular del Pezzo surfaces with degree 4*. East Asian Mathematical Journal, 38(3):321–329, 2022.

## License

No license file is included in the repository, so no license is stated here.
