
class State():
    counter = 0
    def __init__(self, is_initial=False, is_final=False):
        self.name = str(State.counter)
        State.counter += 1

        self.is_initial = is_initial
        self.is_final = is_final

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.name
