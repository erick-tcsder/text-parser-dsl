
from abc import abstractmethod
from dataclasses import dataclass
from typing import List

from .common import ASTNode


class Statement(ASTNode):
    pass


@dataclass
class StatementList(ASTNode):
    statements: List[Statement]

    def get_childs(self) -> List[Statement]:
        return self.statements

    def set_childs(self, childs: List[Statement]):
        self.statements = childs
