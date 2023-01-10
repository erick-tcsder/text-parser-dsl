import ast_nodes
from builtin.types import DSLFloat, DSLString, DSLBoolean, DSLInt
from utils import is_float


def p_expression_bool(p):
    '''expression : expression OR expression
                  | expression AND expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression GR expression
                  | expression LS expression
                  | expression GEQ expression
                  | expression LEQ expression'''
    call = ast_nodes.FunctionCall(
        name=f'__{p.slice[2].type.lower()}',
        args=[p[1], p[3]]
    )
    p[0] = call


def p_expression_math(p):
    '''expression : expression ADD expression
                  | expression MINUS expression
                  | expression MULT expression
                  | expression DIVIDE expression'''
    call = ast_nodes.FunctionCall(
        name=f'__{p.slice[2].type.lower()}',
        args=[p[1], p[3]]
    )
    p[0] = call


def p_expression_unary_bool(p):
    '''expression : NOT expression'''
    call = ast_nodes.FunctionCall(
        name=f'__{p.slice[1].type.lower()}',
        args=[p[2]]
    )
    p[0] = call
    

def p_expression_unary_bool(p):
    '''expression : LEN expression'''
    call = ast_nodes.FunctionCall(
        name=f'__len',
        args=[p[2]]
    )
    p[0] = call


def p_expression_unary_math(p):
    '''expression : MINUS expression %prec UMINUS'''
    call = ast_nodes.FunctionCall(
        name='__neg',
        args=[p[2]]
    )
    p[0] = call


def p_expression_literal_float(p):
    '''expression : FLOAT'''
    p[0] = ast_nodes.Literal(
        value=DSLFloat(float(p[1]))
    )


def p_expression_literal_int(p):
    '''expression : INT'''
    p[0] = ast_nodes.Literal(
        value=DSLInt(int(p[1]))
    )


def p_expression_literal_string(p):
    '''expression : STRING'''
    p[0] = ast_nodes.Literal(
        value=DSLString(p[1])
    )


def p_expression_literal_bool(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = ast_nodes.Literal(
        value=DSLBoolean(True if p[1] == 'true' else False)
    )


def p_expression_capsule(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]


def p_expression_function_simple(p):
    '''expression : ID LPAREN RPAREN'''
    p[0] = ast_nodes.FunctionCall(
        name=p[1],
        args=[]
    )


def p_expression_function_param(p):
    '''expression : ID LPAREN values RPAREN'''
    p[0] = ast_nodes.FunctionCall(
        name=p[1],
        args=p[3]
    )


def p_expression_indexing(p):
    '''expression : ID LBRACKET expression RBRACKET'''
    p[0] = ast_nodes.FunctionCall(
        name='__index',
        args=[p[1], p[3]]
    )

def p_values_single(p):
    '''values : expression'''
    p[0] = [p[1]]


def p_values_multi(p):
    '''values : expression COMMA values'''
    p[0] = [p[1]]+p[3]


def p_expression_assign(p):
    '''expression : assign'''
    p[0] = p[1]


def p_assign(p):
    '''assign : ID ASSIGN expression'''
    p[0] = ast_nodes.VariableAssign(
        name=p[1],
        value=p[3]
    )


def p_expression_variable(p):
    '''expression : ID'''
    p[0] = ast_nodes.VariableCall(
        name=p[1]
    )


def p_expression_literal_array(p):
    '''expression : LBRACKET values RBRACKET'''
    p[0] = ast_nodes.LiteralArray(
        values=p[2]
    )
