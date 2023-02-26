from operators import *
class Clear():
    def __init__(self, expression,symbols):
        self.expression = expression
        self.symbols = symbols

    #Validar que la cantidad de parentesis este balanceada
    def validate_expression_parenthesis(self):
        opening_parenthesis = [LeftParenthesis().symbol]
        closing_parenthesis = [RightParenthesis().symbol]
        counter_parenthesis = 0
        positions_opening = []
        positions_closing = []

        for i in range(len(self.expression)):
            if self.expression[i] in opening_parenthesis: #si es un parentesis izquierdo
                counter_parenthesis += 1 #aumenta el contador
                positions_opening.append(i) #guarda la posicion del parentesis
            elif self.expression[i] in closing_parenthesis: #si es un parentesis derecho
                counter_parenthesis -= 1 #disminuye el contador
                if positions_opening != []: #si hay parentesis izquierdos
                    positions_opening.pop() #elimina el ultimo parentesis izquierdo
                else:
                    positions_closing.append(i) #hay mas derechos que izquierdos
        if counter_parenthesis != 0: #Esta desbalanceado
            if positions_opening != []:
                return False, "Error: Missing closing parenthesis of parenthesis in position " + ','.join(map(str, positions_opening))
            elif positions_closing != []:
                return False, "Error: Missing opening parenthesis of parenthesis in position " + ','.join(map(str, positions_closing))
        else:
            return True, ""

    #Validar que dentro de los parentesis no este vacio
    def validate_expression_inside_parenthesis(self,alphabet):
        flag_parenthesis = True
        if alphabet == []: #No vino nada
             flag_parenthesis = False
        else:
            inside = []
            new_expression = list(self.expression)

            #Se recorre la expresion
            while len(new_expression) > 0 :

                value = new_expression[-1]

                if value == RightParenthesis().symbol: #Si es un parentesis derecho evalua
                    counter_R = 0 #Si hay mas de un parentesis
                    counter_L = 0
                    new_expression.pop()

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
                            inside = inside[::-1] #reverse the list

                            if inside[0] == RightParenthesis().symbol:
                                inside = []
                                break
                            else:
                                inside.append(new_expression.pop())
                        else:
                            counter_R += 1
                            inside.append(new_expression.pop())

                    if inside == []:
                        flag_parenthesis = False
                        break
                    else:
                        flag_parenthesis = True
                    inside = []

                if flag_parenthesis == False:
                    break
                elif flag_parenthesis == True and len(new_expression) > 0:
                    new_expression.pop()
        if flag_parenthesis == False:
            return flag_parenthesis, "Error: Empty parenthesis"
        else:
         return flag_parenthesis, ""

    #Valida las necesidades de cada operador
    def validate_expression_operators(self):
        operators = [KleeneStar().symbol, Concatenation().symbol, Union().symbol, QuestionMark().symbol, PositiveClosure().symbol]
        flag_operator = True
        error = ""
        for i in range(len(self.expression)):
            if self.expression[i] in operators and flag_operator ==True:
                if self.expression[i] == Union().symbol:

                    #check if has a symbol before and after
                    flag_operator,error = Union().valid_operation(self.expression,self.symbols)
                elif self.expression[i] == KleeneStar().symbol:

                    flag_operator,error = KleeneStar().valid_operation(self.expression)

                elif self.expression[i] == QuestionMark().symbol:
                    flag_operator,error = QuestionMark().valid_operation(self.expression)
                elif self.expression[i] == PositiveClosure().symbol:

                    flag_operator,error = PositiveClosure().valid_operation(self.expression)
            elif flag_operator == False:
                break
            else:
                pass
        return flag_operator,error


    #Realiza la transformacion dependiendo del symbol
    def clean_special_operators(self,symbol, new_expression):
        #pop the symbol
        new_expression.pop()
        a = []
        inside = []
        external_letters = []

        while len(new_expression) > 0 :
            value = new_expression[-1]
            #evaluate value not in symbols
            if value != RightParenthesis().symbol:
                if inside != []: #demas letras
                    external_letters.append(new_expression.pop())
                #evaluate if the value is not a symbol
                elif value not in self.symbols:

                    a.append(new_expression.pop())
                    break
                else:
                    a.append(new_expression.pop())

            elif value == RightParenthesis().symbol:
                counter_R = 0 #Count if there are more than one parenthesis
                counter_L = 0
                new_expression.pop()

                #iterate until you find the left parenthesis
                while len(new_expression) > 0:
                    value = new_expression[-1]
                    if value != LeftParenthesis().symbol and value != RightParenthesis().symbol:
                        inside.append(new_expression.pop()) #agregar el valor
                    elif value == LeftParenthesis().symbol and counter_R == counter_L:
                        new_expression.pop() #se termina dentro de los parentesis
                        break
                    elif value == LeftParenthesis().symbol and counter_R != counter_L:
                        counter_L += 1 #hay mas parentesis izquierdos
                        inside.append(new_expression.pop()) #agregar el valor
                    else:
                        counter_R += 1 #hay mas parentesis derechos
                        inside.append(new_expression.pop())
                #esta entre parentesis
                inside = list((symbol.get_representation(''.join(reversed(inside)))))
                new_expression = new_expression + inside
                break
            else:
                pass
        if a != []:
            #make conversion, no esta entre parentesis
            conversion = list((symbol.get_representation(''.join(reversed(a)))))
            new_expression = new_expression + conversion

        return new_expression


    #Realiza la transformacion de los simbolos especiales
    def make_changes_operators(self):
        new_expression = []

        for i in range(len(self.expression)):
            new_expression.append(self.expression[i])
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

        for i in range(len(self.expression)):
            new_expression.append(self.expression[i])

            if i < len(self.expression) -1:

                if self.expression[i] == KleeneStar().symbol or self.expression[i] == RightParenthesis().symbol or self.expression[i] == Epsilon().symbol :
                    if self.expression[i+1] != RightParenthesis().symbol and self.expression[i+1] not in self.symbols:

                        new_expression.append(Concatenation().symbol) #add concatenation operator
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
