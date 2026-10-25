"""The warehouse trial graph from notebook 1, for notebooks 2 and 3 to import."""

import os

os.environ.setdefault("LANCEDB_LOG", "error")  # hide LanceDB's first-write WARN; import this before lancedb

from lance_csr import GraphConfig

NODES = {
    "Robot":    [{"id": "R17"}, {"id": "R04"}, {"id": "R11"}],
    "Aisle":    [{"id": "aisle-7"}, {"id": "aisle-8"}, {"id": "aisle-9"}],
    "Hazard":   [{"id": "pallet"}, {"id": "forklift"}, {"id": "oil"}],
    "Response": [{"id": "reroute"}, {"id": "slow_down"}],
}

EDGES = {
    "VISITED":    [("R17", "aisle-8"), ("R04", "aisle-8"), ("R04", "aisle-9"), ("R11", "aisle-9")],
    "HAS_HAZARD": [("aisle-7", "pallet"), ("aisle-8", "forklift"), ("aisle-9", "oil")],
    "HANDLED_BY": [("forklift", "reroute"), ("oil", "slow_down")],
}


def write_graph(db):
    for label, rows in NODES.items():
        db.create_table(label, rows, mode="overwrite")
    for rel, pairs in EDGES.items():
        db.create_table(rel, [{"src": s, "dst": d} for s, d in pairs], mode="overwrite")


def graph_config():
    builder = GraphConfig.builder()
    for label in NODES:
        builder = builder.node_table(label, "id")
    builder = (
        builder.rel_table("VISITED", "Robot", "Aisle", "src", "dst")
        .rel_table("HAS_HAZARD", "Aisle", "Hazard", "src", "dst")
        .rel_table("HANDLED_BY", "Hazard", "Response", "src", "dst")
    )
    return builder.build()
