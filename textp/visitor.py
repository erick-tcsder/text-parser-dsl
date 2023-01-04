def _qualname(obj):
    """Get the fully-qualified name of an object (including module)."""
    return obj.__module__ + '.' + obj.__qualname__

def _declaring_class(obj):
    """Get the name of the class that declared an object."""
    name = _qualname(obj)
    return name[:name.rfind('.')]

# Stores the actual visitor methods
_methods = {}

# Delegating visitor implementation


def _visitor_impl(self, arg, *args, **kwargs):
    """Actual visitor method implementation."""
    qnam = _qualname(type(self))
    method = _methods.get((qnam, type(arg)), None)
    if method is None:
        return _methods[(qnam, None)](self, arg, *args, **kwargs)
    return method(self, arg, *args, **kwargs)

# The actual @visitor decorator


def visitor(arg_type=None):
    """Decorator that creates a visitor method."""

    def decorator(fn):
        declaring_class = _declaring_class(fn)
        _methods[(declaring_class, arg_type)] = fn

        # Replace all decorated methods with _visitor_impl
        return _visitor_impl

    return decorator
