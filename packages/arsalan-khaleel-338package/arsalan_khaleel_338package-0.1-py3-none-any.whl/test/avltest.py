from myLib.datastructures.trees.AVL import AVL

# Create an AVL tree object
avl = AVL()

# Insert some values into the AVL tree
avl.insert(10)
avl.insert(20)
avl.insert(30)
avl.insert(40)
avl.insert(50)

# Print the inorder traversal of the AVL tree
avl.inorder()

# Search for a node in the AVL tree
search_node = avl.search(30)
if search_node:
    print(f"Node {search_node.get_data()} found in AVL tree")
else:
    print("Node not found in AVL tree")

# Delete a node from the AVL tree
avl.delete(20)

# Print the inorder traversal of the AVL tree after deletion
avl.inorder()
