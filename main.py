#TODO
#bug con epsilon , preguntar cambio en visualize y node_automata
from expr_postfix import PostfixConverter

#initialize alphabet
validate =False
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
afn.visualize()

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

print('----------------------------------------')
print('SIMULACION DFA')
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
dfa = node_root.make_dfa_direct(alfabeto.getAlphabetNames())
print('Estados :',dfa.states)
print('Transiciones: ',dfa.transitions)
print('Estado inicial: ',dfa.initial)
print('Estado final: ',dfa.finals)
print('Alfabeto: ',dfa.alphabet)
dfa.visualize()

#print state.list
'''for state in dfa.states:
    print(state,state.list)'''
#dfa.visualize()


'''for node in postorder_labeled:
    #print null
    print(node.value,node.null_node,node.firstpos,node.lastpos,node.follow)
'''

