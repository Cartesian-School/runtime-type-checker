![CI](https://img.shields.io/github/actions/workflow/status/Cartesian-School/runtime-type-checker/ci.yml?branch=master&label=CI&logo=github)
![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-3776AB?logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-supported-111111)



# Runtime Type Checker

Minimal decorator `@runtime_check` that validates function arguments and return values **at runtime** using Python annotations. No external dependencies.


```
runtime-type-checker/
├── src/
│   └── runtime_check.py
├── tests/
│   └── test_runtime_check.py
├── docs/
│   └── source/
│       ├── conf.py
│       └── index.rst
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitlab-ci.yml
├── pyproject.toml
├── README.md
└── .gitignore
```

## Features

- ✅ Supports `int/str/...`, `Union/Optional`, `list[T]`, `set[T]`, `tuple[...]`, `dict[K, V]`
- ✅ Preserves function metadata
- ✅ Pure stdlib (`inspect`, `typing`)
- ✅ CI for linting, typing, testing, docs (GitHub Actions / GitLab CI)


## Install (local dev)

This project uses a plain `src/` layout without packaging. Just run:

```bash
python -m pip install --upgrade pip
pip install -r <(echo -e "ruff\nmypy\npytest\nsphinx")
````

Or with **uv**:

```bash
uv pip install ruff mypy pytest sphinx
```

## Usage

```python
from runtime_check import runtime_check

@runtime_check
def greet(name: str) -> str:
    return "Hello " + name

print(greet("Alice"))  # OK
# greet(123) -> TypeError
```

## Tests

```bash
PYTHONPATH=. pytest -q
```

## Docs

Local build:

```bash
sphinx-build -b html docs/source docs/build
# open docs/build/index.html
```

## CI

* GitHub Actions: `.github/workflows/ci.yml`
* GitLab CI: `.gitlab-ci.yml`

## License

MIT

