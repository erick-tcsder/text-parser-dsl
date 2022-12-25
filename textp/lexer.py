from ply import lex


tokens = (
    'SEMICOLON',

    # region ExtraFirstOpsNames
    'RARROW',
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
    'GREP',
    'SELECTOR',
    'EACH',
    'FIND',
    'FROM',
    'DO',
    'WORD',
)


t_SEMICOLON = ';'

# region ExtraFirstOps
t_BARROW = r'->'
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
t_XOR = r'\^'
t_BNOT = r'~'
# endregion

t_ASSIGN = r'='
t_POINT = r'\.'


def t_STRING(t):
    r'"(\.|[^\"])*"'
    t.value = t.value[1:-1]
    return t

# TODO: Quitar las palabras claves como tokens
# La razón de esto está aquí https://ply.readthedocs.io/en/latest/ply.html#specification-of-tokens
# Básicamente se pueden detectar como prefijo de otra palabra
# Ahí dice cómo hacerlo


t_DPIN = 'DPIN'
t_DPOUT = 'DPOUT'
t_GREP = 'GREP'
t_SELECTOR = 'SELECTOR'
t_EACH = 'EACH'
t_FIND = 'FIND'
t_FROM = 'FROM'
t_DO = 'DO'
t_WORD = r'[[_a-zA-Z][_a-zA-Z0-9]*]'
t_ID = r'[_a-zA-Z][_a-zA-Z0-9]*'

t_ignore = ' \t'


def t_NUMBER(t):
    r'\d+(.\d+)?'
    t.value = float(t.value)
    return t


# Se implemento la funcion por el orden de prioridad que aplica
# ply para las expresiones regulares
# ver https://stackoverflow.com/questions/2910338
# TODO La diferencia entre tipo y id es sintáctica?
# Si los tipos se escriben distinto ok, sino se debería poner
# como id y en el checkeo semántico comprobar qué es
def t_TYPE(token):
    r'[_A-Z]+'
    return token


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
