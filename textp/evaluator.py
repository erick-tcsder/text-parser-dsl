from visitor import visitor
from ast_nodes import *
from typing import Any

class Evaluator:
    def __init__(self):
        self.variables = {}

    @visitor(StatementList)
    def visit(self, statement_list: StatementList):
        for statement in statement_list.statements:
            self.visit(statement)

    @visit(Statement)
    def visit(self, statement: Statement):
        """Evalúa una declaración."""
        if isinstance(statement, Assign):  # si la declaración es una asignación
            return self.evaluate_assignment(statement)
        elif isinstance(statement, FunctionCall):  # si la declaración es una llamada a función
            return self.evaluate_function_call(statement)

    @visitor(VariableDefinition)
    def visit(self, node):
        value = self.visit(node.value)
        self.variables[node.name] = value

    @visitor(Number)
    def visit(self, node):
        return node.value
    
    @visitor(GetVariableValue)
    def visit(self, node: GetVariableValue) -> Any:
        # Obtener el valor de la variable
        return self.variables[node.name]

    @visitor(BinaryOperation)
    def visit(self, node):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)

        if node.op == "+":
            return left_value + right_value
        elif node.op == "-":
            return left_value - right_value
        elif node.op == "*":
            return left_value * right_value
        elif node.op == "/":
            return left_value / right_value