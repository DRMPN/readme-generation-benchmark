# Ride-ig80qt_h

A Python library for building and analyzing road networks, computing shortest paths, and serving route requests for ride-hailing applications. The project implements efficient path-finding algorithms (including Dijkstra, A\*, and heuristic/precomputed approaches), graph preprocessing, clustering of the road network, and visualization tools.

---

## ✨ Features

- **OSM graph loading** — download and build routable road graphs from OpenStreetMap data.
- **Graph preprocessing** — build centroid graphs and subgraphs for faster queries.
- **Shortest path algorithms**:
  - Classic **Dijkstra** algorithm
  - **A\*** search with heuristics
  - **Precomputed Fork Approximation (PFA)** — fast approximate shortest paths:
    - Basic PFA
    - Advanced PFA
    - Dijkstra-based PFA
    - Heuristic-based PFA
- **Clustering** — partition the road network into clusters to speed up routing queries.
- **Heuristics** — custom heuristic functions for A\*-style search and acceleration.
- **Visualization**:
  - Draw graphs and routes on interactive **Folium** maps
  - Draw graphs and routes with **Matplotlib**
- **Benchmarking** — compare algorithm accuracy and runtime.
- **Notebook examples** — ready-to-run Jupyter notebooks demonstrating the library.

---

## 📁 Project Structure

```
Ride-ig80qt_h/
├── heuristics.py                 # Heuristic functions for A* / PFA
├── utils.py                      # Utility helpers
├── graph_osm_loader.py           # Download and load OSM road graphs
├── centroids_graph_builder.py    # Build centroid-based auxiliary graphs
├── clustering.py                 # Graph clustering algorithms
├── benchmark.py                  # Benchmarking of path-finding algorithms
│
├── pfa.py                        # Precomputed Fork Approximation core
├── advenced_pfa.py               # Advanced PFA variant
├── dijkstra_pfa.py               # Dijkstra-based PFA
├── heuristic_pfa.py              # Heuristic-based PFA
├── excraction_pfa.py             # PFA extraction utilities
│
├── folium_drawer.py              # Interactive map visualization (Folium)
├── matplotlib_drawer.py          # Static visualization (Matplotlib)
├── exceptions.py                 # Custom exceptions
│
├── examples.ipynb                # General usage examples
├── heuristic_example.ipynb       # Heuristic algorithm examples
├── benchmark_examples.ipynb      # Benchmark examples
│
├── requirements.txt              # pip dependencies
├── pyproject.toml / poetry.lock  # Poetry project configuration
├── LICENSE                       # License
│
└── *.png / *.csv / *.pkl         # Images, data files, and pickled graphs
```

---

## 🚀 Installation

### Using pip

```bash
pip install -r requirements.txt
```

### Using Poetry

```bash
poetry install
```

---

## 📖 Usage

### 1. Load a road graph from OSM

```python
from graph_osm_loader import GraphOsmLoader

loader = GraphOsmLoader()
graph = loader.load("Prague")   # or coordinates / place name
```

### 2. Find the shortest path (Dijkstra / A\*)

```python
from heuristics import haversine_heuristic

path = a_star(graph, source, target, heuristic=haversine_heuristic)
```

### 3. Fast approximate routing with PFA

```python
from pfa import PFA

pfa = PFA(graph)
pfa.build()                       # precompute structures
path = pfa.find_path(source, target)
```

### 4. Cluster the graph

```python
from clustering import Clustering

clusters = Clustering(graph).build()
```

### 5. Visualize results

```python
from folium_drawer import FoliumDrawer

FoliumDrawer(graph).draw_path(path, "route.html")
```

> See the bundled notebooks — `examples.ipynb`, `heuristic_example.ipynb`, and `benchmark_examples.ipynb` — for full working examples.

---

## 📊 Benchmarking

The `benchmark.py` module compares algorithms in terms of:

- **Path quality** — deviation of the found path length from the true shortest path
- **Query speed** — average time to answer a routing request
- **Preprocessing time and memory**

Results (accuracy, speed, acceleration, density metrics) are shown in `benchmark_examples.ipynb` and the included images (e.g. `metrics.png`, `speed.png`, `all_y.png`).

---

## 🗺️ Data Files

| File | Description |
|---|---|
| `R41485.pkl`, `R62145.pkl` | Pickled road graphs |
| `random_points.csv` | Random sample points for benchmarks |
| `subgraph_path.png` | Example of a subgraph path |
| `Prague.png`, `milan.png` | Example city maps |
| `clustering.png`, `a_star nodes.png` | Algorithm visualizations |
| `speed.png`, `metrics.png`, etc. | Benchmark result plots |

---

## 🛠️ Tech Stack

- **Python 3**
- **NetworkX** — graph data structures and algorithms
- **OSMnx / geopandas** — OpenStreetMap data retrieval
- **Folium** — interactive map visualization
- **Matplotlib** — static plots
- **Poetry** — dependency management

---

## 📄 License

This project is licensed under the terms found in the [LICENSE](LICENSE) file.

---

## 👥 Credits

Developed as part of the ITMO University project *Ride* (see `ITMO.png`, `Ride_Logo-05.png`).
