from time import sleep
from production import Production
from state_definition import State
from automata.automata import Automata

class AutomataLR(Automata):
    def __init__(self, states, alphabet, transitions, initial, finals, tokens_list=None):
        super().__init__(states, alphabet, transitions, initial, finals)
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.ignored_tokens = []
        self.initial = initial
        self.finals = finals
        self.tokens_list = tokens_list
        self.identified_tokens = []
        self.goto = {}
        self.action = {}
        self.stack = []
        self.productions = {}

    def simulate(self,tokens):
        words = tokens
        print('\n')
        print('WORDS\n',words)
        words.append('$')
        #reverse the list
        words.reverse()
        #print(self.action)
        #print(self.productions)

        #Append the first state to the stack
        self.stack.append(self.initial)
        a = words.pop()
        while(True):
            #check the action
            #print('STACK',self.stack)
            #print('WORD',a)
            if a in self.ignored_tokens:
                a = words.pop()
                continue
            print('ACTION',self.action[self.stack[-1]][a])
            if (self.action[self.stack[-1]][a]) !=None:
                if (self.action[self.stack[-1]][a])[0] == 's':
                    #push the state to the stack
                    #search the state
                    for state in self.states:
                        if state.name == (self.action[self.stack[-1]][a])[1:]:
                            self.stack.append(state)
                            break

                    #get the next word
                    a = words.pop()
                elif (self.action[self.stack[-1]][a])[0] == 'r':
                    #get the production
                    #print('NUMBE',int((self.action[self.stack[-1]][a])[1:]))
                    production = self.productions[int((self.action[self.stack[-1]][a])[1:])]
                    #get the number of elements to pop
                    print('PRODUCTION',production.left,'-->',production.right)
                    number_pop = len(production.get_separated_right())
                    #pop the elements
                    for i in range(number_pop):
                        self.stack.pop()
                    #push the goto
                    self.stack.append(self.goto[self.stack[-1]][production.left])
                    #append the production to the identified tokens
                    self.identified_tokens.append(production)
                elif self.action[self.stack[-1]][a] == 'accept':
                    print('ACCEPTED')
                    break
            else:
                print(f'ERROR SINTACTICO there is no intersection between {self.stack[-1]} and {a}')
                exit()
                break