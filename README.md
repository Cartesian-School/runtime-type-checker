# Runtime Type Checker

🧪 Minimal decorator `@runtime_check` that validates function arguments and return types using Python's type hints — at runtime.

## ✅ Features

- Supports `int`, `str`, `list[int]`, `dict[str, int]`, `Union[int, str]`
- No external dependencies (uses only `typing`, `inspect`)
- Easy to integrate into your existing codebase

## 🚀 CI/CD Included

- ✅ GitHub Actions: lint, type, test, build docs
- ✅ GitLab CI: same setup

## 📚 Documentation

Generated with Sphinx. Run:

```bash
cd docs
make html
```

## 🔍 Example

```python
@runtime_check
def greet(name: str) -> str:
    return "Hello " + name

greet("Alice")  # OK
greet(123)      # TypeError
```
