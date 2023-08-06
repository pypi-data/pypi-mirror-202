from myLib.datastructures.linear.DLL import DoublyLL

# # Create a new doubly linked list object
dll = DoublyLL()

# Test the insert_head method
dll.insert_head(1)
dll.insert_head(2)
dll.insert_head(3)
assert [node.data for node in dll] == [3, 2, 1]

# Test the delete_tail method
dll.delete_tail()
assert [node.data for node in dll] == [3, 2]
assert dll.tail.data == 2

dll.delete_tail()
assert [node.data for node in dll] == [3]
assert dll.tail.data == 3

dll.delete_tail()
assert [node.data for node in dll] == []
try:
    dll.delete_tail()
except Exception as e:
    assert str(e) == 'List is empty'

# Test the search method
dll.insert_head(1)
dll.insert_head(2)
dll.insert_head(3)
assert dll.search(1).data == 1
assert dll.search(2).data == 2
assert dll.search(3).data == 3
assert dll.search(4) is None

# Test the delete method
node = dll.search(2)
dll.delete(node)
assert [node.data for node in dll] == [3, 1]

# Test the clear method
dll.clear()
assert [node.data for node in dll] == []