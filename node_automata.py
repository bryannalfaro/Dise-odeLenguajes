#Node for the automata
from state_definition import State
from afn_automata import AFN_automata
from alphabet_definition import AlphabetDefinition
from operators import *

class Node():
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.automata = []
        self.symbols = AlphabetDefinition().getSymbolDictionary()

    def make_alphabetic_automata(self,node):
        #make automata for an alphabet symbol
        state1 = State(True,False)
        state2 = State(False,True)
        transition = dict()
        automata = AFN_automata([state1,state2],node.value,[transition],state1,state2)

        automata.make_movement(node.value, state1, state2)

        return automata

    def make_or_automata(self,a1,a2):
        #make automata for or operator
        state1 = State(True,False)
        state2 = State(False,True)
        automatas = [a1,a2]
        transition = dict()
        automata = AFN_automata([state1,state2],[],[transition],state1,state2)

        automata.make_movement('e',state1, a1.initial)
        a1.make_movement('e',a1.finals, state2)

        automata.make_movement('e',state1, a2.initial)
        a2.make_movement('e',a2.finals, state2)

        for i in range(len(automatas)):
            i = automatas[i]
            i.finals.is_final=False

            #add transition from automata i to the automata

            for j in i.transitions:
                #print(j)
                transition_dict = i.transitions[j]
                #print(type(j))
                for symbol in transition_dict:
                    #print(symbol)
                    symbol_dict = transition_dict[symbol]
                    for state in symbol_dict:
                        #print(state)
                        #print(j)
                        #print(symbol)
                        automata.make_movement(symbol,j, state)
        return automata

    def make_kleene_automata(self,a1):
        #make automata for kleene star operator
        state1 = State(True,False)
        state2 = State(False,True)
        transition = dict()
        automata = AFN_automata([state1,state2],[],[transition],state1,state2)

        automata.make_movement('e',state1, a1.initial)
        automata.make_movement('e',state1, state2)
        a1.make_movement('e',a1.finals, state2)
        a1.make_movement('e',a1.finals, a1.initial)

        a1.finals.is_final=False

        #add transition from automata i to the automata
        for j in a1.transitions:
            transition_dict = a1.transitions[j]
            for symbol in transition_dict:
                symbol_dict = transition_dict[symbol]
                for state in symbol_dict:
                    automata.make_movement(symbol,j, state)
        return automata

    def make_concatenation_automata(self,a2,a1):
        #make automata for concatenation operator
        automatas = [a1,a2]
        state1 = a1.initial
        state2 = a2.finals
        transition = dict()
        automata = AFN_automata([state1,state2],[],[transition],state1,state2)

        state_join = None
        #add transition from automata i to the automata
        for iterator in range(len(automatas)):
            if iterator == 0:
                state_join = a1.finals
                a1.finals.is_final=False
                state_join.is_final=False
            i = automatas[iterator]
            #print(i.transitions)
            states_count = 0
            for j in i.transitions:

                transition_dict = i.transitions[j]
                for symbol in transition_dict:

                    symbol_dict = transition_dict[symbol]

                    for state in symbol_dict:
                        #print(iterator,states_count)
                        if iterator==1 and states_count==0:
                            automata.make_movement(symbol,state_join, state)
                        else:
                            automata.make_movement(symbol,j, state)
                    states_count+=1
        return automata


    #Postorder traversal
    def make_postorder(self):
        #make postorder and save it in array
        postorder = []
        if self.left:
            postorder = self.left.make_postorder()
        if self.right:
            postorder = postorder + self.right.make_postorder()
        postorder.append(self)
        return postorder

    #Read each node
    def make_automata(self,nodes_postorder):
        for i in range(len(nodes_postorder)):
            i = nodes_postorder[i]
            #check if it is an alphabet symbol
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



