from abc import ABC, abstractmethod
from typing import List
from typing_extensions import Self


class ASTNode(ABC):
    @abstractmethod
    def get_childs(self) -> List[Self]:
        pass
    
    @abstractmethod
    def set_childs(self, childs:List[Self]):
        pass
