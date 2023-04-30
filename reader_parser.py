class Reader_Parser():
    def __init__(self,path):
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



    def read(self):
        file = open(self.path, "r")
        for line in file:
            self.file_string += line
        self.process_file()
        file.close()
        print(self.file_string)
        print('COMMENTS: ',self.comments)

    def process_file(self):
        #Recorrer string
        i = 0
        while i < len(self.file_string):
            self.current_char = self.file_string[i]
            if self.processing_tokens:
                self.actual_tok = None
                self.process_token()
                i = self.pos
            else:
                #Caso en que se encuentre un comentario
                if self.current_char == '/' and self.get_next_char(self.file_string,self.pos) == '*':
                    self.comment()
                    self.comments.append(self.current_string)
                    self.current_string = ''
                #Caso en que se encuentre un let
                elif self.current_char == 'l' and self.get_next_char(self.file_string,self.pos) == 'e' and self.get_next_char(self.file_string,self.pos + 1) == 't' and self.get_next_char(self.file_string,self.pos + 2) == ' ':
                    self.process_definition()
                #Caso en que se encuentre un rule
                elif self.current_char == 'r' and self.get_next_char(self.file_string,self.pos) == 'u' and self.get_next_char(self.file_string,self.pos+1) == 'l' and self.get_next_char(self.file_string,self.pos+2) == 'e':
                    self.process_rule()
                    self.processing_tokens = True
                # if self.current_char == '{':
                #     self.header = self.process_action(False)
                elif self.current_char == '\n' or self.current_char == ' ' or self.current_char == '\t':
                    pass
                else:
                    self.errors.append('ERROR: Invalid syntax')
                    #ignore until the end of the line
                    while self.current_char != '\n':
                        self.current_char = self.get_next_char(self.file_string,self.pos)
                        self.pos += 1

                self.pos += 1
                i = self.pos

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