from abc import ABC
from dataclasses import dataclass
from dsl_ast.expressions import *
from dsl_ast.statements import *
from dsl_ast.scope_calls import *
from dsl_ast.control import *
from dsl_ast.definitions import *


@dataclass
class ReceivingFromInput:
    variable_name: str


@dataclass
class SendingToOutput:
    text_to_send: Expression


@dataclass
class RegexExpression:
    pattern: str
    target: str


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
class Find(Expression, ABC):
    search: Expression
    source: str
