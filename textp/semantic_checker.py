from visitor import visitor
from ast_nodes import *
import re

class SemanticChecker:
    def __init__(self):
        # flag to find SendingToOutput (DPOUT)
        self.sending_to_output_found = False
        # flag to find ReceivingFromInput (DPIN)
        self.receiving_from_input_found = False

        # Lista de tipos definidas
        self.types = {"INT": Number}
        # Lista de funciones definidas
        self.functions = {}  
        # Lista de variables definidos
        self.variables = {}

    @visitor(StatementList)
    def visit(self, statement_list: StatementList):
        '''statement_list : statement_list statement SEMICOLON
                          | empty'''

        # Comprueba que cada statement sea valido
        for statement in statement_list.statements:            
            if self.visit(statement) is None:
                return False
        return True
    
    @visitor(VariableDefinition)
    def visit_type(self, node):
        '''assign : type ID ASSIGN expression'''

        # Si el tipo de la declaracion es correcto
        if node._type not in self.types:
            raise SemanticError(f"Type {node.name} doesn't exists")

        # Si el nombre de la variable no esta tomado
        if node.name in self.variables:
            raise SemanticError(f"Variable name {node.name} already taken")

        # Computamos el tipo de la expresión asociada
        detected_type = self.visit(node.value)

        # Si coincide con el tipo impuesto a la variable, lo devolvemos
        if detected_type == self.types[node._type]:
            self.variables[node.name] = self.types[node._type]
            return self.types[node._type]

        # En caso contrario, devolvemos error
        elif not detected_type != None:
            raise SemanticError(f"Cannot  {node.name}")

    @visitor(FunctionDefinition)
    def visit(self, node: FunctionDefinition) -> bool:
        # Verificar que el tipo de retorno exista
        if node.return_type not in self.types:
            raise SemanticError(f"Type {node.return_type} not defined")

        # Verificar que los parámetros tengan tipos válidos
        for param in node.variables:
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
        if node.name in self.variables:
            raise SemanticError(f"Parameter {node.name} already defined")

        # Añadir el parámetro al diccionario de parámetros definidos
        self.variables[node.name] = node

        return True

    @visitor(ParameterList)
    def visit(self, node: ParameterList) -> bool:
        for parameter in node.variables:
            valid = self.visit(parameter)
            if not valid:
                return False
        return True

    @visitor(CMPExp)
    def visit(self, node: CMPExp):
        '''comparison : math_expression
                      | comparison comparison_operator math_expression'''

        # Verificamos si el nodo se corresponde con la primera producción
        if node.exp2 is None:
            return self.visit(node.exp1)

        # En otro caso, se corresponde con la segunda
        exp1_type = self.visit(node.exp1)
        exp2_type = self.visit(node.exp2)

        # Si alguna de las expresiones es erronea, devolvemos None
        # (en este punto, el error ya fue reportado por un metodo anterior)
        if exp1_type is None or exp2_type is None:
            return None

        # Una comparación es válida solo si se comparan tipos iguales
        if exp1_type == exp2_type:
            return exp1_type

        else:
            raise SemanticError(f"Mismatch types in comparison")

        
    @visitor(Factor)
    def visit(self, node: Factor):
        '''factor : NUMBER
                  | ID
                  | LPAREN math_expression RPAREN'''

        # NOTA: AST NODE FACTOR DEBE TENER TRES CAMPOS
        # VALUE: SI EL FACTOR ES UN VALOR, EN TAL CASO, EL RESTO DE CAMPOS ESTARAN EN NONE
        # NAME: SI ES UNA VARIABLE, EN TAL CASO, EL RESTO DE CAMPOS ESTARAN EN NONE
        # EXP: SI ES UNA EXPRESION, EN TAL CASO, EL RESTO DE CAMPOS EN NONE

        # SIEMPRE PUEDES EVITAR ESO, TENER UN SOLO CAMPO Y CASTEAR, PERO HABRAN CONFLICTOS
        # POR EJEMPLO, CON LOS STRINGS Y LOS IDS.
        # SI PONES UN PROTOCOLO PARA EVITAR CONFLICTOS (ENCERRAR LOS STRINGS ENTRE "" POR EJEMPLO)
        # ENTONCES PUEDES TENER UN SOLO CAMPO Y RESOLVER CASTEANDO.
        # EN ESE CASO, POR SUPUESTO, NADA DE PREGUNTAR SI ES NONE: PREGUNTAS SI ES UN STRING, Y EN QUE
        # FORMATO, O SI ES UN EXPRESSION.

        # Verificamos si el nodo se corresponde con la primera producción
        if node.value is not None:
            return Number

        # Verificamos si el nodo se corresponde con la segunda producción
        if node.name is not None:
            # Verificamos que la variable esté declarada y, en ese caso,
            # devolvemos el tipo de la variable
            if node.name in self.variables:
                return self.variables[node.name]
            # En otro caso, devolvemos error
            else:
                raise SemanticError(f"Variable {node.name} doesn't exists")

        # En otro caso, se trata de la tercera producción
        return self.visit(node.exp)

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
    
    def visit_Grep(self, node: Grep):
    # Verificar que la expresión regular es válida
        try:
            re.compile(node.pattern)
        except re.error:
            self.add_error(f"Invalid regex pattern: {node.pattern}")

    def visit_Select(self, node: Select):
    # Verificar que la expresión regular es válida
        try:
            re.compile(node.selection)
        except re.error:
            self.add_error(f"Invalid regex pattern: {node.selection}")
        # Verificar que la fuente es una cadena de texto
        source_type = self.get_variable_type(node.source)
        if source_type != 'WORD':
            self.add_error(f"Invalid source type for SELECT: {source_type}")
        # Verificar que la lista de declaraciones es válida
        self.visit(node.statements)

    def visit_Foreach(self, node: Foreach):
    # Verificar que la iterable es una lista
        iterable_type = self.get_variable_type(node.iterable)
        if iterable_type != 'WORD[]':
            self.add_error(f"Invalid iterable type for EACH: {iterable_type}")
        # Verificar que la lista de declaraciones es válida
        self.visit(node.statements)

    def visit_Find(self, node: Find):
    # Verificar que la expresión regular es válida
        try:
            re.compile(node.search)
        except re.error:
            self.add_error(f"Invalid regex pattern: {node.search}")
        # Verificar que la fuente es una cadena de texto
        source_type = self.get_variable_type(node.source)
        if source_type != 'WORD':
            self.add_error(f"Invalid source type for FIND: {source_type}")

class SemanticError(Exception):
    def __init__(self, message: str):
        self.message = message