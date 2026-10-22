# ride_pfa

---

[![PyPi](https://badge.fury.io/py/ride_pfa.svg)](https://badge.fury.io/py/ride_pfa)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![networkx](https://img.shields.io/badge/NetworkX-blue.svg?style=flat-square)
![osmnx](https://img.shields.io/badge/OSMnx-purple.svg?style=flat-square)
![scipy](https://img.shields.io/badge/SciPy-8CAAE6.svg?style=flat-square&logo=scipy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E.svg?style=flat-square&logo=scikitlearn&logoColor=white)
![folium](https://img.shields.io/badge/Folium-77B829.svg?style=flat-square&logo=Folium&logoColor=white)
![numpy](https://img.shields.io/badge/NumPy-013243.svg?style=flat-square&logo=NumPy&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458.svg?style=flat-square&logo=pandas&logoColor=white)
![python](https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=black)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Benchmarks](#benchmarks)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This project is a Python library for shortest-path search on OpenStreetMap road networks, using graph community detection (clustering) to accelerate path finding relative to a plain Dijkstra baseline. It is aimed at researchers and developers working on routing or graph algorithms who are comfortable with Python. The library provides a programmatic API for loading OSM city graphs, clustering road networks into communities, building a coarsened centroid graph, and running several path-finding algorithms, along with mapping-based visualization. Example notebook workflows cover general usage, heuristic search, and benchmarking against a Dijkstra baseline; see Getting Started for runnable steps.

---

## Core Features

*   **OSM Graph Ingestion:** Load large-scale, real-world road networks directly from OpenStreetMap data. This capability enables rigorous testing and benchmarking of routing algorithms against metropolitan-sized graphs.
*   **Hierarchical Graph Acceleration:** Uses community detection (e.g., Louvain, K-means) to cluster nodes and construct a coarse centroid graph. This significantly reduces computational complexity for shortest path searches on massive networks.
*   **Advanced Pathfinding Core:** Supports multiple pathfinding strategies, ranging from standard Dijkstra implementations to optimized heuristic and extraction-based algorithms. This allows for comparative performance analysis between routing techniques.
*   **Geospatial Visualization:** Provides integrated tools for visualizing both the underlying network structure and the resulting optimized paths on interactive maps.

---

## Installation

**Prerequisites:** Python ^3.10 (per `pyproject.toml`)

### From PyPI

If the package is published on PyPI, install it with:

```sh
pip install ride_pfa
```

### From source

From a local checkout of the repository, install with Poetry (uses `pyproject.toml` / `poetry.lock`):

```sh
poetry install
```

Alternatively, install the dependencies from `requirements.txt`:

```sh
pip install -r requirements.txt
```

---

## Getting Started

### Prerequisites

- Python >= 3.10 (per `pyproject.toml`)
- Dependencies installed via Poetry (`pyproject.toml` / `poetry.lock`) or from `requirements.txt`, including networkx, osmnx, scipy, scikit-learn, matplotlib, and folium
- Jupyter (ipykernel) if you want to run the example notebooks

### Quickstart

1. Install ride_pfa and its dependencies (see [Installation](#installation)).
2. The core workflow — load a city graph, cluster it, build the coarsened centroid graph, and run path finding:

```python
from ride_pfa import graph_osm_loader
import ride_pfa.centroid_graph.centroids_graph_builder as cgb
import ride_pfa.path_finding as pfa
import ride_pfa.clustering as cls
import ride_pfa.utils as utils

# Download an OSM city graph (e.g. Paris)
g = graph_osm_loader.get_graph(graph_osm_loader.osm_cities_example['Paris'])

# Inverse edge weights improve Louvain clustering
utils.add_inverse_edges_weight(g, weight='length', inverse_weight='inverse')

# Cluster the graph and build the centroid graph
cms_resolver = cls.LouvainKMeansCommunityResolver(
    resolution=1, weight='inverse', k_means_weight='length'
)
cg = cgb.CentroidGraphBuilder().build(g, cms_resolver)

# Compare Dijkstra on the full graph vs. extraction-based hierarchical search
baseline = pfa.Dijkstra(g)
test_alg = pfa.ExtractionPfa(
    g=g, upper=pfa.Dijkstra(cg.g), down=pfa.Dijkstra(g), cluster='cluster'
)

nodes = list(g.nodes())
s, t = nodes[0], nodes[15]
cost, path = baseline.find_path(s, t)
extraction_cost, extraction_path = test_alg.find_path(s, t)
```

3. For an annotated end-to-end procedure — timing the centroid-graph build, running the A* heuristic variant, and comparing against Dijkstra — see the [Benchmarks](#benchmarks) section. Runnable notebooks with folium/matplotlib visualization are listed under [Examples](#examples).

---

## Benchmarks

The package ships with benchmark tooling — a `ride_pfa/benchmark.py` module, a `data/results` directory, and example notebooks covering general usage, heuristics, and benchmarking — but no measured figures are reproduced in this document. Run the procedure below (as demonstrated in the example notebooks under [examples/](./examples)) to obtain numbers on your own hardware.

### Reproducible procedure

```python
from ride_pfa import graph_osm_loader
import ride_pfa.centroid_graph.centroids_graph_builder as cgb
import ride_pfa.path_finding as pfa
import ride_pfa.clustering as cls
import ride_pfa.utils as utils

# 1. Load a city graph; pass cache_path to reuse a local pickle across runs
g = graph_osm_loader.get_graph(
    graph_osm_loader.osm_cities_example['Paris'],
    cache_path='data/cache',
)

# 2. The example uses inverse edge weights for Louvain clustering
utils.add_inverse_edges_weight(g, weight='length', inverse_weight='inverse')

# 3. Resolve communities, build the centroid graph, and time the construction
cms_resolver = cls.LouvainKMeansCommunityResolver(
    resolution=1, weight='inverse', k_means_weight='length'
)
builder = cgb.CentroidGraphBuilder()
t_build, cg = utils.get_execution_time(
    lambda: builder.build(g, cms_resolver), iterations=1
)

# 4. Compare against the Dijkstra baseline
baseline = pfa.Dijkstra(g)
extraction = pfa.ExtractionPfa(
    g=g, upper=pfa.Dijkstra(cg.g), down=pfa.Dijkstra(g), cluster='cluster'
)
nodes = list(g.nodes())
s, t = nodes[0], nodes[15]
cost_base, path_base = baseline.find_path(s, t)
cost_ext, path_ext = extraction.find_path(s, t)

# 5. Heuristic variant
astar = pfa.MinClusterDistanceBuilder(workers=2).build_astar(g, cms_resolver)
cost_astar, path_astar = astar.find_path(s, t)
```

Replace `LouvainKMeansCommunityResolver` with `cls.LouvainCommunityResolver(...)` to benchmark plain Louvain clustering.

### What is measured

- **Preprocessing time.** `utils.get_execution_time(callable, iterations=N)` returns the elapsed time together with the callable's result; the example times a single centroid-graph build with `iterations=1`.
- **Path cost vs. baseline.** `find_path` returns the path cost and the path itself; the notebooks compare this cost against `pfa.Dijkstra` for the same origin/destination pair. This is a correctness cross-check, not a published accuracy or speedup figure.

### Available test cities

`graph_osm_loader.osm_cities_example` provides ready-to-use OSM relation IDs:

| City | OSM ID |
| --- | --- |
| Barcelona | `R347950` |
| Paris | `R71525` |
| Prague | `R435514` |
| Moscow | `R2555133` |
| Singapore | `R17140517` |
| Berlin | `R62422` |
| Rome | `R41485` |
| Rio | `R2697338` |
| Delhi | `R1942586` |

### Notes

- The initial graph download goes through osmnx and requires network access; use the `cache_path` argument of `get_graph` to store the graph locally for repeatable runs.
- All timings are hardware- and environment-dependent; treat any figures you obtain as specific to your setup.
- API names, signatures, and the city IDs above (e.g., `LouvainKMeansCommunityResolver`, `ExtractionPfa`, `get_execution_time`, `osm_cities_example`) should be confirmed against the repository source before scripting against them.

---

## Examples

Runnable notebooks are available in [examples/](./examples):

- **`examples.ipynb`** — general usage: loading a city OSM graph, clustering it, building the centroid graph, and comparing Dijkstra with the extraction-based hierarchical search, including folium/matplotlib visualization.
- **`heuristic_example.ipynb`** — heuristic search on the clustered graph using the min-cluster-distance A* builder.
- **`benchmark_examples.ipynb`** — benchmarking the path-finding algorithms against a Dijkstra baseline.

---

## Contributing

Contributions are welcome:

- Open an issue to report a bug or propose a feature.
- Submit a pull request with a focused change, keeping the code style consistent with the existing modules.
- If your change affects path finding, clustering, or benchmarking, re-run the relevant notebook in [examples/](./examples) to confirm behavior.

---

## License

This project is distributed under the Apache 2.0 License. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use ride_pfa in your research, please cite it using a template such as the one below, filling in the author(s), year, and canonical repository URL from the project metadata.

### APA format:

    <Authors> (<Year>). ride_pfa [Computer software]. <Repository URL>

### BibTeX format:

    @misc{ride_pfa,
        author = {<Authors>},
        title = {ride_pfa},
        year = {<Year>},
        url = {<Repository URL>}
    }

---
