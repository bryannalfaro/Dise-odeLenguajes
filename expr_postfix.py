from alphabet_definition import AlphabetDefinition
from operators import *
from automata.node_automata import Node
from cleaning_expr import Clear
from Symbol import Symbol


class PostfixConverter:
    def __init__(self, expression):
        self.expression = expression
        self.alphabet = AlphabetDefinition()
        self.symbols = self.alphabet.getSymbolDictionary()
        self.stack_operators = []
        self.postfix_stack = []
        self.nodes_stack = []

    def build_Alphabet(self):
        for i in self.expression:
            if i not in self.symbols:
                self.alphabet.addSymbol(Symbol(i))

    def convertToPostfix(self, validate):
        # Se verifica el balanceo de parentesis
        flag_validation, error_message = Clear(
            self.expression, self.symbols).validate_expression_parenthesis()
        # Se verifica los operadores
        flag_operators, error_message_op = Clear(
            self.expression, self.symbols).validate_expression_operators()
        # se verifica que no haya parentesis vacios
        flag_parentesis, error_message_empty = Clear(
            self.expression, self.symbols).validate_expression_inside_parenthesis(self.alphabet)

        # Si alguna de las flags es falsa mostrar error
        if flag_validation == False or flag_operators == False or flag_parentesis == False:
            if error_message != "":
                print(error_message)
            if error_message_op != "":
                print(error_message_op)
            if error_message_empty != "":
                print(error_message_empty)
            validate = False
            postfix = ""

        # Si no hay errores
        else:
            # Agregar concatenacion
            self.expression = Clear(self.expression, self.symbols).preprocess()

            for i in self.expression:
                # Si es un simbolo del alfabeto
                if i not in self.symbols:
                    self.postfix_stack.append(i)
                # Si es un operador
                elif i in self.symbols:
                    if len(self.stack_operators) == 0:
                        self.stack_operators.append(i)
                    # Si es (
                    elif i == LeftParenthesis().symbol:
                        self.stack_operators.append(i)
                    # Si es ) y vaciar hasta encontrar (
                    elif i == RightParenthesis().symbol:
                        while self.stack_operators[-1] != LeftParenthesis().symbol:
                            self.postfix_stack.append(
                                self.stack_operators.pop())
                        self.stack_operators.pop()  # Sacar el (
                    else:
                        # Mientras la precedencia es menor o igual
                        while len(self.stack_operators) != 0 and self.symbols[i].precedence <= self.symbols[self.stack_operators[-1]].precedence:
                            self.postfix_stack.append(
                                self.stack_operators.pop())
                        self.stack_operators.append(i)

            # Vaciar el stack de operadores al final
            while len(self.stack_operators) != 0:
                self.postfix_stack.append(self.stack_operators.pop())
            validate = True
            postfix = (''.join(self.postfix_stack))
        return (postfix, validate)

    def make_nodes(self, expression):
        for i in range(len(expression)):
            i = expression[i]
            # Verificar si es un simbolo del alfabeto
            if i not in self.symbols:
                self.nodes_stack.append(Node(i))
            else:
                # Verificar si es *
                if i == KleeneStar().symbol:
                    node = Node(i)
                    node.left = self.nodes_stack.pop()
                    self.nodes_stack.append(node)
                # Verfiicar si es |
                elif i == Union().symbol:
                    node = Node(i)
                    node.right = self.nodes_stack.pop()
                    node.left = self.nodes_stack.pop()
                    self.nodes_stack.append(node)
                # Verificar si es .
                elif i == Concatenation().symbol:
                    node = Node(i)
                    node.right = self.nodes_stack.pop()
                    node.left = self.nodes_stack.pop()
                    self.nodes_stack.append(node)
        return self.nodes_stack.pop()
