def is_float(anything):
    try:
        float(anything)
        return True
    except ValueError:
        return False