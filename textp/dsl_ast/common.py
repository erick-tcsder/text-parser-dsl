from abc import ABC, abstractmethod
from typing import List
from typing_extensions import Self


class ASTNode(ABC):
    '''
    Like every tree a node should have children. This should allow to navigate 
    the tree independently of the data format of each node.
    '''
    @abstractmethod
    def get_children(self) -> List[Self]:
        pass
    
    @abstractmethod
    def set_children(self, childs: List[Self]):
        pass
