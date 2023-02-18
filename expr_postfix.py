#TODO
#validaciones
#start graph
from alphabet_definition import AlphabetDefinition
from operators import *
from node_automata import Node
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


    def convertToPostfix(self,validate):
        #clean the expression
        flag_validation = Clear(self.expression,self.symbols).validate_expression_parenthesis()
        #check operators
        flag_operators = Clear(self.expression,self.symbols).validate_expression_operators()
        if flag_validation == False or flag_operators == False:
            print("Error: invalid expression")
            validate = False
            postfix = ""
        else:
            self.expression = Clear(self.expression,self.symbols).preprocess()
            #print(''.join(self.expression))
            #print(self.expression)

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
