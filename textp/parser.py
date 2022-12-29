from ply import *
import lexer
import ast_nodes 
import utils

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
    '''statement : variable_def
  	             | input
                 | output'''
    p[0] = p[1]


def p_variable(p):
    '''variable_def : type ID ASSIGN expression'''
    p[0] = ast_nodes.VariableDefinition(
        _type = p[1],
        name = p[2],
        value = p[4]        
    )
    

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

def p_binary(p):
        '''binary : BAND
                  | BOR
                  | BXOR
                  | DIVIDE
                  | MINUS
                  | EQ
                  | GEQ
                  | NEQ
                  | NOT
                  | PLUS
                  | TIMES'''
        p[0] = p[1]


def p_expression(p):
    '''expression : ID
                  | NUMBER
                  | expression binary expression'''
    if len(p)==4:
        p[0] = ast_nodes.BinaryOp(
            var1 = p[1],
            var2 = p[3],
            op = p[2] )
    elif utils.is_float(p[1]):
        p[0] = ast_nodes.Number(value=p[1])
    else:
        p[0] = ast_nodes.GetVariableValue(name=p[1])

def p_error(t):
    print("Illegal sentence %s" % t.value[0])
    t.lexer.skip(1)

parser = yacc.yacc()


def parse(data, debug=False):
    parser.error = 0
    p = parser.parse(data, debug=debug)
    if parser.error:
        return None
    return p


if __name__ == '__main__':
    print(parse('INT jelow = num & 2;', debug=False))
    print(parse('INT five = 5;', debug=False))


# @TODO visitante con los chekeos sema'nticos:
# - TYPE sea un tipo va'lido
# - cuando se kiera obtener el valor de una variable, esa variable tiene q existir
# @TODO visitante evaluador
# - q el programa tenga un statement output 