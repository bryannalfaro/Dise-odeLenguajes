from operators import *
#Class for define the alphabet while reading the string
class AlphabetDefinition:
    def __init__(self):
        self.alphabet = []

    def getAlphabet(self):
        return self.alphabet

    def addSymbol(self, symbol):
        self.alphabet.append(symbol)

        #get symbol dictionary, ADD EPSILON OR NOT
    def getSymbolDictionary(self):
        operators = [KleeneStar(), Concatenation(), Union(), LeftParenthesis(), RightParenthesis(), QuestionMark(), PositiveClosure()]
        symbolDictionary = {}
        for i in range(len(operators)):
            symbolDictionary[operators[i].symbol] = operators[i]
        return symbolDictionary