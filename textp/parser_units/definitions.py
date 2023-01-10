from .. import ast_nodes


def p_var_def(p):
    '''variable_def : type ID ASSIGN expression'''
    p[0] = ast_nodes.VariableDefinition(
        name=p[2],
        type=p[1],
        value=p[4]
    )


def p_function_def_simple(p):
    '''function_def : type ID LPAREN  RPAREN LCURLY statement_list RCURLY'''
    p[0] = ast_nodes.FunctionDefinition(
        name=p[2],
        type=p[1],
        parameters=ast_nodes.ParameterList([]),
        code=p[6]
    )


def p_function_def_params(p):
    '''function_def : type ID LPAREN parameter_list RPAREN LCURLY statement_list RCURLY'''
    p[0] = ast_nodes.FunctionDefinition(
        name=p[2],
        type=p[1],
        parameters=p[4],
        code=p[7]
    )


def p_parameter(p):
    '''parameter : type ID'''
    p[0] = ast_nodes.ParameterDefinition(
        name=p[2],
        type=p[1]
    )


def p_parameters_single(p):
    '''parameter_list : parameter'''
    p[0] = ast_nodes.ParameterList([p[1]])


def p_parameters_multi(p):
    '''parameter_list : parameter COMMA parameter_list'''
    right: ast_nodes.ParameterList = p[3]
    p[0] = ast_nodes.ParameterList([p[1]]+right.parameters)
