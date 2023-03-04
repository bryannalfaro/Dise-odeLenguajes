#TODO
#bug con epsilon , preguntar cambio en visualize y node_automata
#comprobar minimizacion con 2 dfas
#Como elegir el inicial de minimizacion%
#eliminar estados muertos?
from expr_postfix import PostfixConverter
from state_definition import State

#initialize alphabet
validate =False
State.counter = 0

while validate == False:

    expression = input("Enter an expression: ")
    if expression == "":
        print("Error: empty expression")
    else:
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


nodes_postorder = node_root.make_postorder()
afn = node_root.make_automata(nodes_postorder)


print('Estados :',afn.states)
print('Transiciones: ',afn.transitions)
print('Estado inicial: ',afn.initial)
print('Estado final: ',afn.finals)
print('Alfabeto: ',afn.alphabet)
#afn.visualize()
input()
'''print('----------------------------------------')
print('SIMULACION AFN')
flag_sim = True
while flag_sim:
    afn_word = input("Enter a word: ")
    print('SIMULATION AFN SAYS: ',afn.simulate_nfa(afn_word))

    answer= input("Do you want to simulate another word? (y/f): ")
    if answer == 'f':
        flag_sim = False
print('----------------------------------------')'''
print('AFN TO DFA WITH SUBSETS')
dfa = afn.make_dfa()
print('Estados :',dfa.states)
print('Transiciones: ',dfa.transitions)
print('Estado inicial: ',dfa.initial)
print('Estado final: ',dfa.finals)
print('Alfabeto: ',dfa.alphabet)
#dfa.visualize()
a = len(dfa.minimize())
input()

'''print('SIMULACION DFA')
flag_sim = True
while flag_sim:
    dfa_word = input("Enter a word: ")
    print('SIMULATION DFA SAYS: ',dfa.simulate_dfa(dfa_word))

    answer= input("Do you want to simulate another word? (y/f): ")
    if answer == 'f':
        flag_sim = False
print('----------------------------------------')


a = input("Enter to continue...") #solo para la siguiente
print('----------------------------------------')'''

print('DFA DIRECT')

#direct dfa
expression_postfix = PostfixConverter(expression,"#")

postfix,validate= expression_postfix.convertToPostfix(validate)
alfabeto = expression_postfix.build_Alphabet()
#print('ALF',alfabeto.getAlphabetNames())

#print('Postfix: ',postfix)
node_root = expression_postfix.make_nodes(postfix)#nodo root
#print(node_root.value)
postorder_labeled= node_root.label_leafs()

node_root.make_rules(postorder_labeled)

#print(node_root.follow)
dfa_direct = node_root.make_dfa_direct(alfabeto.getAlphabetNames())
print('Estados :',dfa_direct.states)
print('Transiciones: ',dfa_direct.transitions)
print('Estado inicial: ',dfa_direct.initial)
print('Estado final: ',dfa_direct.finals)
print('Alfabeto: ',dfa_direct.alphabet)
#dfa_direct.visualize()

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
print('MINIMAL DFA')
b = len(dfa_direct.minimize())

print(a==b)

print('----------------------------------------')