from parser_units.expressions import *
from parser_units.statements import *
from parser_units.control import *
from parser_units.typing import *
from parser_units.definitions import *
from semantics.semantic_checker import SemanticChecker
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
    ('left', 'OR', 'AND'),
    ('left', 'EQ', 'NEQ', 'GR', 'LS', 'GEQ', 'LEQ'),
    ('left', 'ADD', 'MINUS'),
    ('left', 'MULT', 'DIVIDE'),
    ('right', 'UMINUS'),             # Unary
    ('right', 'NOT'),               # Unary
)

start = 'program'


def p_program(p):
    '''program : statement_list'''
    p[0] = ast_nodes.Program(p[1])


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


def p_error(t, *args, **kwargs):
    if t is None:
        print("Unexpected end of file")
        return
    print(f"Syntax error. line:{t.lexer.lineno} Unexpected character {t.value}")
    skip_step = t.lexer.lexdata[t.lexer.lexpos+1:].find(';')
    t.lexer.skip(skip_step)


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
    ast = parse('''int[] functi (int a) { 
                        return [a]; 
                    };
                    
                    int[] test = [1,2,3];
                    
                    foreach v in test {
                        break;
                    }; 
                    
                    while(true) {
                        if false{
                            break
                        } else {
                            if (false) {
                                continue;
                            };
                        };
                    };''')
    print(ast)
    SemanticChecker().visit(ast)
