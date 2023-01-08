from abc import abstractmethod
from dataclasses import dataclass
from typing import List
from .expressions import Expression


@dataclass(slots=True)
class Call(Expression):
    name: str

    @abstractmethod
    def get_children(self) -> List[Expression]:
        pass

    @abstractmethod
    def set_children(self, children: List[Expression]):
        pass


@dataclass(slots=True)
class VariableCall(Call):
    def get_children(self) -> List[Expression]:
        return []

    def set_children(self, children: List[Expression]):
        pass


@dataclass(slots=True)
class FunctionCall(Call):
    args: List[Expression]

    def get_children(self) -> List[Expression]:
        return self.args

    def set_children(self, children: List[Expression]):
        self.args = children


@dataclass(slots=True)
class IndexCall(Call):
    arg: Expression

    def get_children(self) -> List[Expression]:
        return [self.arg]

    def set_children(self, children: List[Expression]):
        self.arg = children[0]
