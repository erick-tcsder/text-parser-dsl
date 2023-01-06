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
        if isinstance(
                statement, VariableDefinition):  # si la declaración es una asignación
            return self.evaluate_assignment(statement)
        # si la declaración es una llamada a función
        elif isinstance(statement, FunctionDefinition):
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

    @visitor(ArrayDefinition)
    def visit(self, node: ArrayDefinition):
        # obtener el tamaño del array
        size = self.visit(node.size)
        # crear el array con el tamaño especificado
        array = [None] * size
        # asignar cada valor del array
        for i, value in enumerate(node.values):
            array[i] = self.visit(value)
        # guardar el array en el contexto actual
        self.context.set_variable(node.name, array)

    @visitor(Values)
    def visit(self, node: Values):
        # crear una lista para almacenar los valores
        values = []
        # obtener el valor de cada elemento y agregarlo a la lista
        for value in node.values:
            values.append(self.visit(value))
        return values

    @visitor(Value)
    def visit(self, node: Value):
        # obtener el valor de la variable
        return self.context.get_variable(node.name)

    @visitor(ForLoop)
    def visit(self, node: ForLoop):
        # Evaluar la expresión de rango o iterable del bucle
        range_or_iterable = self.visit(node.range)

        # Si el rango es una expresión, obtener el rango como una lista
        if isinstance(range_or_iterable, Expression):
            range_or_iterable = self.visit(range_or_iterable)

        # @TODO: ver lo del context
        # Por cada elemento en el rango o iterable
        for element in range_or_iterable:
            # Asignar el elemento a la variable del bucle
            self.variables[node.loop_variable] = element

            # Evaluar la lista de declaraciones del cuerpo del bucle
            self.visit(node.statements)

    @visitor(VariableAssignment)
    def visit(self, node: VariableAssignment):
        value = self.visit(node.value)
        self.variables[node.name] = value

    @visitor(Range)
    def visit(self, node: Range) -> Any:
        # Implementa la lógica para evaluar un rango aquí
        start = self.visit(node.start)
        end = self.visit(node.end)
        return range(int(start, int(end)+1))
