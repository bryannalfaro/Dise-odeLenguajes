
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
                    print(i.token)
                    #exec(i.definition.strip()) #yalex has return as definitions
                else:
                    print('NO DEFINITION',i.token)
