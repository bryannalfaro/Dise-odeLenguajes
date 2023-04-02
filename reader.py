from alphabet_definition import *
class Reader():
    def __init__(self, path):
        self.path = path
        self.text = ""
        self.definitions = []
        self.current_char = None
        self.next_char = None
        self.actual_line = None
        self.pos = 0
        self.definitions = {}
        self.comments = []
        self.current_string = ''
        self.temp_array = []
        self.symbols = AlphabetDefinition().getSymbolDictionary()
        self.rule_stack = {}
        self.token_name = ''
        self.processing_tokens = False
        self.regex = ''
        self.valid_scapes = ['n','t','r','v','f','a','b','e','\\','\'','"']

    def read_file(self):
        #read line by line
        with open(self.path, 'r') as file:
            for line in file:
                self.pos = 0
                self.actual_line = line
                print("Processing line: ")
                print(line)
                self.process_line(line)
            print(self.comments)
            print('TOKENS',self.rule_stack)
            print('DEFINITION',self.definitions)

    def get_tokens_expression(self):
        #recorrer el diccionario de tokens y armar la expresion regular
        for key in self.rule_stack:
            for i in self.rule_stack[key]:
                #if it is not the last element
                if i != self.rule_stack[key][-1]:
                    self.regex += '('+i+')' + '|'
                else:
                    self.regex += '('+i+')'
        print("FINAL REGEX: ",self.regex)
        return self.regex

    def process_line(self, line):
        if self.processing_tokens:
            self.process_token(line)
        else:
            for self.current_char in line:
                if self.current_char == '(' and self.get_next_char(line,self.pos) == '*':
                    self.comment()
                    self.comments.append(self.current_string)
                    self.current_string = ''
                    break
                elif self.current_char == 'l' and self.get_next_char(line,self.pos) == 'e' and self.get_next_char(line,self.pos + 1) == 't' and self.get_next_char(line,self.pos + 2) == ' ':
                    self.process_definition()
                    break
                elif self.current_char == 'r' and self.get_next_char(line,self.pos) == 'u' and self.get_next_char(line,self.pos+1) == 'l' and self.get_next_char(line,self.pos+2) == 'e':
                    self.process_rule()
                    self.processing_tokens = True
                    break
                else:
                    pass
                    #print('ELSE',self.current_char)
                #self.expand_dictionary()
                #print('JAJA',self.definitions['ws'][1])
                self.pos += 1

    def process_token(self, line):
        for self.current_char in line:
            if self.current_char == '(' and self.get_next_char(line,self.pos) == '*':
                self.comment()
                self.comments.append(self.current_string)
                self.current_string = ''
                break
            else:
                temp_word = ''
                if self.current_char != ' ':
                    while self.current_char != None  and self.current_char != '\n':
                        while self.current_char != "'" and self.current_char not in self.symbols.keys() and self.current_char != '[' and self.current_char != '"' and self.current_char != ' ' and self.current_char != '\n':
                            if self.current_char not in self.symbols.keys():
                                print('CONSUMING CHARS')

                                temp_word += self.current_char
                                self.current_char = self.get_next_char(self.actual_line,self.pos)
                                self.pos += 1
                                print('CURRENT ALL1',self.current_string,self.current_char in self.symbols.keys(),temp_word)
                        print('SALI DEL WHILE')
                        if temp_word in self.definitions.keys():
                            print('DEFINING WORD',temp_word)
                            self.current_string += self.definitions[temp_word]
                            self.rule_stack[self.token_name].append(self.current_string)
                            temp_word = ''
                            self.current_string = ''
                            self.current_char = self.get_next_char(self.actual_line,self.pos)
                            self.pos += 1
                        elif self.current_char == "'":
                            print('EVALURATING SINGLE')
                            self.evaluate_single()
                            self.rule_stack[self.token_name].append(self.current_string)
                            print('S',self.current_string,self.current_char,self.temp_array)
                        elif self.current_char == '"':
                            print('EVALURATING DOUBLE')
                            self.evaluate_double()
                            self.rule_stack[self.token_name].append(self.current_string)
                            print('D',self.current_string,self.current_char,self.temp_array)
                        else:
                            self.current_char = self.get_next_char(self.actual_line,self.pos)
                            self.pos += 1
                    print('CURRENT STRING SALE',self.current_string)

                    self.pos += 1
                    self.current_string = ''
                    break
                else:
                    self.current_char = self.get_next_char(self.actual_line,self.pos)
                    self.pos += 1


    def process_rule(self):
        print('RULE',self.current_char,self.pos)
        self.coincidir('r')
        self.coincidir('u')
        self.coincidir('l')
        self.coincidir('e')
        print('RULE2',self.current_char,self.pos)
        self.coincidir(' ')
        self.process_name()
        print('RULE3',self.current_char,self.pos,self.current_string)
        key = self.current_string
        self.token_name = key
        self.current_string = ''
        self.temp_array = []
        self.coincidir(' ')
        self.coincidir('=')
        self.current_char = self.get_next_char(self.actual_line,self.pos)
        self.pos += 1
        self.rule_stack[key] = []

    #Se maneja la definicion let
    def process_definition(self):
        print('ENTRANDO A PROCESS DEFINITION',self.current_char,self.current_string)
        self.coincidir('l')
        self.coincidir('e')
        self.coincidir('t')
        self.coincidir(' ')
        self.process_name()
        key = self.current_string
        self.current_string = ''
        self.temp_array = []
        self.coincidir(' ')
        self.coincidir('=')
        self.coincidir(' ')

        self.process_expression()
        self.definitions[key] = self.current_string
        #print('S3',self.current_char,self.pos,self.current_string)
        if self.current_char == ' ':
            self.current_char = self.get_next_char(self.actual_line,self.pos)
            self.pos += 1
            if self.current_char == '(' and self.get_next_char(self.actual_line,self.pos) == '*':
                self.current_string = ''
                self.comment()
                self.comments.append(self.current_string)
                self.current_string = ''
        #value = self.current_string

        print('DEFINITIONS',self.definitions)

        #print('TEMP ARRAY',self.definitions['delim'])
        self.current_string = ''


    def expand_dictionary(self):
        #iterate dictionary and find the keys that are in the values
        temp_string = ''
        temp_pos_string = []
        for key in self.definitions:
            for value in self.definitions[key]:
                temp_string = ''
                for i in range(len(value)):
                    temp_pos_string.append(i)
                    if temp_string in self.definitions.keys():
                        temp_string += self.definitions[value[i]]
                    else:
                        temp_string += value[i]
                temp_pos_string = []

    #Obtener el nombre de variable en let
    def process_name(self):
        while self.current_char != ' ':
            self.current_string += self.current_char
            self.current_char = self.get_next_char(self.actual_line,self.pos)
            self.pos += 1

    def process_expression(self):
        #caso en que es un []
        if self.current_char == '[' and self.get_next_char(self.actual_line,self.pos) == "'":
            self.process_list()
            if self.current_char == ' ' and self.get_next_char(self.actual_line,self.pos) == '(' and self.get_next_char(self.actual_line,self.pos + 1) == '*':
                self.current_string = ''
                self.comment()
                print('COMENTARIO ADENTRO DE EXPRESION',self.current_string)
                self.comments.append(self.current_string)
                self.current_string = ''
            elif self.current_char != '':
                print('NO FINALIZA EXPRESION')
                self.process_expression()
        elif self.current_char == '[' and self.get_next_char(self.actual_line,self.pos) == '"':
            self.process_list()
        elif self.current_char == "'":
            self.evaluate_single()
        else:
            temp_word = ''
            while self.current_char != None and self.current_char != ' ' and self.current_char != '\n':
                while self.current_char != "'" and self.current_char not in self.symbols.keys() and self.current_char != '[' and self.current_char != '"':
                    print('CONSUMING CHARS DETECTING VAR')
                    temp_word += self.current_char
                    self.current_char = self.get_next_char(self.actual_line,self.pos)
                    self.pos += 1
                    #print('CURRENT ALL1',self.current_string,self.current_char in self.symbols.keys())
                if temp_word in self.definitions.keys():
                    self.current_string += self.definitions[temp_word]
                    temp_word = ''
                elif self.current_char == "'":
                    print('EVALURATING SINGLE')
                    self.evaluate_single()
                    print('S',self.current_string,self.current_char,self.temp_array)
                elif self.current_char == '"':
                    print('EVALUATING DOUBLE')
                    self.evaluate_double()
                    print('S',self.current_string,self.current_char,self.temp_array)
                elif self.current_char == '[':
                    print('EVALUATING LIST')
                    self.process_list(False)
                    #print('S',self.current_string,self.current_char,self.temp_array)
                elif self.current_char in self.symbols.keys():
                    print('ADDING THE SYMBOL TO THE STRING')
                    #print('Adentro',self.current_char,self.temp_array,self.current_string)
                    self.current_string += self.current_char
                    self.current_char = self.get_next_char(self.actual_line,self.pos)
                    self.pos += 1
                    #self.temp_array = []
                print('CURRENT ALL',self.current_string,self.current_char,self.temp_array)

    def process_list(self,initial_exp = True):
        #self.current_string += self.current_char
        self.coincidir('[')

        while self.current_char != "]":
            if self.current_char == "'":
                print('EVALUATING SINGLE IN LIST')
                self.evaluate_single(True)
            elif self.current_char == '-':
                print(self.temp_array)
                print('EVALURATING -')
                self.evaluate_range()
            elif self.current_char == '"':
                print('EVALURATING DOUBLE')
                self.evaluate_double(True)

        #self.current_string += self.current_char
        self.coincidir(']')
        #print('LIST',self.current_string)
        print('TEMP LIST',self.temp_array)
        temp_string = ''

        temp_string += '('
        for element in self.temp_array:
            element = str(element)
            print(element, self.temp_array[-1])
            if element != str(self.temp_array[-1]):
                temp_string += element + '|'
            else:
                temp_string += element
        temp_string += ')'
        print('TEMP PROCESS EXPRESSION STRING',temp_string)
        if initial_exp:
            self.current_string = temp_string.strip()
        else:
            self.current_string += temp_string.strip()

    def evaluate_double(self,inside_list = False):
        #self.current_string += self.current_char
        self.coincidir('"')
        text = ''
        while self.current_char != '"':
            if self.current_char == '\\' and self.get_next_char(self.actual_line,self.pos) in self.valid_scapes:
                print('YA HERE')
                self.current_char = self.get_next_char(self.actual_line,self.pos)
                self.pos += 1
                if self.current_char in self.valid_scapes:
                    if self.current_char == 'n':
                        text = '\n'
                    elif self.current_char == 't':
                        text = '\t'

                    print('TEXT here',text, ord(text))
                    if len(str(ord(text))) ==1:
                        text = '00'+str(ord(text))
                    elif len(str(ord(text))) == 2:
                        text = '0'+str(ord(text))
                    else:
                        text = str(ord(text))

                self.temp_array.append(text)
                text = ''
                self.current_string += self.current_char
                self.current_char = self.get_next_char(self.actual_line,self.pos)
                self.pos += 1
            else:
                print('VINE',self.current_char)
                text += self.current_char
                print('TEXT',text)
                if len(str(ord(text))) ==1:
                    text = '00'+str(ord(text))
                elif len(str(ord(text))) == 2:
                    text = '0'+str(ord(text))
                else:
                    text = str(ord(text))

                self.temp_array.append(text)
                text = ''
                self.current_char = self.get_next_char(self.actual_line,self.pos)
                self.pos += 1

        print('HERE IN DOUBLE SALI',self.current_char,self.current_string,self.temp_array,text)
        if inside_list:
            self.current_string += text
        else:
            temp_string = ''
            temp_string += '('
            for element in self.temp_array:
                element = str(element)
                print(element, self.temp_array[-1])
                if element != str(self.temp_array[-1]):
                    temp_string += element + '|'
                else:
                    temp_string += element
            temp_string += ')'
            print('TEMP PROCESS EXPRESSION STRING',temp_string)
            self.current_string = temp_string.strip()


        self.coincidir('"')


    def evaluate_range(self):
        #self.current_string += self.current_char
        self.coincidir('-')
        #print('CURRENT STRING -',self.current_string)
        self.evaluate_single(True)
        print('TEMP ARRAY OF RANGE',self.temp_array)
        self.expand_range()
        #print('HERE AA J',self.current_char,self.current_string)

    def expand_range(self):
        #get the ascii value of the first char and the last char and then expand the range
        print('EXPANDING RANGE')
        #pop the last element
        last = self.temp_array.pop()
        #pop the first element
        first = self.temp_array.pop()
        print('FIRST',chr(int(first)))
        print('LAST',chr(int(last)))
        for i in range(int(first),int(last) + 1):
            if len(str(i)) ==1:
                i = '00'+str(i)
            elif len(str(i))==2:
                i = '0'+str(i)
            self.temp_array.append(i)
        print('TEMP ARRAY EXPAND',self.temp_array)

    def evaluate_single(self,inside_list = False):
        print('EVALUATING SINGLE inside',self.current_string)
        self.coincidir("'")
        #get one char
        text = ''
        while self.current_char != "'":
            if self.current_char == '\\':
                print('YA HERE')
                self.current_char = self.get_next_char(self.actual_line,self.pos)
                self.pos += 1
                if self.current_char == 'n':
                    text = '\n'
                elif self.current_char == 't':
                    text = '\t'
                elif self.current_char == 's':
                    text = '\s'
                print('TEXT here',text)
                self.current_string += self.current_char
                self.current_char = self.get_next_char(self.actual_line,self.pos)
                self.pos += 1
            else:
                print('VINE',self.current_char)
                text += self.current_char
                print('TEXT',text)

                self.current_char = self.get_next_char(self.actual_line,self.pos)
                self.pos += 1
        print('SALI DE EVALUAR SINGLE',text,ord(text))
        if len(str(ord(text))) ==1:
            text = '00'+str(ord(text))
        elif len(str(ord(text))) == 2:
            print('SOY LEN 2')
            text = '0'+str(ord(text))
        else:
            text = str(ord(text))

        if inside_list:
            self.temp_array.append(text)
        else:
            self.current_string += text

        #self.current_string += text
        self.coincidir("'")

    def comment(self):
        self.current_string += self.current_char
        print('YES',self.current_string)
        self.coincidir('(')
        self.current_string += self.current_char
        print('YES',self.current_string)
        self.coincidir('*')
        while self.current_char != '*' and self.get_next_char(self.actual_line,self.pos) != ')':
            self.current_string += self.current_char
            self.current_char = self.get_next_char(self.actual_line,self.pos)
            self.pos += 1

        self.current_string += self.current_char
        self.coincidir('*')
        self.current_string += self.current_char
        self.coincidir(')')

    def coincidir(self,terminal):
        if self.current_char == terminal:
            self.current_char = self.get_next_char(self.actual_line,self.pos)
            self.pos += 1
        elif self.current_char == None:
            pass
        else:
            print('Error')

    def get_next_char(self, line, pos = None):

        index = pos
        if index + 1 < len(line):
            print('line',line[index + 1])
            return line[index + 1]
        else:
            print('aahh')
            return None

