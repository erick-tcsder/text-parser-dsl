import ast_nodes
from bultin.types import DSLFloat, DSLString, DSLBoolean, DSLInt
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
