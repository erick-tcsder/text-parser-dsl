from .parser_units.expressions import *
from .parser_units.statements import *
from .parser_units.control import *
from .parser_units.typing import *
from .parser_units.definitions import *
from .semantics.semantic_checker import SemanticChecker
from ply import *
from . import lexer
from . import ast_nodes
from . import utils
from .evaluator import Evaluator
from .visitor import visitor
from .builtin import types


tokens = lexer.tokens

precedence = (
    ('right', 'ASSIGN'),
    ('left', 'OR', 'AND'),
    ('left', 'EQ', 'NEQ', 'GR', 'LS', 'GEQ', 'LEQ'),
    ('left', 'ADD', 'MINUS'),
    ('left', 'MULT', 'DIVIDE'),
    ('right', 'UMINUS'),            # Unary
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
    parser.error = True


parser = yacc.yacc()


def parse(data, debug=True):
    parser.error = 0
    p = parser.parse(data, debug=debug)
    if parser.error:
        raise Exception("Syntax error at parsing")
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
    ast = parse('''int[][] cribe=[[1]];
                    
                    for (int i=1 : i<100 : i=i+1) {
                        push(cribe,i,[1]);
                    };
                    
                    for (int i=2 : i<= 100 : i=i+1) {
                        if (len(cribe[i-1])==1) {
                            for (int k=i*2 : k <= 100 : k=k+i){
                                push(cribe[k-1],len(cribe[k-1]),i);
                            };
                        };
                    };
                    
                    int count=len(cribe[99]);
                    while (count>0) {
                        output(cribe[99][count-1]);
                        count=count-1;
                    };
                    
                    ''', False)
    print(ast)
    SemanticChecker().visit(ast)
    Evaluator().evaluate(ast)
