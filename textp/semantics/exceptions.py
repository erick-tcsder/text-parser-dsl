class SymbolAlreadyDeclaredException(Exception):
    pass


class SymbolReservedException(Exception):
    pass


class SymbolNameForbiddenException(Exception):
    pass


class VariableNotDeclaredException(Exception):
    pass


class FunctionNotDeclaredException(Exception):
    pass


class WrongArgumentTypesException(Exception):
    pass


class WrongAmountOfArgumentsException(Exception):
    pass


class InvalidArrayLiteralException(Exception):
    pass


class ExpectedBooleanException(Exception):
    pass


class ExpectedArrayException(Exception):
    pass


class UnexpectedReturnException(Exception):
    pass


class UnexpectedStatementException(Exception):
    pass


class WrongTypeReturnException(Exception):
    pass
