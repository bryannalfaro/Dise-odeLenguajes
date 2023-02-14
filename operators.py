#Make abstract class operators

from abc import ABC, abstractmethod

class Operator(ABC):
    @abstractmethod
    def __init__(self):
        self.symbol = None
        self.precedence = None
        self.associativity = None

#Make kleene star operator
class KleeneStar(Operator):
    def __init__(self):
        self.symbol = '*'
        self.precedence = 3
        self.associativity = 'right'

#Make concatenation operator
class Concatenation(Operator):
    def __init__(self):
        self.symbol = '.'
        self.precedence = 2
        self.associativity = 'left'

#Make union operator
class Union(Operator):
    def __init__(self):
        self.symbol = '|'
        self.precedence = 1
        self.associativity = 'left'

#Make left parenthesis operator
class LeftParenthesis(Operator):
    def __init__(self):
        self.symbol = '('
        self.precedence = 0
        self.associativity = None

#Make right parenthesis operator
class RightParenthesis(Operator):
    def __init__(self):
        self.symbol = ')'
        self.precedence = 0
        self.associativity = None

#Make question mark operator
class QuestionMark(Operator):
    def __init__(self):
        self.symbol = '?'
        self.precedence = 3
        self.associativity = 'right'

    def get_representation(self, symbol):
        #return (a|ε)
        #if RightParenthesis().symbol not in symbol and LeftParenthesis().symbol not in symbol:
         #   return symbol+'|'+Epsilon().symbol
        #else:
        if len(symbol) == 1:
            return '('+symbol+Union().symbol+Epsilon().symbol+')'
        else:
            return '('+'('+symbol+')'+Union().symbol+Epsilon().symbol + ')'
#Positive closure operator
class PositiveClosure(Operator):
    def __init__(self):
        self.symbol = '+'
        self.precedence = 3
        self.associativity = 'right'

    def get_representation(self, symbol):
        if len(symbol) == 1:
            return '('+symbol+symbol+KleeneStar().symbol+')'
        else:
            return '('+'('+symbol+')'+'('+symbol+')'+KleeneStar().symbol+')'

#Make epsilon operator
class Epsilon(Operator):
    def __init__(self):
        self.symbol = 'ε'
        self.precedence = 0
        self.associativity = None



