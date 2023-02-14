from operators import *
class Clear():
    def __init__(self, expression,symbols):
        self.expression = expression
        self.symbols = symbols

    def clean_special_operators(self,symbol, new_expression):

        new_expression.pop()
        a = []
        inside = []
        external_letters = []
        #pop the question mark and the symbols before it
        while len(new_expression) > 0 :
            #print('new while',new_expression)
            value = new_expression[-1]
            #print('value',value)
            #evaluate value not in symbols
            if value != RightParenthesis().symbol:
                if inside != []: #demas letras
                    external_letters.append(new_expression.pop())
                #evaluate if the value is not a symbol
                elif value not in self.symbols:

                    a.append(new_expression.pop())
                    #conversion = list((QuestionMark().get_representation(''.join(reversed(a)))))
                    break
                else:
                    a.append(new_expression.pop())

            #elif value == LeftParenthesis().symbol:
            #    new_expression.pop()
            #   break
            elif value == RightParenthesis().symbol:
                counter_R = 0
                counter_L = 0
                new_expression.pop()
                #print('right',new_expression)
                #iterate until you find the left parenthesis
                while len(new_expression) > 0:
                    value = new_expression[-1]
                    if value != LeftParenthesis().symbol and value != RightParenthesis().symbol:
                        inside.append(new_expression.pop())
                    elif value == LeftParenthesis().symbol and counter_R == counter_L:
                        new_expression.pop()
                        break
                    elif value == LeftParenthesis().symbol and counter_R != counter_L:
                        counter_L += 1
                        inside.append(new_expression.pop())
                    else:
                        counter_R += 1
                        inside.append(new_expression.pop()) #PROVISIONAL
                inside = list((symbol.get_representation(''.join(reversed(inside)))))
                new_expression = new_expression + inside
                #print("inside",inside)
                #print("new expresion right",new_expression)
                break
            else:
                pass
                #a.append(new_expression.pop())
                #print('inside',inside)
                #inside = list((QuestionMark().get_representation(''.join(reversed(inside)))))
        #print("a question",a)
        if a != []:
            #make conversion
            conversion = list((symbol.get_representation(''.join(reversed(a)))))
            new_expression = new_expression + conversion
        #print("new",new_expression)
        #print(conversion,inside,external_letters)
        #new_expression = new_expression +inside + external_letters
        return new_expression



    def make_changes_operators(self):
        new_expression = []

        for i in range(len(self.expression)):
            new_expression.append(self.expression[i])
            #print("new_expression for",new_expression)

            #if inside != [] and new_expression[-1] == LeftParenthesis().symbol:
            #    new_expression.pop()
            if self.expression[i] == QuestionMark().symbol:
                new_expression = self.clean_special_operators(QuestionMark(), new_expression)
            elif self.expression[i] == PositiveClosure().symbol:
                new_expression = self.clean_special_operators(PositiveClosure(), new_expression)


        return new_expression

    #add the concatenation operator after the kleene star
    def preprocess(self):
        new_expression = []

        self.expression = self.make_changes_operators()
        self.expression = ''.join(self.expression)
        #print('after symbols',self.expression)

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
                    #add concatenation between alphabet and left parenthesis
                    elif self.expression[i+1] == LeftParenthesis().symbol:

                        new_expression.append(Concatenation().symbol)

        return new_expression
