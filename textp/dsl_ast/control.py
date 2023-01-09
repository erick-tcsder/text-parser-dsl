
from dataclasses import dataclass
from typing import List

from .common import ASTNode
from .expressions import Expression, VariableAssign
from .statements import StatementList
from .definitions import VariableDefinition


@dataclass(slots=True)
class IfStatement(ASTNode):
    condition: Expression
    then_code: StatementList
    else_code: StatementList | None = None

    def get_children(self) -> List[ASTNode]:
        return [self.condition, self.then_code, self.else_code]

    def set_children(self, children: List[ASTNode]):
        self.condition = children[0]
        self.then_code = children[1]
        self.else_code = children[2]


@dataclass(slots=True)
class Loop(ASTNode):
    pass


@dataclass(slots=True)
class WhileLoop(Loop):
    exp: Expression
    loop_code: StatementList

    def get_children(self) -> List[ASTNode]:
        return [self.exp, self.loop_code]

    def set_children(self, children: List[ASTNode]):
        self.exp = children[0]
        self.loop_code = children[1]


@dataclass(slots=True)
class ForLoop(Loop):
    variable_def: VariableDefinition
    condition: Expression
    step: VariableAssign
    code: StatementList

    def get_children(self) -> List[ASTNode]:
        return [
            self.variable_def,
            self.condition,
            self.step,
            self.code
        ]

    def set_children(self, children: List[ASTNode]):
        self.variable_def = children[0]
        self.condition = children[1]
        self.step = children[2]
        self.code = children[3]


@dataclass(slots=True)
class ForeachLoop(Loop):
    variable: str
    array: Expression
    code: StatementList

    def get_children(self) -> List[ASTNode]:
        return [
            self.array,
            self.code
        ]

    def set_children(self, children: List[ASTNode]):
        self.array = children[0]
        self.code = children[1]
