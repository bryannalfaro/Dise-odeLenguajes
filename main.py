from expr_postfix import PostfixConverter
from state_definition import State
from automata.tree import Tree
from reader import Reader
from reader_parser import Reader_Parser
import pickle
from generate_code import GeneratingScanner
from automata.LR0 import AutomataLR
from construct_lr0 import ConstructLR
#initialize alphabet
validate =False
State.counter = 0

#read file
yal_file = input('Enter the file to read: ')
reader = Reader(yal_file)
flag  = reader.read_file()

if flag == False:
    print('Error reading file')
    exit()
expression = reader.get_tokens_expression()

#read parser file
yapar_file = input('Enter the file to read: ')
reader_parser = Reader_Parser(yapar_file,reader.tokens_file)
flag = reader_parser.read()

if flag == False:
    print('Error reading file')
    exit()

print("LOS TOKENS SI COINCIDEN")

#make the automata
automata_lr = ConstructLR(reader_parser.productions_list,reader_parser.tokens)
automata = automata_lr.make_automata()
print('FIRST',automata_lr.first('expression'))
print('FOLLOW',automata_lr.follow('expression'))
actions, goto = automata_lr.make_table(automata)
automata.action = actions
automata.goto = goto
automata.simulate()

#automata.visualization()
input()

'''
THIS PART IS FOR THE DFA DIRECT
'''
a = input("Enter to continue...") #solo para la siguiente
print('----------------------------------------')

print('DFA DIRECT')
print('EXPRESSION DFA: ',expression)
#direct dfa
expression_postfix = PostfixConverter(expression, tokens_file = reader.tokens_file) #Se aumenta la expresion

postfix,validate= expression_postfix.convertToPostfix(validate)
alfabeto = expression_postfix.build_Alphabet()
print('ALF',alfabeto.getAlphabetNames())

#print('Postfix: ',postfix)
node_root = expression_postfix.make_nodes(postfix)#nodo root

#tree = Tree(node_root)
#tree.dot.render('tree.gv', view=True)

#print(node_root.value)
postorder_labeled= node_root.label_leafs() #se enumeran las hojas
for i in reader.tokens_file:
    print(i.token,i.value,i.definition,i.id_leaf)
node_root.make_rules(postorder_labeled) #se hacen las reglas

#print(node_root.follow)
dfa_direct = node_root.make_dfa_direct(alfabeto.getAlphabetNames())
# print('Estados :',dfa_direct.states)
# print('Transiciones: ',dfa_direct.transitions)
# print('Estado inicial: ',dfa_direct.initial)
# print('Estado final: ',dfa_direct.finals)
# print('Alfabeto: ',dfa_direct.alphabet)
#dfa_direct.visualize()
input()
print('----------------------------------------')

print('SIMULACION DFA DIRECTO')

#make the dfa pickle
with open('dfa', 'wb') as handle:
    pickle.dump(dfa_direct, handle, protocol=pickle.HIGHEST_PROTOCOL)

#create the scanner
header = reader.header
trailer = reader.trailer
scanner = GeneratingScanner(header,trailer)
scanner.build_scanner()
print('----------------------------------------')


a = input("Enter to continue...") #solo para la siguiente
print('----------------------------------------')