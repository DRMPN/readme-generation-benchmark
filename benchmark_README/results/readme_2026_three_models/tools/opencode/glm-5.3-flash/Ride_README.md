# RIDE

![RIDE logo](images/Ride_Logo-05.png)

`ride_pfa` is a Python library for fast path finding on road networks. It loads drivable street networks from OpenStreetMap, partitions them into communities (Louvain / Louvain + K-Means), and builds a higher-level *centroid graph* that is used to accelerate shortest-path queries — either through hierarchical "extraction" search or an A* heuristic based on minimum inter-cluster distances. A benchmark module measures how a candidate algorithm compares to a baseline such as Dijkstra in terms of speed-up and path-length error.

## Features

- **Classic shortest-path algorithms** on `networkx` graphs: `Dijkstra`, `BiDijkstra` (bidirectional) and `AStar` with a pluggable heuristic.
- **Cluster-restricted search**: every algorithm can be limited to a set of allowed clusters via the `cluster` node attribute.
- **Hierarchical (extraction) path finding**: `ExtractionPfa` first finds a cluster sequence on a small upper-level graph, then runs the low-level search only inside those clusters.
- **Heuristic path finding**: `MinClusterDistanceBuilder` builds an A* whose heuristic is the minimum distance between the clusters of the two nodes.
- **Graph clustering**: Louvain and a Louvain + K-Means combination, with utilities to write cluster labels back onto graph nodes.
- **Centroid graph construction**: a compact higher-level graph where each cluster is represented by its barycenter.
- **OSM integration**: download a city's drive network by OSM relation id, with optional pickle caching.
- **Benchmarking**: compare two path-finding algorithms on many origin–destination pairs (relative path-length error and acceleration).
- **Visualization**: matplotlib and folium drawing of graphs, communities and paths.
- **Delivery-focused clustering heuristics**: angle clustering, spherical medoids and radial clustering.

## Requirements

- Python `>= 3.10`
- Core dependencies: `networkx`, `osmnx`, `numpy`, `scipy`, `scikit-learn`, `kmedoids`, `folium`, `matplotlib`, `geopandas`, `ortools`, `tqdm`, `requests`, `contextily` (see `pyproject.toml` for the full list)

## Installation

From the repository root:

```bash
pip install -r requirements.txt
```

or, using [Poetry](https://python-poetry.org/):

```bash
poetry install
```

The example notebooks add the repository root to `sys.path`, so you can also simply run them from the `examples/` directory without installing the package.

## Quick start

The snippet below follows `examples/examples.ipynb` and `examples/benchmark_examples.ipynb`:

```python
from ride_pfa import graph_osm_loader
import ride_pfa.centroid_graph.centroids_graph_builder as cgb
import ride_pfa.clustering as cls
import ride_pfa.path_finding as pfa
import ride_pfa.utils as utils

# 1. Download a city street network from OSM (relation ids for several cities
#    are available in graph_osm_loader.osm_cities_example)
g = graph_osm_loader.get_graph(graph_osm_loader.osm_cities_example['Paris'])

# 2. Cluster the graph. Louvain uses the inverse edge length as its weight,
#    K-Means uses the plain length
utils.add_inverse_edges_weight(g, weight='length', inverse_weight='inverse')
cms_resolver = cls.LouvainKMeansCommunityResolver(
    resolution=1, weight='inverse', k_means_weight='length'
)

# 3. Build the higher-level centroid graph
cg = cgb.CentroidGraphBuilder().build(g, cms_resolver)

# 4. Pick two nodes and run path finding
nodes = list(g.nodes())
s, t = nodes[0], nodes[15]

baseline = pfa.Dijkstra(g)
extraction = pfa.ExtractionPfa(
    g=g,
    upper=pfa.Dijkstra(cg.g),   # search on the centroid graph
    down=pfa.Dijkstra(g),       # search on the original graph
    cluster='cluster',
)

length, path = extraction.find_path(s, t)      # -> (cost, [node, node, ...])
baseline_length, baseline_path = baseline.find_path(s, t)
```

### Heuristic A*

```python
astar = pfa.MinClusterDistanceBuilder(workers=4).build_astar(g, cms_resolver)
heuristic_length, heuristic_path = astar.find_path(s, t)
```

### Benchmarking

```python
import ride_pfa.benchmark as bench

points = utils.generate_points(g, num=100)
stat = bench.PfaComparator(
    baseline=baseline,
    test_algorithm=extraction,
    points=points,
    workers=4,
).compare()

print(stat)  # path-length error (%) and acceleration vs the baseline
```

### Visualization

```python
import ride_pfa.drawer as dw
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(15, 15))
dw.draw_paths_matplotlib(
    g,
    [(baseline_path, 'red'), (path, 'green')],
    ax=ax,
)
plt.show()

m = dw.draw_graph_folium(g)                 # interactive map
m = dw.draw_path_folium(g, path, m=m, color='red')
```

## API overview

### Path finding (`ride_pfa.path_finding`)

All algorithms implement the `PathFinding` interface. `find_path(start, end)` returns a `(length, path)` tuple, where `path` is a list of node ids.

| Class | Description |
| --- | --- |
| `Dijkstra` | Classic Dijkstra search. |
| `BiDijkstra` | Bidirectional Dijkstra. |
| `AStar` | A* with a custom heuristic `h(u, v)`. |
| `ExtractionPfa` | Two-level search: a path over the upper (centroid) graph yields a cluster sequence that restricts the low-level search. |
| `PathFindingAdvanced` | Dijkstra terminated early once all requested target nodes are settled (`find_distance_to_all`). |
| `MinClusterDistanceBuilder` | `HeuristicBuilder` that precomputes minimum distances between cluster pairs (in parallel) and returns an `AStar` using them as a heuristic. |

Cluster-restricted search is exposed through `find_path_cls(start, end, cms)`, where `cms` is a set of cluster ids; nodes whose `cluster` attribute is not in `cms` are ignored. If no path exists, `RidePathNotFoundException` (from `ride_pfa.exceptions`) is raised.

### Clustering (`ride_pfa.clustering`)

- `LouvainCommunityResolver` — Louvain community detection (via `networkx`), configured by `weight`, `resolution` and `seed`.
- `LouvainKMeansCommunityResolver` — Louvain followed by an iterative K-Means refinement around cluster barycenters.
- `validate_cms` — splits communities into connected components and writes the resulting cluster index into each node's `cluster` attribute (this attribute is what the cluster-restricted algorithms rely on).

### Centroid graph (`ride_pfa.centroid_graph`)

`CentroidGraphBuilder.build(g, cms)` returns a `CentroidGraph` with:

- `g` — the upper-level graph: one node per cluster (the cluster barycenter), edges between neighbouring clusters weighted by the shortest distance between their centroids;
- `cls2c` — cluster id → centroid node id;
- `cls2n` — cluster id → set of neighbouring clusters;
- `cls2hubs` — cluster id → nodes that are adjacent to other clusters;
- `cms` — the communities themselves.

### Delivery clustering heuristics (`ride_pfa.heuristics`)

Helpers for clustering requests/deliveries that start from a common hub; each writes labels into node attributes:

- `angle_clustering` — HDBSCAN over the angle of each node with respect to the hub (`angle_cluster` attribute);
- `spherical_medoids` — k-medoids over pairwise angular distances (`spherical_cluster` attribute);
- `radial_clustering` — HDBSCAN over the length of deliveries leaving the hub (`radial_cluster` attribute).

These functions require the graph nodes to carry `x`/`y` coordinate attributes.

### OSM loading (`ride_pfa.graph_osm_loader`)

- `get_graph(city_id, cache_path=None)` — downloads the `drive` network inside an OSM relation boundary (via `osmnx`), converts it to an undirected `networkx.Graph` with `length` edge weights and `x`/`y` node coordinates, removes self-loops and optionally pickles the result under `cache_path`.
- `osm_cities_example` — OSM relation ids for Barcelona, Paris, Prague, Moscow, Singapore, Berlin, Rome, Rio and Delhi.

### Benchmarking (`ride_pfa.benchmark`)

- `PfaComparator(baseline, test_algorithm, points, workers, iterations)` — runs both algorithms on a list of origin–destination pairs (in parallel) and collects `Statistics`.
- `Statistics` — aggregates path lengths and timings; `get_err()` returns the relative path-length error of the test algorithm (in %), `get_acceleration()` returns baseline time divided by test time, and `repr()` prints a summary (min/median/mean/max).

### Visualization (`ride_pfa.drawer`)

- `draw_graph_matplotlib`, `draw_paths_matplotlib` — static plots, optionally colouring nodes by community;
- `draw_graph_folium`, `draw_path_folium` — interactive folium maps.

### Utilities (`ride_pfa.utils`)

- `get_optimal_clusters_number(nodes)` — an estimated number of clusters for a graph with the given number of nodes;
- `add_inverse_edges_weight(g, weight, ...)` — adds `1 / (weight + eps)` as a new edge attribute (useful as a Louvain weight);
- `generate_points(graph, num)` — random origin–destination pairs for benchmarking;
- `get_execution_time(func, iterations, ...)` — average execution time of a callable.

## Repository structure

```
.
├── ride_pfa/                  # the library
│   ├── graph_osm_loader.py    # OSM network loading and caching
│   ├── clustering/            # Louvain / Louvain + K-Means community detection
│   ├── centroid_graph/        # higher-level centroid graph construction
│   ├── path_finding/          # Dijkstra, BiDijkstra, A*, extraction and heuristic PFA
│   ├── heuristics.py          # delivery clustering heuristics (HDBSCAN, k-medoids)
│   ├── benchmark.py           # PfaComparator / Statistics
│   ├── drawer/                # matplotlib and folium visualization
│   ├── utils.py               # helper utilities
│   └── exceptions.py          # RideException, RidePathNotFoundException
├── examples/                  # Jupyter notebooks with end-to-end usage
│   ├── examples.ipynb         # extraction and heuristic path finding
│   ├── benchmark_examples.ipynb
│   └── heuristic_example.ipynb
├── data/                      # sample data (random_points.csv, pickled results)
├── images/                    # logos and illustrative figures
├── pyproject.toml             # Poetry project definition
├── requirements.txt           # pinned dependencies (exported from Poetry)
├── poetry.lock
├── .readthedocs.yml           # Read the Docs build configuration (Sphinx)
└── LICENSE                    # Apache License 2.0
```

## License

This project is licensed under the [Apache License 2.0](LICENSE).
