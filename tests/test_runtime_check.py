from src.runtime_check import runtime_check
import pytest

@runtime_check
def greet(name: str) -> str:
    return "Hello " + name

@runtime_check
def add_all(numbers: list[int]) -> int:
    return sum(numbers)

def test_greet_correct():
    assert greet("Alice") == "Hello Alice"

def test_greet_invalid():
    with pytest.raises(TypeError):
        greet(123)

def test_add_all_correct():
    assert add_all([1, 2, 3]) == 6

def test_add_all_invalid():
    with pytest.raises(TypeError):
        add_all(["a", "b"])
