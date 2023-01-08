
from abc import ABC
from dataclasses import dataclass

from bultin.types.commmon import DSLType


@dataclass
class Expression(ABC):
    pass


@dataclass
class Literal(Expression):
    value: DSLType


@dataclass
class BinaryOperation(Expression):
    left_value: Expression
    right_value: Expression
    op: str


@dataclass
class UnaryOperation(Expression):
    value: Expression
    op: str
