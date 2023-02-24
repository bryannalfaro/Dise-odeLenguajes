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

'''flag_sim = True
while flag_sim:
    afn_word = input("Enter a word: ")
    print('SIMULATION AFN SAYS: ',afn.simulate_nfa(afn_word))

    answer= input("Do you want to simulate another word? (y/f): ")
    if answer == 'f':
        flag_sim = False'''

dfa = afn.make_dfa()
print('Estados :',dfa.states)
print('Transiciones: ',dfa.transitions)
print('Estado inicial: ',dfa.initial)
print('Estado final: ',dfa.finals)
print('Alfabeto: ',dfa.alphabet)
#dfa.visualize()


#direct dfa
expression_postfix = PostfixConverter(expression,"#")
alfabeto = expression_postfix.build_Alphabet()
print('ALF',alfabeto)
postfix,validate= expression_postfix.convertToPostfix(validate)

print('Postfix: ',postfix)
node_root = expression_postfix.make_nodes(postfix)#nodo root
print(node_root.value)
postorder_labeled= node_root.label_leafs()

node_root.make_rules(postorder_labeled)

print(node_root.follow)
dfa = node_root.make_dfa_direct(alfabeto.getAlphabetNames())
print('Estados :',dfa.states)
print('Transiciones: ',dfa.transitions)
print('Estado inicial: ',dfa.initial)
print('Estado final: ',dfa.finals)
print('Alfabeto: ',dfa.alphabet)

#print state.list
for state in dfa.states:
    print(state,state.list)
dfa.visualize()


for node in postorder_labeled:
    #print null
    print(node.value,node.null_node,node.firstpos,node.lastpos,node.follow)


