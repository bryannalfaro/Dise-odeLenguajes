from alphabet_definition import AlphabetDefinition
from operators import *
from cleaning_expr import Clear

class PostfixConverter:
    def __init__(self, expression):
        self.expression = expression
        self.alphabet = AlphabetDefinition()
        self.symbols = self.alphabet.getSymbolDictionary()
        self.stack_operators = []
        self.postfix_stack = []

    def build_Alphabet(self):
        for i in self.expression:
            if i not in self.symbols:
                self.alphabet.addSymbol(i)


    def convertToPostfix(self):
        #clean the expression
        self.expression = Clear(self.expression,self.symbols).preprocess()
        #print(''.join(self.expression))
        #print(self.expression)

        #Iterate through the expression
        for i in self.expression:

            #check if it is an alphabet symbol
            if i not in self.symbols:

                self.postfix_stack.append(i)
            #Check if the character is an operator
            elif i in self.symbols:
                if len(self.stack_operators) == 0:
                    self.stack_operators.append(i)
                #check if it is (
                elif i == '(':
                    self.stack_operators.append(i)
                #check if it is ) and empty the stack until (
                elif i == ')':
                    while self.stack_operators[-1] != '(':
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

        print(''.join(self.postfix_stack))