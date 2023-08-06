class Tnode:
    def __init__(self, data=0, balance=0, parent=None, left=None, right=None):
        self.data = data
        self.balance = balance
        self.parent = parent
        self.left = left
        self.right = right

    def set_data(self, data):
        self.data = data

    def set_balance(self, balance):
        self.balance = balance

    def set_parent(self, parent):
        self.parent = parent

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def get_data(self):
        return self.data

    def get_balance(self):
        return self.balance

    def get_parent(self):
        return self.parent

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def print_node(self):
        print(f"Data: {self.data}, Balance: {self.balance}")

    def to_string(self):
        return str(self.data)
    def find(self, val):
        if self.data == val:
            return self
        elif val < self.data and self.left:
            return self.left.find(val)
        elif val > self.data and self.right:
            return self.right.find(val)
        else:
            return None