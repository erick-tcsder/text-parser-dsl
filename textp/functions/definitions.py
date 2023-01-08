from dataclasses import dataclass
from typing import Any, Callable, List
from bultin.types import DSLType


@dataclass(slots=True)
class FunctionDefinition:
    name: str
    param_types: List[DSLType]
    return_type: DSLType


@dataclass(slots=True)
class BuiltinFunctionDef(FunctionDefinition):
    py_func: Callable


@dataclass(slots=True)
class DSLFunctionDef(FunctionDefinition):
    code: Any  # NOTE: Should store an ast node with the definition on code
