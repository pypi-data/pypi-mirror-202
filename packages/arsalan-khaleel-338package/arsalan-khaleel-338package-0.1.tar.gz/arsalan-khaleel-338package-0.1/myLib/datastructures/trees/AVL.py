from myLib.datastructures.trees.BST import BST
class AVL(BST):
    def __init__(self, val=None):
        super().__init__(val)
        self.balance_tree()

    def set_root(self, root):
        super().set_root(root)
        self.balance_tree()

    def insert(self, val):
        super().insert(val)
        print(f"Inserting node with value {val}")
        current = self.root.find(val)
        parent = current.parent if current else None
        grandparent = parent.parent if parent else None
        print(f"Node: {current}, Parent: {parent}, Grandparent: {grandparent}")
        self.balance_tree()


    def balance_tree(self):
        def update_balance(node):
            if node is None:
                return 0
            left_height = update_balance(node.left)
            right_height = update_balance(node.right)
            node.balance = left_height - right_height
            return max(left_height, right_height) + 1

        def rotate_left(node):
            new_root = node.right
            node.right = new_root.left
            if new_root.left is not None:
                new_root.left.parent = node
            new_root.left = node
            new_root.parent = node.parent
            node.parent = new_root
            if new_root.parent is not None:
                if new_root.parent.left == node:
                    new_root.parent.left = new_root
                else:
                    new_root.parent.right = new_root
            else:
                self.root = new_root

        def rotate_right(node):
            new_root = node.left
            node.left = new_root.right
            if new_root.right is not None:
                new_root.right.parent = node
            new_root.right = node
            new_root.parent = node.parent
            node.parent = new_root
            if new_root.parent is not None:
                if new_root.parent.left == node:
                    new_root.parent.left = new_root
                else:
                    new_root.parent.right = new_root
            else:
                self.root = new_root

        def balance(node):
            if node is None:
                return
            balance(node.left)
            balance(node.right)
            if node.balance < -1:
                if node.right.balance > 0:
                    rotate_right(node.right)
                rotate_left(node)
            elif node.balance > 1:
                if node.left.balance < 0:
                    rotate_left(node.left)
                rotate_right(node)
        

        update_balance(self.root)
        balance(self.root)
    
    def inorder(self):
        def inorder_traversal(node):
            if node is None:
                return
            inorder_traversal(node.left)
            print(node.get_data())
            inorder_traversal(node.right)
        inorder_traversal(self.root)