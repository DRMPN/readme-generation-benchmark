# ride_pfa

`ride_pfa` is a Python package for shortest-path finding on road networks loaded from OpenStreetMap. It includes exact baselines (Dijkstra, bidirectional Dijkstra, A*), a cluster-based path-finding approach that uses a community-detection-derived centroid graph, heuristic clustering helpers, a benchmarking utility for comparing path-finding methods, and drawing helpers for Matplotlib and Folium.

## Overview

The package is organized into these modules:

- **`graph_osm_loader`**: Loads drivable street graphs from OpenStreetMap through OSMnx, with a predefined set of example cities.
- **`clustering`**: Community detection with `LouvainCommunityResolver` and `LouvainKMeansCommunityResolver`, which refines Louvain communities with K-means-style reassignment.
- **`centroid_graph`**: `CentroidGraphBuilder` builds a graph of cluster centroids and inter-cluster distances from a clustered road graph.
- **`path_finding`**: Path-finding algorithms:
  - `Dijkstra`, `BiDijkstra`, and `AStar` (in `dijkstra_pfa`)
  - `ExtractionPfa`, which restricts a detailed search to clusters selected by a coarse search on the centroid graph
  - `MinClusterDistanceBuilder`, which builds an A* heuristic from precomputed minimum distances between clusters
  - `PathFindingAdvanced` (in `advenced_pfa`), a helper that computes distances from one node to a set of target nodes
- **`heuristics`**: Clustering functions for delivery-style point sets: `angle_clustering`, `radial_clustering`, and `spherical_medoids`.
- **`benchmark`**: `PfaComparator` runs a baseline and a test path-finding method on the same point pairs and reports length error and speed-up (acceleration).
- **`drawer`**: `draw_graph_matplotlib`, `draw_paths_matplotlib`, `draw_graph_folium`, and `draw_path_folium`.
- **`utils`**: Helpers such as `add_inverse_edges_weight`, `generate_points`, `get_execution_time`, and `get_optimal_clusters_number`.
- **`exceptions`**: `RideException` and `RidePathNotFoundException`, which is raised when no path exists between two nodes.

The example notebooks report a run on the Paris graph. In `benchmark_examples.ipynb`, the cluster-based method built on 105 clusters over 100 random point pairs. Its output reports a route-length error with a maximum of 51.9194%, a minimum of 0.0000%, and a median of 4.7511%. The reported acceleration (baseline time divided by test time) had a median of 6.3546 and a mean of 6.8154.

## Repository Layout

```
ride_pfa/            Package source
examples/            Jupyter notebooks (examples, benchmarks, heuristics)
data/                random_points.csv and cached results (data/results/*.pkl)
images/              Figures used for documentation
pyproject.toml       Poetry project metadata and dependencies
poetry.lock          Locked dependency versions
requirements.txt     Pinned dependencies with hashes
.readthedocs.yml     Read the Docs build configuration
LICENSE              Apache License 2.0
```

## Installation

Requirements:

- Python 3.10 or newer (`pyproject.toml` specifies `^3.10`).
- Internet access if you want to download OpenStreetMap graphs, because `graph_osm_loader` queries OSM through OSMnx.

### Option 1: Poetry

The repository includes `pyproject.toml` (Poetry-compatible, build backend `poetry.core`) and `poetry.lock`:

```bash
poetry install
```

### Option 2: pip with pinned requirements

`requirements.txt` lists pinned versions with hashes:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Main dependencies

From `pyproject.toml`:

- `networkx`, `osmnx`, `geopandas`
- `ortools`, `scipy`, `scikit-learn`, `kmedoids`
- `matplotlib`, `folium`, `contextily`
- `tqdm`, `requests`, `ipykernel`
- `furo` (documentation theme)

## Usage

### Loading a graph

`graph_osm_loader` provides a dictionary of example cities mapped to OpenStreetMap relation IDs. Available keys are `Barcelona`, `Paris`, `Prague`, `Moscow`, `Singapore`, `Berlin`, `Rome`, `Rio`, and `Delhi`.

```python
from ride_pfa import graph_osm_loader

city_id = graph_osm_loader.osm_cities_example['Paris']
g = graph_osm_loader.get_graph(city_id)
```

`get_graph(city_id, cache_path=None)` works as follows:

- If `cache_path` is given and a pickle named `<city_id>.pickle` exists there, the graph is loaded from it.
- Otherwise the graph is downloaded with `geocode_to_gdf` and `graph_from_polygon` (drive network, simplified), then saved to `cache_path` if one was given.
- Self-loop edges are removed before the graph is returned.

Each edge carries a `length` attribute, and each node carries `x` and `y` coordinates.

### Computing a shortest path with a baseline

```python
from ride_pfa import path_finding as pfa

baseline = pfa.Dijkstra(g)
length, path = baseline.find_path(start_node, end_node)
```

`BiDijkstra` and `AStar` follow the same `find_path` interface. `AStar` takes an optional heuristic `h(u, v)`.

### Cluster-based path finding

The workflow in `examples/examples.ipynb` is:

1. Add an inverse-length weight, which the notebook recommends for Louvain clustering:

   ```python
   from ride_pfa import utils
   utils.add_inverse_edges_weight(g, weight='length', inverse_weight='inverse')
   ```

2. Detect clusters and build the centroid graph:

   ```python
   from ride_pfa import clustering as cls
   from ride_pfa.centroid_graph import centroids_graph_builder as cgb

   cms_resolver = cls.LouvainKMeansCommunityResolver(
       resolution=1, weight='inverse', k_means_weight='length')
   cg = cgb.CentroidGraphBuilder().build(g, cms_resolver)
   ```

3. Combine a coarse search on the centroid graph with a detailed search restricted to the selected clusters:

   ```python
   test_alg = pfa.ExtractionPfa(
       g=g,
       upper=pfa.Dijkstra(cg.g),
       down=pfa.Dijkstra(g),
       cluster='cluster',
   )
   length, path = test_alg.find_path(s, t)
   ```

### Benchmarking

`examples/benchmark_examples.ipynb` compares a test method with a baseline over random point pairs:

```python
from ride_pfa import benchmark as bench

points = utils.generate_points(g, num=100)
stat = bench.PfaComparator(
    baseline=baseline,
    test_algorithm=test_alg,
    points=points,
    workers=4,
).compare()
print(stat)
```

`Statistics` provides `get_err()` (percentage difference in path length) and `get_acceleration()` (baseline time divided by test time). `PfaComparator` uses `multiprocessing.Pool` when `workers > 1`, and `iterations` controls how many times each query is timed.

### Heuristic clustering

`examples/heuristic_example.ipynb` shows the functions in `ride_pfa.heuristics`:

```python
from ride_pfa.heuristics import angle_clustering, radial_clustering, spherical_medoids
```

- `angle_clustering(dg, central_node_id, end_nodes=None, min_cluster_size=3)` clusters nodes by their angle around a central node, using HDBSCAN. It writes the labels to the node attribute `angle_cluster`.
- `radial_clustering(dg, central_node_id, len_attrbute='length', min_cluster_size=3)` clusters the lengths of edges leaving the central node. It writes the labels to `radial_cluster`.
- `spherical_medoids(dg, central_node_id, end_nodes=None, kmax=10, kmin=2)` clusters the pairwise angles of direction vectors using k-medoids. It writes the labels to `spherical_cluster`.

All three require nodes with `x` and `y` attributes. Node attributes must be present on the graph before these functions are called.

### Drawing

```python
import matplotlib.pyplot as plt
from ride_pfa import drawer as dw

ax = dw.draw_graph_matplotlib(g)
ax = dw.draw_paths_matplotlib(g, [(path, None)], ax=ax)
plt.show()
```

`draw_graph_folium` and `draw_path_folium` produce interactive Folium maps.

## Configuration

The repository has no configuration file or environment variables for the library itself. Behavior is set through function and class parameters:

| Component | Parameters |
|---|---|
| `get_graph` | `city_id`, `cache_path` |
| `LouvainCommunityResolver` | `weight`, `cluster`, `write_community`, `resolution`, `seed` (default 1534) |
| `LouvainKMeansCommunityResolver` | adds `max_iteration` (default 20), `print_log`, `k_means_weight` |
| `CentroidGraphBuilder` | `log`, `name` (default `'cluster'`), `weight` (default `'length'`) |
| `PfaComparator` | `workers` (default 4), `iterations` (default 4), `print_log` |
| `MinClusterDistanceBuilder` | `workers` (default 4) |

Cluster membership is stored on each node under the attribute named by `cluster` (default `'cluster'`), so the same name must be passed to the path-finding classes that use it.

Read the Docs is configured by `.readthedocs.yml`. It uses Ubuntu 20.04, Python 3.11, installs `requirements.txt` in `post_install`, and points Sphinx at `docs/source/conf.py`. The `docs/` directory is not included in the supplied file tree.

## Data

- `data/random_points.csv` contains random point data for experiments.
- `data/results/R41485.pkl` and `data/results/R62145.pkl` are stored result files. The relation ID `R41485` corresponds to Rome in `osm_cities_example`. The contents of these files are not documented in the repository.

## Development

- Install the dependencies with Poetry (`poetry install`) or pip (`pip install -r requirements.txt`).
- Packages are declared in `pyproject.toml` with `poetry-core` as the build backend.
- Notebooks in `examples/` add the parent directory to `sys.path`, so run them from the `examples/` folder or adjust those paths.
- Development notes are not in the repository. `.gitignore` is present, and the `pyproject.toml` `authors` and `description` fields still hold template placeholders.

## Testing

The supplied file tree contains no test directory and no test configuration. The notebooks in `examples/` show example usage and benchmark results, but they are not automated tests. No testing command is documented.

## License

This project is licensed under the **Apache License, Version 2.0**. See the [LICENSE](LICENSE) file for the full text.

The appendix of the included `LICENSE` file still contains the template placeholders `[yyyy]` and `[name of copyright owner]`, so the copyright holder is not specified in the supplied files.
