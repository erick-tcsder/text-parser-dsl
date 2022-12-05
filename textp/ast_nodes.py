from abc import ABC
from typing import List
from dataclasses import dataclass


class Expression(ABC):
    pass


@dataclass
class VariableDefinition:
    _type: str
    name: str
    value: Expression
    

@dataclass
class ReceivingFromInput:
    variable_name: str


@dataclass
class SendingToOutput:
    text_to_send: Expression


@dataclass
class Type:
    name: str


@dataclass
class ListOfType:
    name: str

@dataclass
class GetVariableValue:
    name: str

@dataclass
class Number:
    value: float


@dataclass
class Statement:
    pass


@dataclass
class StatementList:
    statements: List[Statement]

    def append(self, statement: Statement):
        new_statements = self.statements + [statement]
        return StatementList(statements=new_statements)
    