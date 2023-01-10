
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from typing_extensions import Self

from ..builtin.types.commmon import DSLType
from ..builtin.types.array import DSLArray
from .common import ASTNode


@dataclass
class Expression(ASTNode):
    pass


@dataclass(slots=True)
class Literal(Expression):
    value: DSLType

    def get_children(self) -> List[Expression]:
        return []

    def set_children(self, childs: List[Expression]):
        pass


@dataclass(slots=True)
class LiteralArray(Expression):
    values: List[Expression]

    def get_children(self) -> List[Expression]:
        return self.values

    def set_children(self, children: List[Expression]):
        self.values = children

@dataclass(slots=True)
class VariableAssign(Expression):
    name: str
    value: Expression

    def get_children(self) -> List[Expression]:
        return [self.value]

    def set_children(self, children: List[Expression]):
        self.value = children[0]
