def _qualname(obj) -> str:
    """Get the fully-qualified name of an object (including module)."""
    return obj.__module__ + '.' + obj.__qualname__


def _declaring_class(obj) -> str:
    """Get the name of the class that declared an object."""
    name = _qualname(obj)
    return name[:name.rfind('.')]


# Stores the actual visitor methods
_methods = {}

# Delegating visitor implementation


def _visitor_impl(self, arg, *args, **kwargs):
    """Actual visitor method implementation."""
    qnam = _qualname(type(self))

    # Check if the object has a special method for the visitor
    magic_m_name = '__'+qnam[qnam.rfind('.')+1:].lower()+'__'

    if hasattr(arg, magic_m_name):
        return getattr(arg, magic_m_name)(*args, **kwargs)

    # Check if an specific visitor for that type exist
    method = _methods.get((qnam, type(arg)), None)
    if method is None:
        # Call the default otherwise
        default = _methods.get((qnam, None), None)
        if default is None:
            raise Exception(
                f"Visitor in {type(self)} for {type(arg)} not found nor a default")
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
