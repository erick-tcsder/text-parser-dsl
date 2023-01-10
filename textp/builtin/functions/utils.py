from typing import List, Type
from ..types import DSLType, DSLFloat, DSLInt, DSLBoolean, DSLString, DSLArray

DSLTypeDef = Type[DSLType]
ArgumentTypes = List[DSLTypeDef]


def check_indexable(arg: DSLTypeDef):
    return issubclass(arg, DSLArray) or arg == DSLString


def validate_math(args: ArgumentTypes) -> DSLTypeDef:
    if len(args) != 2:
        return None
    if args[0] == DSLInt and args[1] == DSLInt:
        return DSLInt
    if all((a in [DSLFloat, DSLInt] for a in args)):
        return DSLFloat


def validate_boolean(args: ArgumentTypes):
    return DSLBoolean if (len(args) == 2 and all(
        (a == DSLBoolean for a in args))) else None


def validate_cmp(args: ArgumentTypes):
    if len(args) != 2:
        return None
    if validate_math(args) is not None:
        return DSLBoolean
    if all((a == DSLString for a in args)):
        return DSLBoolean


def validate_static(expected_args: ArgumentTypes, return_type: DSLTypeDef):
    def __inner(args: ArgumentTypes):
        if len(args) != len(expected_args):
            return None
        for rec, expect in zip(args, expected_args):
            if rec != expect:
                return None
        return return_type
    return __inner


def validate_and(*validations):
    def __inner(args: ArgumentTypes):
        r = validations[0](args)
        if r is None:
            return None
        for v in validations[1:]:
            r_ch = v(args)
            if r_ch is None:
                return None
        return r
    return __inner


def validate_or(*validations):
    def __inner(args: ArgumentTypes):
        for v in validations:
            r_ch = v(args)
            if r_ch is not None:
                return r_ch
        return None
    return __inner


def validate_array_index_value(mode: int):
    def __inner(arg: ArgumentTypes):
        if mode >= 1:
            if not issubclass(arg[0], DSLArray):
                return None
        if mode >= 2:
            if arg[1] != DSLInt:
                return None
        if mode >= 3:
            if arg[2] != arg[0].get_subtype():
                return None
        if mode == 2:
            return arg[0].get_subtype()
        return DSLBoolean
    return __inner


def array_push(arr, pos, value):
    try:
        arr.insert(pos, value)
        return True
    except:
        return False


def array_pop(arr, pos, value):
    try:
        arr.pop(pos, value)
        return True
    except:
        return False


def validate_indexable_access(args: ArgumentTypes):
    if len(args) != 2 or not check_indexable(args[0]):
        return None
    if args[1] != DSLInt:
        return None
    if issubclass(args[0], DSLArray):
        return args[0].get_subtype()
    if args[0] == DSLString:
        return DSLString


def validate_indexable_len(args: ArgumentTypes):
    if len(args) != 1 or not check_indexable(args[0]):
        return None
    if issubclass(args[0], DSLArray) or args[0] == DSLString:
        return DSLInt
