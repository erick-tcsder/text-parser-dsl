import ast_nodes
from builtin.types import DSLFloat, DSLString, DSLBoolean, DSLInt
from utils import is_float


def p_expression_bool(p):
    '''expression : expression BOR expression
                  | expression BAND expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression GR expression
                  | expression LS expression
                  | expression GEQ expression
                  | expression LEQ expression'''
    p[0] = ast_nodes.BinaryOperation(
        exp1=p[1],
        exp2=p[3],
        op=p[2],
    )


def p_expression_math(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = ast_nodes.BinaryOperation(
        left_value=p[1],
        right_value=p[3],
        op=p[2],
    )


def p_expression_unary_bool(p):
    '''expression : NOT expression'''
    p[0] = ast_nodes.UnaryOperation(
        value=p[2],
        op=p[1],
    )


def p_expression_unary_math(p):
    '''expression : MINUS expression %prec UMINUS'''
    p[0] = ast_nodes.UnaryOperation(
        value=p[2],
        op=p[1],
    )


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
        value=DSLBoolean(bool(p[1]))
    )


def p_expression_capsule(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]


def p_expression_variable(p):
    '''expression : ID'''
    p[0] = ast_nodes.VariableCall(
        name=p[1]
    )


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
    p[0] = ast_nodes.IndexCall(
        name=p[1],
        arg=p[3]
    )

def p_values_single(p):
    '''values : expression'''
    p[0] = [p[1]]


def p_values_multi(p):
    '''values : expression COMMA values'''
    p[0] = [p[1]]+p[3]
