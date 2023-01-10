from typing import Type
from .definition import BuiltinFunctionDef

BUILTIN_FUNCS = {}


def __declare_function(_func: BuiltinFunctionDef):
    '''
    Used to add builtin functions below.
    '''
    BUILTIN_FUNCS[_func.name] = _func


# region Declarations

# endregion
