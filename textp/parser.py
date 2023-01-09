from parser_units.expressions import *
from parser_units.statements import *
from parser_units.control import *
from parser_units.typing import *
from parser_units.definitions import *
from ply import *
import lexer
import ast_nodes
import utils
# import evaluator
from visitor import visitor
import builtin.types as types


tokens = lexer.tokens

precedence = (
    ('right', 'ASSIGN'),
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
    ast = parse('''int[][] functi (int a,int b) { 
                        5+6; 
                    };
                    
                    foreach v in values {
                        string vaca = "vaca muu";
                        vaca = st = 34 / 2;
                        return 6;
                    }; 
                    
                    while(true) {
                        if false | true {
                            break;
                        } else {
                            if (false) {
                                continue;
                            };
                        };
                    };''')
    print(ast)
