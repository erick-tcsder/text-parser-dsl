from typing import Any, Callable, Dict, List, Tuple


def _qualname(obj) -> str:
    """Get the fully-qualified name of an object (including module)."""
    return obj.__module__ + '.' + obj.__qualname__


def _declaring_class(obj) -> str:
    """Get the name of the class that declared an object."""
    name = _qualname(obj)
    return name[:name.rfind('.')]


# Stores the actual visitor methods
_methods: Dict[str, List[Tuple[type, Callable]]] = {}


def _impl_getter(visitor: str, arg: Any):
    impls = _methods[visitor]
    for tp, fn in impls:
        if tp is None or isinstance(arg, tp):
            return fn
    raise Exception(
        f"Implementation of visitor {visitor} for {type(arg)} not found nor a default")


def _visitor_impl(self, arg, *args, **kwargs):  # Delegating visitor implementation
    """Actual visitor method implementation."""
    qnam = _qualname(type(self))

    # Check if the object has a special method for the visitor
    magic_m_name = '__'+qnam[qnam.rfind('.')+1:].lower()+'__'

    if hasattr(arg, magic_m_name):
        return getattr(arg, magic_m_name)(*args, **kwargs)

    # Check if an specific visitor for that type exist
    method = _impl_getter(qnam, arg)

    return method(self, arg, *args, **kwargs)

# The actual @visitor decorator


def visitor(arg_type=None):
    """Decorator that creates a visitor method."""

    def decorator(fn):
        declaring_class = _declaring_class(fn)
        if declaring_class not in _methods:
            _methods[declaring_class] = []
        _methods[declaring_class].append((arg_type, fn))

        # Replace all decorated methods with _visitor_impl
        return _visitor_impl

    return decorator
