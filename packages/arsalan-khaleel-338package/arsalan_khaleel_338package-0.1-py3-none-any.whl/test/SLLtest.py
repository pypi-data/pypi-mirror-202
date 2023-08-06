from myLib.datastructures.linear.SLL import SinglyLL, Node


# create a new linked list
my_list = SinglyLL()

# create some nodes
node1 = Node(10)
node2 = Node(20)
node3 = Node(30)

# insert nodes into the linked list
my_list.insert_head(node1)
my_list.insert_tail(node2)
my_list.insert(node3, 1)

# print the linked list
my_list.print()

# search for a node
result = my_list.search(node2)
if result:
    print(f"Node found: {result.data}")
else:
    print("Node not found")

# delete a node
my_list.delete(node1)

# print the linked list again
my_list.print()
