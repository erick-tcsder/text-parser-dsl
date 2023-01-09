import ast_nodes


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
                 | function_def
                 | variable_def
                 | while_loop
                 | for_loop
                 | foreach_loop
                 | expression
                 | continue
                 | break
                 | return
                 | empty'''
    p[0] = p[1]


def p_break(p):
    '''break : BREAK'''
    p[0] = ast_nodes.Break()


def p_continue(p):
    '''continue : CONTINUE'''
    p[0] = ast_nodes.Continue()


def p_return(p):
    '''return : RETURN expression'''
    p[0] = ast_nodes.Return(
        value=p[2]
    )
