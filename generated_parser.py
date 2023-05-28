
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

