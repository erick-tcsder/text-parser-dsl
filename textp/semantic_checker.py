from visitor import visitor
from ast_nodes import *
from typing import Boolean


class SemanticChecker:
    def __init__(self):
        #flag to find SendingToOutput (DPOUT)
        self.sending_to_output_found = False

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
    
    @visitor 

    # INT b = 3 + a;
    
   