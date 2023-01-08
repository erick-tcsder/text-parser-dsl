from typing import Type
from .int import *
from .string import *
from .float import *
from .bool import *

TYPENAMES = {}


def __declare_type(_type: Type[DSLType]):
    '''
    Used to add builtin types below.
    '''
    TYPENAMES[_type.get_dsl_name()] = _type


# region Declarations
__declare_type(DSLBoolean)
__declare_type(DSLFloat)
__declare_type(DSLInt)
__declare_type(DSLString)
# endregion
