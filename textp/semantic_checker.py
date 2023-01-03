from visitor import visitor
from ast_nodes import *
from typing import Boolean


class SemanticChecker:
    def __init__(self):
        #flag to find SendingToOutput (DPOUT)
        self.sending_to_output_found = False
        #flag to find ReceivingFromInput (DPIN)
        self.receiving_from_input_found = False
        self.types ={}
        self.functions = {}  # <-- almacenar las funciones definidas
        # Atributo para almacenar los parámetros definidos
        self.parameters = {}

    @visitor(StatementList)
    def visit(self, statement_list: StatementList) -> Boolean:
        for statement in statement_list.statements:            
            valid = self.visit(statement)
            if not valid:
                return False        
        return True
    
    @visitor(VariableDefinition)
    def visit(self, node):
        initialization_valid = self.visit(node.value)
        if not initialization_valid:
            return False

        try:
            _ = self.parameters[node.name] 
        except KeyError:  # variable not found
            self.parameters[node.name] = True
            return True
    
    @visitor(Type)
    def visit_type(self, node):
        # Verificar que el tipo no se haya definido previamente
        if node.name in self.types:
            raise SemanticError(f"Type {node.name} already defined")

        # Añadir el tipo al diccionario de tipos definidos
        self.types[node.name] = node

    @visitor(ListOfType)
    def visit_list_of_type(self, node):
        # Verificar que el tipo no se haya definido previamente
        if node.name in self.types:
            raise SemanticError(f"Type {node.name} already defined")

        # Añadir el tipo al diccionario de tipos definidos
        self.types[node.name] = node


    @visitor(FunctionDefinition)
    def visit(self, node: FunctionDefinition) -> bool:
        # Verificar que el tipo de retorno exista
        if node.return_type not in self.types:
            raise SemanticError(f"Type {node.return_type} not defined")

        # Verificar que los parámetros tengan tipos válidos
        for param in node.parameters:
            if param.type_name not in self.types:
                raise SemanticError(f"Type {param.type_name} not defined")

        # Verificar que la función no se haya definido previamente
        if node.name in self.functions:
            raise SemanticError(f"Function {node.name} already defined")

        # Añadir la función al diccionario de funciones definidas
        self.functions[node.name] = node
        return True       

    @visitor(Parameter)
    def visit(self, node: Parameter) -> bool:
        # Verificar que el tipo del parámetro exista
        try:
            _ = self.types[node._type]
        except KeyError:  # Type not found
            raise SemanticError(f"Type {node._type} not defined")

        # Verificar que el nombre del parámetro no se haya utilizado previamente
        if node.name in self.parameters:
            raise SemanticError(f"Parameter {node.name} already defined")

        # Añadir el parámetro al diccionario de parámetros definidos
        self.parameters[node.name] = node

        return True

    @visitor(ParameterList)
    def visit(self, node: ParameterList) -> bool:
        for parameter in node.parameters:
            valid = self.visit(parameter)
            if not valid:
                return False

        return True

    @visitor(CMPExp)
    def visit(self, node: CMPExp) -> bool:
        # Verificar que las expresiones sean válidas
        exp1_valid = self.visit(node.exp1)
        if not exp1_valid:
            return False

        exp2_valid = self.visit(node.exp2)
        if not exp2_valid:
            return False

        # Verificar que el operador sea válido
        if node.op not in ['<', '>', '<=', '>=', '==', '!=']:
            raise SemanticError(f"Invalid operator {node.op}")

        return True

    @visitor(ReceivingFromInput)
    def visit(self, node: ReceivingFromInput) -> bool:
        # Verificar que la variable a la que se le asignará el valor ingresado por el usuario exista
        if node.variable_name not in self.variables:
            raise SemanticError(f"Variable {node.variable_name} not defined")

        # Mark the flag as True to indicate that the program is receiving input
        self.receiving_from_input_found = True

        return True

    @visitor(SendingToOutput)
    def visit(self, node: SendingToOutput) -> bool:
        # Verificar que el texto a enviar sea una expresión válida
        if not isinstance(node.text_to_send, Expression):
            raise SemanticError("Invalid expression to send to output")

        # Establecer flag para indicar que se está enviando algo a la salida
        self.sending_to_output_found = True

        return True

class SemanticError(Exception):
    def __init__(self, message: str):
        self.message = message