from graphviz import Digraph
class Automata():
    def __init__(self, states, alphabet, transitions, initial, finals):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial = initial
        self.finals = finals

    #visualize the automata with graphviz
    def visualize(self):
        graph_dot = Digraph('automata1',format='pdf')
        for state in self.states:
            if state.is_initial:
                graph_dot.node(state.name, state.name, shape='circle')
            elif state.is_final:
                graph_dot.node(state.name, state.name, shape='doublecircle')

        for transition in self.transitions:
            #print(self.transitions[transition])
            for symbol in self.transitions[transition]:
                #print(self.transitions[transition][symbol])
                for transition_final in self.transitions[transition][symbol]:
                    #print(transition_final)
                    graph_dot.edge(transition.__str__(),transition_final.__str__(),label=str(symbol))

        graph_dot.render(directory='test-output', view=True)