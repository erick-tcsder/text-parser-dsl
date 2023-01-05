from ply import *
import lexer
import ast_nodes 
import utils
import evaluator

tokens = lexer.tokens

def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]


def p_statement_list(p):
    '''statement_list : statement_list statement SEMICOLON 
                      | empty'''
    no_statement = len(p) == 2
    if no_statement:
        p[0] = ast_nodes.StatementList([])
    elif p[3] == ';':
        statement_list = p[1]
        statement = p[2]
        p[0] = statement_list.append(statement)  
    else:
        # @TODO grita
        pass

def p_statement(p):
    '''statement : if_statement
                 | assign
  	             | input
                 | output
                 | function_definition
                 | for_loop
                 | foreach_loop
                 | expression'''
    p[0] = p[1]


def p_assign(p):
    '''assign : type ID ASSIGN expression'''
    p[0] = ast_nodes.VariableDefinition(
        _type = p[1],
        name = p[2],
        value = p[4]        
    )
    print(p[0].name)
    

def p_type(p):
    '''type : TYPE
            | TYPE LBRACKET RBRACKET'''
    simple_type = len(p) == 2
    if simple_type:
        p[0] = ast_nodes.Type(name=p[1])
    else:
        p[0] = ast_nodes.ListOfType(name=p[1])

    
def p_empty(p):
    '''empty : '''


def p_input(p):
    '''input : DPIN GR GR ID'''
    p[0] = ast_nodes.ReceivingFromInput(
        variable_name = p[4]
    )
    

def p_output(p):
    '''output : ID GR GR DPOUT'''
    p[0] = ast_nodes.SendingToOutput(
        text_to_send = p[1]
    )

def p_expression(p):
    '''expression : boolean_expression'''
    p[0] = p[1]

def p_function_definition(p):
    '''function_definition : DEF ID LPAREN parameter_list RPAREN LCURLY statement_list RCURLY'''
    p[0] = ast_nodes.FunctionDefinition(
        name = p[2],
        parameters = p[4],
        statements = p[7]
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
        _type = p[1],
        name = p[2]
    )

def p_if_statement(p):
    '''if_statement : IF expression THEN LCURLY statement_list RCURLY ELSE LCURLY statement_list RCURLY'''
    p[0] = ast_nodes.IFStatement(
        exp = p[2],
        THENstatemet= p[5],
        ELSEstatement = p[9]
    )

def p_boolean_expression(p):
    '''boolean_expression : boolean_term
                          | boolean_expression BOR boolean_term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ast_nodes.ORExp(
            exp= p[1],
            term= p[3]
        )

def p_boolean_term(p):
    '''boolean_term : boolean_factor
                    | boolean_term BAND boolean_factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ast_nodes.ANDExp(
            term = p[1],
            factor = p[3]
        )

def p_boolean_factor(p):
    '''boolean_factor : NOT boolean_primary
                      | boolean_primary'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ast_nodes.NOTExp(p[2])

def p_boolean_primary(p):
    '''boolean_primary : comparison
                       | LPAREN boolean_expression RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_comparison(p):
    '''comparison : math_expression
                  | expression comparison_operator math_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ast_nodes.CMPExp(
            exp1 = p[1],
            exp2 = p[3],
            op = p[2]
        )
    
def p_math_expressions(p):
    '''math_expression : term
                       | math_expression PLUS term
                       | math_expression MINUS term''' 
    
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '+':
        p[0] = ast_nodes.BinaryOperation(
            left_value = p[1],
            right_value = p[3],
            op = '+'
        )
    else:
        p[0] = ast_nodes.BinaryOperation(
            left_value = p[1],
            right_value = p[3],
            op = '-'
        )

def p_term(p):
    '''term : factor
            | term TIMES factor
            | term DIVIDE factor'''
    if len(p)==2:
        p[0] = p[1]
    else:
        if p[2] == '*':
            p[0] = ast_nodes.BinaryOperation(
                left_value = p[1],
                right_value = p[3],
                op = '*'
            )
        else:
            p[0] = ast_nodes.BinaryOperation(
                left_value = p[1],
                right_value = p[3],
                op = '/'
            )
    
def p_comparison_operator(p):
    '''comparison_operator : EQ
                           | NEQ
                           | LS
                           | LEQ
                           | GR
                           | GEQ'''
    p[0] = p[1]


def p_factor(p):
    '''factor : NUMBER
              | ID
              | LPAREN math_expression RPAREN'''
    print(p[0])
    if len(p) == 4:
        p[0] = p[3]
    elif utils.is_float(p[1]):
        p[0] = ast_nodes.Number(p[1])
    else:
        p[0]= ast_nodes.GetVariableValue(p[1])

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


def parse(data, debug=False):
    parser.error = 0
    p = parser.parse(data, debug=debug)
    if parser.error:
        return None
    return p


if __name__ == '__main__':
    #print(parse('def functi (INT a, INT b, INT c) : INT c=1; ;', debug=False))
    print()
    #print(parse('for i in 1..5: i >> DPOUT; ;', debug=False))
    print()
    #print(parse('foreach w in wordt: w >> DPOUT; ;', debug=False))
    
    print(parse('if a > b then { INT k = 5;} else {INT j = 6;} ;', debug=False))
    ast = parse("INT k = 5; INT j = 2 + k;", debug= True)
    print(ast)
    evaluator = evaluator.Evaluator()
    print(evaluator.visit(ast))
