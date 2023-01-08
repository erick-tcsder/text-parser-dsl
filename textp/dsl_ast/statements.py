
from abc import abstractmethod
from dataclasses import dataclass
from typing import List

from .common import ASTNode


class Statement(ASTNode):
    pass


@dataclass(slots=True)
class StatementList(ASTNode):
    statements: List[Statement]

    def get_children(self) -> List[Statement]:
        return self.statements

    def set_children(self, childs: List[Statement]):
        self.statements = childs
