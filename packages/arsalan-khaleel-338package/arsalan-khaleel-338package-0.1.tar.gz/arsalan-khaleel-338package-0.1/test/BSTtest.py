from myLib.datastructures.trees.BST import BST

# create a BST instance
bst = BST()

# insert some values
bst.insert(5)
bst.insert(3)
bst.insert(7)
bst.insert(2)
bst.insert(4)
bst.insert(6)
bst.insert(8)

# print the tree in order and breadth-first order
print("In-order traversal:")
bst.print_in_order()
print("Breadth-first traversal:")
bst.print_bf()

# delete a node and print the tree again
bst.delete(3)
print("In-order traversal after deleting 3:")
bst.print_in_order()
print("Breadth-first traversal after deleting 3:")
bst.print_bf()

# search for a node
result = bst.search(6)
if result:
    print("Found node:", result.data)
else:
    print("Node not found.")
