# delPezzo

`delPezzo` is a SageMath module for studying flexibility of affine cones over del Pezzo surfaces. It models divisor and curve classes in the Picard lattice, constructs cylinders on surfaces, and searches for cylinder collections that give generic flexibility for ample polarizations. The implementation also supports weak del Pezzo surfaces described by dependencies among blow-up points.

The package metadata lists version `2025.1` and Python `>=3.9`, but the source uses Python 3.10 syntax (including union types and `match`/`case`), so Python 3.10 or newer is required in practice. SageMath is also required at runtime: the implementation uses SageMath's lattices, cones, matrices, and quadratic forms. The repository does not declare SageMath as a pip dependency or pin a SageMath version.

## Getting started

Use a SageMath installation whose Python is 3.10 or newer, with `pytest` available. From the repository root, install the package into SageMath's Python environment if it is not already importable, then run the tests:

```sh
sage -pip install -e .
sage -python -m pytest
```

The test configuration is in `pyproject.toml`. The package has no configured command-line script; use its Python API from SageMath's Python interpreter (for example, `sage -python`).

## Quick example

```python
from delPezzo import CylinderGenerator, Finder, Surface

# A generic del Pezzo surface of degree 5.
S = Surface(5)

# Generate cylinders from selected constructions.
constructions = ["lines", "lines2", "tangent"]
cylinders = list(CylinderGenerator.all_cylinders(S, constructions))
print(S)
print(f"Generated {len(cylinders)} cylinders")

# Search collections on the cone of effective curve classes and its subdivisions.
finder = Finder(S, constructions=constructions)
complete = finder.all_coverings_are_genflex()
if not complete:
    complete = finder.iterate()
print(f"All current polarization cones covered: {complete}")
for covering in finder.coverings:
    print(covering.NE_cone.type(), covering.is_generically_flexible)
```

`Finder.iterate()` subdivides cones whose current cylinder collection has not established generic flexibility. Its return value reports whether all the resulting coverings are generically flexible; the `coverings` attribute contains the current `ConeCovering` records.

## Main API

The package exports its main classes and data helpers from `delPezzo`:

- **`Surface(degree, dependencies=None, extra=None)`** models a del Pezzo surface of degree 1 through 9 in the blow-up basis of the Picard lattice. It provides the canonical and line classes, intersection pairing, negative curves, the effective-curve cone (`NE`), and its dual ample cone (`Ample`). Pass a `WeakDependencies` instance to specify collinear triples, infinitely-near blow-up chains, six points on a conic, and cusp-cubic dependencies.
- **`Contraction`** represents a valid contraction of curves on a surface. `Surface.contractions_P2()` generates contractions to the plane used by the cylinder-generation routines.
- **`Cylinder`**, **`CylinderList`**, and **`CylinderGenerator`** represent cylinders, collections of cylinders, and construction/search routines. A cylinder records its construction, supporting and complementary curve classes, and optional fiber or base-point information. A `CylinderList` can test polarity, completeness, and generic flexibility on a cone or a named representative.
- **`NE_SubdivisionCone`** represents cones formed by subdivisions of the effective-curve cone and provides helpers for generating children and obtaining representative cone types. `relint_contains_relint` and `relints_intersect` are relative-interior predicates for rational polyhedral cones.
- **`Finder`** searches cylinder collections on the polarization cones of a surface. It accepts optional construction names and optional recommended coverings.
- **`generate_surface(line)`, `generate_surfaces(degree)`, and `Lubbes_lines()`** parse and expose the bundled `Lubbes_list.txt` data. `generate_surfaces` yields the entries matching the requested degree.

Curve classes use coordinates in the basis `L, E_0, E_1, ...`; the intersection form is diagonal with entries `1, -1, -1, ...`. `Surface.dot(a, b)` computes the intersection product. The blow-up point indices used by `WeakDependencies` start at zero.

## Cylinder construction names

Pass construction names to `CylinderGenerator.all_cylinders(surface, constructions)` or `Finder(..., constructions=...)`. Names recognized by the generator are:

| Name | Construction | Degree condition in the generator |
| --- | --- | --- |
| `LL` | Searches pairs of line classes on a contraction to the plane. | No explicit degree guard in this dispatch. |
| `QT` | Searches conic/line (tangent) configurations on a contraction to the plane. | No explicit degree guard in this dispatch. |
| `lines` | Lines through specified blown-up points. | No explicit degree guard in this dispatch. |
| `lines2` | A pencil from two lines through pairs of blown-up points. | Degree at most 5. |
| `tangent` | Conic-and-tangent configurations. | Degree at least 3. |
| `P1xP1` | A construction using a `P1 x P1` fibration. | Degrees 3 through 7. |
| `cuspcubic` | A cuspidal-cubic construction. | Degree 2. |

These are dispatch conditions, not a guarantee that every construction is applicable to every weak surface. `CylinderGenerator.all_cylinders` first ranges over the surface's generated contractions and then applies the requested constructions.

## Weak surfaces and bundled data

`WeakDependencies` records the point configurations used to describe weak surfaces: `collinear_triples`, `infinitesimal_chains`, `sixs_on_conic`, and `cusp_cubics`. For example:

```python
from delPezzo import Surface, WeakDependencies

dependencies = WeakDependencies(collinear_triples=[[0, 1, 2]])
S = Surface(6, dependencies=dependencies)
```

The repository includes `src/delPezzo/Lubbes_list.txt`, which is read by the `generate_surface` and `generate_surfaces` helpers. For example:

```python
from delPezzo import generate_surfaces

degree_four_surfaces = list(generate_surfaces(4))
```

## Tests

Run the test suite from the repository root with SageMath's Python, as shown above. Tests are under `tests/` and exercise surface classes, cones and subdivisions, cylinder constructions, contractions, and parsing of the bundled data. Some tests are explicitly marked as skipped in the source.

## References

The code's bibliography is in [`bibliography.rst`](bibliography.rst). The package description and surface model follow the work cited there, including Alexander Perepechko, [“Generic flexibility of affine cones over del Pezzo surfaces in Sagemath”](https://arxiv.org/abs/2305.06462). Related references in that file cover cylinders on del Pezzo surfaces and flexibility of affine cones.
