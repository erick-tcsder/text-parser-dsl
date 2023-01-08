
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from typing_extensions import Self

from bultin.types.commmon import DSLType
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
class BinaryOperation(Expression):
    left_value: Expression
    right_value: Expression
    op: str

    def get_children(self) -> List[Expression]:
        return [self.left_value, self.right_value]

    def set_children(self, childs: List[Expression]):
        self.left_value = childs[0]
        self.right_value = childs[1]


@dataclass(slots=True)
class UnaryOperation(Expression):
    value: Expression
    op: str

    def get_children(self) -> List[Expression]:
        return [self.value]

    def set_children(self, childs: List[Expression]):
        self.value = childs[0]
