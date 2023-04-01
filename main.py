from expr_postfix import PostfixConverter
from state_definition import State
from automata.tree import Tree
from reader import Reader
#initialize alphabet
validate =False
State.counter = 0

#read file
reader = Reader('slr-2.yal')
reader.read_file()
expression = reader.get_tokens_expression()
'''for key in reader.definitions:
    #evaluate if it is not the last one
    if key != list(reader.definitions.keys())[-1]:
        expression += reader.definitions[key] + '|'
    else:
        expression += reader.definitions[key]'''

print('EXPRESSION: ',expression)
input()
while validate == False:

        expression_postfix = PostfixConverter(expression)
        expression_postfix.build_Alphabet()
        postfix,validate= expression_postfix.convertToPostfix(validate) #Get postfix


'''#for every expression in pruebas.txt print the postfix expression
with open('pruebas.txt') as f:
    for expression in f:
        print(expression)
        expression_postfix = PostfixConverter(expression)
        expression_postfix.build_Alphabet()
        expression_postfix.convertToPostfix()'''

#POSTFIX Y AFN
print('POSTFIX Y AFN')
print('Postfix: ',postfix)
node_root = expression_postfix.make_nodes(postfix)#nodo root

#visualize tree
tree = Tree(node_root)
tree.dot.render('tree.gv', view=True)

#a = input("Enter to continue...") #solo para la siguiente


'''nodes_postorder = node_root.make_postorder()
for node in nodes_postorder:
    print('NODE',node.value)
afn = node_root.make_automata(nodes_postorder)


print('Estados :',afn.states)
print('Transiciones: ',afn.transitions)
print('Estado inicial: ',afn.initial)
print('Estado final: ',afn.finals)
print('Alfabeto: ',afn.alphabet)
afn.visualize()
a = input()
print('----------------------------------------')
print('SIMULACION AFN')
flag_sim = True
while flag_sim:
    afn_word = input("Enter a word: ")
    print('SIMULATION AFN SAYS: ',afn.simulate_nfa(afn_word))

    answer= input("Do you want to simulate another word? (y/f): ")
    if answer == 'f':
        flag_sim = False
print('----------------------------------------')
print('AFN TO DFA WITH SUBSETS')
dfa = afn.make_dfa()
print('Estados :',dfa.states)
print('Transiciones: ',dfa.transitions)
print('Estado inicial: ',dfa.initial)
print('Estado final: ',dfa.finals)
print('Alfabeto: ',dfa.alphabet)
dfa.visualize()
a=input()
print('----------------------------------------')
print('MINIMIZACION DFA SUBSETS')
minimized_dfa = dfa.minimize(dfa.states)

print('Estados: ',minimized_dfa.states)
print('Transiciones: ',minimized_dfa.transitions)
print("Estado inicial: ",minimized_dfa.initial)
print('Estado final: ',minimized_dfa.finals)
print('Alfabeto: ',minimized_dfa.alphabet)

minimized_dfa.visualize()

#print('Estados minimizados :',minimized_dfa)
#a = len(minimized_dfa)
print('----------------------------------------')
input()

print('SIMULACION DFA SUBSETS')
flag_sim = True
while flag_sim:
    dfa_word = input("Enter a word: ")
    print('SIMULATION DFA SAYS: ',dfa.simulate_dfa(dfa_word))

    answer= input("Do you want to simulate another word? (y/f): ")
    if answer == 'f':
        flag_sim = False
print('----------------------------------------')


a = input("Enter to continue...") #solo para la siguiente
print('----------------------------------------')

print('SIMULACION DFA MINIMO')
flag_sim = True
while flag_sim:
    dfa_word = input("Enter a word: ")
    print('SIMULATION MIN DFA SAYS: ',minimized_dfa.simulate_dfa(dfa_word))

    answer= input("Do you want to simulate another word? (y/f): ")
    if answer == 'f':
        flag_sim = False
print('----------------------------------------')'''


a = input("Enter to continue...") #solo para la siguiente
print('----------------------------------------')

print('DFA DIRECT')

#direct dfa
expression_postfix = PostfixConverter(expression,"#") #Se aumenta la expresion

postfix,validate= expression_postfix.convertToPostfix(validate)
alfabeto = expression_postfix.build_Alphabet()
#print('ALF',alfabeto.getAlphabetNames())

#print('Postfix: ',postfix)
node_root = expression_postfix.make_nodes(postfix)#nodo root
#print(node_root.value)
postorder_labeled= node_root.label_leafs() #se enumeran las hojas

node_root.make_rules(postorder_labeled) #se hacen las reglas

#print(node_root.follow)
dfa_direct = node_root.make_dfa_direct(alfabeto.getAlphabetNames())
print('Estados :',dfa_direct.states)
print('Transiciones: ',dfa_direct.transitions)
print('Estado inicial: ',dfa_direct.initial)
print('Estado final: ',dfa_direct.finals)
print('Alfabeto: ',dfa_direct.alphabet)
dfa_direct.visualize()
input()
print('----------------------------------------')

print('SIMULACION DFA DIRECTO')
flag_sim = True
while flag_sim:
    dfa_word = input("Enter a word: ")
    print('SIMULATION DIRECT DFA SAYS: ',dfa_direct.simulate_dfa(dfa_word))

    answer= input("Do you want to simulate another word? (y/f): ")
    if answer == 'f':
        flag_sim = False
print('----------------------------------------')


a = input("Enter to continue...") #solo para la siguiente
print('----------------------------------------')

#print state.list
'''for state in dfa_direct.states:
    print(state,state.list)'''
#dfa_direct.visualize()


'''for node in postorder_labeled:
    #print null
    print(node.value,node.null_node,node.firstpos,node.lastpos,node.follow)
'''

print('----------------------------------------')
#minimal DFA
print('MINIMAL DFA DIRECT')
minimized_direct = dfa_direct.minimize(dfa_direct.states)
print('Estados: ',minimized_direct.states)
print('Transiciones: ',minimized_direct.transitions)
print("Estado inicial: ",minimized_direct.initial)
print('Estado final: ',minimized_direct.finals)
print('Alfabeto: ',minimized_direct.alphabet)
#print('Estados minimizados :',minimized_direct)
#b = len(minimized_direct)

#print(a==b)
minimized_direct.visualize()
print('----------------------------------------')

print('----------------------------------------')

print('SIMULACION DFA MINIMO DIRECTO')
flag_sim = True
while flag_sim:
    dfa_word = input("Enter a word: ")
    print('SIMULATION MIN DFA  DIRECT SAYS: ',minimized_direct.simulate_dfa(dfa_word))

    answer= input("Do you want to simulate another word? (y/f): ")
    if answer == 'f':
        flag_sim = False
print('----------------------------------------')


a = input("Enter to continue...") #solo para la siguiente
print('----------------------------------------')