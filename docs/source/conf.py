# -- Sphinx configuration -------------------------------------------------
from __future__ import annotations
import sys
from pathlib import Path

# Paths
CONF_DIR = Path(__file__).resolve().parent  # docs/source
DOCS_DIR = CONF_DIR.parent  # docs
ROOT_DIR = DOCS_DIR.parent  # проект
SRC_DIR = ROOT_DIR / "src"

# Make 'src/' visible to autodoc (robust, path from conf.py)
sys.path.insert(0, str(SRC_DIR))

project = "Runtime Type Checker"
author = "Siergej Sobolewski"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

# Root document (Sphinx 8)
root_doc = "index"

# Type hints rendering
autodoc_typehints = "description"
napoleon_google_docstring = True
napoleon_numpy_docstring = True

templates_path = ["_templates"]
html_static_path = ["_static"]

# Create _static if missing to silence warnings
(CONF_DIR / "_static").mkdir(parents=True, exist_ok=True)

# Theme with fallback
try:
    import furo  # noqa: F401

    html_theme = "furo"
except Exception:
    html_theme = "alabaster"
