# ride_pfa

`ride_pfa` is a Python library for fast path finding on road networks. It provides tools for loading street graphs from OpenStreetMap, clustering graph nodes into communities, building hierarchical "centroid graphs" for accelerated routing, and running or benchmarking a variety of shortest-path algorithms (Dijkstra, bidirectional Dijkstra, A*, and cluster-based extraction methods). It also includes utilities for visualizing graphs and paths with both Matplotlib and Folium.

The project is developed as a research/tooling effort around accelerating point-to-point route queries on large urban road networks.

## Features

- **OSM graph loading** — download street networks for example cities via `ride_pfa.graph_osm_loader`
- **Graph clustering** — partition graph nodes into communities using Louvain or a Louvain + K-means hybrid (`ride_pfa.clustering`)
- **Centroid graph building** — construct a smaller "upper-level" graph of cluster centroids for hierarchical routing (`ride_pfa.centroid_graph`)
- **Path finding algorithms** — including Dijkstra, bidirectional Dijkstra, A* with custom heuristics, and a multi-level extraction-based approach (`ride_pfa.path_finding`)
- **Benchmarking** — compare path finding algorithms on accuracy and acceleration (`ride_pfa.benchmark`)
- **Visualization** — draw graphs, clusters, and paths with Matplotlib or interactive Folium maps (`ride_pfa.drawer`)
- **Utilities** — inverse edge weights, random point generation, execution timing, and more (`ride_pfa.utils`)

## Project Structure

```
ride_pfa/
├── __init__.py
├── benchmark.py                  # Algorithm comparison utilities
├── centroid_graph/
│   └── centroids_graph_builder.py  # CentroidGraph and CentroidGraphBuilder
├── clustering/
│   └── clustering.py             # Community detection (Louvain, Louvain+KMeans)
├── drawer/
│   ├── folium_drawer.py          # Interactive map visualization
│   └── matplotlib_drawer.py      # Static plot visualization
├── exceptions.py                 # Custom exceptions
├── graph_osm_loader.py           # OpenStreetMap graph loading
├── heuristics.py                 # A* heuristic helpers
├── path_finding/
│   ├── advenced_pfa.py           # Advanced distance queries
│   ├── dijkstra_pfa.py           # Dijkstra, BiDijkstra, AStar
│   ├── excraction_pfa.py         # ExtractionPfa (hierarchical routing)
│   ├── heuristic_pfa.py          # Heuristic builders for A*
│   └── pfa.py                    # Base classes and type definitions
└── utils.py                      # General utilities
```

## Installation

### Using Poetry

```bash
git clone <repository-url>
cd ride_pfa
poetry install
```

### Using pip

```bash
pip install -r requirements.txt
```

### Requirements

- Python >= 3.10

Key dependencies include:

| Package       | Purpose                                    |
|---------------|--------------------------------------------|
| `ortools`     | Operations research / optimization          |
| `geopandas`   | Geospatial data handling                    |
| `networkx`    | Graph data structures and algorithms        |
| `osmnx`       | OpenStreetMap graph retrieval               |
| `scikit-learn`| Clustering (K-means)                        |
| `scipy`       | Scientific computing                        |
| `matplotlib`  | Static visualization                        |
| `folium`      | Interactive map visualization               |
| `contextily`  | Basemap tiles for geospatial plots          |
| `kmedoids`    | K-medoids clustering                        |
| `tqdm`        | Progress bars                               |
| `requests`    | HTTP requests                               |

## Quick Start

The following example is based on the `examples/benchmark_examples.ipynb` notebook and demonstrates downloading a graph, building a centroid graph, running path finding, and benchmarking:

```python
import sys
sys.path.append('../')

from ride_pfa import graph_osm_loader
import ride_pfa.centroid_graph.centroids_graph_builder as cgb
import ride_pfa.path_finding as pfa
import ride_pfa.clustering as cls
import ride_pfa.utils as utils
import ride_pfa.benchmark as bench
from ride_pfa.centroid_graph import CentroidGraph

# Download a graph for an example city
id = graph_osm_loader.osm_cities_example['Paris']
g = graph_osm_loader.get_graph(id)

# Add inverse edge weights for better Louvain clustering
utils.add_inverse_edges_weight(g, weight='length', inverse_weight='inverse')

# Build the centroid graph using Louvain + K-means clustering
cms_resolver = cls.LouvainKMeansCommunityResolver(
    resolution=1,
    weight='inverse',
    k_means_weight='length'
)
cg_builder = cgb.CentroidGraphBuilder()
cg = cg_builder.build(g, cms_resolver)

# Set up baseline and test algorithms
baseline = pfa.Dijkstra(g)
test_alg = pfa.ExtractionPfa(
    g=g,
    upper=pfa.Dijkstra(cg.g),
    down=pfa.Dijkstra(g),
    cluster='cluster'
)

# Generate random origin/destination pairs
points = utils.generate_points(g, num=100)

# Compare algorithms
stat = bench.PfaComparator(
    baseline=baseline,
    test_algorithm=test_alg,
    points=points,
    workers=4
).compare()

print(stat)
```

## Usage

### Path Finding Algorithms

All path finding algorithms implement the `PathFinding` or `PathFindingCls` interface and return a `Path` tuple of `(total_length, [node_ids])`.

- **`Dijkstra`** — standard Dijkstra shortest path on the full graph.
- **`BiDijkstra`** — bidirectional Dijkstra, searching from both endpoints simultaneously.
- **`AStar`** — A* search with a pluggable heuristic function `h(u, v)`.
- **`ExtractionPfa`** — hierarchical approach: first finds a path through the centroid (upper-level) graph, then refines it on the lower-level graph constrained to the clusters along the upper path.

### Clustering

The library provides community detection resolvers that partition the graph and annotate nodes with a `cluster` attribute:

- **`LouvainCommunityResolver`** — Louvain modularity-based community detection with configurable `resolution` and `seed`.
- **`LouvainKMeansCommunityResolver`** — extends Louvain with a K-means-like refinement step using graph barycenters, configurable via `max_iteration` and `k_means_weight`.

### Centroid Graph

The `CentroidGraphBuilder` builds a `CentroidGraph` containing:
- `g` — the reduced graph of cluster centroids
- `cls2n` — mapping of each cluster to its neighboring clusters
- `cls2c` — mapping of each cluster to its centroid node
- `cls2hubs` — mapping of each cluster to its boundary (hub) nodes
- `cms` — the community assignment

### Visualization

**Matplotlib:**
```python
from ride_pfa.drawer import draw_graph_matplotlib, draw_paths_matplotlib

draw_graph_matplotlib(g, cms=cms)
draw_paths_matplotlib(g, paths=[(path1, 'red'), (path2, 'blue')])
```

**Folium (interactive):**
```python
from ride_pfa.drawer import draw_graph_folium, draw_path_folium

m = draw_graph_folium(g, cms=cms)
m = draw_path_folium(g, path, m=m, color='red', weight=5)
m
```

## Examples

The `examples/` directory contains Jupyter notebooks demonstrating the library:

- `examples.ipynb` — general usage examples
- `benchmark_examples.ipynb` — benchmarking path finding algorithms against a Dijkstra baseline on real city networks (e.g., Paris)
- `heuristic_example.ipynb` — building and using A* heuristics

## Benchmark Results

The benchmarking module (`ride_pfa.benchmark`) provides `PfaComparator` to evaluate algorithms on:
- **Path error** (`err_max`, `err_min`, `err_median`, `err_mean`) — deviation from the baseline shortest path length
- **Acceleration** (`acceleration_max`, `acceleration_min`, `acceleration_median`, `acceleration_mean`) — speedup factor relative to the baseline

Pre-computed results are stored in `data/results/` as pickle files.

## Configuration

### Clustering Parameters

| Parameter          | Default      | Description                                        |
|--------------------|--------------|----------------------------------------------------|
| `resolution`       | `1`          | Louvain resolution parameter                        |
| `seed`             | `1534`       | Random seed for reproducibility                     |
| `weight`           | `'length'`   | Edge attribute used for community detection         |
| `cluster`          | `'cluster'`  | Node attribute name for storing cluster assignment  |
| `max_iteration`    | `20`         | K-means refinement iterations (LouvainKMeans only)  |
| `k_means_weight`   | `None`       | Weight for K-means step (defaults to `weight`)      |

### Path Finding Parameters

| Parameter | Default     | Description                                    |
|-----------|-------------|------------------------------------------------|
| `weight`  | `'length'`  | Edge attribute used for shortest path costs    |
| `cluster` | `'cluster'` | Node attribute for cluster membership filtering|

### Heuristic Builder

`MinClusterDistanceBuilder` precomputes minimum distances between cluster pairs (optionally in parallel with configurable `workers`) and returns an `AStar` instance using this as the heuristic.

## Documentation

Documentation is configured for [ReadTheDocs](https://readthedocs.org/) via the `.readthedocs.yml` file, using Sphinx with the `furo` theme. The Sphinx configuration is expected at `docs/source/conf.py`.

## Development

To set up a development environment:

1. Clone the repository
2. Install [Poetry](https://python-poetry.org/)
3. Run `poetry install`
4. Activate the virtual environment with `poetry shell`

The project uses `poetry.lock` to ensure reproducible builds. The `pyproject.toml` defines all dependencies and build configuration (backend: `poetry-core`).

Example notebooks append the repository root to `sys.path` to import the package directly from source:

```python
import sys
sys.path.append('../')
```

## Testing

The repository does not include a dedicated test suite. Functional verification is performed through the example notebooks in `examples/`, which exercise the main modules (graph loading, clustering, centroid graph building, path finding, and benchmarking) against real-world data.

Sample data for testing and demonstration is available in:
- `data/random_points.csv` — randomly generated origin/destination points
- `data/results/` — pre-computed benchmark results

## License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for the full license text.

```
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
