from bultin.types import TYPENAMES

KEYWORDS = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'greep': 'GREEP',
    'select': 'SELECTOR',
    'each': 'EACH',
    'from': 'FROM',
    'do': 'DO',
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
}

KEYWORDS.update(
    ((t,
      'TYPE'
      ) for t in TYPENAMES.keys())
)
