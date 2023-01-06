from ply import lex

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'greep': 'GREEP',
    'select': 'SELECTOR',
    'each': 'EACH',
    'from': 'FROM',
    'do': 'DO',
    'find': 'FIND',
    'regexp': 'REGEXP',
    'filter': 'FILTER',
    'word': 'WORD',
    'for': 'FOR',
    'foreach': 'FOREACH',
    'in': 'IN',
    'def': 'DEF',
}

tokens = [
    'SEMICOLON',

    # region ExtraFirstOpsNames
    'BARROW',
    # endregion

    # region ConditionalsNames
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
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    # endregion

    # region BitNames
    'BAND',
    'BOR',
    'BXOR',
    'BNOT',
    # endregion

    'ASSIGN',
    'POINT',

    'STRING',

    'DPIN',
    'DPOUT',
    'TYPE',
    'NUMBER',
    'COMMA',
    'DOUBLE_DOT',
    'COLON',
] + list(reserved.values())


t_SEMICOLON = ';'
t_COMMA = ','
t_DOUBLE_DOT = '\.\.'
t_COLON = ':'

# region ExtraFirstOps
# t_BARROW = r'->'
# endregion

# region Conditionals
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
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
# endregion

# region Bit
t_BAND = r'&'
t_BOR = r'\|'
# t_XOR = r'\^'
t_BNOT = r'~'
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


def t_TYPE(token):
    r'INT|STRING|WORD'
    return token


def t_ID(t):
    r'[_a-zA-Z][_a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t


t_ignore = ' \t'


def t_NUMBER(t):
    r'\d+(.\d+)?'
    t.value = float(t.value)
    return t


def t_IN(t):
    r'IN'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)


# construye el lexer
lex.lex()


def tokenize(source: str):
    lex.input(source)
    while True:
        token = lex.token()
        if not token:
            break
        yield token
