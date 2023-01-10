from scopes import Scope
from ast_nodes import *
from utils import Singleton
from visitor import visitor
from keywords import KEYWORDS
from builtin.functions.definition import BuiltinFunctionDef
from builtin.types import DSLBoolean, DSLType, get_array_type
from typing import Any


class DSLRuntimeError(Exception):
    pass


@dataclass
class ReturnedValue():
    value: Any


class Evaluator(metaclass=Singleton):
    @visitor(Program)
    def evaluate(self, p: Program, scope: Scope = Scope(), *args, **kwargs):
        self.evaluate(p.statements, scope, *args, **kwargs)

    @visitor(StatementList)
    def evaluate(self, sts: StatementList, scope: Scope, *args, **kwargs):
        for st in sts.statements:
            r = self.evaluate(st, scope, *args, **kwargs)
            if r is not None and r:
                return r

    @visitor(VariableDefinition)
    def evaluate(
            self, var_def: VariableDefinition, scope: Scope, *args, **kwargs):
        scope.variables[var_def.name] = self.evaluate(
            var_def.value, scope, *args, **kwargs)

    @visitor(VariableAssign)
    def evaluate(self, assign: VariableAssign, scope: Scope, *args, **kwargs):
        scope.assignvariable(
            assign.name, self.evaluate(
                assign.value, scope, *args, **kwargs))

    @visitor(VariableCall)
    def evaluate(self, v_call: VariableCall, scope: Scope, *args, **kwargs):
        return scope.getvariable(v_call.name)

    @visitor(FunctionDefinition)
    def evaluate(self, f_def: FunctionDefinition, scope: Scope, *args, **kwargs):
        scope.dsl_function[f_def.name] = f_def

    @visitor(FunctionCall)
    def evaluate(self, f_cal: FunctionCall, scope: Scope, *args, **kwargs):
        func = scope.getfunction(f_cal.name)
        if isinstance(func, FunctionDefinition):
            new_scope = scope.create_child()
            for revieved, param in zip(f_cal.args, func.parameters.parameters):
                e = self.evaluate(revieved)
                new_scope.variables[param.name] = e
            return self.evaluate(func.code, new_scope, *args, **kwargs).value
        elif isinstance(func, BuiltinFunctionDef):
            return func.py_func(*
                                [self.evaluate(e, scope, *args, **kwargs)
                                 for e in f_cal.args])

    @visitor(IfStatement)
    def evaluate(self, ifst: IfStatement, scope: Scope, *args, **kwargs):
        cond = self.evaluate(ifst.condition, scope, *args, **kwargs)
        if cond:
            return self.evaluate(
                ifst.then_code, scope.create_child(),
                *args, **kwargs)
        else:
            if ifst.else_code is not None:
                return self.evaluate(
                    ifst.then_code, scope.create_child(),
                    *args, **kwargs)

    @visitor(WhileLoop)
    def evaluate(self, while_loop: WhileLoop, scope: Scope, *args, **kwargs):
        cond = self.evaluate(while_loop.condition, scope, *args, **kwargs)
        while (cond):
            r = self.evaluate(
                while_loop.code, scope=scope.create_child(),
                *args, **kwargs)
            if r == Break:
                break
            elif isinstance(r, ReturnedValue):
                return r
            else:
                cond = self.evaluate(while_loop.condition,
                                     scope, *args, **kwargs)

    @visitor(ForLoop)
    def evaluate(self, for_loop: ForLoop, scope: Scope, *args, **kwargs):
        it_var = self.evaluate(
            for_loop.variable_def.value, scope, *args, **kwargs)
        new_scope = scope.create_child()
        new_scope.variables[for_loop.variable_def.name] = it_var
        cond = self.evaluate(for_loop.condition, new_scope, *args, **kwargs)
        while (cond):
            r = self.evaluate(
                for_loop.code, scope=new_scope,
                *args, **kwargs)
            if r == Break:
                break
            elif isinstance(r, ReturnedValue):
                return r
            else:
                self.evaluate(for_loop.step, new_scope, *args, **kwargs)
                it_var = new_scope.getvariable(for_loop.variable_def.name)
                new_scope = scope.create_child()
                new_scope.variables[for_loop.variable_def.name] = it_var
                cond = self.evaluate(for_loop.condition,
                                     new_scope, *args, **kwargs)

    @visitor(ForeachLoop)
    def evaluate(self, foreach: ForeachLoop, scope: Scope, *args, **kwargs):
        arr_var = self.evaluate(foreach.array, scope, *args, **kwargs)
        for v in arr_var.value:
            new_scope = scope.create_child()
            new_scope.variables[foreach.variable] = v
            r = self.evaluate(
                foreach.code, scope=new_scope,
                *args, **kwargs)
            if r == Break:
                break
            elif isinstance(r, ReturnedValue):
                return r

    @visitor(Continue)
    def evaluate(self, *args, **kwargs):
        return Continue

    @visitor(Break)
    def evaluate(self, *args, **kwargs):
        return Break

    @visitor(Literal)
    def evaluate(self, literal: Literal, *args, **kwargs):
        return literal.value.value

    @visitor(Return)
    def evaluate(self, ret: Return, scope: Scope, *args, **kwargs):
        return ReturnedValue(self.evaluate(ret.value, scope, *args, **kwargs))

    @visitor(LiteralArray)
    def evaluate(self, array: LiteralArray, scope: Scope, *args, **kwargs):
        return [self.evaluate(v, scope, *args, **kwargs) for v in array.values]
