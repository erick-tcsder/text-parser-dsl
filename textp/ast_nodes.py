from abc import ABC
from typing import Any, List, Union
from dataclasses import dataclass
from bultin.types.commmon import DSLType


@dataclass
class Expression(ABC):
    pass


@dataclass
class Literal(Expression):
    value: DSLType


@dataclass
class VariableDefinition:
    _type: str
    name: str
    value: Expression


@dataclass
class Values:
    values: List[Union['Number', Expression]]


@dataclass
class ArrayDefinition:
    _type: str
    name: str
    size: 'Number'
    values: Values


@dataclass
class BinaryOperation(Expression):
    left_value: Expression
    right_value: Expression
    op: str


@dataclass
class UnaryOperation(Expression):
    value: Expression
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
class Statement:
    pass


@dataclass
class IFStatement:
    exp: Expression
    THENstatemet: 'StatementList'
    ELSEstatement: 'StatementList'


@dataclass
class StatementList:
    statements: List[Statement]


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
    return_type: Type


@dataclass
class FunctionDefinitionList:
    function_definitions: List[FunctionDefinition]

    def append(self, function_definition: FunctionDefinition):
        new_function_definitions = self.function_definitions + [
            function_definition]
        return FunctionDefinitionList(
            function_definitions=new_function_definitions)


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
