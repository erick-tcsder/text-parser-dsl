from typing import Type
from .definition import BuiltinFunctionDef
from .utils import *
from ..types import DSLBoolean, get_array_type

BUILTIN_FUNCS = {}


def __declare_function(_func: BuiltinFunctionDef):
    '''
    Used to add builtin functions below.
    '''
    BUILTIN_FUNCS[_func.name] = _func


# region Math
__declare_function(BuiltinFunctionDef(
    name='__add',
    type_validation_func=validate_math,
    py_func=lambda x, y: x+y
))
__declare_function(BuiltinFunctionDef(
    name='__minus',
    type_validation_func=validate_math,
    py_func=lambda x, y: x-y
))
__declare_function(BuiltinFunctionDef(
    name='__mult',
    type_validation_func=validate_math,
    py_func=lambda x, y: x*y
))
__declare_function(BuiltinFunctionDef(
    name='__divide',
    type_validation_func=validate_math,
    py_func=lambda x, y: x // y if
    (isinstance(x, int) and isinstance(y, int)) else x / y
))
__declare_function(BuiltinFunctionDef(
    name='__neg',
    type_validation_func=validate_or(
        validate_static([DSLFloat], DSLFloat),
        validate_static([DSLInt], DSLInt)
    ),
    py_func=lambda x: (-x)
))
# endregion
# region Conditions
__declare_function(BuiltinFunctionDef(
    name='__or',
    type_validation_func=validate_boolean,
    py_func=lambda x, y: (x or y)
))
__declare_function(BuiltinFunctionDef(
    name='__and',
    type_validation_func=validate_boolean,
    py_func=lambda x, y: (x and y)
))
__declare_function(BuiltinFunctionDef(
    name='__not',
    type_validation_func=validate_static([DSLBoolean], DSLBoolean),
    py_func=lambda x: (not x)
))
__declare_function(BuiltinFunctionDef(
    name='__eq',
    type_validation_func=validate_cmp,
    py_func=lambda x, y: x == y
))
__declare_function(BuiltinFunctionDef(
    name='__neq',
    type_validation_func=validate_cmp,
    py_func=lambda x, y: x != y
))
__declare_function(BuiltinFunctionDef(
    name='__gr',
    type_validation_func=validate_cmp,
    py_func=lambda x, y: x > y
))
__declare_function(BuiltinFunctionDef(
    name='__ls',
    type_validation_func=validate_cmp,
    py_func=lambda x, y: x < y
))
__declare_function(BuiltinFunctionDef(
    name='__geq',
    type_validation_func=validate_cmp,
    py_func=lambda x, y: x >= y
))
__declare_function(BuiltinFunctionDef(
    name='__leq',
    type_validation_func=validate_cmp,
    py_func=lambda x, y: x <= y
))
# endregion
# region Arrays
__declare_function(BuiltinFunctionDef(
    name='push',
    type_validation_func=validate_array_index_value(3),
    py_func=array_push
))
__declare_function(BuiltinFunctionDef(
    name='pop',
    type_validation_func=validate_array_index_value(2),
    py_func=array_pop
))
__declare_function(BuiltinFunctionDef(
    name='__index',
    type_validation_func=validate_indexable_access,
    py_func=lambda arr, ind: arr[ind]
))
__declare_function(BuiltinFunctionDef(
    name='len',
    type_validation_func=validate_indexable_len,
    py_func=len
))
# endregion
# region Strings
__declare_function(
    BuiltinFunctionDef(
        name='sub',
        type_validation_func=validate_static(
            [DSLString, DSLInt, DSLInt],
            DSLString),
        py_func=lambda s, start, size: s[start: start + size]
    )
)
__declare_function(
    BuiltinFunctionDef(
        name='concat',
        type_validation_func=validate_static(
            [DSLString, DSLString],
            DSLString),
        py_func=lambda x, y: x+y
    )
)
__declare_function(
    BuiltinFunctionDef(
        name='split',
        type_validation_func=validate_static(
            [DSLString, DSLString],
            get_array_type(DSLString)),
        py_func=lambda x, y: x.split(y)
    )
)
__declare_function(
    BuiltinFunctionDef(
        name='lines',
        type_validation_func=validate_static(
            [DSLString],
            get_array_type(DSLString)),
        py_func=lambda x, y: x.split('\n')
    )
)
__declare_function(
    BuiltinFunctionDef(
        name='lower',
        type_validation_func=validate_static(
            [DSLString],
            DSLString),
        py_func=lambda x: x.lower()
    )
)
__declare_function(
    BuiltinFunctionDef(
        name='upper',
        type_validation_func=validate_static(
            [DSLString],
            DSLString),
        py_func=lambda x: x.upper()
    )
)
__declare_function(
    BuiltinFunctionDef(
        name='swap_case',
        type_validation_func=validate_static(
            [DSLString],
            DSLString),
        py_func=lambda x: x.swapcase()
    )
)
__declare_function(
    BuiltinFunctionDef(
        name='reverse',
        type_validation_func=validate_static(
            [DSLString],
            DSLString),
        py_func=lambda x: ''.join(reversed(x))
    )
)
__declare_function(
    BuiltinFunctionDef(
        name='join',
        type_validation_func=validate_static(
            [DSLString,get_array_type(DSLString)],
            DSLString),
        py_func=lambda x,y: x.join(y)
    )
)
# endregion
__declare_function(
    BuiltinFunctionDef(
        name='output',
        type_validation_func=lambda x: (DSLString if len(x) == 1 else None),
        py_func=lambda x: print(x)
    )
)
__declare_function(
    BuiltinFunctionDef(
        name='__input',
        type_validation_func=lambda: DSLString,
        py_func=lambda: read_block()
    )
)
