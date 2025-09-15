from typing import get_type_hints, get_origin, get_args, Union
import inspect

def runtime_check(func):
    sig = inspect.signature(func)
    hints = get_type_hints(func)

    def check_type(value, expected_type):
        origin = get_origin(expected_type)
        args = get_args(expected_type)

        if origin is None:
            return isinstance(value, expected_type)

        if origin is Union:
            return any(check_type(value, typ) for typ in args)

        if origin is list and isinstance(value, list):
            return all(check_type(item, args[0]) for item in value)

        if origin is dict and isinstance(value, dict):
            k_t, v_t = args
            return all(check_type(k, k_t) and check_type(v, v_t) for k, v in value.items())

        return True

    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        for name, value in bound.arguments.items():
            expected_type = hints.get(name)
            if expected_type and not check_type(value, expected_type):
                raise TypeError(f"Argument '{name}' expected {expected_type}, got {type(value)}")

        result = func(*args, **kwargs)
        expected_return = hints.get("return")
        if expected_return and not check_type(result, expected_return):
            raise TypeError(f"Return value expected {expected_return}, got {type(result)}")

        return result

    return wrapper
