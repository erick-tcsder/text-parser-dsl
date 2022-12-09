from visitor import visitor
from ast_nodes import *
from typing import Boolean


class SemanticChecker:
    def __init__(self):
        #flag to find SendingToOutput (DPOUT)
        self.sending_to_output_found = False
        self.types ={}

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
            _ = self.variables[node.name] 
        except KeyError:  # variable not found
            self.variables[node.name] = True
            return True
    
    @visitor(Type)
    def visit_type(self, node):
        # Verificar que el tipo no se haya definido previamente
        if node.name in self.types:
        raise SemanticError(f"Type {node.name} already defined")

        # Añadir el tipo al diccionario de tipos definidos
        self.types[node.name] = node

    @visitor(ast_nodes.ListOfType)
    def visit_list_of_type(self, node):
        # Verificar que el tipo no se haya definido previamente
        if node.name in self.types:
        raise SemanticError(f"Type {node.name} already defined")

        # Añadir el tipo al diccionario de tipos definidos
        self.types[node.name] = node

    @visitor(ast_nodes.Assignment)
    def visit_assignment(self, node):
        # Verificar que el tipo de la variable se haya definido
        if node.var_type not in self.types:
        raise SemanticError(f"Type {node.var_type} not defined")

        # Verificar que el tipo del valor coincida con el tipo de la variable
        if type(node.value).__name__ != self.types[node.var_type].name:
        raise SemanticError(f"Value of type {type(node.value).__name__} cannot be assigned to variable of type {node.var_type}")
        
    @visitor(Actions)
    def visit(self, node):
        pass

    @visitor(Action)
    def visit(self, node):
        pass

    @visitor(FilterExp)
    def visit(self, node):
        pass

    @visitor(FindExp)
    def visit(self, node):
        pass

    @visitor(EachExp)
    def visit(self, node):
        pass

    @visitor(SelectExp)
    def visit(self, node):
        pass

    @visitor(GrepExp)
    def visit(self, node):
        pass


    # INT b = 3 + a;