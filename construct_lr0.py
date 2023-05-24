from time import sleep
from Symbol import Symbol
from production import Production
from state_definition import State
from automata.LR0 import AutomataLR
from operators import *
from graphviz import Digraph
class ConstructLR():
    def __init__(self, productions,tokens,ignored_tokens):
        super().__init__()
        self.yalex_productions = productions
        self.ignored_tokens = ignored_tokens
        self.C_aut = None
        self.gramatical_elements = []
        self.expand_productions_without_dot = []
        self.production_indicate = None
        self.productions = []
        self.make_productions()
        self.expanded_productions = []
        self.already_evaluated = []
        self.expanded_productions_original = []
        self.expand_production()
        self.tokens = tokens
        self.actions_table = {}
        self.goto_table = {}


        self.J_results = []

    #make the productions
    def make_productions(self):
        for production in self.yalex_productions:
            left = production
            for right_item in self.yalex_productions[production]:
                right = right_item.strip()
                self.productions.append(Production(left,right))

        # #print every production with his left and right
        # for production in self.productions:
        #      print('PRODUCTION')
        #      print(production.left,'-->',production.right)

        #get the gramatical elements
        for production in self.productions:
            if production.left not in self.gramatical_elements:
                self.gramatical_elements.append(production.left)

            word = ''
            count = 0
            flag = False
            #iterate until find . and then save the word
            while count < len(production.right):
                if production.right[count] == ' ' and word != '':
                    #evaluate if word is not in the gramatical elements
                    if word not in self.gramatical_elements:
                        self.gramatical_elements.append(word)
                    word = ''
                else:
                    word += production.right[count]
                count += 1
            if word not in self.gramatical_elements:
                self.gramatical_elements.append(word)
        # print('GRAMATICAL ELEMENTS')
        # for i in self.gramatical_elements:
        #     print(i)


    #Function to add the dot and the augmented production
    def expand_production(self):
        #add the first production to expanded production
        self.expanded_productions.append(Production(self.productions[0].left+"'",self.productions[0].left))
        self.production_indicate = Production(self.productions[0].left+"'",self.productions[0].left)

        #add the rest of the productions to expanded productions
        for production in self.productions:
            self.expanded_productions.append(production)

        #save an independent copy
        for production in self.expanded_productions:
            self.expand_productions_without_dot.append(Production(production.left,production.right))


        for i in range(len(self.expanded_productions)):
            print('expanded',self.expanded_productions[i].left,'-->',self.expanded_productions[i].right)

        #add dot to the expanded productions
        for i in range(len(self.expanded_productions)):
            self.expanded_productions[i].right = '. '+self.expanded_productions[i].right

        # for i in self.expanded_productions:
        #      print('expanded',i.left,'-->',i.right)

        # for i in range(len(self.expand_productions_without_dot)):
        #     print('expanded copy',self.expand_productions_without_dot[i].left,'-->',self.expand_productions_without_dot[i].right)

    #Construct the closure for LR0 automata
    def closure(self, state):

        self.J_results = state #lista de objetos tipo Production
        #recorrer y encontrar el punto seguido de un no terminal
        change = True
        while change:
            append = False
            change = False

            for i in range(len(self.J_results)):
                    #iterate until find . and then save the word
                    word = ''
                    count = 0
                    flag = False
                    #iterate until find . and then save the word
                    while count < len(self.J_results[i].right):
                        if flag:
                            if self.J_results[i].right[count] == ' ':
                                flag = False
                            else:
                                word += self.J_results[i].right[count]
                        if self.J_results[i].right[count] == '.':
                            flag = True
                            if self.J_results[i].right[count+1] == ' ':
                                count += 1
                        count += 1
                    #print('WORD',word)

                    #search in productions where the left is the word
                    for production in self.expanded_productions:
                        if production.left == word:
                            #check if the production .left is not in the J_results left
                            for j in range(len(self.J_results)):
                                if production == self.J_results[j]:
                                    change = False
                                    break
                                else:
                                    change = True



                            if change:
                                self.J_results.append(production)
                                change = True
                                append = True #There is still elements to evaluate in the array
                            # else:
                            #     for i in range(len(self.J_results)):
                            #         if self.J_results[i].is_eval == False:
                            #             change = True
            if append:
                change = True

        #print('vines')
        # for i in self.J_results:
        #     print(i.left,'-->',i.right)
        #sleep(10)
        return self.J_results

    #function to move the dot
    def move_dot(self, right):
        array  = []
        #while to save workd and add to the array
        count = 0
        flag = False
        word = ''
        index_dot = None
        while count < len(right):
            if right[count] == ' ' and word != '':
                if word == '.':
                    index_dot = len(array)
                array.append(word)
                word = ''
            else:
                word += right[count]
            count += 1
        array.append(word)
        #switch the dot with the next element
        temp = array[index_dot]
        array[index_dot] = array[index_dot+1]
        array[index_dot+1] = temp
        #make the array a string
        string = ''
        for i in array:
            #add with space
            if i != '':
                string += i + ' '
            else:

                string += i
        #print('ARRAY',string)
        return string

    #function to handle the goto of lor0
    def goto(self, state, symbol):
        #make a list to store the productions
        goto_list = []
        #print('GOTO')
        index_dot = None
        #iterate over the state
        for production in state:
            #iterate until find . and then save the word
                word = ''
                count = 0
                flag = False
                #iterate until find . and then save the word
                while count < len(production.right):
                    if flag:
                        if production.right[count] == ' ':
                            flag = False
                        else:
                            word += production.right[count]
                    if production.right[count] == '.':
                        flag = True
                        if production.right[count+1] == ' ':
                            count += 1
                    count += 1
                #print('WORD',word)

                if word == symbol:
                    #print('here')
                    new= Production(production.left,self.move_dot(production.right))
                    new.is_closure = True
                    goto_list.append(new)

        #print('GOTO LIST before closure')
        # for i in goto_list:
        #     print(i.left,'-->',i.right)

        #make the closure of the goto_list
        goto_list = self.closure(goto_list)
        #print('GOTO LIST')
        # for i in goto_list:
        #     print(i.left,'-->',i.right)

        return goto_list

    def make_automata(self):
        initial_state = State(is_initial=True)
        initial_prod = self.expanded_productions[0]
        initial_prod.is_closure = True
        initial_state.list = self.closure([initial_prod])
        C_group = []
        transitions = {}
        #initialize empty transitions

        C_group.append(initial_state)
        change = True
        while change:
            change = False
            is_double = False
            for state in C_group:

                if state.evaluated == False:
                    state.evaluated = True
                    for symbol in self.gramatical_elements:
                        #print('Symbol ',symbol)
                        goto = self.goto(state.list,symbol)

                        if goto != None and goto != []:
                            #print('STATE 1 AND STATE 2',state.name,new_state.name,state.list,new_state.list)
                            #check if are the same
                            new_state = State()
                            new_state.list = goto
                            new_state.convert_list_to_array()
                            for i in C_group:
                                if i.array == new_state.array:
                                    new_state = i
                                    #print('SAME')
                                    is_double = True
                            if is_double == False:
                                C_group.append(new_state)
                                #add the transition
                                if state not in transitions:
                                    transitions[state] = {}
                                transitions[state][symbol] = new_state
                                change = True
                            else:
                                #add the transition to itself
                                if state not in transitions:
                                    transitions[state] = {}
                                transitions[state][symbol] = new_state
                                is_double = False
                                change = True

                        else:
                            pass

        #print(len(C_group))
        #make the final states those who has the expanded production
        for state in C_group:
            for production in state.list:

                if production.left == self.production_indicate.left:
                    if production.right.strip() == self.production_indicate.right+' .':
                        state.is_final = True
                        print('FINAL STATE',state.name)
        self.C_aut = C_group
        #make the automata
        automata = AutomataLR(C_group,self.gramatical_elements,transitions,initial_state,[state for state in C_group if state.is_final])
        automata.tokens_list = self.tokens
        automata.productions = self.expand_productions_without_dot
        automata.ignored_tokens = self.ignored_tokens
        return automata


    def first(self,symbol):
        #add the last epsilon
        #print('FIRST',symbol)
        first = []
        flag = False
        #check if the symbol is a terminal
        if symbol in self.tokens and symbol not in first:
            first.append(symbol)
        else:
            #print('NOT TERMINAL')
            for production in self.expand_productions_without_dot:
                if production.left == symbol:
                    arr = self.divide_production(production.right)
                    for j in range(len(arr)):

                        if arr[j] == Epsilon().symbol:
                            first.append(Epsilon().symbol)
                            break
                        elif arr[j] == symbol:
                            break
                        else:
                            first_arr = self.first(arr[j])
                            for i in first_arr:
                                if i == Symbol('ε').name:
                                    first_arr.remove(i)
                                    flag = True
                            if flag == False:
                                first+=first_arr
                                break
                            else:
                                first+=first_arr
        return list(set(first))

    def follow(self,symbol):
        follow = []
        #print(symbol, self.already_evaluated)

        #print(self.production_indicate.left)
        if symbol == self.production_indicate.left: #if is the initial symbol
            #print("ENTRE",symbol)
            follow.append(Symbol('$').name)
            self.already_evaluated.append(self.production_indicate.left)
        for production in self.expand_productions_without_dot:
            arr = self.divide_production(production.right)
            for i in range(len(arr)):
                #print('ARR',arr[i])
                if arr[i] == symbol:
                    self.already_evaluated.append(symbol)
                    if i == len(arr)-1: #if is the last symbol
                        if production.left != symbol:
                            #print('PROD LEFT FOLLOW',production.left)
                            if production.left not in self.already_evaluated:
                                follow += self.follow(production.left)
                                self.already_evaluated.append(production.left)
                            else:
                                break

                            #print('FOLLOW',follow)
                    else: #make first of the next symbol
                        #print('HERE')
                        first_arr = self.first(arr[i+1])
                        #print('FIRST',first_arr)
                        for j in first_arr:
                            if j == Symbol('ε').name: #if epsilon is in the first
                                first_arr.remove(j)
                                if production.left not in self.already_evaluated:
                                    follow += self.follow(production.left)
                                    self.already_evaluated.append(production.left)
                                else:
                                    break
                        follow += first_arr
                        #print('FOLLOW 2',follow)

        self.already_evaluated = []
        return list(set(follow))

    def divide_production(self,production):
        prod_array = []

        temp = ''
        for i in range(len(production)):
            if production[i] == ' ':
                prod_array.append(temp)
                temp = ''
            else:
                temp += production[i]
        prod_array.append(temp)

        return prod_array

    def make_table(self,automata):
        # print(automata.states)
        # print(automata.alphabet)
        # print(automata.tokens_list)
        # print(automata.identified_tokens)
        # print(automata.transitions)
        # print(automata.initial)
        # print(automata.finals)
        print("TABLE")
        for state in automata.states:
            self.actions_table[state] = {}
            self.goto_table[state] = {}

        #print(self.goto_table)


        #fill goto
        for state in automata.states:
            for symbol in automata.alphabet:
                if symbol not in automata.tokens_list:
                    #print('STATE',state,symbol,automata.transitions[state])
                    try:
                        if symbol in automata.transitions[state]:
                            #print('yes',automata.transitions[state][symbol])
                            self.goto_table[state][symbol] = automata.transitions[state][symbol]
                        else:
                            self.goto_table[state][symbol] = None
                    except:
                        self.goto_table[state][symbol] = None

        #print('GOTO TABLE')
        #print(self.goto_table)

        #fill actions
        #append the terminal
        automata.tokens_list.append(Symbol('$').name)
        for state in automata.states:
            for symbol in automata.tokens_list:
                #verify if the state is final
                if state.is_final and symbol == Symbol('$').name:
                    #print("state FINAL")
                    self.actions_table[state][symbol] = 'accept'
                elif symbol != Epsilon().symbol:
                    try:
                        if symbol in automata.transitions[state]:
                            #verify if is a shift/reduce conflict

                                self.actions_table[state][symbol] = 's'+automata.transitions[state][symbol].name


                        else:
                            self.actions_table[state][symbol] = None
                    except:
                        self.actions_table[state][symbol] = None
                else:
                    self.actions_table[state][symbol] = None

        #print('ACTIONS TABLE BEFORE')
        #print(self.actions_table)
        #print(self.already_evaluated)
        # fill the reductions
        for state in automata.states:
            if state.is_final == False:
                for production in state.list:
                    #print(state,production.left,production.right)
                    #print('PRODUCTION',production.left,production.right)
                    if production.right.strip()[-1] == '.':
                        #print('PRODUCTION',production.left,'-->',production.right)
                        for symbol in automata.tokens_list:
                            #print('FOLLO PRODUCTION',production.left,state)

                            #print('FOLLOW',state,self.follow(production.left))
                            if symbol in self.follow(production.left):
                                for prod in range(len(self.expand_productions_without_dot)):
                                    #print('PROVING',self.expand_productions_without_dot[prod].left==production.left,self.expand_productions_without_dot[prod].right,production.right.strip()[:-1], self.expand_productions_without_dot[prod].right==production.right.strip()[:-2], len(self.expand_productions_without_dot[prod].right),len(production.right.strip()[:-2]))
                                    if self.expand_productions_without_dot[prod].left == production.left and self.expand_productions_without_dot[prod].right.strip() == production.right.strip()[:-2]:
                                        #print('SAME')
                                        #detect shift/reduce conflict
                                        if self.actions_table[state][symbol] != None:
                                            print(f'SHIFT/REDUCE CONFLICT: You want to reduce but there is {self.actions_table[state][symbol]} in state {state.name} with symbol {symbol}')
                                            exit()

                                        else:
                                            self.actions_table[state][symbol] = 'r'+str(prod)
                                            break

        # print('ACTIONS TABLE')
        # print(self.actions_table)

        #visualize table html format with graphviz
        # Define the table as a list of lists
        graph = Digraph(format='pdf', node_attr={'shape': 'record'})
        graph.attr(rankdir='LR')

        custom_label = ''
        custom_label += '<<table border="0" cellborder="1" cellspacing="0">'
        #put the states as columns
        custom_label += '<tr><td rowspan="2">STATES</td>'
        custom_label += '<td colspan="'+str(len(automata.tokens_list))+'">ACTIONS</td>'
        custom_label += '<td colspan="'+str(len(list(set(automata.alphabet) - set(automata.tokens_list))))+'">GOTO</td>'
        custom_label += '</tr>'

        custom_label += '<tr>'
        for i in automata.tokens_list:
            custom_label += '<td>'+i+'</td>'
        for i in list(set(automata.alphabet) - set(automata.tokens_list)):
            custom_label += '<td>'+i+'</td>'
        custom_label += '</tr>'

        for state in automata.states:
            custom_label += '<tr>'
            custom_label += '<td>'+state.name+'</td>'
            for symbol in automata.tokens_list:
                if self.actions_table[state][symbol] != None:
                    custom_label += '<td>'+self.actions_table[state][symbol]+'</td>'
                else:
                    custom_label += '<td></td>'
            for symbol in list(set(automata.alphabet) - set(automata.tokens_list)):
                if self.goto_table[state][symbol] != None:
                    custom_label += '<td>'+self.goto_table[state][symbol].name+'</td>'
                else:
                    custom_label += '<td></td>'
            custom_label += '</tr>'



        custom_label += '</table>>'

        graph.node(name='table',label = custom_label)
        #graph.render(directory='test-output',view=True)

        return self.actions_table,self.goto_table

