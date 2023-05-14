class Production():
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.is_closure = False
        self.is_eval = False