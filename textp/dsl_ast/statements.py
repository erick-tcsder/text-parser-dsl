
from abc import abstractmethod
from dataclasses import dataclass
from typing import List

from .common import ASTNode


class Statement(ASTNode):
    @abstractmethod
    def get_childs(self) -> List[ASTNode]:
        pass


@dataclass
class StatementList:
    statements: List[Statement]

    def get_childs(self) -> List[Statement]:
        return self.statements
