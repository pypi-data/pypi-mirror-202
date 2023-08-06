class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
class SinglyLL:
    def __init__(self, head=None):
        self.head = head
        self.tail = head
        self.size = 1 if head else 0
    def insert_head(self, node):
        if not self.head:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head = node
        self.size += 1
    def insert_tail(self, node):
        if not self.tail:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1
    def insert(self, node, position):
        if position < 0 or position > self.size:
            raise IndexError('Index out of range')
        if position == 0:
            self.insert_head(node)
        elif position == self.size:
            self.insert_tail(node)
        else:
            current = self.head
            for _ in range(position - 1):
                current = current.next
            node.next = current.next
            current.next = node
            self.size += 1
    def sorted_insert(self, node):
        if not self.is_sorted():
            self.sort()
        if not self.head or node.data < self.head.data:
            self.insert_head(node)
        elif node.data >= self.tail.data:
            self.insert_tail(node)
        else:
            current = self.head
            while current.next and current.next.data < node.data:
                current = current.next
            node.next = current.next
            current.next = node
            self.size += 1
    def search(self, node):
        current = self.head
        while current:
            if current.data == node.data:
                return current
            current = current.next
        return None
    def delete_head(self):
        if not self.head:
            raise Exception('List is empty')
        self.head = self.head.next
        if not self.head:
            self.tail = None
        self.size -= 1
    def delete_tail(self):
        if not self.tail:
            raise Exception('List is empty')
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            current = self.head
            while current.next != self.tail:
                current = current.next
            current.next = None
            self.tail = current
        self.size -= 1
    def delete(self, node):
        if not self.head:
            raise Exception('List is empty')
        if self.head.data == node.data:
            self.delete_head()
        elif self.tail.data == node.data:
            self.delete_tail()
        else:
            current = self.head
            while current.next and current.next.data != node.data:
                current = current.next
            if current.next:
                current.next = current.next.next
                self.size -= 1
    def sort(self):
        if self.size < 2:
            return
        new_head = None
        while self.head:
            node = self.head
            self.head = self.head.next
            if not new_head or node.data < new_head.data:
                node.next = new_head
                new_head = node
            else:
                current = new_head
                while current.next and node.data > current.next.data:
                    current = current.next
                node.next = current.next
                current.next = node
        self.head = new_head
    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0
    def print(self):
        print(f'List length: {self.size}')
        print(f'Sorted status: {"sorted" if self.is_sorted() else "not sorted"}')
        print('List content: ', end='')
        current = self.head
        while current:
            print(current.data, end=' ')
            current = current.next
        print()
    def is_sorted(self):
        current = self.head
        while current and current.next:
            if current.data > current.next.data:
                return False
            current = current.next
        return True