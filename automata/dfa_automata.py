from automata.automata import Automata
from Symbol import Symbol
import copy
class DFA_automata(Automata):
    def __init__(self, states, alphabet, transitions, initial, finals):
        super().__init__(states, alphabet, transitions, initial, finals)
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions[0]
        self.initial = initial
        self.finals = finals


    def move(self, state, symbol):
        if state in self.transitions:
            if symbol in self.transitions[state]:
                 return self.transitions[state][symbol][0]
            else:
                return None
        else:
            return None
    def simulate_dfa(self,word):
        s0 = self.initial

        for symbol in word:
            s0 = self.move(s0, symbol)

        if s0 in self.finals:
            return True
        else:
            return False


    def make_pi_new(self,partition2):
        temporal = {}
        #print('partition2',partition2)
        for i in range(0, len(partition2)):
            #print('1i',i,partition2[i])
            if len(partition2[i])>1:
                for state in partition2[i]:
                    #vaciar temporal cuando se cambia de simbolo
                    for symbol in self.alphabet:
                        if symbol!=Symbol('#').name and symbol!=Symbol('ε').name:
                            #If the move of a state is in the same group
                            move_state = self.move(state,symbol)
                            for iu in range(0, len(partition2)):
                                #print('HEE',move_state,partition2[i],symbol)
                                if move_state in partition2[iu]:
                                        #print('here',state)
                                        #make dictionary state and symbol
                                        if state in temporal:
                                            temporal[state].update({symbol:partition2[iu]})
                                        else:
                                            temporal[state] = {symbol:partition2[iu]}
                                        #print('temporal2',temporal)
                #print('temporal',temporal)
                #print('ajaj',i)
                flipped = {}
                ignored = []
                for symbol in range(0, len(self.alphabet)):
                    if self.alphabet[symbol]!=Symbol('#').name and self.alphabet[symbol]!=Symbol('ε').name:
                        #agrupar por esa letra
                        flipped = {}
                        for key, value in temporal.items():
                            if key not in ignored:
                                if self.alphabet[symbol] in value:
                                    #print('je',value,value[self.alphabet[symbol]])
                                    if tuple(value[self.alphabet[symbol]]) not in flipped:
                                        if len(flipped)==0:
                                            flipped[tuple(value[self.alphabet[symbol]])] = [key]
                                        else:
                                            flipped[tuple(value[self.alphabet[symbol]])] = [key]
                                            ignored.append(key)

                                    else:
                                        flipped[tuple(value[self.alphabet[symbol]])].append(key)
                        #print("internal",flipped,ignored)

                #partition with ignored states
                #print('i',i)
                #print('HEEEEJFALKS',partition2[i],state)
                for state in ignored:
                    partition2[i].remove(state)
                    partition2.append([state])
                #print('partition2 YAAA',partition2)

                temporal = {}
            #print('partition2',partition2)

        return partition2

    #Minimization of DFA
    def minimize(self):
        #Divide the states into two groups, final and non-final
        final_states = self.finals
        non_final_states = list(set(self.states) - set(final_states))
        print("Final states: ", final_states)
        print("Non-final states: ", non_final_states)

        #Iterate the partition
        partition = [non_final_states, final_states]
        new_partition = []
        print("Initial partition: ", partition)
        new_partition = copy.copy(partition)
        while True:
                new_partition2 = self.make_pi_new(new_partition)
                print('new_partition2 RESULTAT',new_partition2)
                if new_partition2 == partition:
                     break
                else:
                    new_partition = new_partition2
                    partition = new_partition2
