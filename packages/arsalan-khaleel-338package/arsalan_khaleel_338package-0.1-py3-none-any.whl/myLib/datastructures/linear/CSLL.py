from myLib.datastructures.linear.SLL import SinglyLL
class SinglyCLL(SinglyLL):
    def __init__(self, head=None):
        super().__init__(head)
        if head:
            self.tail = head
            self.tail.next = head
    def insertHead(self, node):
        if not self.head:
            self.head = node
            self.tail = node
            self.tail.next = self.head
        else:
            node.next = self.head
            self.head = node
            self.tail.next = self.head
        self.size += 1
    def insertTail(self, node):
        if not self.tail:
            self.head = node
            self.tail = node
            self.tail.next = self.head
        else:
            node.next = self.head
            self.tail.next = node
            self.tail = node
        self.size += 1
    def insert(self, node, position):
        if position > self.size:
            return
        if position == 0:
            self.insertHead(node)
            return
        if position == self.size:
            self.insertTail(node)
            return
        current_node = self.head
        for i in range(position - 1):
            current_node = current_node.next
        node.next = current_node.next
        current_node.next = node
        self.size += 1
    def deleteHead(self):
        if not self.head:
            return
        temp = self.head
        if not temp.next or temp == temp.next:
            self.head = None
            self.tail = None
            self.size = 0
            return
        self.head = self.head.next
        self.tail.next = self.head
        temp.next = None
        self.size -= 1
    def deleteTail(self):
        if not self.tail:
            return
        if not self.head.next or self.head == self.head.next:
            self.head = None
            self.tail = None
            self.size = 0
            return
        current_node = self.head
        while current_node.next != self.tail:
            current_node = current_node.next
        current_node.next = self.head
        self.tail = current_node
        self.size -= 1
    def delete(self, data):
        if not self.head:
            return
        if self.head.data == data:
            self.deleteHead()
            return
        current_node = self.head
        while current_node.next != self.head and current_node.next.data != data:
            current_node = current_node.next
        if current_node.next == self.head:
            return
        temp = current_node.next
        current_node.next = temp.next
        temp.next = None
        if not current_node.next or current_node == current_node.next:
            self.tail = None
            self.head = None
            self.size = 0
            return
        if not current_node.next:
            self.tail = current_node
        elif not current_node.prev:
            self.head = current_node.next
        else:
            pass 
        self.size -= 1
    def clear(self):
        while self.head and self.head != self.tail:
            self.deleteHead()