from builtin import types


def p_type_simple(p):
    '''type : TYPE'''
    p[0] = types.TYPENAMES[p[1]]


def p_type_array(p):
    '''type : type LBRACKET RBRACKET'''
    p[0] = types.get_array_type(p[1])
