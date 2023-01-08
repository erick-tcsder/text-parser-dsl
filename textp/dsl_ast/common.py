from abc import ABC, abstractmethod
from typing import List
from typing_extensions import Self


class ASTNode(ABC):
    @abstractmethod
    def get_childs(self) -> List[Self]:
        pass
