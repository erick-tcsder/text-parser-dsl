from visitor import visitor
from ast_nodes import *
from typing import Any

class Evaluator:
    def __init__(self):
        self.variables = {}

    @visitor(str)
    def visit(self, node: str) -> Any:
        return node
    
    @visitor(StatementList)
    def visit(self, statement_list: StatementList):
        for statement in statement_list.statements:
            self.visit(statement)

    @visitor(Statement)
    def visit(self, statement: Statement):
        """Evalúa una declaración."""
        if isinstance(statement, VariableDefinition):  # si la declaración es una asignación
            return self.evaluate_assignment(statement)
        elif isinstance(statement, FunctionDefinition):  # si la declaración es una llamada a función
            return self.evaluate_function_call(statement)

    @visitor(VariableDefinition)
    def visit(self, node: VariableDefinition):
        try:
            value = self.variables[node.name]
            return value
        except:
            value = self.visit(node.value)
            self.variables[node.name] = value
            return value

    @visitor(Number)
    def visit(self, node: Number):
        return node.value
    
    @visitor(GetVariableValue)
    def visit(self, node: GetVariableValue) -> Any:
        # Obtener el valor de la variable
        return self.variables[node.name]

    @visitor(BinaryOperation)
    def visit(self, node: BinaryOperation):
        left_value = self.visit(node.left_value)
        right_value = self.visit(node.right_value)

        if node.op == "+":
            return left_value + right_value
        elif node.op == "-":
            return left_value - right_value
        elif node.op == "*":
            return left_value * right_value
        elif node.op == "/":
            return left_value / right_value
        
    @visitor(ReceivingFromInput)
    def visit(self, node: ReceivingFromInput):
        # Obtener el valor de entrada y asignarlo a la variable especificada
        value = input()
        self.variables[node.variable_name] = value

    @visitor(SendingToOutput)
    def visit(self, node: SendingToOutput):
        # Evaluar la expresión y enviar el resultado a la salida
        value = self.visit(node.text_to_send)
        print(value)
    
    @visitor(ORExp)
    def visit(self, node: ORExp):
        left_value = self.visit(node.exp)
        right_value = self.visit(node.term)
        return left_value or right_value

    @visitor(ANDExp)
    def visit(self, node: ANDExp):
        left_value = self.visit(node.term)
        right_value = self.visit(node.factor)
        return left_value and right_value

    @visitor(NOTExp)
    def visit(self, node: NOTExp):
        value = self.visit(node.term)
        return not value
    
    @visitor(CMPExp)
    def visit(self, node: CMPExp) -> Any:
        exp1 = self.visit(node.exp1)
        exp2 = self.visit(node.exp2)

        if node.op == "==":
            return exp1 == exp2
        elif node.op == "!=":
            return exp1 != exp2
        elif node.op == "<":
            return exp1 < exp2
        elif node.op == ">":
            return exp1 > exp2
        elif node.op == "<=":
            return exp1 <= exp2
        elif node.op == ">=":
            return exp1 >= exp2