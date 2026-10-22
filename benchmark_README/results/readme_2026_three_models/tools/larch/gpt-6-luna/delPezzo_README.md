# Del Pezzo Surfaces

A Python project for exploring computational questions about del Pezzo surfaces and related algebraic geometry. The repository includes modules for surfaces, cones, cylinders, and finding or parsing classification data, alongside tests covering several degrees and geometric operations.

## Contents

| File | Purpose |
|---|---|
| `surface.py` | Surface-related functionality |
| `cone.py` | Cone-related functionality |
| `cylinder.py` | Cylinder-related functionality |
| `finder.py` | Search or discovery functionality |
| `Lubbes_parse.py` | Parsing utilities for Lubbes-related data |
| `Lubbes_list.txt` | Lubbes-related classification data |
| `bibliography.rst` | Bibliographic references |
| `test_*.py` | Tests for surfaces, contractions, blowups, and examples by degree |
| `tests.ipynb` | Jupyter notebook for exploratory work |
| `pyproject.toml` | Project and build configuration |

The test suite includes cases for degrees 1 through 6, as well as topics such as contractions, blowups, weak degree-6 surfaces, and degree-2 examples.

## Requirements

The project’s Python version and dependencies are defined in `pyproject.toml`. Check that file for the supported Python version and any installation requirements.

## Installation

From the repository root, install the project in editable mode:

```bash
python -m pip install -e .
```

If you do not need an installation, you can also work directly from a checkout by running commands from the repository root.

## Running the tests

Run the full test suite with:

```bash
python -m pytest
```

Run an individual test module, for example:

```bash
python -m pytest test_surface.py
```

The tests are the best reference for concrete examples of the project’s current interfaces and expected behavior.

## Exploring the code

Start with `surface.py` for surface-related code, then consult `cone.py`, `cylinder.py`, and `finder.py` for related functionality. For the classification data, see `Lubbes_list.txt` and its parser, `Lubbes_parse.py`.

The repository also includes an exploratory notebook:

```bash
jupyter notebook tests.ipynb
```

You may need to install Jupyter separately if it is not already available in your environment.

## References

See [`bibliography.rst`](bibliography.rst) for references. The Lubbes-related data files are included in the repository; consult their contents and the bibliography when using or interpreting that data.

## Notes

This README describes the repository at a high level. For exact function signatures, input formats, and mathematical conventions, refer to the source code and tests.
