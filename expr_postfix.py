from alphabet_definition import AlphabetDefinition
from operators import *

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


    def make_changes_operators(self):
        new_expression = []
        for i in range(len(self.expression)):
            new_expression.append(self.expression[i])

            #Evaluate the question mark
            if self.expression[i] == QuestionMark().symbol:
                    new_expression.pop()
                    a = []
                    #pop the question mark and the symbols before it
                    while len(new_expression) > 0 :
                        a.append(new_expression.pop())
                    new_expression = list((QuestionMark().get_representation(''.join(reversed(a)))))
            #Evaluate the positive closure
            if self.expression[i] == PositiveClosure().symbol:
                    new_expression.pop()
                    a = []
                    #pop the question mark and the symbols before it
                    while len(new_expression) > 0 :
                        a.append(new_expression.pop())
                    new_expression = list((PositiveClosure().get_representation(''.join(reversed(a)))))
        return new_expression

    #add the concatenation operator after the kleene star
    def preprocess(self):
        new_expression = []

        self.expression = self.make_changes_operators()
        self.expression = ''.join(self.expression)


        for i in range(len(self.expression)):
            new_expression.append(self.expression[i])

            if i < len(self.expression) -1:

                if self.expression[i] == KleeneStar().symbol or self.expression[i] == RightParenthesis().symbol or self.expression[i] == Epsilon().symbol :
                    if self.expression[i+1] != RightParenthesis().symbol and self.expression[i+1] not in self.symbols:

                        new_expression.append(Concatenation().symbol)
                    elif self.expression[i+1] == LeftParenthesis().symbol:

                        new_expression.append(Concatenation().symbol)
                #add concatenation operator between two alphabet symbols
                elif self.expression[i] not in self.symbols:
                    if self.expression[i+1] not in self.symbols and self.expression[i+1] != RightParenthesis().symbol:

                        new_expression.append(Concatenation().symbol)

        return new_expression




    def convertToPostfix(self):

        #Iterate through the expression
        self.expression = self.preprocess()

        print(''.join(self.expression))


        #print(self.expression)
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
                #check if it is )
                elif i == ')':
                    while self.stack_operators[-1] != '(':
                        self.postfix_stack.append(self.stack_operators.pop())
                    self.stack_operators.pop()
                else:
                    #while the precedence is less or equal

                    while len(self.stack_operators) != 0 and self.symbols[i].precedence <= self.symbols[self.stack_operators[-1]].precedence:
                        self.postfix_stack.append(self.stack_operators.pop())
                    self.stack_operators.append(i)


                    '''if self.symbols[i].precedence< self.symbols[self.stack_operators[-1]].precedence:
                        self.postfix_stack.append(self.stack_operators.pop())
                        self.stack_operators.append(i)
                    elif self.symbols[i].precedence == self.symbols[self.stack_operators[-1]].precedence:
                        self.postfix_stack.append(self.stack_operators.pop())
                        self.stack_operators.append(i)
                    else:
                        self.stack_operators.append(i)'''

        #Empty the stack
        while len(self.stack_operators) != 0:
            self.postfix_stack.append(self.stack_operators.pop())

        print(''.join(self.postfix_stack))