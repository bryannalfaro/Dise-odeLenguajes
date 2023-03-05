from automata.automata import Automata
from Symbol import Symbol
import copy
from state_definition import State

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
        new_arr = []

        for i in range(0, len(partition2)): #recorro los grupos de la particion
            if len(partition2[i])>1: #No hay solo un estado en el grupo
                for state in partition2[i]: #recorro los estados del grupo
                    #vaciar temporal cuando se cambia de simbolo
                    for symbol in self.alphabet:
                        if symbol!=Symbol('#').name or symbol!=Symbol('ε').name:
                           #Hacer movimiento para verificar el grupo al que se mueve
                            move_state = self.move(state,symbol)
                            #Si no tiene transicion se agrega un estado muerto
                            if move_state==None:
                                #print('HERE NONEEE',state)
                                if state in temporal:
                                    temporal[state].update({symbol:[1000]})
                                else:
                                    temporal[state] = {symbol:[1000]}
                            else:
                                for iu in range(0, len(partition2)): #Se verifica a que grupo va
                                    #print('HEE',move_state,partition2[i],symbol)
                                    #print('PARTITION2',partition2[iu])
                                    if move_state in partition2[iu]:
                                            #print('here',state)
                                            #make dictionary state and symbol
                                            if state in temporal:
                                                temporal[state].update({symbol:partition2[iu]})
                                            else:
                                                temporal[state] = {symbol:partition2[iu]}
                                            #print('temporal2',temporal)
                                            break

                                    #print('temporal2',temporal)
                #print('temporal',temporal)
                #print('ajaj',i)
                flipped = {}
                ignored = []
                #Por cada simbolo se verifica si hay un cambio de grupo, se arma un diccionario
                #de la forma grupo: [estados] para [estados] sean un nuevo grupo
                for symbol in range(0, len(self.alphabet)):
                    if self.alphabet[symbol]!=Symbol('#').name or self.alphabet[symbol]!=Symbol('ε').name:
                        flipped = {}
                        for key, value in temporal.items():
                            if key not in ignored:
                                if self.alphabet[symbol] in value:
                                    #print('je',value,value[self.alphabet[symbol]])
                                    if tuple(value[self.alphabet[symbol]]) not in flipped and tuple(value[self.alphabet[symbol]])!=[]:
                                        if len(flipped)==0:
                                            flipped[tuple(value[self.alphabet[symbol]])] = [key]
                                        else:
                                            flipped[tuple(value[self.alphabet[symbol]])] = [key]
                                            ignored.append(key)

                                    else:

                                        flipped[tuple(value[self.alphabet[symbol]])].append(key)

                                else:
                                    #print('KEYEYYYY',key)
                                    ignored.append(key)
                        #print("internal",flipped,ignored)
                        if ignored!=[]:
                            #print('breaak')
                            break

                for key,value in flipped.items():
                    new_arr.append(value)

                temporal = {}
            else:
                #Si solo es un estado, se apendea al new_arr
                new_arr.append(partition2[i])

        #print('NEWWW',new_arr)
        #delete empty groups
        for i in range(0, len(new_arr)):
            if len(new_arr[i])==0:
                new_arr.pop(i)
                break

        return new_arr

    #Minimization of DFA
    def minimize(self):
        #Divide the states into two groups, final and non-final
        final_states = self.finals
        non_final_states = list(set(self.states) - set(final_states))
        new_states = []
        #print("Final states: ", final_states)
        #print("Non-final states: ", non_final_states)

        #Iterate the partition
        partition = [non_final_states, final_states]
        new_partition = []
        #print("Initial partition: ", partition)
        new_partition = copy.copy(partition)
        while True:
                new_partition2 = self.make_pi_new(new_partition)
                #print('new_partition2 RESULTAT',new_partition2)
                if new_partition2 == partition:
                     break
                else:
                    new_partition = new_partition2
                    partition = new_partition2

        print(new_partition2)
        #build the new DFA
        for i in range(0, len(new_partition2)):
            #print('I',self.initial)
            if self.initial in new_partition2[i]:
                #Create a state
                initial = State(True,False)
                initial.list = new_partition2[i]
                new_states.append(initial)

        #check finals
        for i in range(0, len(new_partition2)):
            for j in range(0, len(self.finals)):
                #print('WORKINGGG',self.finals[j],'INITIAL',self.initial,new_partition2[i])
                if self.finals[j] in new_partition2[i] and self.initial == self.finals[j]:
                     #put the initial state as final
                    new_states[0].is_final = True
                    #print('NEW111',new_states[0].is_final,new_states[0].is_initial)
                    break
                elif self.finals[j] in new_partition2[i]:
                    #print('YESSSS')
                   #Create final state
                    final = State(False,True)
                    final.list = new_partition2[i]
                    new_states.append(final)
                    break
                else:
                    pass



        #print('NEW',new_states)
        n = copy.copy(new_states)

        for i in range(0, len(new_partition2)):
            #check the list of new states if they are already
            for j in range(0, len(new_states)):
                #print('NJ',new_partition2[i],new_states[j].list)
                if new_partition2[i] == new_states[j].list:
                    #print('here')
                    break

                elif j == len(new_states)-1:
                    #print('here2')
                    new_state = State(False,False)
                    new_state.list = new_partition2[i]
                    new_states.append(new_state)
                    break

        #print('new_states',new_states)
        #check the finals in new_states
        new_finals = []
        for i in range(0, len(new_states)):
            if new_states[i].is_final:
                new_finals.append(new_states[i])

        #print('new_finals',new_finals)


        #make transitions
        new_transitions = dict()
        for i in range(0, len(new_states)):
            for symbol in self.alphabet:
                if symbol!=Symbol('#').name and symbol!=Symbol('ε').name:
                    #print('ENTREEE',Symbol('ε').name,symbol)
                    move = self.move((new_states[i].list)[0],symbol)
                    #print('MOVE',move)
                    if move!=None:
                        for j in range(0, len(new_states)):
                            if move in new_states[j].list:
                                if new_states[i] in new_transitions:
                                    new_transitions[new_states[i]].update({symbol:[new_states[j]]})
                                else:
                                    new_transitions[new_states[i]] = {symbol:[new_states[j]]}
                                break

        #print('new_transitions',new_transitions)
        #make the new DFA
        new_dfa = DFA_automata(new_states, self.alphabet, [new_transitions], new_states[0], new_finals)
        return new_dfa