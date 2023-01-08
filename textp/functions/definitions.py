from abc import ABC
from dataclasses import dataclass
from typing import Any, Callable, Iterable
from bultin.types import DSLType


@dataclass(slots=True)
class FunctionDefinition(ABC):
    '''
    Basic defined function.
    '''
    name: str
    param_types: Iterable[DSLType]
    return_type: DSLType


@dataclass(slots=True)
class BuiltinFunctionDef(FunctionDefinition):
    '''
    Function with implementation madded in python, not in the DSL.
    '''
    py_func: Callable


@dataclass(slots=True)
class DSLFunctionDef(FunctionDefinition):
    '''
    Function implemented on the DSL code. Has a reference to the 
    implementation code.
    '''
    code: Any  # NOTE: Should store an ast node with the definition on code
