from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Type

from ..builtin.types import DSLType

from .common import ASTNode
from .expressions import Expression
from .statements import StatementList


@dataclass(slots=True)
class Definition(ASTNode):
    name: str
    type: Type[DSLType]

    @abstractmethod
    def get_children(self) -> List[ASTNode]:
        pass

    @abstractmethod
    def set_children(self, children: List[ASTNode]):
        pass


@dataclass(slots=True)
class VariableDefinition(Definition):
    value: Expression

    def get_children(self) -> List[ASTNode]:
        return [self.value]

    def set_children(self, children: List[ASTNode]):
        self.value = children


# Function definition nodes
@dataclass(slots=True)
class ParameterDefinition(Definition):
    def get_children(self) -> List[ASTNode]:
        return []

    def set_children(self, children: List[ASTNode]):
        pass


@dataclass(slots=True)
class ParameterList(ASTNode):
    parameters: List[ParameterDefinition]

    def get_children(self) -> List[ParameterDefinition]:
        return self.parameters

    def set_children(self, children: List[ParameterDefinition]):
        self.parameters = children


@dataclass(slots=True)
class FunctionDefinition(Definition):
    parameters: ParameterList
    code: StatementList

    def get_children(self) -> List[ASTNode]:
        return [self.parameters, self.code]

    def set_children(self, children: List[ASTNode]):
        self.parameters = children[0]
        self.code = children[1]
