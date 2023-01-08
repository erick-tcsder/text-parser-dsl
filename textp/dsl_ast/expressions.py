
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from typing_extensions import Self

from bultin.types.commmon import DSLType
from .common import ASTNode


@dataclass
class Expression(ASTNode):
    pass


@dataclass
class Literal(Expression):
    value: DSLType

    def get_childs(self) -> List[Expression]:
        return []

    def set_childs(self, childs: List[Expression]):
        pass


@dataclass
class BinaryOperation(Expression):
    left_value: Expression
    right_value: Expression
    op: str

    def get_childs(self) -> List[Expression]:
        return [self.left_value, self.right_value]

    def set_childs(self, childs: List[Expression]):
        self.left_value = childs[0]
        self.right_value = childs[1]


@dataclass
class UnaryOperation(Expression):
    value: Expression
    op: str

    def get_childs(self) -> List[Expression]:
        return [self.value]

    def set_childs(self, childs: List[Expression]):
        self.value = childs[0]
