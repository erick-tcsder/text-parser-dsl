
from abc import abstractmethod
from dataclasses import dataclass
from typing import List

from .common import ASTNode
from .expressions import Expression


class Statement(ASTNode):
    pass


@dataclass(slots=True)
class StatementList(ASTNode):
    statements: List[Statement]

    def get_children(self) -> List[Statement]:
        return self.statements

    def set_children(self, childs: List[Statement]):
        self.statements = childs


@dataclass(slots=True)
class Break(ASTNode):
    def get_children(self) -> List[ASTNode]:
        return []

    def set_children(self, _: List[ASTNode]):
        pass


@dataclass(slots=True)
class Continue(ASTNode):
    def get_children(self) -> List[ASTNode]:
        return []

    def set_children(self, _: List[ASTNode]):
        pass


@dataclass(slots=True)
class Return(ASTNode):
    value: Expression
    def get_children(self) -> List[Expression]:
        return [self.value]

    def set_children(self, children: List[Expression]):
        self.value=children[0]