# Tutorial on Hyperdimensional Computing
## ODSC AI West 2026

This repo contains tutorial notebooks for the Hyperdimensional Computing (HDC) + graph demo in [ODSC West 2026](https://odsc.ai/west/).

The demo shown in our talk follows a fleet of warehouse robots that learn from each other using hypervector representations.
When **R17** has a "near-miss" (avoided collision) with a forklift in aisle 8, or **R04** skids on oil in aisle 9 and finds that slowing
down lets it cross the obstacle, those experiences **become part of a memory the whole fleet shares**, so a new robot **R11**
already knows to slow down before it enters aisle 9 as it encounters the oil spill for the first time.

The full demo shown on stage is a real running system built with HDC: a fleet simulation with simulated sensors
and LiDAR, a policy engine that picks each robot's response to a hazard, a REST API service
with a UI that watches the fleet move in real time, and a hypervector memory that is revised episode by episode as
the robots learn. The code for that system is complex, and isn't included in this intro tutorial repo.

## What this repo covers

The notebooks in this repo are designed to introduce the basics of HDC, and the following key aspect of the workflow we built:

> **HDC proposes candidates. The graph validates whether those paths actually exist.**

The code walks through use a simple warehouse graph from the talk (3 robots, 3 aisles, 3 hazards and 2
responses) and just three libraries: [LanceDB](https://docs.lancedb.com/) for storage,
[lance-csr](https://github.com/hyperdimensionalcomputingai/lance-csr) for Cypher queries, and
[torchhd](https://github.com/hyperdimensional-computing/torchhd) for HDC. We don't complicate this example: 
there are no sensors, no simulation and no UI, so every step fits in a few lines of code. They assume you know graphs
and graph databases, and nothing about HDC.

1. [A warehouse robot graph in LanceDB](src/01_warehouse_trial_graph.ipynb): store the graph
   as LanceDB tables and query it with Cypher. This is the exact source of truth.
2. [The three operators of HDC](src/02_hdc_operators.ipynb): hypervectors, and the three
   operations on them, binding ⊗, bundling ⊕ and permutation ρ, with the math beside each
   one.
3. [HDC proposes, the graph validates](src/03_hdc_proposes_graph_validates.ipynb): encode
   the whole graph as one hypervector, ask it questions, and check every proposed answer
   against the graph, including the wrong ones.

## Setup

You need [uv](https://docs.astral.sh/uv/getting-started/installation/). It installs Python 3.12
for you if it's missing.

On Apple Silicon Macs (macOS 11+) and Linux x86_64 (glibc 2.28+, such as Ubuntu 20.04+),
`lance-csr` installs from a prebuilt wheel. No Rust or `protoc` installation is needed.

```bash
git clone https://github.com/hyperdimensionalcomputingai/odsc-west-2026.git
cd odsc-west-2026
uv sync --locked --no-build-package lance-csr
uv run jupyter lab src/
```

The install command requires a wheel for `lance-csr`, so it won't unexpectedly start a source
build. Intel Macs and Windows do not have prebuilt `lance-csr` wheels; use one of the supported
platforms for this tutorial. For source builds, see the
[lance-csr installation guide](https://github.com/hyperdimensionalcomputingai/lance-csr/blob/main/python/README.md#installation).

### Running

Open `01_warehouse_trial_graph.ipynb` first. On Linux, torch installs as a CPU-only build, so
there's no multi-gigabyte CUDA download.

Run the tests (executes every notebook headless) with `uv run pytest`.
