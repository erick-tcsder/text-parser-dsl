
from typing import Callable, List, Type
from builtin.types import DSLType


class BuiltinFunctionDef:
    name: str
    type_validation_func: Callable[[List[Type[DSLType]]], Type[DSLType]]
    py_func: Callable
