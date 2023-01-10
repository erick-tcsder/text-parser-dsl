from ..scopes import Scope
from ..ast_nodes import *
from ..utils import Singleton
from ..visitor import visitor
from ..keywords import KEYWORDS
from .exceptions import *
from ..builtin.functions.definition import BuiltinFunctionDef
from ..builtin.types import DSLBoolean, DSLType, get_array_type


class SemanticChecker(metaclass=Singleton):
    def validate_symbol_name(self, name: str, scope: Scope):
        if name in KEYWORDS or scope.hasbuiltinfunction(name):
            raise SymbolReservedException(f"Name {name} reserved")
        elif scope.hasdefinition(name, local_only=True):
            raise SymbolAlreadyDeclaredException(
                f"Symbol {name} was previously declared")
        elif name.startswith('__'):
            raise SymbolNameForbiddenException(
                f"Symbol names can't start with double underscore ('__')")

    def try_variable_creation(
            self, name: str, scope: Scope, type: Type[DSLType]):
        self.validate_symbol_name(name, scope)
        scope.variables[name] = type

    def check_in_loop(self, allow_continue_and_break):
        if not allow_continue_and_break:
            raise UnexpectedStatementException(
                f"The break and continue statement can only be inside a loop code")

    @visitor(Program)
    def visit(self, p: Program, scope: Scope = Scope(), *args, **kwargs):
        self.visit(p.statements, scope, *args, **kwargs)

    @visitor(FunctionDefinition)
    def visit(self, _def: FunctionDefinition, scope: Scope, *args,
              expected_return=None, **kwargs):
        self.validate_symbol_name(_def.name, scope)
        scope.dsl_function[_def.name] = _def
        f_scope = scope.create_child()
        for p in _def.parameters.parameters:
            self.try_variable_creation(p.name, f_scope, p.type)
        self.visit(_def.code, scope=f_scope, *args, **
                   kwargs, expected_return=_def.type)

    @visitor(VariableDefinition)
    def visit(self, _def: VariableDefinition, scope: Scope, *args, **kwargs):
        self.try_variable_creation(_def.name, scope, self.visit(
            _def.value, scope, *args, **kwargs))

    @visitor(FunctionCall)
    def visit(self, fc: FunctionCall, scope: Scope, *args, **kwargs):
        func = scope.getfunction(fc.name)
        args: List[Type[DSLType]] = [self.visit(
            p, scope=scope, *args, **kwargs) for p in fc.args]
        if func is None:
            raise FunctionNotDeclaredException(
                f"There is no function called {fc.name} for parameters of type ({','.join((t.get_dsl_name() for t in args))})")
        if isinstance(func, FunctionDefinition):
            pty = [t.type for t in func.parameters.parameters]
            if len(args) != len(pty):
                raise WrongAmountOfArgumentsException(
                    f"The function {fc.name} expected {len(pty)} arguments, recieved {len(args)}")
            for i, (expected, recieved) in enumerate(zip(pty, args)):
                if expected != recieved:
                    raise WrongArgumentTypesException(
                        f"The function {fc.name} expected {expected.get_dsl_name()} at position {i+1}, recieved {recieved.get_dsl_name()}"
                    )
            return func.type
        elif isinstance(func, BuiltinFunctionDef):
            rtype = func.type_validation_func(args)
            if rtype is None:
                raise WrongArgumentTypesException(
                    f"The function {fc.name} can't recieved those kind of parameters")
            return rtype

    @visitor(VariableCall)
    def visit(self, var: VariableCall, scope: Scope, *args, **kwargs):
        r = scope.getvariable(var.name)
        if r is None:
            raise VariableNotDeclaredException(
                f"Variable {var.name} not declared")
        return r

    @visitor(LiteralArray)
    def visit(self, array: LiteralArray, scope: Scope, *args, **kwargs):
        if len(array.values) == 0:
            raise InvalidArrayLiteralException(
                f"Direct array notation need at least one element in the array, sorry")
        guessed = self.visit(array.values[0], scope, *args, **kwargs)
        for exp in array.values[1:]:
            if self.visit(exp, scope, *args, **kwargs) != guessed:
                raise InvalidArrayLiteralException(
                    f"All memebers of an array must have the same type")
        return get_array_type(guessed)

    @visitor(IfStatement)
    def visit(self, ifst: IfStatement, scope: Scope, *args, **kwargs):
        if self.visit(ifst.condition, scope, *args, **kwargs) != DSLBoolean:
            raise ExpectedBooleanException(
                f"The expression in the condition of an if statement must return a boolean value")
        self.visit(ifst.then_code, scope.create_child(), *args, **kwargs)
        if ifst.else_code is not None:
            self.visit(ifst.else_code, scope.create_child(), *args, **kwargs)

    @visitor(WhileLoop)
    def visit(self, while_loop: WhileLoop, scope: Scope, *args,
              allow_continue_and_break=False, **kwargs):
        if self.visit(
                while_loop.condition, scope, *args, **kwargs) != DSLBoolean:
            raise ExpectedBooleanException(
                f"The expression in the condition of a while statement must return a boolean value")
        self.visit(while_loop.code, scope.create_child(), *args,
                   **kwargs, allow_continue_and_break=True)

    @visitor(ForLoop)
    def visit(self, for_loop: ForLoop, scope: Scope, *args,
              allow_continue_and_break=False, **kwargs):
        new_scope = scope.create_child()
        self.visit(for_loop.variable_def, new_scope, *args, **kwargs)
        if self.visit(
                for_loop.condition, new_scope, *args, **kwargs) != DSLBoolean:
            raise ExpectedBooleanException(
                f"The expression in the condition of a for statement must return a boolean value")
        self.visit(for_loop.step, new_scope, *args, **kwargs)
        self.visit(for_loop.code, new_scope, *args, **
                   kwargs, allow_continue_and_break=True)

    @visitor(ForeachLoop)
    def visit(self, foreach: ForeachLoop, scope: Scope, *args,
              allow_continue_and_break=False, **kwargs):
        arr_type: Type[DSLArray] = self.visit(
            foreach.array, scope, *args, **kwargs)
        if not issubclass(arr_type, DSLArray):
            raise ExpectedArrayException(
                f"An array was expected in foreach statement, got {arr_type}")
        new_scope = scope.create_child()
        self.try_variable_creation(
            foreach.variable, new_scope, arr_type.get_subtype())
        self.visit(foreach.code, new_scope, *args, **
                   kwargs, allow_continue_and_break=True)

    @visitor(Return)
    def visit(self, returnst: Return, scope: Scope, *args,
              expected_return: Type[DSLType] | None = None, **kwargs):
        if expected_return is None:
            raise UnexpectedReturnException(f"A return was not expected")
        r: Type[DSLType] = self.visit(returnst.value, scope, *args, **kwargs)
        if r != expected_return:
            raise WrongTypeReturnException(
                f"Type {expected_return.get_dsl_name()} expected in return, got {r.get_dsl_name()}")

    @visitor(Break)
    def visit(self, st: Break, scope: Scope, *args,
              allow_continue_and_break=False, **kwargs):
        self.check_in_loop(allow_continue_and_break)

    @visitor(Continue)
    def visit(self, st: Continue, scope: Scope, *args,
              allow_continue_and_break=False, **kwargs):
        self.check_in_loop(allow_continue_and_break)

    @visitor(Literal)
    def visit(self, exp: Literal, scope: Scope, *args, **kwargs):
        return type(exp.value)

    @visitor(ASTNode)
    def visit(self, node: ASTNode, scope: Scope, *args, **kwargs):
        print(f"What do we do with the drunken {type(node).__qualname__}...")
        for child in node.get_children():
            self.visit(child, scope, *args, **kwargs)
