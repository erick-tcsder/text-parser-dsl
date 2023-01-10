
from dataclasses import dataclass
from typing import Any, Callable, List, Type
from builtin.types import DSLType

@dataclass
class BuiltinFunctionDef:
    name: str
    type_validation_func: Callable[[List[Type[DSLType]]], Type[DSLType]]
    py_func: Callable[[Any],Any]
