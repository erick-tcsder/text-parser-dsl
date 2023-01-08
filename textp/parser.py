from parser_units.expressions import *
from ply import *
import lexer
import ast_nodes
import utils
# import evaluator
from visitor import visitor
import builtin.types as types


tokens = lexer.tokens

precedence = (
    ('left', 'BOR', 'BAND'),
    ('left', 'EQ', 'NEQ', 'GR', 'LS', 'GEQ', 'LEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),             # Unary
    ('right', 'NOT'),               # Unary
)

start = 'program'


def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]


def p_statement_list(p):
    '''statement_list : statement SEMICOLON statement_list
                      | empty'''
    no_statement = len(p) == 2
    if no_statement:
        p[0] = ast_nodes.StatementList([])
    else:
        if p[1] is None:
            p[0] = p[3]
        else:
            p[0] = ast_nodes.StatementList([p[1]]+p[3].statements)


def p_statement(p):
    '''statement : if_statement
                 | function_definition
                 | for_loop
                 | foreach_loop
                 | expression
                 | empty'''
    p[0] = p[1]

# TODO: Use expressions instead of directly numbers for arrays
# def p_assign(p):
#     '''assign : type ID ASSIGN expression
#               | ID ASSIGN expression
#               | type ID LBRACKET NUMBER RBRACKET ASSIGN LBRACKET values RBRACKET'''
#     if len(p) == 5:  # Asignación con declaración de tipo
#         p[0] = ast_nodes.VariableDefinition(
#             _type=p[1],
#             name=p[2],
#             value=p[4]
#         )
#     elif len(p) == 4:  # Asignación sin declaración de tipo
#         p[0] = ast_nodes.VariableAssignment(
#             name=p[1],
#             value=p[3]
#         )
#     else:
#         p[0] = ast_nodes.ArrayDefinition(
#             _type=p[1],
#             name=p[2],
#             size=int(p[4]),
#             values=p[8]
#         )


def p_type_simple(p):
    '''type : TYPE'''
    p[0] = types.TYPENAMES[p[1]]


def p_type_array(p):
    '''type : type LBRACKET RBRACKET'''
    p[0] = types.get_array_type(p[1])


def p_empty(p):
    '''empty : '''

# TODO: Change syntax to avoid DPOUT shift/reduce conflict
# def p_input(p):
#     '''input : DPIN GR GR ID'''
#     p[0] = ast_nodes.ReceivingFromInput(
#         variable_name=p[4]
#     )


# def p_output(p):
#     '''output : ID GR GR DPOUT'''
#     p[0] = ast_nodes.SendingToOutput(
#         text_to_send=p[1]
#     )


def p_function_definition(p):
    '''function_definition : DEF type ID LPAREN parameter_list RPAREN LCURLY statement_list RCURLY'''
    p[0] = ast_nodes.FunctionDefinition(
        name=p[3],
        parameters=p[5],
        statements=p[8],
        return_type=p[2]
    )


def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA parameter
                      | parameter
                      | empty'''
    if len(p) == 2:
        p[0] = ast_nodes.ParameterList([])
    elif len(p) == 4:
        parameter_list = p[1]
        parameter = p[3]
        p[0] = parameter_list.append(parameter)
    else:
        p[0] = p[1]


def p_parameter(p):
    '''parameter : type ID'''
    p[0] = ast_nodes.Parameter(
        _type=p[1],
        name=p[2]
    )


def p_if_statement(p):
    '''if_statement : IF expression THEN LCURLY statement_list RCURLY ELSE LCURLY statement_list RCURLY'''
    p[0] = ast_nodes.IFStatement(
        exp=p[2],
        THENstatemet=p[5],
        ELSEstatement=p[9]
    )


# def p_values(p):
#     '''values : expression
#               | expression COMMA values'''
#     f = ast_nodes.Values([p[1]])
#     if len(p) == 2:
#         p[0] = f
#     else:
#         p[0] = f.extend(p[3])


# def p_values_empty(p):
#     '''values : empty'''
#     p[0] = ast_nodes.Values([])


def p_for_loop(p):
    '''for_loop : FOR ID IN range LCURLY statement_list RCURLY'''
    p[0] = ast_nodes.ForLoop(
        loop_variable=p[2],
        range=p[4],
        statements=p[6]
    )


def p_foreach_loop(p):
    '''foreach_loop : FOREACH ID IN ID LCURLY statement_list RCURLY'''
    p[0] = ast_nodes.ForeachLoop(
        loop_variable=p[2],
        iterable=p[4],
        statements=p[6]
    )


def p_range(p):
    '''range : expression DOUBLE_DOT expression
             | expression'''
    if len(p) == 4:
        p[0] = ast_nodes.Range(start=p[1], end=p[3])
    else:
        p[0] = ast_nodes.Range(start=p[1])


def p_error(t):
    print("Illegal sentence %s" % t.value)
    t.lexer.skip(1)


parser = yacc.yacc()


def parse(data, debug=True):
    parser.error = 0
    p = parser.parse(data, debug=debug)
    if parser.error:
        return None
    return p


if __name__ == '__main__':
    # print(
    #     parse(
    #         'def INT functi (INT a, INT b, INT c) { INT c=1; } ;',
    #         debug=False))
    # print()
    # # print(parse('for i in 1..5: i >> DPOUT; ;', debug=False))
    # print()
    # # print(parse('foreach w in wordt: w >> DPOUT; ;', debug=False))
    # ast = parse("INT a [ 5 ] = [ 1 , 2, 3 , 4 , 5];", debug=False)
    # print(ast)
    # evaluator = evaluator.Evaluator()
    # ast = parse('( apply(5) * var / sign(-13.0,true) )+"ja";;')
    ast = parse('def int[][] functi (int a,int b) { 5+6; }; var[5+6];')
    print(ast)
