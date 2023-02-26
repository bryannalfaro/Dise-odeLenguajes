#Node for the automata
from state_definition import State
from automata.afn_automata import AFN_automata
from alphabet_definition import AlphabetDefinition
from operators import *
from Symbol import Symbol

class Node():
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.automata = []
        self.symbols = AlphabetDefinition().getSymbolDictionary()

    def make_alphabetic_automata(self,node):
        #Hacer automata para el simbolo alfabético
        state1 = State(True,False)
        state2 = State(False,True)
        transition = dict()
        automata = AFN_automata([state1,state2],[Symbol(node.value).name],[transition],state1,state2)

        automata.make_movement(Symbol(node.value).name, state1, state2)

        return automata

    def make_or_automata(self,a1,a2):
        #Hacer automata para el simbolo |
        state1 = State(True,False)
        state2 = State(False,True)
        epsilon = Symbol('ε').name
        automatas = [a1,a2]
        transition = dict()
        automata = AFN_automata([state1,state2],[],[transition],state1,state2)

        automata.make_movement(epsilon,state1, a1.initial) #transicion epsilon del estado inicial al estado inicial del automata 1
        a1.make_movement(epsilon,a1.finals, state2) #transicion epsilon del estado final del automata 1 al estado final

        automata.make_movement(epsilon,state1, a2.initial) #transicion epsilon del estado inicial al estado inicial del automata 2
        a2.make_movement(epsilon,a2.finals, state2) #transicion epsilon del estado final del automata 2 al estado final

        for i in range(len(automatas)):
            i = automatas[i]
            i.finals.is_final=False #el estado final del automata i ya no es final

            #add transition from automata i to the automata with symbol
            for j in i.transitions:
                transition_dict = i.transitions[j]
                for symbol in transition_dict:
                    symbol_dict = transition_dict[symbol]
                    for state in symbol_dict:
                        automata.make_movement(symbol,j, state)
        return automata

    def make_kleene_automata(self,a1):
        #Hacer automata para el simbolo *
        state1 = State(True,False)
        state2 = State(False,True)
        transition = dict()
        automata = AFN_automata([state1,state2],[],[transition],state1,state2)
        epsilon = Symbol('ε').name
        automata.make_movement(epsilon,state1, a1.initial) #transicion epsilon del estado inicial al estado inicial del automata 1
        automata.make_movement(epsilon,state1, state2) #transicion epsilon del estado inicial al estado final
        a1.make_movement(epsilon,a1.finals, state2) #transicion epsilon del estado final del automata 1 al estado final
        a1.make_movement(epsilon,a1.finals, a1.initial) #transicion epsilon del estado final del automata 1 al estado inicial del automata 1

        a1.finals.is_final=False #el estado final del automata ya no es final

        #add transition from automata i to the automata
        for j in a1.transitions:
            transition_dict = a1.transitions[j]
            for symbol in transition_dict:
                symbol_dict = transition_dict[symbol]
                for state in symbol_dict:
                    automata.make_movement(symbol,j, state)
        return automata

    def make_concatenation_automata(self,a2,a1):
        #Hacer automata para el simbolo .
        automatas = [a1,a2]
        state1 = a1.initial
        state2 = a2.finals
        transition = dict()
        automata = AFN_automata([state1,state2],[],[transition],state1,state2)

        state_join = None
        #add transition from automata i to the automata
        for iterator in range(len(automatas)):
            if iterator == 0:
                state_join = a1.finals #guardar el estado final del automata 1
                a1.finals.is_final=False #el estado final del automata 1 ya no es final
                state_join.is_final=False #el estado final del automata 1 ya no es final
            i = automatas[iterator]
            states_count = 0 #contador para saber si es el primer estado
            for j in i.transitions:
                transition_dict = i.transitions[j]
                for symbol in transition_dict:
                    symbol_dict = transition_dict[symbol]
                    for state in symbol_dict:
                        if iterator==1 and states_count==0:
                            automata.make_movement(symbol,state_join, state) #Se hace la union
                        else:
                            automata.make_movement(symbol,j, state) #Se arman las demas transiciones
                    states_count+=1
        return automata


    #Postorder traversal
    def make_postorder(self):
        #Arreglo para guardar el recorrido
        postorder = []
        if self.left:
            postorder = self.left.make_postorder()
        if self.right:
            postorder = postorder + self.right.make_postorder()
        postorder.append(self)
        return postorder

    #Leer cada nodo y armar el automata con Thompson
    def make_automata(self,nodes_postorder):
        for i in range(len(nodes_postorder)):
            i = nodes_postorder[i]
            #Verificar si es un simbolo del alfabeto
            if i.value not in self.symbols:
                self.automata.append(self.make_alphabetic_automata(i))
            if i.value == Union().symbol:
                automata1 = self.automata.pop()
                automata2 = self.automata.pop()

                self.automata.append(self.make_or_automata(automata1,automata2))
            if i.value == KleeneStar().symbol:

                automata1 = self.automata.pop()
                self.automata.append(self.make_kleene_automata(automata1))
            if i.value == Concatenation().symbol:

                automata1 = self.automata.pop()
                automata2 = self.automata.pop()
                self.automata.append(self.make_concatenation_automata(automata1,automata2))
        return self.automata.pop()



