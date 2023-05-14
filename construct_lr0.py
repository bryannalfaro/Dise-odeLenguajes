from time import sleep
from production import Production
from state_definition import State
from automata.LR0 import AutomataLR
class ConstructLR():
    def __init__(self, productions):
        super().__init__()
        self.yalex_productions = productions
        self.gramatical_elements = []
        self.production_indicate = None
        self.productions = []
        self.make_productions()
        self.expanded_productions = []
        self.expand_production()

        self.J_results = []

        # state = State()
        # state.list = [self.expanded_productions[4]]
        # self.closure(state.list)
        # self.goto(state.list,'factor')

        print('sali')

    #make the productions
    def make_productions(self):
        for production in self.yalex_productions:
            left = production
            for right_item in self.yalex_productions[production]:
                right = right_item.strip()
                self.productions.append(Production(left,right))

        #print every production with his left and right
        for production in self.productions:
             print('PRODUCTION')
             print(production.left,'-->',production.right)

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



    def expand_production(self):
        #add the first production to expanded production
        self.expanded_productions.append(Production(self.productions[0].left+"'",self.productions[0].left))
        self.production_indicate = Production(self.productions[0].left+"'",self.productions[0].left)

        #add the rest of the productions to expanded productions
        for production in self.productions:
            self.expanded_productions.append(production)


        #add dot to the expanded productions
        for i in range(len(self.expanded_productions)):
            self.expanded_productions[i].right = '. '+self.expanded_productions[i].right

        for i in self.expanded_productions:
             print('expanded',i.left,'-->',i.right)

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
                                append = True
                            # else:
                            #     for i in range(len(self.J_results)):
                            #         if self.J_results[i].is_eval == False:
                            #             change = True
            if append:
                change = True

        #print('vines')
        for i in self.J_results:
            print(i.left,'-->',i.right)
        #sleep(10)
        return self.J_results

    def move_dot(self, right):
        array  = []
        #make the string an array in for loop
        #while to save workd and add to the array
        count = 0
        flag = False
        word = ''
        index_dot = None
        #print('RIGHT',right)
        while count < len(right):
            #print(word,right[count])
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
        #make the closure of the goto_list
        #print('GOTO LIST before closure')
        # for i in goto_list:
        #     print(i.left,'-->',i.right)
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
                        #print('GOTO IN AUTOMATA')
                        # for i in goto:
                        #     print(i.left,'-->',i.right)
                        # sleep(1)

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
                                #print the state and the new state
                                # print('STATE')
                                # for i in state.list:
                                #     print(i.left,'-->',i.right)
                                # print('NEW STATE')
                                # for i in new_state.list:
                                #     print(i.left,'-->',i.right)
                                # print('TRANSITION')
                                # print(transitions)
                                change = True
                            else:
                                #add the transition to itself
                                if state not in transitions:
                                    transitions[state] = {}
                                transitions[state][symbol] = new_state
                                # print('STATE')
                                # for i in state.list:
                                #     print(i.left,'-->',i.right)
                                # print('NEW STATE')
                                # for i in new_state.list:
                                #     print(i.left,'-->',i.right)
                                # print('TRANSITION')
                                # print(transitions)
                                is_double = False
                                change = True

                        else:
                            pass

        print(len(C_group))
        #make the final states those who has the expanded production
        for state in C_group:
            for production in state.list:

                if production.left == self.production_indicate.left:
                    if production.right.strip() == self.production_indicate.right+' .':
                        state.is_final = True
                        print('FINAL STATE',state.name)

        #make the automata
        automata = AutomataLR(C_group,self.gramatical_elements,transitions,initial_state,[state for state in C_group if state.is_final])
        return automata