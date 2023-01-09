def is_float(anything):
    try:
        float(anything)
        return True
    except ValueError:
        return False


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        kwargs = kwargs.copy()
        name = kwargs.get("name", "root")
        kwargs.pop('name', None)
        if (cls, name) not in cls._instances:
            cls._instances[cls, name] = super(
                Singleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls, name]
