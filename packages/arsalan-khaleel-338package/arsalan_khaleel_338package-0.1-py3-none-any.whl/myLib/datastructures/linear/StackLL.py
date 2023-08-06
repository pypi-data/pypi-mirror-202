from myLib.datastructures.linear.SLL import SinglyLL
class LLStack(SinglyLL):
    def __init__(self):
        super().__init__()
    def push(self, node):
        super().insert_head(node)
    def pop(self):
        if not self.head:
            return None
        temp = self.head
        super().delete_head()
        return temp.data
    def peek(self):
        if not self.head:
            return None
        return self.head.data
    def isEmpty(self):
        return not bool(self.head)
    def inser_tail(self, node):
        pass
    def insert(self, node, position):
        pass
    def sorted_insert(self, node):
        pass
    def search(self, data):
        pass
    def delete_tail(self):
        pass
    def delete(self, data):
        pass
    def sort(self):
        pass