from myLib.datastructures.linear.SLL import SinglyLL
from myLib.datastructures.nodes.DNode import DNode


class DoublyLL(SinglyLL):
    def __init__(self):
        super().__init__()
        self.tail = None
    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next


    def insert_head(self, data):
        new_node = DNode(data)  # create new node with the given data
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1


    
    def insert_tail(self, data):
        new_node = DNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        elif not self.tail:
            self.tail = new_node
            self.tail.prev = self.head
            self.head.next = self.tail
        else:
            new_node.prev = self.tail
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
            self.head = self.head.next
            self.head.prev = None
        self.size -= 1

    
    def delete_tail(self):
        if self.head is None:
            raise Exception('List is empty')
        elif self.head.next is None:
            self.head = None
            self.tail = None
            return
        else:
            second_last = self.head
            while second_last.next.next is not None:
                second_last = second_last.next
            self.tail = second_last  # Update tail pointer
            second_last.next = None

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

    def search(self, data):
        curr_node = self.head
        while curr_node:
            if curr_node.data == data:
                return curr_node
            curr_node = curr_node.next
        return None