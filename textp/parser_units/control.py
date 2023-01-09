import ast_nodes


def p_if_else(p):
    '''if_statement : IF expression LCURLY statement_list RCURLY ELSE LCURLY statement_list RCURLY'''
    p[0] = ast_nodes.IfStatement(
        condition=p[2],
        then_code=p[4],
        else_code=p[8]
    )


def p_if_only(p):
    '''if_statement : IF expression LCURLY statement_list RCURLY'''
    p[0] = ast_nodes.IfStatement(
        condition=p[2],
        then_code=p[4]
    )


def p_while(p):
    '''while_loop : WHILE expression LCURLY statement_list RCURLY'''
    p[0] = ast_nodes.WhileLoop(
        exp=p[2],
        loop_code=p[4]
    )


def p_for(p):
    '''for_loop : FOR LPAREN variable_def COLON expression COLON assign RPAREN LCURLY statement_list RCURLY'''
    p[0] = ast_nodes.ForLoop(
        variable_def=p[3],
        condition=p[5],
        step=p[7],
        code=p[10]
    )


def p_foreach(p):
    '''foreach_loop : FOREACH ID IN expression LCURLY statement_list RCURLY'''
    p[0] = ast_nodes.ForeachLoop(
        variable=p[2],
        array=p[4],
        code=p[6]
    )
