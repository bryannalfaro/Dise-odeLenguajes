#TODO
#Ascii
#Valores counter
#Epsilons
#Flujo al error
from expr_postfix import PostfixConverter

#initialize alphabet

expression = input("Enter an expression: ")
if expression == "":
    print("Error: empty expression")
    exit(1)

'''#for every expression in pruebas.txt print the postfix expression
with open('pruebas.txt') as f:
    for expression in f:
        print(expression)
        expression_postfix = PostfixConverter(expression)
        expression_postfix.build_Alphabet()
        expression_postfix.convertToPostfix()'''

expression_postfix = PostfixConverter(expression)
expression_postfix.build_Alphabet()
postfix = expression_postfix.convertToPostfix() #Get postfix
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
