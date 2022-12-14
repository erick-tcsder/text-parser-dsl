from ply import lex
from .keywords import KEYWORDS as reserved

tokens = [
    'SEMICOLON',

    # region ExtraFirstOpsNames
    'BARROW',
    # endregion

    # region ConditionalsNames
    'AND',
    'OR',
    'EQ',
    'NEQ',
    'GR',
    'LS',
    'GEQ',
    'LEQ',
    'NOT',
    # endregion

    # region BracketlikesNames
    'LBRACKET',
    'RBRACKET',
    'LCURLY',
    'RCURLY',
    'LPAREN',
    'RPAREN',
    # endregion

    'ID',  # Standard id

    # region ArithmeticNames
    'ADD',
    'MINUS',
    'MULT',
    'DIVIDE',
    # endregion

    'QUOTE',

    'ASSIGN',
    'POINT',

    'STRING',

    'DPIN',
    'DPOUT',
    'FLOAT',
    'INT',
    'COMMA',
    'DOUBLE_DOT',
    'COLON',
] + list(set(reserved.values()))


t_SEMICOLON = ';'
t_COMMA = ','
t_DOUBLE_DOT = '\.\.'
t_COLON = ':'

# region ExtraFirstOps
# t_BARROW = r'->'
# endregion

# region Conditionals
t_AND = r'&'
t_OR = r'\|'
t_EQ = '=='
t_NEQ = '!='
t_GR = '>'
t_LS = '<'
t_GEQ = '>='
t_LEQ = '<='
t_NOT = '!'
# endregion

# region Bracketlikes
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
# endregion

# region Arithmetic
t_ADD = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIVIDE = r'/'
# endregion

t_ASSIGN = r'='
t_POINT = r'\.'


def t_STRING(t):
    r'"(\.|[^\"])*"'
    t.value = t.value[1:-1]
    return t


def t_DPIN(t):
    r'DPIN'
    return t


def t_DPOUT(t):
    r'DPOUT'
    return t


def t_ID(t):
    r'[_a-zA-Z][_a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t


t_ignore = ' \t'


def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_IN(t):
    r'IN'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# construye el lexer
lex.lex()


def tokenize(source: str):
    lex.input(source)
    while True:
        token = lex.token()
        if not token:
            break
        yield token
