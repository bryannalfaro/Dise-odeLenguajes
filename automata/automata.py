from graphviz import Digraph
class Automata():
    def __init__(self, states=None, alphabet=None, transitions=None, initial=None, finals=None):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial = initial
        self.finals = finals

    #visualize the automata with graphviz
    def visualize(self):
        graph_dot = Digraph('automata1',format='pdf')
        graph_dot.attr(rankdir='LR')
        for state in self.states:
            if state.is_initial and state.is_final==False: #CORRECCION EPSILON
                graph_dot.node(state.name, state.name, shape='circle')
            elif state.is_final:
                graph_dot.node(state.name, state.name, shape='doublecircle')

        for transition in self.transitions:
            for symbol in self.transitions[transition]:

                for transition_final in self.transitions[transition][symbol]:
                    #print('trans',transition_final)
                    graph_dot.edge(transition.__str__(),transition_final.__str__(),label=str(symbol))

        graph_dot.render(directory='test-output',view=True)

    def visualization(self):
        graph_dot = Digraph('automata1',format='pdf', node_attr={'shape': 'record'})
        graph_dot.attr(rankdir='LR')
        print(len(self.states) )
        print(self.states)

        for state in self.states:
            counter = 0
            if state.is_initial==False and state.is_final==False:
                custom_label = ''
                custom_label = state.name + ' | '
                for i in state.list:
                    if i.is_closure:
                        #print('true')
                        custom_label += i.left+':'+i.right+'\\n'
                    else:
                        if counter == 0:
                            custom_label += '|'
                            counter += 1
                        #print('false')
                        custom_label += i.left+':'+i.right+'\\n'
                graph_dot.node(name= state.name,label = custom_label)
            elif state.is_final:
                custom_label = ''
                custom_label = state.name + ' | '
                for i in state.list:
                    if i.is_closure:
                        custom_label += i.left+':'+i.right+'\\n'
                    else:
                        if counter == 0:
                            custom_label += '|'
                            counter += 1
                        #print('false')
                        custom_label += i.left+':'+i.right+'\\n'
                graph_dot.node(name= state.name,label = custom_label, color='blue')
            else:
                custom_label = ''
                custom_label = state.name + ' | '
                for i in state.list:
                    if i.is_closure:
                        custom_label += i.left+':'+i.right+'\\n'
                    else:
                        if counter == 0:
                            custom_label += '|'
                            counter += 1
                        #print('false')
                        custom_label += i.left+':'+i.right+'\\n'
                graph_dot.node(name= state.name,label = custom_label)

        #print(  'transitions',self.transitions)
        for transition in self.transitions:
            for symbol in self.transitions[transition]:
                #print('symbol',symbol,self.transitions[transition][symbol],transition)

                graph_dot.edge(transition.__str__(),self.transitions[transition][symbol].__str__(),label=str(symbol))

        graph_dot.render(directory='test-output1',view=True)
