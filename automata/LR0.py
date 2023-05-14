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
        self.initial = initial
        self.finals = finals
        self.tokens_list = tokens_list
        self.identified_tokens = []