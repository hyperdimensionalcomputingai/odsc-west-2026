from pathlib import Path

import nbformat
import pytest
from nbclient import NotebookClient

ROOT = Path(__file__).parent.parent
NOTEBOOKS = sorted((ROOT / "src").glob("*.ipynb"))


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_notebook_runs(path, tmp_path, monkeypatch):
    # The kernel runs from tmp_path, so put src/ (home of warehouse_trial.py) on its path.
    monkeypatch.setenv("PYTHONPATH", str(ROOT / "src"))
    nb = nbformat.read(path, as_version=4)
    # Run in tmp_path so *.lancedb lands there, not in the repo.
    NotebookClient(nb, timeout=120, kernel_name="python3", resources={"metadata": {"path": tmp_path}}).execute()
