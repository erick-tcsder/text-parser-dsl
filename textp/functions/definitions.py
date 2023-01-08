from abc import ABC
from dataclasses import dataclass
from typing import Any, Callable, Iterable, List
from builtin.types import DSLType


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
    The special arg validation is for function that allows complex 
    argument formats. Like the ones working with arrays.
    '''
    py_func: Callable
    special_arg_validation: Callable[[List[DSLType]], bool] | None = None


@dataclass(slots=True)
class DSLFunctionDef(FunctionDefinition):
    '''
    Function implemented on the DSL code. Has a reference to the 
    implementation code.
    '''
    code: Any  # NOTE: Should store an ast node with the definition on code
