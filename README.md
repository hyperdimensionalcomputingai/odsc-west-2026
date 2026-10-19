# odsc-west-2026

Code for the Hyperdimensional Computing (HDC) and graph demo in ODSC West 2026.

The tutorial builds towards one idea: **HDC proposes candidates. The graph validates whether
those paths actually exist.** It uses one warehouse trial graph (robots, aisles,
hazards and responses), stored in LanceDB and queried with Cypher through lance-graph.

1. [A warehouse robot graph in LanceDB](src/01_warehouse_trial_graph.ipynb)
2. [The three operators of HDC](src/02_hdc_operators.ipynb)
3. [HDC proposes, the graph validates](src/03_hdc_proposes_graph_validates.ipynb)

## Setup

```bash
# install uv once: https://docs.astral.sh/uv/getting-started/installation/
git clone <repo-url> && cd odsc-west-2026
uv sync
uv run jupyter lab src/
```

Open `01_warehouse_trial_graph.ipynb` first. `uv sync` installs Python 3.12 itself if it is
missing.

Run the tests (executes every notebook headless) with `uv run pytest`.
