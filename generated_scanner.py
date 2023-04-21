
import pickle
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

            