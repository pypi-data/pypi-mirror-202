

from myLib.datastructures.nodes.TNode import Tnode

class BST:
    def __init__(self, val=None):
        if isinstance(val, Tnode):
            self.root = val
        elif val is not None:
            self.root = Tnode(val)
        else:
            self.root = None

    def set_root(self, root):
        self.root = root

    def get_root(self):
        return self.root

    def insert(self, val):
        if isinstance(val, Tnode):
            node = val
        else:
            node = Tnode(val)
        if self.root is None:
            self.root = node
        else:
            current = self.root
            while current is not None:
                if node.data < current.data:
                    if current.left is None:
                        current.left = node
                        break
                    else:
                        current = current.left
                else:
                    if current.right is None:
                        current.right = node
                        break
                    else:
                        current = current.right

    def delete(self, val):
        def min_value_node(node):
            while node.left is not None:
                node = node.left
            return node

        def delete_node(node, val):
            if node is None:
                return node
            if val < node.data:
                node.left = delete_node(node.left, val)
            elif val > node.data:
                node.right = delete_node(node.right, val)
            else:
                if node.left is None:
                    temp = node.right
                    node = None
                    return temp
                elif node.right is None:
                    temp = node.left
                    node = None
                    return temp
                temp = min_value_node(node.right)
                node.data = temp.data
                node.right = delete_node(node.right, temp.data)
            return node

        if self.search(val) is not None:
            self.root = delete_node(self.root, val)
        else:
            print(f"{val} is not in the tree")

    def search(self, val):
        current = self.root
        while current is not None:
            if val == current.data:
                return current
            elif val < current.data:
                current = current.left
            else:
                current = current.right
        return None

    def print_in_order(self):
        def in_order(node):
            if node is not None:
                in_order(node.left)
                print(node.data, end=' ')
                in_order(node.right)

        in_order(self.root)
        print()

    def print_bf(self):
        if self.root is None:
            return
        queue = [self.root]
        while len(queue) > 0:
            level_size = len(queue)
            for i in range(level_size):
                node = queue.pop(0)
                print(node.data, end=' ')
                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)
            print()