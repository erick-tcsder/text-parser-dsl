from dataclasses import dataclass
from typing import Any, Dict
from typing_extensions import Self


@dataclass(slots=True)
class Scope:
    parent: Self | None = None
    variables: Dict[str, Any] = {}
    functions: Dict[str, Any] = {}

    @property
    def isGlobal(self): return self.parent is None

    def has_definition(self, id: str, local_only: bool = False) -> bool:
        return id in self.variables or id in self.functions or (
            self.parent is
            not None and not local_only and self.parent.has_definition(id))

    def has_variable(self, id: str, local_only: bool = False) -> bool:
        return id in self.variables or (
            self.parent is not None and
            not local_only and self.parent.has_variable(id))

    def has_function(self, id: str, local_only: bool = False) -> bool:
        return id in self.functions or (
            self.parent is not None and
            not local_only and self.parent.has_function(id))

    def getVariable(self, id: str, local_only: bool = False) -> Any:
        v = self.variables.get(id, None)
        if not local_only and v is None and self.parent is not None:
            return self.parent.getVariable(id)
        return v

    def getFunction(self, id: str, local_only: bool = False) -> Any:
        v = self.functions.get(id, None)
        if not local_only and v is None and self.parent is not None:
            return self.parent.getFunction(id)
        return v

    def create_child(self) -> Self:
        return Scope(self)

    @property
    def top(self) -> Self:
        return self if self.isGlobal else self.parent.top
