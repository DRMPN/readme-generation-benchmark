# ride_pfa

`ride_pfa` is a Python library for path finding on weighted NetworkX graphs. It includes Dijkstra and A* search, community-based graph reduction and path extraction, OSM road-network loading, clustering helpers, route visualization, and benchmark utilities.

## Features

- Find weighted paths with `Dijkstra`, `BiDijkstra`, or `AStar`.
- Resolve graph communities with Louvain clustering, optionally followed by a graph-distance k-means-style refinement.
- Build a centroid graph and use `ExtractionPfa` to search between communities and then within the selected communities.
- Build an A* searcher with a minimum inter-community-distance heuristic.
- Load drive networks for OSM administrative areas using OSMnx.
- Visualize graphs and paths with Matplotlib or Folium, and compare path finders with the benchmark helpers.

## Requirements and installation

The project metadata specifies Python `^3.10` and declares its dependencies in `pyproject.toml`. Install the project and dependencies with Poetry from the repository root:

```bash
poetry install
```

The main dependencies include NetworkX, NumPy, SciPy, scikit-learn, OSMnx, GeoPandas, Matplotlib, Folium, and OR-Tools. The notebooks use Jupyter.

## Basic path finding

Path finders accept a NetworkX graph and, by default, use the edge attribute named `length`. Each call to `find_path(start, end)` returns `(distance, path)`, where `path` is an ordered list of node IDs. The graph must have the requested edge-weight attribute on its edges.

```python
import networkx as nx
from ride_pfa.path_finding import Dijkstra

graph = nx.Graph()
graph.add_edge(1, 2, length=2.0)
graph.add_edge(2, 3, length=3.0)
graph.add_edge(1, 3, length=8.0)

finder = Dijkstra(graph)  # weight="length" by default
distance, path = finder.find_path(1, 3)

print(distance)  # 5.0
print(path)      # [1, 2, 3]
```

Pass a different edge-attribute name as `weight`, for example `Dijkstra(graph, weight="travel_time")`, when the graph uses another cost field. `Dijkstra`, `BiDijkstra`, and `AStar` are available from `ride_pfa.path_finding`. `AStar` accepts a heuristic callable as its `h` argument; its default heuristic is zero.

## Community-based path finding

The package can partition a graph, build a smaller graph whose nodes represent communities, and extract a route by first finding a route on that smaller graph and then searching the corresponding communities in the original graph.

```python
from ride_pfa.clustering import LouvainKMeansCommunityResolver
from ride_pfa.centroid_graph.centroids_graph_builder import CentroidGraphBuilder
from ride_pfa.path_finding import Dijkstra, ExtractionPfa
from ride_pfa.utils import add_inverse_edges_weight

# `graph` is a connected NetworkX graph with `length` on every edge.
# Louvain's clustering weight and the path/centroid distance weight can differ.
add_inverse_edges_weight(graph, weight="length", inverse_weight="inverse")
resolver = LouvainKMeansCommunityResolver(
    weight="inverse",
    k_means_weight="length",
)
centroid_graph = CentroidGraphBuilder().build(graph, resolver)

finder = ExtractionPfa(
    g=graph,
    upper=Dijkstra(centroid_graph.g),
    down=Dijkstra(graph),
    cluster="cluster",
)
distance, path = finder.find_path(start_node, end_node)
```

The resolver writes the community ID to each original graph node's `cluster` attribute by default. `ExtractionPfa` expects this attribute (or the configured `cluster` name) on the original graph. The upper path finder operates on the centroid graph; the lower path finder operates on the original graph. The notebook `examples/examples.ipynb` demonstrates this workflow with an OSM graph.

The clustering module also provides `LouvainCommunityResolver`. `LouvainKMeansCommunityResolver` starts with Louvain communities and iteratively assigns nodes by graph distance to community centers. The centroid graph builder selects a barycenter for each community and connects adjacent communities using weighted graph distances.

## A* with a community-distance heuristic

`MinClusterDistanceBuilder` constructs an A* finder whose heuristic uses precomputed minimum distances between communities. Pass either an `AbstractCommunityResolver` or an already resolved community collection:

```python
from ride_pfa.clustering import LouvainCommunityResolver
from ride_pfa.path_finding import MinClusterDistanceBuilder

resolver = LouvainCommunityResolver()
finder = MinClusterDistanceBuilder(workers=2).build_astar(graph, resolver)
distance, path = finder.find_path(start_node, end_node)
```

This builder uses the default edge-weight name `length` and cluster attribute name `cluster`. Ensure the graph has a usable community assignment; a resolver with its default `write_community=True` writes the cluster attribute when resolving it. The builder's `workers` setting controls multiprocessing for the distance precomputation.

## Loading OSM road graphs

`ride_pfa.graph_osm_loader.get_graph(city_id, cache_path=None)` loads an OSMnx drive network for the administrative area identified by an OSM relation ID. It returns an undirected NetworkX graph with node `x`/`y` coordinates and edge `length` attributes; self-loops are removed. Without a cached graph, loading requires access to the services used by OSMnx. If `cache_path` is supplied, the loader reads or writes a pickle named `<city_id>.pickle` in that directory; the directory must already exist when a new graph is to be cached.

Example:

```python
from ride_pfa.graph_osm_loader import get_graph, osm_cities_example

graph = get_graph(osm_cities_example["Paris"], cache_path="./cache")
```

The IDs defined in `osm_cities_example` are:

| Key | OSM relation ID |
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

`get_graph()` defaults to `R2555133` (Moscow).

## Clustering, visualization, and benchmarks

- `ride_pfa.heuristics` provides `angle_clustering`, `spherical_medoids`, and `radial_clustering` for graphs of delivery/request points. The angle and spherical methods require node `x` and `y` coordinate attributes; these functions add their cluster labels to node attributes.
- `ride_pfa.drawer` provides `draw_graph_matplotlib`, `draw_paths_matplotlib`, `draw_graph_folium`, and `draw_path_folium`. These drawing helpers use node `x`/`y` coordinates. A route is represented as a list of node IDs.
- `ride_pfa.benchmark.PfaComparator` compares a baseline path finder with another finder over supplied `(start, end)` pairs. Its `Statistics` result includes lengths, paths, and timings, with helpers for relative length error and speed ratios.
- `ride_pfa.utils` includes helpers for adding inverse edge weights, generating random node pairs, and timing a callable.

The repository's `examples/` directory contains Jupyter notebooks for the path-finding workflows (`examples.ipynb`), coordinate-based clustering (`heuristic_example.ipynb`), and benchmarks (`benchmark_examples.ipynb`).

## Project layout

```text
ride_pfa/
  clustering/       Community resolvers
  centroid_graph/   Community centroid-graph construction
  drawer/           Matplotlib and Folium visualization
  path_finding/     Path-finder implementations
  benchmark.py      Path-finder comparison utilities
  graph_osm_loader.py
  heuristics.py     Coordinate/radial clustering helpers
  utils.py
examples/           Jupyter notebooks
data/               Example data and saved results
images/             Images used by the examples
```

## License

This project is distributed under the Apache License 2.0; see [`LICENSE`](LICENSE).
