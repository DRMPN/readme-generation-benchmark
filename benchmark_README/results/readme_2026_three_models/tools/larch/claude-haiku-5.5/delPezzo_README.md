# delPezzo-t_5yhss8

> **Note:** This README was written from the file listing alone, without access to the source code. Module descriptions are inferred from file names and should be checked against the actual code. Sections marked **[TODO]** need details from the author.

## Overview

`delPezzo-t_5yhss8` is a Python project for working with **del Pezzo surfaces**, the smooth (and some singular) projective rational surfaces with ample anticanonical class, classified by degree $d = K_S^2 \in \{1, \dots, 9\}$. The codebase appears to cover:

- Representing del Pezzo surfaces of various degrees and their structure (blow-ups, contractions, cones, cylinders).
- Degree-specific tests for degrees 1 through 6, including weak del Pezzo surfaces of degree 6.
- Parsing and handling of a list of surfaces from Lubbes's classification (`Lubbes_list.txt`, `Lubbes_parse.py`).
- A search routine (`finder.py`) for locating surfaces or configurations with given properties.
- Literature references in `bibliography.rst`.

## Project Structure

```
delPezzo-t_5yhss8/
├── __init__.py            # Package initialisation
├── surface.py             # Core surface class / data structure
├── finder.py              # Search for surfaces or configurations
├── cone.py                # Cone-type constructions
├── cylinder.py            # Cylinder-type constructions
├── Lubbes_parse.py        # Parser for the Lubbes classification data
├── Lubbes_list.txt        # Data file: list of surfaces (Lubbes)
├── bibliography.rst       # References
├── tests.ipynb            # Jupyter notebook with worked examples/tests
├── pyproject.toml         # Build and packaging configuration
└── test_*.py              # Test suite (see below)
```

### Source modules

| File | Inferred purpose |
|------|------------------|
| `__init__.py` | Makes the directory an importable package. |
| `surface.py` | Core representation of del Pezzo surfaces: degree, blow-up data, and related invariants. |
| `finder.py` | Search routines for surfaces or configurations meeting given criteria. |
| `cone.py` | Constructions and checks for conic-bundle or cone-type surfaces. |
| `cylinder.py` | Constructions and checks for cylinder-type surfaces. |
| `Lubbes_parse.py` | Reads `Lubbes_list.txt` and converts entries into project objects. |

### Data

- **`Lubbes_list.txt`**: a plain-text list of surfaces taken from the Lubbes classification. **[TODO]** Document the format (columns, encoding of blow-up points or Picard lattice data).

### Documentation

- **`bibliography.rst`**: references for the mathematics and algorithms used. **[TODO]** Add a summary of the key sources.
- **`tests.ipynb`**: a notebook of examples and interactive checks, useful as a tutorial.

## Installation

The project is configured with `pyproject.toml`. From the project root:

```bash
pip install .
```

For development, install in editable mode:

```bash
pip install -e .
```

**[TODO]** Confirm the Python version requirement and list runtime dependencies (e.g. NumPy, SymPy, or other algebra libraries).

## Usage

**[TODO]** Replace the examples below with the actual API. The following shows the intended style only:

```python
from delPezzo import surface
from delPezzo.Lubbes_parse import load_lubbes_list

# Load the classification data
surfaces = load_lubbes_list("Lubbes_list.txt")

# Inspect a surface
S = surfaces[0]
print(S)
```

For a fuller walkthrough, open `tests.ipynb` in Jupyter:

```bash
jupyter notebook tests.ipynb
```

## Testing

The test suite uses `pytest` and is organised by topic:

| Test file | Covers |
|-----------|--------|
| `test_surface.py` | Core surface class |
| `test_finder.py` | Search routines |
| `test_contraction.py` | Contraction of curves |
| `test_blowups.py` | Blow-up constructions |
| `test_various.py` | Miscellaneous checks |
| `test_Lubbes.py` | Lubbes data parsing and consistency |
| `test_weak_deg6.py` | Weak del Pezzo surfaces of degree 6 |
| `test_deg1.py` ... `test_deg5.py` | Surfaces of degrees 1 to 5 |
| `test_deg2.py`, `test_deg2_B2.py`, `test_deg2_KimPark.py` | Degree 2 surfaces, including specific subcases (B2 and Kim–Park) |
| `test_deg3.py`, `test_deg4.py`, `test_deg5.py` | Degrees 3 to 5 |

Run the full suite from the project root:

```bash
pytest
```

Run a single module:

```bash
pytest test_deg2.py -v
```

## Mathematical Background

A **del Pezzo surface** of degree $d$ is a smooth projective surface $S$ over an algebraically closed field with $-K_S$ ample and $K_S^2 = d$. Standard facts used throughout:

- For $1 \le d \le 9$, $S$ is either $\mathbb{P}^2$ blown up in $9-d$ points in general position, or $\mathbb{P}^1 \times \mathbb{P}^1$ (degree 8).
- The **(-1)-curves** (lines) are the key combinatorial objects; their configuration determines the automorphism group and the moduli structure.
- **Weak del Pezzo surfaces** allow $-K_S$ to be nef and big rather than ample, which is why the degree 6 weak case is tested separately.
- Degree 2 surfaces are double covers of $\mathbb{P}^2$ branched along a quartic, and degree 1 surfaces are double covers of the quadric cone branched along a sextic section.

**[TODO]** Check these statements against the conventions used in the code, especially any field assumptions and whether singular or weak surfaces are included.

## Bibliography

See `bibliography.rst` for full references. **[TODO]** List the main works here, for example:

- Lubbes's classification of del Pezzo surfaces (source of `Lubbes_list.txt`).
- Kim and Park on degree 2 del Pezzo surfaces (`test_deg2_KimPark.py`).
- Standard references on del Pezzo surfaces, such as Manin's *Cubic Forms* and Dolgachev's *Classical Algebraic Geometry*.

## Contributing

1. Fork the repository and create a feature branch.
2. Add or update tests for any change in behaviour.
3. Run `pytest` before opening a pull request.
4. **[TODO]** Add style guidelines (formatter, linter, docstring convention).

## License

**[TODO]** Specify the license and copyright holder.

## Acknowledgements

**[TODO]** Credit contributors and any external data sources.

---

If you paste the contents of the main modules (especially `surface.py`, `finder.py`, and `Lubbes_parse.py`), `pyproject.toml`, and a few test files, I can replace the inferred descriptions with accurate ones and fill in the Usage, Installation, and Bibliography sections.
