# Plan: an HDC + graph tutorial companion for ODSC West 2026

## Goal

A short, hands-on tutorial that goes with the talk slides. Attendees are new to both
hyperdimensional computing (HDC) and lance-csr, so every cell must be small and readable.
It teaches the three HDC operators (binding, bundling, permutation) with math in markdown
cells and short code in Python cells. It uses one small graph, a warehouse trial taken
from the R17 story, so the audience recognises the robots, aisles and hazards from the slides.

The motto the tutorial builds towards:

> **HDC proposes candidates. The graph validates whether those paths actually exist.**

## What this is not

- Not a port of the R17 demo. No FastAPI, no UI, no sensors, no LiDAR, no fleet simulation,
  no policy engine, no episodes or memory revisions. The source repo
  (`ODSC/odsc-west-2026`, `src/r17/`) is for reference only. Copy no code from it except
  the edge-encoding idea in `hdc.py::relationship` (s ⊗ r ⊗ ρ(t)).
- No level (numeric) encoding, no trained models, no text embeddings, no Polars.
- No custom HDC library. Call `torchhd` directly in the notebook cells so attendees see the
  real API.

## Audience rules (apply to every markdown cell and code cell)

- Say **hypervector**, never "vector", for HDC representations. Product terms such as
  LanceDB's "vector search" stay as they are.
- Notation: bundling is **⊕** (never `+`), binding is **⊗**, permutation is **ρ**, and
  inverse permutation is **ρ⁻¹**. Use `+` only for scalar addition.
- Call the data a **warehouse trial**. Never call it a "toy" graph or toy example, and don't
  play down how small it is.
- Describe structure as **key-value pairs** (key: value). Don't use the words "symbol",
  "role", "shared seed" or "identical on every robot". If you need it, say the codebook is
  "fixed, and shared by the whole fleet".
- Plain, conversational prose. One idea per markdown cell, at most 3 to 4 sentences, then
  the code that shows it. No slogans and no defensive framing.
- Code cells stay short: 1 to 8 lines, no classes, no helper functions defined inside
  notebooks unless a beginner can read them at a glance. Print results in a readable form,
  for example rounded scores in a small table.

## The warehouse trial graph

Eleven nodes and nine edges, taken from Act 3 of the talk. Four node labels and three
relationship types. Keep exactly this. It is small enough to draw on one slide.

| Label | Nodes |
|---|---|
| `Robot` | R17, R04, R11 |
| `Aisle` | aisle-7, aisle-8, aisle-9 |
| `Hazard` | pallet, forklift, oil |
| `Response` | reroute, slow_down |

| Relationship | Edges (src → dst) |
|---|---|
| `VISITED` | R17 → aisle-8, R04 → aisle-8, R04 → aisle-9, R11 → aisle-9 |
| `HAS_HAZARD` | aisle-7 → pallet, aisle-8 → forklift, aisle-9 → oil |
| `HANDLED_BY` | forklift → reroute, oil → slow_down |

Story mapping, for the markdown cells: R17 had the forklift near-miss in aisle 8. R04 turned
away from aisle 8, then skidded on oil in aisle 9 and found that slowing down fixed it. R11
went into aisle 9 and already knew to slow down. aisle-7 is blocked by a fallen pallet and
nobody visits it. That gives one hazard with no visitor, which is useful later.

Optional, add only if a slide needs it: node properties such as `Robot.role = "delivery"` or
`Response.speed_mps = 0.5`. Don't add more nodes or edge types.

## Repository layout

```
odsc-west-2026/
├── README.md                 # what this is, how to run it (uv sync; uv run jupyter lab)
├── PLAN.md                   # this file
├── pyproject.toml            # Python 3.12, pinned deps, managed by uv (below)
├── uv.lock                   # committed, so every attendee gets the same versions
├── src/                      # the notebooks live here
│   ├── warehouse_trial.py    # the warehouse trial data plus two short loaders (≈40 lines)
│   ├── 01_warehouse_trial_graph.ipynb
│   ├── 02_hdc_operators.ipynb
│   └── 03_hdc_proposes_graph_validates.ipynb
└── tests/
    └── test_notebooks.py     # executes all three notebooks headless
```

Add `*.lancedb/` to `.gitignore`. Notebooks are committed **with outputs**, so attendees can read them on GitHub without
running anything. Re-run each notebook top to bottom before committing so the outputs match the code.

### Installation with uv

Use [uv](https://docs.astral.sh/uv/) for everything: the Python version, the virtual
environment, dependencies, the lockfile and running commands. Don't use pip, conda or
`requirements.txt`, and don't tell attendees to activate a venv. `uv run` handles that.

**Setting up the repo (implementer, once).** Pin the same versions the R17 demo uses. They
were verified together.

```bash
uv init --app --python 3.12 --no-readme   # keep the existing README.md
uv add "torch==2.6.0" "torch-hd==5.8.4" "lancedb==0.33.0" "lance-csr==0.3.1" \
       "pyarrow>=18,<25" "jupyterlab>=4,<5" "ipykernel>=6,<8"
uv add --dev "pytest>=8,<10" "nbclient>=0.10,<1"
```

Then delete the `main.py` stub that `uv init` creates, set `requires-python = ">=3.12,<3.13"`
in `pyproject.toml`, and commit `pyproject.toml` and `uv.lock`. Delete the `.python-version` file that uv writes: `requires-python` already pins 3.12.
`ipykernel` is a main dependency, not a dev one, so the notebooks find the project's kernel
under `uv run jupyter lab`. `warehouse_trial.py` sits in `src/`, next to the
notebooks, so notebooks 2 and 3 import it with a plain `from warehouse_trial import ...`.
Jupyter runs each notebook from its own folder, so no `sys.path` change and no packaging is
needed. `tests/test_notebooks.py` runs each notebook from a temp directory, so the test puts
`src/` on `PYTHONPATH` for the kernel. Keep that if you change how the notebooks import the
module.

`pyproject.toml` points torch at the PyTorch CPU index on Linux only (`[tool.uv.sources]`
with a `sys_platform == 'linux'` marker, plus an explicit `[[tool.uv.index]]`), so Linux
installs don't pull CUDA wheels. macOS and Windows wheels on PyPI are already CPU-only.

lance-csr 0.3.1 publishes wheels for native macOS arm64 (macOS 11+) and Linux x86_64
(glibc 2.28+). Use `uv sync --locked --no-build-package lance-csr` so attendee setup
never falls back to a Rust source build. Other platforms are outside the wheel-based setup.

**Attendee setup (goes in the README, nothing else needed).**

```bash
# install uv once: https://docs.astral.sh/uv/getting-started/installation/
git clone <repo-url> && cd odsc-west-2026
uv sync --locked --no-build-package lance-csr
uv run jupyter lab src/
```

`uv sync` installs Python 3.12 itself if it is missing. **Tests:** `uv run pytest`. Don't add a
Justfile, Docker or CI config unless asked.

### `warehouse_trial.py` (the only shared code)

Holds only what notebooks 2 and 3 need so they don't repeat notebook 1:

- `NODES: dict[str, list[dict]]` and `EDGES: dict[str, list[tuple[str, str]]]`: the tables
  above, as plain Python literals.
- `write_graph(db)`: one LanceDB table per node label (column `id`), and one per
  relationship type (columns `src`, `dst`), all with `mode="overwrite"`.
- `graph_config()`: `GraphConfig.builder()` with `.node_table(label, "id")` for each
  label and `.rel_table(rel, from_table, to_table, "src", "dst")` for each relationship
  type: VISITED maps Robot to Aisle, HAS_HAZARD maps Aisle to Hazard, and HANDLED_BY maps
  Hazard to Response.

Notebook 1 writes these same steps out inline, because that is the lesson. The module must
mirror them exactly. Notebooks 2 and 3 import from it.

LanceDB prints a Rust `WARN ... No existing dataset ... it will be created` line on first
write. Silence it, for example by setting the Rust log level env var before importing
lancedb (check which variable works), so beginners don't think something broke.

## Notebook 1: a warehouse trial graph in LanceDB and lance-csr (~10 min)

1. **Intro (md).** Three robots, three aisles, three hazards, and the Act 3 story in four
   sentences. Include a small diagram of the graph: a mermaid block or a static PNG.
2. **The data (code).** Show `NODES` and `EDGES` inline as Python literals.
3. **Store it in LanceDB (md + code).** One table per node label and one per relationship
   type. `lancedb.connect("warehouse.lancedb")`, `create_table(..., mode="overwrite")`.
   Print `db.table_names()`.
4. **Read back as Arrow (code).** `db.open_table("VISITED").to_arrow()` and show it. Explain
   in one sentence that lance-csr works directly on Arrow tables.
5. **Describe the graph shape (md + code).** Build `GraphConfig` and say which columns are IDs
   and which are edge endpoints.
6. **First Cypher query (code).** Run a one-hop query and show the result:
   `MATCH (r:Robot {id: 'R04'})-[:VISITED]->(a:Aisle) RETURN a.id`
   (expected: aisle-8 and aisle-9).
7. **A multi-hop query that tells the story (code).** "What hazard might R11 meet, and how
   was it handled?" Run the query and show the result:
   ```cypher
   MATCH (r:Robot {id: 'R11'})-[:VISITED]->(a:Aisle)-[:HAS_HAZARD]->(h:Hazard)-[:HANDLED_BY]->(x:Response)
   RETURN r.id, a.id, h.id, x.id
   ```
   (expected: one row: R11, aisle-9, oil, slow_down). Use `CypherQuery(q).with_config(cfg)
   .execute(datasets)` and show the result with `.to_pylist()` or `.to_pandas()` only if
   pandas is already installed. Don't add pandas for this.
8. **Wrap (md).** The graph gives exact answers, but only to questions about paths that are
   stored. Next we build a representation that can propose answers.

## Notebook 2: the three HDC operators (~15 min)

Use the MAP model throughout: `torchhd.random(n, D, vsa="MAP")` gives bipolar ±1
hypervectors. Set `D = 10_000` and a fixed `torch.manual_seed`. Each operator gets a
markdown cell with its LaTeX, then 2 to 4 short code cells that show one property each.

1. **Hypervectors (md + code).** Random hypervectors are almost orthogonal:
   $\cos(\mathbf{a}, \mathbf{b}) \approx 0 \pm 1/\sqrt{D}$.
   Make a hypervector for each node and each relationship type in the warehouse trial graph (the
   codebook). Print a few pairwise cosine similarities with `torchhd.cosine_similarity`.
2. **Store the codebook in LanceDB (code).** Table `hypervectors` with columns `name`,
   `kind` (node label or relationship type) and `vector` (fixed-size list of float32, length
   D). Show one nearest-neighbour lookup with
   `table.search(q).metric("cosine").limit(3)`. That lookup is the clean-up step used later.
   Say in one line that LanceDB's vector search is what turns a noisy hypervector back into
   a name.
3. **Binding ⊗ (md + code).**
   $\mathbf{a} \otimes \mathbf{b}$ multiplies element by element. Show these properties, one
   per cell:
   - the result is dissimilar to both inputs: $\cos(\mathbf{a}\otimes\mathbf{b}, \mathbf{a}) \approx 0$;
   - it undoes itself: $\mathbf{a} \otimes (\mathbf{a} \otimes \mathbf{b}) = \mathbf{b}$,
     because $\mathbf{a} \otimes \mathbf{a} = \mathbf{1}$ for ±1 entries;
   - a key-value pair: `VISITED ⊗ aisle-9`, then unbind with `VISITED` to get aisle-9 back.
   Use `torchhd.bind`.
4. **Bundling ⊕ (md + code).**
   $\mathbf{a} \oplus \mathbf{b} \oplus \mathbf{c}$ adds element by element. The result
   stays similar to every input: $\cos(\mathbf{a} \oplus \mathbf{b} \oplus \mathbf{c}, \mathbf{a}) \approx 1/\sqrt{3}$.
   Bundle R04's two key-value pairs, such as `VISITED ⊗ aisle-8 ⊕ VISITED ⊗ aisle-9`, or
   simply `aisle-8 ⊕ aisle-9`. Show that both aisles score high and aisle-7 scores near 0.
   Use `torchhd.bundle` or `torchhd.multiset`.
5. **Permutation ρ (md + code).** Start with the problem: binding is commutative, so
   `R04 ⊗ aisle-8` and `aisle-8 ⊗ R04` are the same hypervector (cosine 1.0, checked).
   An edge would lose its direction.
   $\rho(\mathbf{a})$ is a cyclic shift (`torchhd.permute(a, shifts=1)`). Show that
   $\cos(\rho(\mathbf{a}), \mathbf{a}) \approx 0$, that $\rho^{-1}(\rho(\mathbf{a})) = \mathbf{a}$
   (`shifts=-1`), and that
   $\mathbf{R04} \otimes \rho(\mathbf{aisle8}) \ne \mathbf{aisle8} \otimes \rho(\mathbf{R04})$.
6. **Wrap (md).** A table of the three operators with what each one does to similarity:
   ⊗ gives a result unlike its inputs, ⊕ gives a result like all of its inputs, and ρ gives
   a result unlike its input but reversible.

## Notebook 3: HDC proposes, the graph validates (~15 min)

1. **One edge, one hypervector (md + code).**
   $\mathbf{e} = \mathbf{s} \otimes \mathbf{r} \otimes \rho(\mathbf{t})$, for example
   `R04 ⊗ VISITED ⊗ ρ(aisle-9)`.
2. **The whole graph, one hypervector (md + code).**
   $\mathbf{G} = \bigoplus_{(s,r,t) \in E} \mathbf{s} \otimes \mathbf{r} \otimes \rho(\mathbf{t})$.
   Build it from `EDGES` in one comprehension and point out that it is still D numbers long.
   Store `G` as one row in LanceDB, for example a `graph_memory` table, so it is clear the
   whole graph fits in one row.
3. **Asking a question (md + code).** "Where did R04 go?"
   $\rho^{-1}(\mathbf{G} \otimes \mathbf{R04} \otimes \mathbf{VISITED}) \approx \mathbf{aisle8} \oplus \mathbf{aisle9} \oplus \text{noise}$.
   Clean up with the LanceDB codebook search from notebook 2 and show the top 4 with scores.
   At D = 10,000 the prototype gave aisle-8 ≈ 0.345 and aisle-9 ≈ 0.343, with everything
   else below 0.02.
4. **Two hops, HDC only (code).** "R11 is heading into aisle-9. What should it expect?"
   Unbind `aisle-9 ⊗ HAS_HAZARD` and you get oil. Unbind `oil ⊗ HANDLED_BY` and you get
   slow_down. Each hop proposes a candidate, and nothing has checked it yet.
5. **Validate with the graph (md + code).** Run the HDC candidates as a Cypher check using
   the notebook 1 query with the proposed IDs filled in:
   `MATCH (a:Aisle {id: $aisle})-[:HAS_HAZARD]->(h:Hazard {id: $hazard})-[:HANDLED_BY]->(x:Response {id: $response}) RETURN ...`
   Build the string with an f-string. Note in a comment that this is fine for a tutorial
   with fixed IDs, but not for user input. A non-empty result means the path is confirmed.
6. **When HDC guesses wrong (md + code).** Rebuild the codebook and G at a small dimension,
   for example `D = 64`, and ask "Where did R04 go?" again. Keep candidates above a score
   threshold, for example 0.05 (0.1 left a real aisle at 0.104 on Linux x86_64). In the prototype (seed 0, D = 64), R04 and forklift came in
   at ≈ 0.12 next to the real aisles. Validate every candidate with Cypher
   (`MATCH (r:Robot {id: 'R04'})-[:VISITED]->(a:Aisle {id: '<candidate>'}) RETURN a.id`)
   and print a table of candidate, HDC score, and whether the graph confirms it. The wrong
   ones get rejected. Pick the seed, D and threshold so that at least one false candidate
   reliably shows up, and record the chosen values in the notebook.
7. **Wrap (md).** HDC gives fast, approximate, compositional proposals from one fixed-size
   hypervector, and can propose answers to questions nobody wrote a query for. The graph
   gives exact, auditable confirmation. Together: **HDC proposes candidates, the graph
   validates whether those paths actually exist.** Link back to the talk's Act 3.

## Testing and acceptance

- `tests/test_notebooks.py` runs each notebook with `nbclient` in a temp working
  directory, so `*.lancedb` lands there, and fails on any cell error.
- Put plain `assert` lines in the notebooks at the key results, so the test checks
  behaviour and attendees see the claim:
  - notebook 1, step 7: exactly one row, `('R11', 'aisle-9', 'oil', 'slow_down')`;
  - notebook 2: commutativity cosine == 1.0; unbinding recovers the value (cosine > 0.99);
  - notebook 3, step 3: top 2 at D = 10,000 are {aisle-8, aisle-9};
  - notebook 3, step 6: at least one candidate is rejected by the graph, and every
    true aisle is confirmed.
- Done when: `uv sync && uv run pytest` passes on a clean clone, all three notebooks run top
  to bottom in under a minute in total on a laptop CPU, and the notebooks are committed
  with fresh outputs from a top-to-bottom run.
- README: the attendee setup block from "Installation with uv" (install uv, `uv sync`,
  `uv run jupyter lab src/`, open `01_...`),
  plus a one-paragraph summary of the motto and links to the three notebooks.

## Open questions for the presenter (don't block on these, use the defaults)

- Should there be a Colab badge? Default: no. Only add it if the venue Wi-Fi is a concern.
