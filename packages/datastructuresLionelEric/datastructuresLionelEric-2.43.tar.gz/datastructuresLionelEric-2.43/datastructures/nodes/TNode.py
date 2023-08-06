
class TNode:
    def __init__(self, data=0, balance=0, parent=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent
        self.balance = balance
    
    def set_data(self, data):
        self.data = data

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def set_parent(self, parent):
        self.parent = parent

    def set_balance(self, balance):
        self.balance = balance

    def get_data(self):
        return self.data

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_parent(self):
        return self.parent

    def get_balance(self):
        return self.balance

    def print(self):
        # print(f"Data: {self.data}, Balance: {self.balance} Parent TNode: {self.parent} TNode Right: {self.right} TNode Left: {self.left}")
        print(f"Data: {self.data}, Balance: {self.balance}")

    def toString(self):
        return str(self.data)

