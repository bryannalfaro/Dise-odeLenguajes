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

    def read_file(self):
        #read line by line
        with open(self.path, 'r') as file:
            for line in file:
                self.pos = 0
                self.actual_line = line
                print("Processing line: ")
                print(line)
                self.process_line(line)

    def process_line(self, line):
        for self.current_char in line:
            if self.current_char == '(' and self.get_next_char(line,self.pos) == '*':
                self.comment()
                self.comments.append(self.current_string)
                self.current_string = ''
                break
            elif self.current_char == 'l' and self.get_next_char(line,self.pos) == 'e' and self.get_next_char(line,self.pos + 1) == 't' and self.get_next_char(line,self.pos + 2) == ' ':
                self.process_definition()
                break
            else:
                pass
                #print('ELSE',self.current_char)
            self.pos += 1

    def process_definition(self):
        print('S',self.current_char,self.pos)
        self.coincidir('l')
        self.coincidir('e')
        self.coincidir('t')
        print('S2',self.current_char,self.pos)
        self.coincidir(' ')
        self.process_name()
        print('S3',self.current_char,self.pos,self.current_string)
        key = self.current_string
        self.current_string = ''
        self.temp_array = []
        self.coincidir(' ')
        self.coincidir('=')
        self.coincidir(' ')
        self.process_expression()
        print('S3',self.current_char,self.pos,self.current_string)
        value = self.current_string
        print('VALUE',value)
        self.definitions[key] = self.temp_array
        print('DEFINITIONS',self.definitions)
        #print('TEMP ARRAY',self.definitions['delim'])
        self.current_string = ''

    def process_name(self):
        while self.current_char != ' ':
            self.current_string += self.current_char
            self.current_char = self.get_next_char(self.actual_line,self.pos)
            self.pos += 1

    def process_expression(self):
        print('EXPRESION CHAR',self.current_char)
        #caso en que es un []
        if self.current_char == '[' and self.get_next_char(self.actual_line,self.pos) == "'":
            self.process_list()
        else:
            while self.current_char != None:
                print('EXPRESION CURRENT CHAR',self.current_char,self.current_string)
                self.current_string += self.current_char
                self.current_char = self.get_next_char(self.actual_line,self.pos)
                self.pos += 1
            print('EXPRESION CURRENT STRING',self.current_string)
            self.temp_array.append(self.current_string.strip())


    def process_list(self):
        print('IM HERE')
        self.current_string += self.current_char
        self.coincidir('[')

        while self.current_char != "]":


            if self.current_char == "'":
                print('EVALURATING SINGLE')
                self.evaluate_single()
            elif self.current_char == '-':
                print(self.temp_array)
                print('EVALURATING -')
                self.evaluate_range()

        self.current_string += self.current_char
        self.coincidir(']')
        print('LIST',self.current_string)

    def evaluate_range(self):
        self.current_string += self.current_char
        self.coincidir('-')
        print('CURRENT STRING -',self.current_string)
        self.evaluate_single()
        print('WATCCHING TEMP ARRAY',self.temp_array)
        self.expand_range()
        print('HERE AA J',self.current_char,self.current_string)

    def expand_range(self):
        #get the ascii value of the first char and the last char and then expand the range
        print('EXPANDING RANGE')
        #pop the last element
        last = self.temp_array.pop()
        #pop the first element
        first = self.temp_array.pop()
        for i in range(ord(first),ord(last) + 1):
            self.temp_array.append(chr(i))
        print('TEMP ARRAY EXPAND',self.temp_array)
    def evaluate_single(self):
        self.current_string += self.current_char
        self.coincidir("'")
        #get one char
        text = ''
        while self.current_char != "'":
            self.current_string += self.current_char
            text += self.current_char
            print('TEXT',text)

            self.current_char = self.get_next_char(self.actual_line,self.pos)
            self.pos += 1
        print('SALI',text)
        self.temp_array.append(text)

        self.current_string += self.current_char
        self.coincidir("'")

    def comment(self):
        self.current_string += self.current_char
        self.coincidir('(')
        self.current_string += self.current_char
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
        print('current',self.current_char)
        print('terminal',terminal)
        if self.current_char == terminal:
            self.current_char = self.get_next_char(self.actual_line,self.pos)
            self.pos += 1
            print('current2',self.current_char)
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

