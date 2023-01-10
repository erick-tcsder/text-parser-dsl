from dataclasses import dataclass
from typing import Any, Dict, Iterable
from typing_extensions import Self

from ..builtin.types.commmon import DSLType
from ..builtin.functions.decl import BUILTIN_FUNCS, BuiltinFunctionDef
from ..ast_nodes import FunctionDefinition


class Scope:
    parent: Self | None = None
    variables: Dict[str, Any] = {}
    builtin_function: Dict[str, BuiltinFunctionDef] = BUILTIN_FUNCS
    dsl_function: Dict[str, FunctionDefinition] = {}

    def __init__(self, parent: Self | None = None):
        self.parent = parent
        self.dsl_function = {}
        self.variables = {}

    @property
    def isGlobal(self): return self.parent is None

    def hasdefinition(self, id: str, local_only: bool = False) -> bool:
        return id in self.variables or id in self.builtin_function or id in self.dsl_function or (
            self.parent is
            not None and not local_only and self.parent.hasdefinition(id))

    def hasvariable(self, id: str, local_only: bool = False) -> bool:
        return id in self.variables or (
            self.parent is not None and
            not local_only and self.parent.hasvariable(id))

    def hasfunction(self, id: str, local_only: bool = False) -> bool:
        return id in self.builtin_function or id in self.dsl_function or (
            self.parent is not None and
            not local_only and self.parent.hasfunction(id))

    def hasbuiltinfunction(self, id: str, local_only: bool = False) -> bool:
        return id in self.builtin_function or (
            self.parent is not None and
            not local_only and self.parent.hasbuiltinfunction(id))

    def hasdslfunction(self, id: str, local_only: bool = False) -> bool:
        return id in self.builtin_function or (
            self.parent is not None and
            not local_only and self.parent.hasdslfunction(id))

    def getvariable(self, id: str, local_only: bool = False) -> Any:
        v = self.variables.get(id, None)
        if not local_only and v is None and self.parent is not None:
            return self.parent.getvariable(id)
        return v

    def getfunction(
            self, id: str,
            local_only: bool = False) -> Any:
        v = self.builtin_function.get(id, None)
        if v is None:
            v = self.dsl_function.get(id, None)
        if not local_only and v is None and self.parent is not None:
            return self.parent.getfunction(id)
        return v

    def getbuiltinfunction(
            self, id: str,
            local_only: bool = False) -> Any:
        v = self.builtin_function.get(id, None)
        if not local_only and v is None and self.parent is not None:
            return self.parent.getbuiltinfunction(id)
        return v

    def getdslfunction(
            self, id: str,
            local_only: bool = False) -> Any:
        v = self.dsl_function.get(id, None)
        if not local_only and v is None and self.parent is not None:
            return self.parent.getdslfunction(id)
        return v

    def assignvariable(
        self, id: str, value: Any,
        local_only: bool = False
    ) -> bool:
        if id in self.variables or local_only:
            self.variables[id] = value
            return True
        elif self.parent is None:
            return False
        else:
            return self.parent.assignvariable(id, value)

    def create_child(self) -> Self:
        return Scope(parent=self)

    @property
    def top(self) -> Self:
        return self if self.isGlobal else self.parent.top
