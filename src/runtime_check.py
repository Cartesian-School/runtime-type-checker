"""Minimal runtime type checker decorator using Python annotations.

This module provides a lightweight decorator that validates function arguments
and return values **at runtime** based on their type annotations.

Features
--------
- Validates function arguments and the return value at call time.
- Supports common typing constructs: builtins (``int``, ``str``...),
  ``Union``/``Optional``, ``list[T]``, ``set[T]``, ``tuple[...]``,
  ``dict[K, V]``, ``Tuple[T, ...]`` and fixed-length tuples.
- Pure stdlib only (``inspect`` and ``typing``), no external dependencies.

Notes
-----
This is a lightweight demonstrator. For production use, consider one of:

- ``beartype`` — fast, annotation-accurate runtime checking.
- ``typeguard`` — lightweight runtime enforcement.
- ``pydantic`` — full-featured data validation & settings management.

Example
-------
.. code-block:: python

   from runtime_check import runtime_check

   @runtime_check
   def greet(name: str) -> str:
       return "Hello " + name

   greet("Alice")    # OK
   # greet(123)      # -> TypeError at runtime
"""

from __future__ import annotations

import functools
import inspect
from collections.abc import Callable
from types import UnionType
from typing import (
    Any,
    ParamSpec,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

P = ParamSpec("P")
R = TypeVar("R")


def runtime_check(func: Callable[P, R]) -> Callable[P, R]:
    """Enforce a function's type annotations at runtime.

    The decorator reads annotations via :func:`typing.get_type_hints` and checks
    both the bound arguments and the returned value against a subset of typing
    constructs (``Union``, parameterized containers, fixed/variadic tuples, etc.).

    Parameters
    ----------
    func:
        A callable to wrap. Its annotations will be enforced at call time.

    Returns
    -------
    Callable[P, R]
        A wrapped callable that raises :class:`TypeError` if the provided
        arguments or the returned value do not match the annotations.

    Raises
    ------
    TypeError
        If an argument value or the return value fails the type check.

    Examples
    --------
    .. code-block:: python

       @runtime_check
       def total(xs: list[int]) -> int:
           return sum(xs)

       total([1, 2, 3])     # OK
       # total(["x"])       # -> TypeError
    """
    sig = inspect.signature(func)
    # get_type_hints resolves ForwardRef and 'from __future__ import annotations'
    hints: dict[str, Any] = get_type_hints(func)

    def _check(value: Any, anno: Any) -> bool:
        """Extended isinstance supporting a useful subset of typing generics."""
        origin = get_origin(anno)
        args = get_args(anno)

        # Plain classes and most typing special cases
        if origin is None:
            # Handle typing.Any and special forms gracefully
            try:
                return isinstance(value, anno)
            except TypeError:
                # For Any or special typing forms -> accept
                return True

        # Union / Optional (supports both typing.Union and PEP 604 X|Y)
        if origin in (Union, UnionType):
            return any(_check(value, opt) for opt in args)

        # Containers
        if origin in (list, set, tuple):
            if origin is list:
                if not isinstance(value, list):
                    return False
                # list[T]
                return not args or all(_check(v, args[0]) for v in value)

            if origin is set:
                if not isinstance(value, set):
                    return False
                # set[T]
                return not args or all(_check(v, args[0]) for v in value)

            if origin is tuple:
                if not isinstance(value, tuple):
                    return False
                if not args:
                    return True
                # Tuple[T, ...]
                if len(args) == 2 and args[1] is Ellipsis:
                    return all(_check(v, args[0]) for v in value)
                # Fixed-length Tuple[T1, T2, ...]
                try:
                    return all(_check(v, a) for v, a in zip(value, args, strict=True))
                except ValueError:
                    # lengths differ
                    return False

        # dict[K, V]
        if origin is dict:
            if not isinstance(value, dict):
                return False
            k_t, v_t = args or (object, object)
            return all(_check(k, k_t) and _check(v, v_t) for k, v in value.items())

        # Fallback: accept unknown typing constructs without blocking
        return True

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        # Bind incoming args to parameter names (applies defaults)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        # Check parameters
        for name, val in bound.arguments.items():
            anno = hints.get(name)
            if anno is not None and not _check(val, anno):
                raise TypeError(
                    f"Argument '{name}' expected {anno!r}, got {type(val)!r} with value={val!r}"
                )

        # Call original function
        result = func(*args, **kwargs)

        # Check return value
        ret_anno = hints.get("return")
        if ret_anno is not None and not _check(result, ret_anno):
            raise TypeError(
                f"Return expected {ret_anno!r}, got {type(result)!r} with value={result!r}"
            )
        return result

    return wrapper
