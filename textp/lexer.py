from ply import lex

reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'greep': 'GREEP',
   'select': 'SELECTOR',
   'each': 'EACH',
   'from':'FROM',
   'do':'DO',
   'find':'FIND',
   'regexp':'REGEXP',
   'filter':'FILTER',
   'word': 'WORD',
   'for': 'FOR',
   'foreach': 'FOREACH',
   'in' : 'IN',
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
    'COLON',
    'DOUBLE_DOT',
] + list(reserved.values())


t_SEMICOLON = ';'
t_COLON = ':'
t_COMMA = ','
t_DOUBLE_DOT = '\.\.'

# region ExtraFirstOps
#t_BARROW = r'->'
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
#t_XOR = r'\^'
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

# IMPORTANTE: es necesario la implementacion de metodos para definir las expresiones
# refuex porque la biblioteca ply prioriza metodos por encima de las definiciones normales
# y las palabras reservadas van a matchear primero con type o con Id que con sus definiciones
# con las implementaciones de los metodos no :)
# def t_IF(t):
#     r'IF'
#     return t

# def t_THEN(t):
#     r'THEN'
#     return t

# def t_ELSE(t):
#     r'ELSE'
#     return t

# def t_DEF(t):
#     r'DEF '
#     return t

# def t_FOREACH(t):
#     r'FOREACH'
#     return t

# def t_FOR(t):
#     r'FOR'
#     return t

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
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

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
