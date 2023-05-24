#write a python file to simulate and read the pickle file of dfa
class GeneratingScanner():
    def __init__(self,header = None,trailer=None):
        self.header = header
        self.trailer = trailer
        self.name_file = 'generated_scanner.py'
        self.name_parser = 'generated_parser.py'

    def build_scanner(self):
        with open(self.name_file,'w') as f:
            if self.header is not None:
                f.write(self.header.strip())
            f.write('''
import pickle
class ScannerSLR():
    def __init__(self):
      self.get_identified = None

    def load_dfa(self):
        #read the dfa
        with open('dfa', 'rb') as handle:
            dfa = pickle.load(handle)
        #read the file to simulate from console
        input_file = input('Enter the file to simulate: ')
        with open(input_file, 'r') as f:
            # Read the contents of the file
            text = f.read()

        #simulate the dfa
        dfa.simulate_dfa(text)
        tokens  = dfa.get_identified()
        self.get_identified = dfa.get_identified()
        yal_tokens = dfa.get_list_tokens()

        for i in tokens:
            if type(i) == str:
                print(i)
            else:
                if i.definition != None:
                    exec(i.definition.strip())
                else:
                    print('NO DEFINITION',i.token)
''')
            if self.trailer is not None:
                f.write(
self.trailer.strip()
                )


    def build_parser(self):
        with open(self.name_parser,'w') as f:
            if self.header is not None:
                f.write(self.header.strip())
            f.write('''
import pickle
class ParserSLR():
    def __init__(self,tokens):
        self.tokens = tokens
        self.load_construct()
        self.automata = None

    def load_construct(self):
        with open('lr0', 'rb') as handle:
            automata_lr = pickle.load(handle)
            automata = automata_lr.make_automata()
            #automata.visualization()
            actions, goto = automata_lr.make_table(automata)
            automata.action = actions
            automata.goto = goto
            self.automata = automata

    def simulate(self):
            self.automata.simulate(self.tokens)

''')



