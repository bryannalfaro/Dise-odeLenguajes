#Make abstract class operators


class Operator():
    def __init__(self, symbol, precedence, associativity):
        self.symbol = symbol
        self.precedence = precedence
        self.associativity = associativity

#Make kleene star operator
class KleeneStar(Operator):
    def __init__(self):
        super().__init__('*', 3, 'right')

    def valid_operation(self,expression):
        flag = True
        counter = 0
        expression_len = len(expression)
        flag = True
        counter = 0
        expression = list(expression)
        expression_len = len(expression)
        index = expression.index(self.symbol)
        try:
            while flag and expression_len>0:

                if expression[counter] == self.symbol:
                    if expression[:index][-1] == Union().symbol:
                        flag = False
                counter += 1
                expression_len -= 1
        except:
          #print('except kleene')
          flag = False
        return flag

#Make concatenation operator
class Concatenation(Operator):
    def __init__(self):
        super().__init__('.', 2, 'left')

#Make union operator
class Union(Operator):
    def __init__(self):
        super().__init__('|', 1, 'left')

    def valid_operation(self,expression,alphabet):
        flag = True
        counter = 0
        expression = list(expression)
        expression_len = len(expression)
        index = expression.index(self.symbol)
        try:
            while flag and expression_len>0:

                if expression[counter] == self.symbol:

                    #print('expression',expression[counter],expression[:expression.index('|')][-1],expression[expression.index("|")+1:])
                    if expression[:index][-1] == self.symbol:
                        flag = False
                    elif expression[index+1:][0] == self.symbol or (expression[index+1:][0] != (LeftParenthesis().symbol) and expression[index+1:][0] in alphabet):
                        flag = False
                counter += 1
                expression_len -= 1
        except:
          flag = False
        return flag

#Make left parenthesis operator
class LeftParenthesis(Operator):
    def __init__(self):
        super().__init__('(', 0, None)

#Make right parenthesis operator
class RightParenthesis(Operator):
    def __init__(self):
        super().__init__(')', 0, None)

#Make question mark operator
class QuestionMark(Operator):
    def __init__(self):
        super().__init__('?', 3, 'right')

    def get_representation(self, symbol):
        #return (a|ε)
        if len(symbol) == 1:
            return '('+symbol+Union().symbol+Epsilon().symbol+')'
        else:
            return '('+'('+symbol+')'+Union().symbol+Epsilon().symbol + ')'

    def valid_operation(self,expression):
        flag = True
        counter = 0
        expression_len = len(expression)
        flag = True
        counter = 0
        expression = list(expression)
        expression_len = len(expression)
        index = expression.index(self.symbol)
        try:
            while flag and expression_len>0:

                if expression[counter] == self.symbol:
                    if expression[:index][-1] == Union().symbol:
                        flag = False
                counter += 1
                expression_len -= 1
        except:
          flag = False
        return flag


#Positive closure operator
class PositiveClosure(Operator):
    def __init__(self):
        super().__init__('+', 3, 'right')

    def get_representation(self, symbol):
        if len(symbol) == 1:
            return '('+symbol+symbol+KleeneStar().symbol+')'
        else:
            return '('+'('+symbol+')'+'('+symbol+')'+KleeneStar().symbol+')'

    def valid_operation(self,expression):
        flag = True
        counter = 0
        expression_len = len(expression)
        flag = True
        counter = 0
        expression = list(expression)
        expression_len = len(expression)
        index = expression.index(self.symbol)
        #print('ja')
        try:
            while flag and expression_len>0:
                #print('ja')
                #print('ja',expression[:index][-1])
                if expression[counter] == self.symbol:
                    if expression[:index][-1] == Union().symbol:
                        flag = False
                counter += 1
                expression_len -= 1
        except:
          print('except')
          flag = False
        return flag

#Make epsilon operator
class Epsilon(Operator):
    def __init__(self):
        super().__init__('ε', 0, None)



