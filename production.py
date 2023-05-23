class Production():
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.is_closure = False
        self.is_eval = False

    def get_separated_right(self):
        separated = []
        temp = ''
        for i in range(len(self.right)):
            if self.right[i] == ' ':
                separated.append(temp)
                temp = ''
            else:
                temp += self.right[i]
        separated.append(temp)
        return separated
