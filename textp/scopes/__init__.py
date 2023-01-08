from dataclasses import dataclass
from typing import Any, Dict, Iterable
from typing_extensions import Self

from builtin.types.commmon import DSLType


@dataclass(slots=True)
class Scope:
    parent: Self | None = None
    variables: Dict[str, Any] = {}
    functions: Dict[str, Any] = {}

    @property
    def isGlobal(self): return self.parent is None

    def hasdefinition(self, id: str, local_only: bool = False) -> bool:
        return id in self.variables or id in self.functions or (
            self.parent is
            not None and not local_only and self.parent.has_definition(id))

    def hasvariable(self, id: str, local_only: bool = False) -> bool:
        return id in self.variables or (
            self.parent is not None and
            not local_only and self.parent.has_variable(id))

    def hasfunction(self, id: str, local_only: bool = False) -> bool:
        return id in self.functions or (
            self.parent is not None and
            not local_only and self.parent.has_function(id))

    def getvariable(self, id: str, local_only: bool = False) -> Any:
        v = self.variables.get(id, None)
        if not local_only and v is None and self.parent is not None:
            return self.parent.getVariable(id)
        return v

    def getfunction(self, id: str, parameters_types: Iterable[DSLType], local_only: bool = False) -> Any:
        v = self.functions.get(id, None)
        if not local_only and v is None and self.parent is not None:
            return self.parent.getFunction(id)
        return v

    def create_child(self) -> Self:
        return Scope(self)

    @property
    def top(self) -> Self:
        return self if self.isGlobal else self.parent.top
