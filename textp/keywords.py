from .builtin.types import TYPENAMES

KEYWORDS = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'greep': 'GREEP',
    'select': 'SELECTOR',
    'each': 'EACH',
    'from': 'FROM',
    'find': 'FIND',
    'regexp': 'REGEXP',
    'filter': 'FILTER',
    'word': 'WORD',
    'for': 'FOR',
    'foreach': 'FOREACH',
    'in': 'IN',
    'def': 'DEF',
    'true': 'TRUE',
    'false': 'FALSE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN'
}

KEYWORDS.update(
    ((t,
      'TYPE'
      ) for t in TYPENAMES.keys())
)
