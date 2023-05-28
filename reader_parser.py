class Reader_Parser():
    def __init__(self,path,yalex_tokens):
        self.yalex_tokens = yalex_tokens
        self.yalex_values = []
        self.get_tok_values()
        self.path = path
        self.file_string = ''
        self.current_char = ''
        self.pos = 0
        self.processing_tokens = False
        self.actual_tok = None
        self.tokens = []
        self.rules = []
        self.comments = []
        self.errors = []
        self.current_string = ''
        self.header = ''
        self.counter_increment = 0
        self.processing_production = False
        self.ignored_tokens = []
        self.productions_list = {}
        self.actual_prod = ''


    def get_tok_values(self):
        for i in self.yalex_tokens:
            self.yalex_values.append(i.token)
        print('YALEX VALUES',self.yalex_values)
    def read(self):
        file = open(self.path, "r",encoding="utf8")
        for line in file:
            self.file_string += line
        self.process_file()
        file.close()
        if len(self.errors) > 0:
            print('ERRORS: ',self.errors)
            return False
        elif len(self.yalex_values) != len(self.tokens):
            print('YAELX TOKENS: ',self.yalex_values)
            print('TOKENS: ',self.tokens)
            return False
        else:
            #print(self.file_string)
            print('COMMENTS: ',self.comments)
            print('TOKENS: ',self.tokens)
            #Ignored
            print('IGNORED: ',self.ignored_tokens)
            print('RULES: ',self.rules)
            print('PRODUCTIONS: ',self.productions_list)
            return True

    def process_file(self):
        #Recorrer string
        i = 0
        while i < len(self.file_string):

            self.current_char = self.file_string[i]
            #print('CHAR: ',self.current_char)

            if self.processing_production:
                #validate if the tokens are in yalex_tokens

                self.productions()
                i = self.pos
            else:
                #Caso en que se encuentre un comentario
                if self.current_char == '/' and self.get_next_char(self.file_string,self.pos) == '*':
                    self.comment()
                    self.comments.append(self.current_string)
                    self.current_string = ''
                #Caso en que se encuentre un let
                elif self.current_char == '%' and self.get_next_char(self.file_string,self.pos) == 't' and self.get_next_char(self.file_string,self.pos+1) == 'o' and self.get_next_char(self.file_string,self.pos+2) == 'k' and self.get_next_char(self.file_string,self.pos+3) == 'e' and self.get_next_char(self.file_string,self.pos+4) == 'n':
                    self.process_token()
                elif self.current_char == '\n' or self.current_char == ' ' or self.current_char == '\t':
                    pass
                #IGNORE
                elif self.current_char == 'I' and self.get_next_char(self.file_string,self.pos) == 'G' and self.get_next_char(self.file_string,self.pos+1) == 'N' and self.get_next_char(self.file_string,self.pos+2) == 'O' and self.get_next_char(self.file_string,self.pos+3) == 'R' and self.get_next_char(self.file_string,self.pos+4) == 'E':
                    self.process_ignore()
                elif self.current_char == '%' and self.get_next_char(self.file_string,self.pos) == '%':
                    for token in self.tokens:
                        print('TOKEN',token)
                        #IF TOKEN IS NOT IN YALEX TOKENS.value
                        if token not in self.yalex_values:
                            print("here ",token)
                            self.errors.append(f'ERROR: Token {token} not found in yalex tokens')
                    self.processing_production = True
                    self.current_char = self.get_next_char(self.file_string,self.pos)
                    self.pos += 1
                else:
                    self.errors.append('ERROR: Invalid syntax')
                    #ignore until the end of the line
                    while self.current_char != '\n':
                        self.current_char = self.get_next_char(self.file_string,self.pos)
                        self.pos += 1
                self.pos += 1
                i = self.pos

    def productions(self):
        while self.current_char != '\n' and self.current_char !=  None:
            if self.current_char == '/' and self.get_next_char(self.file_string,self.pos) == '*':
                self.comment()
                self.comments.append(self.current_string)
                self.current_string = ''
            elif self.current_char == ':':
                #add to dictionary
                self.actual_prod = self.current_string
                self.productions_list[self.current_string] = []
                self.process_production()
            else:
                self.current_string += self.current_char
            self.current_char = self.get_next_char(self.file_string,self.pos)
            self.pos += 1
        self.pos += 1


    def process_production(self):
        #consume until find ;
        self.current_string = ''
        self.coincidir(':')
        while self.current_char != ';':
            if self.current_char == '|':
                self.productions_list[self.actual_prod].append(self.current_string)
                self.current_string = ''
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
            elif self.current_char == '\n':
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
            else:
                self.current_string += self.current_char
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
        self.productions_list[self.actual_prod].append(self.current_string)
        self.current_string = ''



    def process_ignore(self):
        self.coincidir('I')
        self.coincidir('G')
        self.coincidir('N')
        self.coincidir('O')
        self.coincidir('R')
        self.coincidir('E')
        self.coincidir(' ')
        self.process_ignore_sentence()

    def process_ignore_sentence(self):
        while self.current_char != '\n' and self.current_char != None:
            if self.current_char == ' ':
                #clean string and read other token
                self.ignored_tokens.append(self.current_string)
                self.current_string = ''
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
            else:
                self.current_string += self.current_char
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
        self.ignored_tokens.append(self.current_string)
        self.current_string = ''

    def process_token(self):
        self.coincidir('%')
        self.coincidir('t')
        self.coincidir('o')
        self.coincidir('k')
        self.coincidir('e')
        self.coincidir('n')
        self.coincidir(' ')
        self.process_name()

    def process_name(self):
        while self.current_char != '\n' and self.current_char != None:
            if self.current_char == ' ':
                #clean string and read other token
                self.tokens.append(self.current_string)
                self.current_string = ''
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
            else:
                self.current_string += self.current_char
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
        self.tokens.append(self.current_string)
        self.current_string = ''

    #Metodo para evaluar comentario
    def comment(self, init=True):
        if init:
            #self.current_string += self.current_char
            self.coincidir('/')
            #self.current_string += self.current_char
            self.coincidir('*')
            while self.current_char != '*' or self.get_next_char(self.file_string,self.pos) != '/':
                #print('CURRENT',self.current_char,self.pos,self.get_next_char(self.actual_line,self.pos))
                self.current_string += self.current_char
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
                #print('SELF CURRENT',self.current_char,self.get_next_char(self.actual_line,self.pos))

            print('SALIR')
            #self.current_string += self.current_char
            self.coincidir('*')
            #self.current_string += self.current_char
            self.coincidir('/')
        else:
            self.current_char = self.get_next_char(self.file_string,self.pos)
            self.pos += 1
            self.comment_inside += self.current_char
            self.coincidir('/')
            self.comment_inside += self.current_char
            self.coincidir('*')
            while self.current_char != '*' or self.get_next_char(self.file_string,self.pos) != '/':
                self.comment_inside += self.current_char
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1

            self.comment_inside += self.current_char
            self.coincidir('*')
            self.comment_inside += self.current_char
            self.coincidir('/')

    def coincidir(self,terminal):
        if self.current_char == terminal:
            self.current_char = self.get_next_char(self.file_string,self.pos)
            self.pos += 1
            self.counter_increment += 1
        elif self.current_char == None:
            pass
        else:
            print('Error')

    def get_next_char(self, string, pos = None):
        index = pos
        if index + 1 < len(string):
            return string[index + 1]
        else:
            return None