from alphabet_definition import AlphabetDefinition
from operators import *
from automata.node_automata import Node
from cleaning_expr import Clear
from Symbol import Symbol
class PostfixConverter:
    def __init__(self, expression, augmented_value=None):

        if augmented_value is None:
             self.expression = expression
        else:
            self.expression = '('+expression+')' + augmented_value

        self.alphabet = AlphabetDefinition()
        self.symbols = self.alphabet.getSymbolDictionary()
        self.stack_operators = []
        self.postfix_stack = []
        self.nodes_stack = []

    def build_Alphabet(self):
        for i in self.expression:
            if i not in self.symbols:
                self.alphabet.addSymbol(Symbol(i))


    def convertToPostfix(self,validate):
        #clean the expression
        flag_validation,error_message = Clear(self.expression,self.symbols).validate_expression_parenthesis()

        #check operators
        flag_operators,error_message_op = Clear(self.expression,self.symbols).validate_expression_operators()

        flag_parentesis,error_message_empty = Clear(self.expression,self.symbols).validate_expression_inside_parenthesis(self.alphabet)
        #print(flag_parentesis)
        if flag_validation == False or flag_operators == False or flag_parentesis == False:
            if error_message != "":
                print(error_message)
            if error_message_op != "":
                print(error_message_op)
            if error_message_empty != "":
                print(error_message_empty)
            validate = False
            postfix = ""
        else:
            self.expression = Clear(self.expression,self.symbols).preprocess()
            #Iterate through the expression
            print(''.join(self.expression))
            for i in self.expression:

                #check if it is an alphabet symbol
                if i not in self.symbols:

                    self.postfix_stack.append(i)
                #Check if the character is an operator
                elif i in self.symbols:
                    if len(self.stack_operators) == 0:
                        self.stack_operators.append(i)
                    #check if it is (
                    elif i == LeftParenthesis().symbol:
                        self.stack_operators.append(i)
                    #check if it is ) and empty the stack until (
                    elif i == RightParenthesis().symbol:
                        while self.stack_operators[-1] != LeftParenthesis().symbol:
                            self.postfix_stack.append(self.stack_operators.pop())
                        self.stack_operators.pop()
                    else:
                        #while the precedence is less or equal

                        while len(self.stack_operators) != 0 and self.symbols[i].precedence <= self.symbols[self.stack_operators[-1]].precedence:
                            self.postfix_stack.append(self.stack_operators.pop())
                        self.stack_operators.append(i)

            #Empty the stack
            while len(self.stack_operators) != 0:

                self.postfix_stack.append(self.stack_operators.pop())
            validate = True
            postfix = (''.join(self.postfix_stack))
        return (postfix, validate)

    def make_nodes(self,expression):
        for i in range(len(expression)):
            i = expression[i]
            #check if it is an alphabet symbol
            if i not in self.symbols:

                self.nodes_stack.append(Node(i))
            else:
                    #check if it is a *
                    if i == KleeneStar().symbol:
                        node = Node(i)
                        node.left = self.nodes_stack.pop()
                        self.nodes_stack.append(node)
                    #check if it is a |
                    elif i == Union().symbol:
                        node = Node(i)
                        node.right = self.nodes_stack.pop()
                        node.left = self.nodes_stack.pop()
                        self.nodes_stack.append(node)
                    #check if it is a .
                    elif i == Concatenation().symbol:
                        node = Node(i)
                        node.right = self.nodes_stack.pop()
                        node.left = self.nodes_stack.pop()
                        self.nodes_stack.append(node)
        return self.nodes_stack.pop()

