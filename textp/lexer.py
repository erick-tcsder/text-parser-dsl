from ply import lex


tokens = (
    'SEMICOLON',
    'OPEN_BRACKET',
    'CLOSED_BRACKET',
    'EQUALS',
    'GREATER',
    'DPIN',
    'DPOUT',
    'ID',
    'TYPE',
    'NUMBER',
    'GREP',
    'SELECTOR',
    'EACH',
    'FIND',
    'FROM',
    'DO',
    'WORD',
    'LCURLY',
    'RCURLY',)


t_SEMICOLON = ';'
t_EQUALS = '='
t_GREATER = '>'
# TODO: Quitar las palabras claves como tokens
# La razón de esto está aquí https://ply.readthedocs.io/en/latest/ply.html#specification-of-tokens
# Básicamente se pueden detectar como prefijo de otra palabra
# Ahí dice cómo hacerlo
t_DPIN = 'DPIN'
t_DPOUT = 'DPOUT'
t_OPEN_BRACKET = r'\['
t_CLOSED_BRACKET = r'\]'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_GREP = 'GREP'
t_SELECTOR = 'SELECTOR'
t_EACH = 'EACH'
t_FIND = 'FIND'
t_FROM = 'FROM'
t_DO = 'DO'
t_WORD = r'[[_a-zA-Z][_a-zA-Z0-9]*]'
t_ID = r'[_a-zA-Z][_a-zA-Z0-9]*'
t_ignore = ' \t\n'


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


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)


#construye el lexer
lex.lex()


def tokenize(source: str):
    lex.input(source)
    while True:
        token = lex.token()
        if not token:
            break
        yield token