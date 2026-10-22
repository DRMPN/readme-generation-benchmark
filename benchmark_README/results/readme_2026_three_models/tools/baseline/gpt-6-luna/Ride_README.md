# ride_pfa

`ride_pfa` is a Python package for graph path finding and cluster-based path-finding experiments. It provides Dijkstra, bidirectional Dijkstra, and A* search; community detection and centroid-graph construction; an extraction-based path-finding method; graph visualization helpers; and a comparator for measuring route-length error and execution-time acceleration.

The examples use NetworkX road graphs downloaded from OpenStreetMap through OSMnx. The repository also includes notebooks for general examples, heuristic clustering, and benchmarking, plus sample data and result files.

## Features

- Load simplified driving graphs for example cities using OpenStreetMap identifiers.
- Find paths with `Dijkstra`, `BiDijkstra`, or `AStar`.
- Detect graph communities using Louvain, with an optional K-means refinement.
- Build a centroid graph and use it to guide extraction-based path finding.
- Build an A* search heuristic from minimum distances between clusters.
- Cluster graph nodes using angle-, spherical-medoid-, or radial-based methods.
- Draw graphs and paths with Matplotlib or Folium.
- Compare a test algorithm with a baseline using generated start/end pairs.

## Requirements

The project specifies Python `^3.10` and declares its dependencies in `pyproject.toml`. These include NetworkX, OSMnx, GeoPandas, SciPy, scikit-learn, OR-Tools, `kmedoids`, Matplotlib, Folium, and supporting packages. `requirements.txt` provides a pinned dependency set for Python 3.10 through Python 3.x.

## Setup

Clone the repository and enter its root directory. Install dependencies using either Poetry or the supplied requirements file:

```bash
poetry install
```

Or, in a Python 3.10+ environment:

```bash
python -m pip install -r requirements.txt
```

To work with the example notebooks, launch Jupyter from the repository root:

```bash
jupyter notebook examples/
```

The notebooks import the package from the repository, so run them with the project files available on the Python path.

## Quick start

The following workflow follows the repository’s benchmark and general examples: load a city graph, attach an inverse edge weight for community detection, build a centroid graph, and compare a baseline route with an extraction-based route.

```python
from ride_pfa import graph_osm_loader
from ride_pfa import utils
from ride_pfa.clustering import LouvainKMeansCommunityResolver
from ride_pfa.centroid_graph import CentroidGraphBuilder
from ride_pfa.path_finding import Dijkstra, ExtractionPfa

# Download the example Paris driving graph.
graph_id = graph_osm_loader.osm_cities_example["Paris"]
g = graph_osm_loader.get_graph(graph_id)

# Create an inverse of the length weight for Louvain clustering.
utils.add_inverse_edges_weight(
    g,
    weight="length",
    inverse_weight="inverse",
)

resolver = LouvainKMeansCommunityResolver(
    resolution=1,
    weight="inverse",
    k_means_weight="length",
)
centroid_graph = CentroidGraphBuilder().build(g, resolver)

baseline = Dijkstra(g)
extraction = ExtractionPfa(
    g=g,
    upper=Dijkstra(centroid_graph.g),
    down=Dijkstra(g),
    cluster="cluster",
)

start, end = list(g.nodes())[0], list(g.nodes())[15]
distance, path = baseline.find_path(start, end)
extraction_distance, extraction_path = extraction.find_path(start, end)
```

`find_path` returns a pair containing the route distance and a list of node identifiers. In this workflow, the resolver writes a `cluster` attribute to graph nodes, which the extraction algorithm uses to identify clusters for its upper-level search.

## Graph loading and input expectations

`graph_osm_loader.get_graph()` accepts a city identifier and an optional cache directory. If a cached pickle for that identifier is present, it is loaded; otherwise, OSMnx retrieves the area and builds a simplified driving graph. The loader removes self-loop edges and returns an undirected NetworkX graph with node `x` and `y` coordinates and edge `length` values.

Example identifiers are provided in `osm_cities_example`:

| City | Identifier |
|---|---|
| Barcelona | `R347950` |
| Paris | `R71525` |
| Prague | `R435514` |
| Moscow | `R2555133` |
| Singapore | `R17140517` |
| Berlin | `R62422` |
| Rome | `R41485` |
| Rio | `R2697338` |
| Delhi | `R1942586` |

For custom graphs, path-finding algorithms expect the configured edge-weight attribute to exist on traversed edges. Community-based tools use a node cluster attribute, named `cluster` by default. The drawing utilities and coordinate-based heuristics expect node `x` and `y` attributes.

## Configuration and algorithms

Path-finding classes default to the edge weight name `length`. `Dijkstra` and `BiDijkstra` can optionally restrict search to a set of cluster identifiers; `AStar` accepts a heuristic callable. `ExtractionPfa` combines an upper-level path finder on a centroid graph with a lower-level cluster-restricted path finder on the original graph.

`LouvainCommunityResolver` and `LouvainKMeansCommunityResolver` expose options including the weight attribute, cluster attribute name, Louvain resolution, and seed. The K-means resolver also supports a K-means weight, iteration limit, and logging option. `CentroidGraphBuilder` can be configured with the cluster attribute, edge weight, and progress logging.

`utils.add_inverse_edges_weight()` adds an edge attribute calculated as `1 / (weight + eps)`. When no output attribute name is given, it uses `inverse_<weight>`. The examples use this inverse value for Louvain clustering while retaining `length` for shortest-path calculations.

For heuristic search, `MinClusterDistanceBuilder` constructs an A* path finder using minimum inter-cluster distances. The separate functions in `ride_pfa.heuristics` add `angle_cluster`, `spherical_cluster`, or `radial_cluster` node attributes.

## Benchmarking and visualization

`utils.generate_points(graph, num=...)` creates random pairs of distinct graph nodes. Pass those pairs, a baseline algorithm, and a test algorithm to `PfaComparator`:

```python
from ride_pfa.benchmark import PfaComparator
from ride_pfa import utils

points = utils.generate_points(g, num=100)
stats = PfaComparator(
    baseline=baseline,
    test_algorithm=extraction,
    points=points,
    workers=4,
).compare()

print(stats)
```

The comparator records path lengths and execution times. Its `Statistics` output reports percentage route-length error and acceleration (baseline time divided by test time), including maximum, minimum, median, and mean values. The `examples/benchmark_examples.ipynb` notebook demonstrates this workflow.

The `ride_pfa.drawer` package provides `draw_graph_matplotlib`, `draw_paths_matplotlib`, `draw_graph_folium`, and `draw_path_folium` for plotting graphs and routes. The examples notebook demonstrates graph and path visualization.

## Development and testing

The source package is organized by responsibility: `clustering`, `centroid_graph`, `path_finding`, `drawer`, and supporting modules for graph loading, heuristics, benchmarking, exceptions, and utilities. The notebooks in `examples/` are the available executable examples and useful starting points for exploring changes.

No dedicated automated test files or test-runner configuration are included in the supplied repository tree. Use the notebooks for manual checks; graph-loading examples may contact OpenStreetMap when a graph is not already cached. The benchmark notebook can be computationally intensive because it builds a centroid graph and evaluates multiple routes.

## License

This project is distributed under the Apache License, Version 2.0. See [`LICENSE`](LICENSE) for the complete terms.
