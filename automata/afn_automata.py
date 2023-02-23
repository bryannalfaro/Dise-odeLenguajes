from automata.automata import Automata
from Symbol import Symbol
class AFN_automata(Automata):
    def __init__(self, states, alphabet, transitions, initial, finals):
        super().__init__(states, alphabet, transitions, initial, finals)
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions[0]
        self.initial = initial
        self.finals = finals

    #Se realiza la creacion de las transiciones
    def make_movement(self, symbol, state1, state2):
        #Verificar que el simbolo este en el alfabeto si no esta se agrega
        if symbol not in self.alphabet:
            self.alphabet.append(symbol)
        #Verificar los estados
        if state1 not in self.states:
            self.states.append(state1)

        if state2 not in self.states:
            self.states.append(state2)
        #verificar que el primer estado este en el diccionario
        if state1 in self.transitions:
            #verificar que el simbolo este en el diccionario
            if symbol in self.transitions[state1]:
                #agregar el segundo estado al diccionario
                self.transitions[state1][symbol].append(state2)
            else:
                #agregar el simbolo al diccionario
                self.transitions[state1][symbol] = [state2]
        else:
            #agregar el primer estado al diccionario
            self.transitions[state1] = {symbol:[state2]}
        #print(self.transitions)


    #se construye los subconjuntos para DFA
    def make_dfa(self):
        d_states = []
        self.epsilon_closure(self.initial)

    def verify_epsilon_transition(self, state):
        movements_epsilon = []
        for transition in self.transitions:
            if state == transition:
                for symbol in self.transitions[state]:
                    if symbol == Symbol('ε').ascii_repr:
                        for transition_final in self.transitions[state][symbol]:
                            movements_epsilon.append(transition_final)

        return movements_epsilon

    def epsilon_closure(self, state):
        #make an stak to store the states
        stack = []
        e_closure = []
        for i in set([state]):
            stack.append(i)
            #initialize the e_closure with the state
            e_closure.append(i)

        while len(stack) > 0:
            t = stack.pop()
            for u in self.verify_epsilon_transition(t):
                if u not in e_closure:
                    e_closure.append(u)
                    stack.append(u)

        print(e_closure)



