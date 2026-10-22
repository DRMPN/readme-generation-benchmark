# Ride (`ride_pfa`)

![Ride logo](images/Ride_Logo-05.png)

`ride_pfa` is a Python library for shortest-path search on road networks. Besides classic graph search (Dijkstra, bidirectional Dijkstra, A*), it provides a cluster-based approach: the graph is partitioned into communities, a smaller "centroid graph" is built over those communities, and a path is first found on the centroid graph and then refined on the original graph, restricted to the clusters that the coarse path passes through. Road graphs for cities are loaded from OpenStreetMap through `osmnx`.

The package is at version `0.1.2` and is licensed under the Apache License 2.0 (see [LICENSE](LICENSE)).

## Features

- **Path finding** (`ride_pfa.path_finding`)
  - `Dijkstra`: single-source Dijkstra with early exit at the target.
  - `BiDijkstra`: bidirectional Dijkstra.
  - `AStar`: A* with a user-supplied heuristic `h(u, v)`. With the default heuristic (always 0) it behaves like Dijkstra.
  - `ExtractionPfa`: two-level search. It finds a path between the clusters of the start and end nodes on an upper graph (typically the centroid graph), then runs a lower-level search on the original graph limited to the clusters on that path.
  - `MinClusterDistanceBuilder`: builds an `AStar` instance whose heuristic is a precomputed matrix of minimum distances between clusters.
- **Community detection** (`ride_pfa.clustering`)
  - `LouvainCommunityResolver`: Louvain community detection via `networkx`.
  - `LouvainKMeansCommunityResolver`: Louvain followed by K-means-style refinement based on community barycenters.
  - Resolvers can write each node's cluster ID into a node attribute (default `cluster`).
- **Centroid graph** (`ride_pfa.centroid_graph`)
  - `CentroidGraphBuilder`: builds a graph with one node per cluster (the barycenter node of the cluster) and edges between neighboring clusters, weighted by the shortest distance between their centroids.
- **Node-attribute clustering heuristics** (`ride_pfa.heuristics`)
  - `angle_clustering`: HDBSCAN on the angle of each node relative to a central node.
  - `spherical_medoids`: clustering by pairwise angles using `kmedoids`.
  - `radial_clustering`: HDBSCAN on the lengths of edges leaving a central node.
  - These functions write cluster labels into node attributes (`angle_cluster`, `spherical_cluster`, `radial_cluster`).
- **OpenStreetMap loading** (`ride_pfa.graph_osm_loader`)
  - `get_graph(city_id, cache_path=None)`: downloads the drivable road network for an OpenStreetMap relation via `osmnx`, removes self-loops, and returns an undirected `networkx.Graph` with `x`/`y` node coordinates and `length` edge weights. Optionally caches the graph as a pickle in `cache_path`.
  - `osm_cities_example`: a dictionary mapping nine city names to OpenStreetMap relation IDs.
- **Utilities** (`ride_pfa.utils`)
  - `add_inverse_edges_weight`: adds an inverse-weight attribute (`1 / (weight + eps)`) to edges.
  - `generate_points`: generates random pairs of distinct nodes for testing.
  - `get_execution_time`: averages the wall-clock time of a function over several runs.
  - `get_optimal_clusters_number`: computes a cluster-count estimate from the number of nodes.
- **Visualization** (`ride_pfa.drawer`)
  - `draw_graph_matplotlib`, `draw_paths_matplotlib`: static plots with `matplotlib`.
  - `draw_graph_folium`, `draw_path_folium`: interactive maps with `folium`.
- **Benchmarking** (`ride_pfa.benchmark`)
  - `PfaComparator`: runs a baseline and a test algorithm on the same point pairs, in parallel, and collects path lengths and run times.
  - `Statistics`: computes the length error (in percent, relative to the baseline) and the speed-up (baseline time divided by test time).

## Installation

Requirements:

- Python 3.10 or newer (as declared in `pyproject.toml`).
- Network access is needed for `graph_osm_loader.get_graph` because it downloads data from OpenStreetMap.

The repository provides two dependency files:

- `pyproject.toml` and `poetry.lock` for Poetry:

  ```bash
  poetry install
  ```

- `requirements.txt` (pinned versions with hashes) for pip:

  ```bash
  pip install -r requirements.txt
  ```

The main dependencies declared in `pyproject.toml` are `ortools`, `geopandas`, `networkx`, `tqdm`, `scipy`, `scikit-learn`, `osmnx`, `requests`, `ipykernel`, `matplotlib`, `furo`, `folium`, `contextily`, and `kmedoids`.

The package is imported as `ride_pfa`. If you do not install it, run your code from the repository root so that `ride_pfa` can be found.

## Quick start

The following example follows [`examples/examples.ipynb`](examples/examples.ipynb):

```python
from ride_pfa import graph_osm_loader
import ride_pfa.centroid_graph.centroids_graph_builder as cgb
import ride_pfa.clustering as cls
import ride_pfa.path_finding as pfa
import ride_pfa.utils as utils

# Download the road network of Paris (OpenStreetMap relation R71525)
g = graph_osm_loader.get_graph(graph_osm_loader.osm_cities_example['Paris'])

# Louvain uses inverse lengths, so that short roads are favored
utils.add_inverse_edges_weight(g, weight='length', inverse_weight='inverse')

# Cluster the graph and build the centroid graph
cms_resolver = cls.LouvainKMeansCommunityResolver(resolution=1, weight='inverse', k_means_weight='length')
cg = cgb.CentroidGraphBuilder().build(g, cms_resolver)

baseline = pfa.Dijkstra(g)
extraction = pfa.ExtractionPfa(
    g=g,
    upper=pfa.Dijkstra(cg.g),
    down=pfa.Dijkstra(g),
    cluster='cluster',
)

nodes = list(g.nodes())
s, t = nodes[0], nodes[15]

length, path = baseline.find_path(s, t)
ext_length, ext_path = extraction.find_path(s, t)
```

Each `find_path(start, end)` call returns a tuple `(length, path)`, where `path` is a list of node IDs. If no path exists, it raises `ride_pfa.exceptions.RidePathNotFoundException`.

A heuristic-based A* search can be built from the same clustering:

```python
heuristic_alg = pfa.MinClusterDistanceBuilder(workers=2).build_astar(g, cms_resolver)
heuristic_length, heuristic_path = heuristic_alg.find_path(s, t)
```

## Benchmarking

`PfaComparator` runs a baseline algorithm and a test algorithm on the same pairs of nodes:

```python
import ride_pfa.benchmark as bench
import ride_pfa.utils as utils

points = utils.generate_points(g, num=100)
stat = bench.PfaComparator(
    baseline=baseline,
    test_algorithm=extraction,
    points=points,
    workers=4,
).compare()

print(stat)              # error and acceleration summary
stat.get_err()           # per-pair length error in percent
stat.get_acceleration()  # per-pair baseline_time / test_time
```

The saved output of `examples/benchmark_examples.ipynb` reports a mean length error of 6.18% and a median acceleration of 6.35x for its run. These numbers come from one notebook run on one city and one set of points, and they are not a general performance claim; results depend on the graph, the clustering parameters, and the hardware.

## Visualization

Static plot with `matplotlib`:

```python
import matplotlib.pyplot as plt
import ride_pfa.drawer as dw

fig, ax = plt.subplots(figsize=(15, 15))
dw.draw_paths_matplotlib(g, [(path, 'red'), (ext_path, 'green')], ax=ax)
plt.show()
```

Interactive map with `folium`:

```python
m = dw.draw_graph_folium(g)
m = dw.draw_path_folium(g, path, m=m)
m = dw.draw_path_folium(g, ext_path, m=m, color='green')
m.save('paths.html')
```

## Repository layout

```
ride_pfa/
  __init__.py
  exceptions.py              RideException, RidePathNotFoundException
  graph_osm_loader.py        OpenStreetMap graph loading and city IDs
  heuristics.py              angle, spherical, and radial clustering helpers
  utils.py                   helper functions (inverse weights, timing, random points)
  benchmark.py               PfaComparator and Statistics
  clustering/
    clustering.py            community resolvers
  centroid_graph/
    centroids_graph_builder.py  CentroidGraphBuilder
  path_finding/
    pfa.py                   base classes (PathFinding, PathFindingCls)
    dijkstra_pfa.py          Dijkstra, BiDijkstra, AStar
    excraction_pfa.py        ExtractionPfa
    heuristic_pfa.py         MinClusterDistanceBuilder
    advenced_pfa.py          PathFindingAdvanced (one-to-many distances)
  drawer/
    matplotlib_drawer.py     static plots
    folium_drawer.py         interactive maps
examples/                    Jupyter notebooks (main example, heuristic, benchmark)
data/                        sample coordinates and saved result files
images/                      logo and figures
```

The `data/random_points.csv` file contains latitude and longitude pairs (column headers in Russian: "Широта" and "Долгота"). The repository's code does not read this file; it is provided as sample data. The `data/results/` folder contains pickle files whose contents are not documented here.

## Known limitations

- The `ride_pfa/drawer` functions `draw_graph_matplotlib` and `draw_graph_folium` iterate over the `cms` argument with `for i, c in cms:`. This does not unpack a list of clusters correctly, so passing a community list to these functions will likely fail. Calling them without `cms` works as intended.
- `get_graph` requires network access to OpenStreetMap and can take a long time on large cities. Use `cache_path` to store the downloaded graph locally. The cache directory must already exist.
- The repository does not include a test suite or a `docs/` directory, although `.readthedocs.yml` refers to `docs/source/conf.py`.

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for the full text.
