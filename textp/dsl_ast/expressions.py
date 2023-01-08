
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from typing_extensions import Self

from bultin.types.commmon import DSLType
from .common import ASTNode


@dataclass
class Expression(ASTNode):
    @abstractmethod
    def get_childs(self) -> List[Self]:
        pass


@dataclass
class Literal(Expression):
    value: DSLType

    def get_childs(self) -> List[Expression]:
        return []


@dataclass
class BinaryOperation(Expression):
    left_value: Expression
    right_value: Expression
    op: str

    def get_childs(self) -> List[Expression]:
        return [self.left_value, self.right_value]


@dataclass
class UnaryOperation(Expression):
    value: Expression
    op: str

    def get_childs(self) -> List[Expression]:
        return [self.value]
