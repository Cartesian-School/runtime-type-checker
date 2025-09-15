# --- tests/test_runtime_check.py ---
# ruff: noqa: I001

import os
import sys

# Make src/ importable when running tests without installing the package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import pytest  # type: ignore  # noqa: E402
from runtime_check import runtime_check  # noqa: E402


@runtime_check
def greet(name: str) -> str:
    return "Hello " + name


@runtime_check
def add_all(numbers: list[int]) -> int:
    return sum(numbers)


@runtime_check
def collect(point: tuple[int, int] | tuple[int, ...], tags: set[str]) -> dict[str, int]:
    return {t: len(point) for t in tags}


def test_greet_ok():
    assert greet("Alice") == "Hello Alice"


def test_greet_type_error():
    with pytest.raises(TypeError):
        greet(123)  # type: ignore[arg-type]


def test_add_all_ok():
    assert add_all([1, 2, 3]) == 6


def test_add_all_type_error():
    with pytest.raises(TypeError):
        add_all(["a", "b"])  # type: ignore[list-item]


def test_collect_tuple_variants_and_set():
    out = collect((1, 2), {"x", "y"})
    assert out["x"] == 2 and out["y"] == 2
    out2 = collect((1, 2, 3), {"z"})
    assert out2["z"] == 3
    with pytest.raises(TypeError):
        collect(("1", 2), {"bad"})  # type: ignore[arg-type]
