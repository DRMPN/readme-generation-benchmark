# delPezzo

`delPezzo` is a SageMath module for studying flexibility of affine cones over del Pezzo surfaces. It models curve classes in the Picard lattice of generic and weak del Pezzo surfaces, constructs cylinders on those surfaces, and examines cones of divisor classes to test generic flexibility.

The project metadata gives version **2025.1** and requires Python **3.9 or later**. The source imports SageMath’s lattice, cone, matrix, and polyhedral-geometry functionality, so a SageMath environment is needed to use the module. The repository also includes tests and a notebook with examples drawn from the test suite.

## What it provides

The package exposes its main classes and helpers from `delPezzo`:

- **`Surface`** represents a del Pezzo surface of degree 1–9, with a Picard lattice, canonical class, exceptional classes, and cones of curves and ample classes. It can also represent weak del Pezzo surfaces using specified dependencies among blow-up points.
- **`WeakDependencies`** describes configurations including collinear triples, chains of infinitely near points, points on conics, and specified cuspidal cubics.
- **`Contraction`** models a contraction of curves and provides checks such as validity, maximality, and whether the contraction is to the projective plane.
- **`Cylinder`**, **`CylinderList`**, and **`CylinderGenerator`** describe, collect, generate, and test cylinders.
- **`NE_SubdivisionCone`** represents cones obtained by subdividing the cone of curves. Representative cones can be selected by type, such as `B(3)` or `C(2)`.
- **`Finder`** searches for cylinder collections over cones of polarizations and subdivides cones where generic flexibility has not yet been established.
- **`generate_surface`** and **`generate_surfaces`** parse entries from the bundled `Lubbes_list.txt` data.

Cylinder construction methods implemented in the source include `lines`, `lines2`, `tangent`, `P1xP1`, `cuspcubic`, `LL`, and `QT`. Their applicability depends on the surface and contraction; consult the method implementations for the degree restrictions and assumptions of each construction.

## Setup

Use a SageMath installation or environment. The repository’s development container is configured with the `sagemath/sagemath:latest` image. Its creation command installs `ca-certificates`, `tqdm`, and `pytest` using Sage’s pip interface.

To use the checkout without relying on an installed package, make the `src` directory importable:

```bash
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
sage -python
```

Then, in the Sage Python prompt:

```python
from delPezzo import Surface

S = Surface(5)
print(S)
```

To install test utilities in a Sage environment, the container uses:

```bash
sage --pip install tqdm pytest
```

The project metadata declares the package name, version, description, Python requirement, and README location. It does not list SageMath as a project dependency, so ensure SageMath is available separately.

## Usage

Create a surface and inspect its curve data:

```python
from delPezzo import Surface

S = Surface(5)
print(S.minus_one_curves)
print(S.Ample)
```

Generate cylinders from selected constructions, then check whether a collection is generically flexible on the ample cone:

```python
from delPezzo import Surface, CylinderGenerator, CylinderList

S = Surface(5)
cylinders = CylinderList(
    CylinderGenerator.all_cylinders(S, ["lines2"])
)
print(cylinders.is_generically_flexible_on(S.Ample))
```

A cone can be specified by its representative type. For example, the tests use `B(1)` through `B(6)` and types such as `C(4)`:

```python
from delPezzo import NE_SubdivisionCone

cone = NE_SubdivisionCone.representative(S, "B(3)")
```

`CylinderList.get_polar_on` selects cylinders polar on a cone; its `restrict_to_ample` option defaults to `True`. `reduce()` returns a reduced collection. The collection’s `is_generically_flexible_on` method checks polarity, completeness, and transversality, with optional controls for an excluded cone and restriction to ample classes.

The `Finder` class searches using the supplied construction names. For example, the test suite exercises:

```python
from delPezzo import Finder, Surface

S = Surface(5)
finder = Finder(S=S, constructions=["lines", "lines2", "tangent"])
finder.iterate()
print(finder.all_coverings_are_genflex())
```

`Finder` starts with a covering on the cone of curves. `iterate()` subdivides cones whose coverings do not yet establish generic flexibility and returns whether all current coverings are generically flexible.

For weak surfaces, pass dependencies when creating the surface:

```python
from delPezzo import Surface, WeakDependencies

dependencies = WeakDependencies(collinear_triples=[[1, 2, 0]])
S = Surface(6, dependencies=dependencies)
```

Point indices in `WeakDependencies` start at zero. The package also provides `generate_surface(line)` for parsing one Lubbes data entry, and `generate_surfaces(degree)` for iterating over entries of the requested degree. For example, the tests parse `"18 5 [23, 45] 2A1"`.

## Configuration

The project’s pytest settings are in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "--import-mode importlib -p no:warnings"
```

This selects pytest’s `importlib` import mode and disables its warnings plugin. The dev-container configuration specifies a SageMath image, installs `tqdm` and `pytest`, and configures VS Code to use `sage -python` as the Python interpreter.

At runtime, surface configuration is provided through constructor arguments rather than a separate application configuration file. `Surface` accepts a degree, optional `WeakDependencies`, and optional `extra` data. The source specifically reads `extra["tacnodal_curves"]` for degree-2 surfaces. `Finder` accepts construction names and optional recommended cylinder coverings.

## Development

The source package is under `src/delPezzo/`; tests are under `tests/`. The `.devcontainer/devcontainer.json` file provides a SageMath-based VS Code development environment with Python and Jupyter extensions.

The test files cover surface and contraction behavior, Lubbes data parsing, cone and cylinder calculations, and examples associated with del Pezzo surfaces of several degrees. `tests/tests.ipynb` provides a notebook workflow that adds `../src` to `sys.path` and calls selected test functions.

When adding or changing constructions, check the degree and configuration assumptions in the relevant methods and tests. Some functionality is explicitly incomplete: for example, maximal-only disjoint subsets raise `NotImplementedError`, and the degree-1 test is marked as needing a rewrite.

## Testing

Run the test suite from the repository root in an environment where SageMath and pytest are available:

```bash
sage -python -m pytest
```

The tests include computational checks and may take time depending on the SageMath environment. Some tests are intentionally skipped: the degree-1 test is marked as needing a rewrite, and a degree-4 test is marked as not implemented. The degree-2 Kim–Park test file also describes itself as abandoned in its comments.

## References

The repository’s `bibliography.rst` lists research references related to cylinders, affine cones, and flexibility, including work by Cheltsov, Park, and Won; Perepechko; Kim and Park; Lubbes; and Won. It includes the preprint *Generic flexibility of affine cones over del Pezzo surfaces in Sagemath* by Alexander Perepechko (2023).

## License

No license file or license declaration is present in the supplied repository files. Check with the author or repository maintainer for licensing and reuse terms.
