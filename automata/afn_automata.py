from automata.automata import Automata
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


