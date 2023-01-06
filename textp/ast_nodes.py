from abc import ABC
from typing import List, Union
from dataclasses import dataclass


@dataclass
class Expression(ABC):
    pass


@dataclass
class VariableDefinition:
    _type: str
    name: str
    value: Expression

@dataclass
class Value:
    _type: 'Type'
    name: str

@dataclass
class Values:
    values: List[Union['Number', Expression]]
    
    def append(self, value: Value):
        new_values = self.values + [value]
        return Values(values = new_values)

@dataclass
class ArrayDefinition:
    _type: str
    name: str
    size: 'Number'
    values: Values
@dataclass
class BinaryOperation:
    left_value: Expression
    right_value: Expression
    op: str

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
    THENstatemet: 'StatementList'
    ELSEstatement: 'StatementList'
@dataclass
class CMPExp:
    exp1: Expression
    exp2: Expression
    op: str
    
@dataclass
class Factor:
    pass
@dataclass
class StatementList:
    statements: List[Statement]

    def append(self, statement: Statement):
        new_statements = self.statements + [statement]
        return StatementList(statements=new_statements)

@dataclass
class Parameter:
    _type: Type
    name: str

@dataclass
class ParameterList:
    parameters: List[Parameter]
    
    def append(self, parameter: Parameter):
        new_parameters = self.parameters + [parameter]
        return ParameterList(parameters=new_parameters)

@dataclass
class FunctionDefinition:
    name: str
    parameters: ParameterList
    statements: StatementList
    return_type : Type

@dataclass
class FunctionDefinitionList:
    function_definitions: List[FunctionDefinition]
    
    def append(self, function_definition: FunctionDefinition):
        new_function_definitions = self.function_definitions + [function_definition]
        return FunctionDefinitionList(function_definitions=new_function_definitions)
    
@dataclass
class RegexExpression:
    pattern: str
    target: str

@dataclass
class ForLoop:
    loop_variable: str
    range: Union['Range', Expression]
    statements: StatementList

@dataclass
class VariableAssignment:
    name: str
    value: Expression

@dataclass
class ForeachLoop:
    loop_variable: str
    iterable: str
    statements: StatementList

@dataclass
class Range:
    start: Expression
    end: Expression
    
@dataclass
class Grep(Expression, ABC):
    pattern: str
    target: str

@dataclass
class Select(Expression, ABC):
    selection: Expression
    source: str
    statements: StatementList

@dataclass
class Foreach(Expression, ABC):
    loop_variable: str
    iterable: str
    statements: StatementList

@dataclass
class Find(Expression, ABC):
    search: Expression
    source: str