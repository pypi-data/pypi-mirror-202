from myLib.datastructures.linear.DLL import DoublyLL
from myLib.datastructures.nodes.DNode import DNode
class DoublyCLL(DoublyLL):
    def __init__(self):
        super().__init__()
    def insert_head(self, data):
        new_node = DNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            new_node.next = self.head
            new_node.prev = self.tail
            self.head.prev = new_node
            self.tail.next = new_node
            self.head = new_node
        self.size += 1

    def insert_tail(self, data):
        new_node = DNode(data)
        if not self.tail:
            self.head = new_node
            self.tail = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            new_node.next = self.head
            new_node.prev = self.tail
            self.head.prev = new_node
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
    def delete_head(self):
        if not self.head:
            raise Exception('List is empty')
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            next_head = self.head.next
            next_head.prev = self.tail
            self.tail.next = next_head
            self.head = next_head
        self.size -=1
    def delete_tail(self):
        if not self.tail:
            raise Exception('List is empty')
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            prev_tail = self.tail.prev
            prev_tail.next = self.head
            self.head.prev = prev_tail
            self.tail = prev_tail
        self.size -= 1
    def delete(self, node):
        if not self.head:
            raise Exception('List is empty')
        if node == self.head:
            self.delete_head()
        elif node == self.tail:
            self.delete_tail()
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            self.size -= 1
    def clear(self):
        super().clear()
        self.tail = None





























































































































