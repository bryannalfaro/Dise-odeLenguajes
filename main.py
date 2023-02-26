from expr_postfix import PostfixConverter

validate =False
while validate == False:

    expression = input("Enter an expression: ")
    if expression == "":
        print("Error: empty expression")
    else:
        expression_postfix = PostfixConverter(expression) #Se inicia la instancia de Postfix
        expression_postfix.build_Alphabet()
        postfix,validate= expression_postfix.convertToPostfix(validate) #Obtener el postfix y validacion

print('Postfix: ',postfix)
node_root = expression_postfix.make_nodes(postfix)#Hacer el arbol y obtener el nodo raiz

nodes_postorder = node_root.make_postorder() #Se recorre el arbol en postorder
afn = node_root.make_automata(nodes_postorder) #Se crea el automata


print('Estados :',afn.states)
print('Transiciones: ',afn.transitions)
print('Estado inicial: ',afn.initial)
print('Estado final: ',afn.finals)
print('Alfabeto: ',afn.alphabet)
afn.visualize()
