# Ride

Ride is a Python project for working with road-network graphs and finding or analysing routes. It includes OpenStreetMap graph loading, graph construction and clustering utilities, several path-finding implementations, route visualisation, and example notebooks.

## Features

- Load road-network data from OpenStreetMap.
- Build and process graphs, including clustering and centroid-based graph construction.
- Experiment with multiple path-finding approaches and heuristics.
- Draw graphs and routes with Folium or Matplotlib.
- Run benchmarks and explore examples in Jupyter notebooks.

## Repository contents

| File or group | Purpose |
|---|---|
| `graph_osm_loader.py` | Utilities for loading graph data from OpenStreetMap. |
| `centroids_graph_builder.py` | Centroid-based graph construction. |
| `clustering.py` | Graph or data clustering utilities. |
| `heuristics.py` | Heuristics used by the path-finding code. |
| `pfa.py`, `advenced_pfa.py`, `dijkstra_pfa.py`, `excraction_pfa.py`, `heuristic_pfa.py` | Path-finding implementations and related utilities. |
| `folium_drawer.py`, `matplotlib_drawer.py` | Graph and route visualisation. |
| `utils.py`, `exceptions.py` | Shared helpers and project exceptions. |
| `benchmark.py` | Benchmarking code. |
| `examples.ipynb`, `heuristic_example.ipynb`, `benchmark_examples.ipynb` | Interactive examples and experiments. |
| `*.pkl`, `random_points.csv` | Data files used by the project. |
| `*.png`, `*.svg` | Images, visualisation outputs, and project artwork. |
| `pyproject.toml`, `poetry.lock`, `requirements.txt` | Project metadata and dependency specifications. |

The exact data formats and module interfaces are best checked in the corresponding source files and notebooks.

## Requirements

The project uses Python. Dependencies are listed in `pyproject.toml` and `requirements.txt`; `poetry.lock` records a Poetry dependency resolution.

Install with Poetry:

```bash
poetry install
```

Or install from the requirements file:

```bash
python -m pip install -r requirements.txt
```

If you use notebooks, install Jupyter as well if it is not already included in the project dependencies:

```bash
python -m pip install jupyter
```

## Getting started

Start by opening one of the example notebooks:

```bash
jupyter notebook
```

Then open `examples.ipynb`, `heuristic_example.ipynb`, or `benchmark_examples.ipynb`. These notebooks are the best starting point for seeing how the project’s graph, routing, and visualisation components fit together.

The repository does not specify a command-line interface. For programmatic use, inspect the relevant module and notebook to find the supported functions, input formats, and expected graph attributes.

## Working with the data

The repository includes pickle files (`R41485.pkl`, `R62145.pkl`) and `random_points.csv`. Their schemas and intended uses are not documented here, so check the loading code and notebooks before relying on particular columns, keys, or graph attributes.

**Security note:** only load pickle files from sources you trust. Unpickling data can execute arbitrary code.

## Visualisation and outputs

The project includes Folium and Matplotlib drawing modules. Depending on the implementation, Folium can be used for interactive map visualisations and Matplotlib for static plots. Existing PNG files appear to be generated figures or project assets; consult the notebooks and drawing modules to identify how they are produced.

## Benchmarking

`benchmark.py` and `benchmark_examples.ipynb` contain benchmarking-related code. Use the notebook to understand the benchmark inputs and how results are measured. Benchmark results may depend on the graph data, machine, and configuration.

## License

See [`LICENSE`](LICENSE) for the terms under which this project is distributed.

## Notes

Some filenames contain apparent spelling variations, such as `advenced_pfa.py` and `excraction_pfa.py`. Use the filenames as they appear in the repository when importing or navigating to those modules.
