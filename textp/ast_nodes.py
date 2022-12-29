from abc import ABC
from typing import List, Union
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
class ORExp:
    exp: Union['ORExp', 'ANDExp']
    term: 'ANDExp'

@dataclass
class ANDExp:
    term: Union['ANDExp', 'BPrimary']
    factor: 'BPrimary'

@dataclass
class NOTExp:
    term: 'BPrimary'
    
@dataclass
class BPrimary:
    pass

@dataclass
class IFStatement:
    exp: Expression
    THENstatemet: Statement
    ELSEstatement: Statement
@dataclass
class CMPExp:
    exp1: Expression
    exp2: Expression
    op: str
    
@dataclass
class PLUSExp:
    exp: Union['PLUSExp', 'MINUSExp']
    term: Expression

@dataclass
class MINUSExp:
    exp: Union['PLUSExp', 'MINUSExp']
    term: Expression
    
@dataclass
class TIMESExp:
    exp: Union['TIMESExp', 'DIVIDEExp']
    term: 'Factor'
    
@dataclass
class DIVIDEExp:
    exp: Union['TIMESExp', 'DIVIDEExp']
    term: 'Factor'

@dataclass
class Factor:
    pass
@dataclass
class StatementList:
    statements: List[Statement]

    def append(self, statement: Statement):
        new_statements = self.statements + [statement]
        return StatementList(statements=new_statements)
    