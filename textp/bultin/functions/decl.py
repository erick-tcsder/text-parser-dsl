from typing import Type
from functions.definitions import BuiltinFunctionDef

BUILTIN_FUNCS = {}


def __declare_type(_func: BuiltinFunctionDef):
    '''
    Used to add builtin functions below.
    '''
    # Function overloading allowed by indexing with paramaters types
    BUILTIN_FUNCS[(_func.name, *_func.param_types)] = _func


# region Declarations
# endregion
