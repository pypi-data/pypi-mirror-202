from myLib.datastructures.nodes.TNode import TNode
from myLib.datastructures.trees.BST import BST


class AVL(BST):
    def __init__(self, val = None):
        super().__init__()  # call parent constructor
        if val is not None:
            self.root = TNode(val, 0, None, None, None)

    def AVL(self, obj):
        """
        Overload constructor to create an AVL tree from a TNode obj
        """
        self.root = obj  # use TNode obj as the root of the tree
        if obj.left is not None or obj.right is not None:
            # if obj has children create a balanced tree from it iteratively inserting nodes from the original tree and balancing
            # the new created AVL tree
            nodes = []  # list to store nodes in BFS order
            nodes.append(obj)
            i = 0
            while i < len(nodes):
                node = nodes[i]
                i += 1
                if node.left is not None:
                    nodes.append(node.left)
                if node.right is not None:
                    nodes.append(node.right)
            nodes.reverse()  # reverse the list to insert nodes in reverse BFS order
            for node in nodes:
                self.insert(node)

    def set_root(self, node):
        if node is None:
            self.root = None
        else:
            self.root = self.__create_balanced_avl_tree(node)

    def get_root(self):
        return self.root
    
    def __create_balanced_avl_tree(self, node):
        """
        Helper function to create a balanced AVL tree starting from the given node
        """
        if node is None:
            return None
        
        new_node = TNode(node.data)
        new_node.left = self.__create_balanced_avl_tree(node.left)
        new_node.right = self.__create_balanced_avl_tree(node.right)
        
        self.balance(new_node)
        
        return new_node

    def balance(self, node):
        """
        Helper function to balance the AVL tree starting from the given node
        """
        if node is None:
            return 0

        left_height = self.balance(node.left)  # recursively balance left subtree
        right_height = self.balance(node.right)  # recursively balance right subtree

        balance_factor = left_height - right_height  # calculate balance factor

        # check if tree is unbalanced and perform rotations accordingly
        if balance_factor > 1:  # left heavy
            if self.get_height(node.left.left) >= self.get_height(node.left.right):
                node = self.rotate_right(node)
            else:
                node.left = self.rotate_left(node.left)
                node = self.rotate_right(node)
        elif balance_factor < -1:  # right heavy
            if self.get_height(node.right.right) >= self.get_height(node.right.left):
                node = self.rotate_left(node)
            else:
                node.right = self.rotate_right(node.right)
                node = self.rotate_left(node)

        # Update the height of the node
        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1

        return node.height

    def get_height(self, node):
        """
        Helper function to get the height of the given node
        """
        if node is None:
            return 0
        else:
            node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1
            return node.height

    def rotate_left(self, node):
        """
        Rotates the given node and its right child to the left
        """
        right_child = node.right
        node.right = right_child.left

        if right_child.left is not None:
            right_child.left.parent = node

        right_child.parent = node.parent

        if node.parent is None:
            self.root = right_child
        elif node is node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

        # Update the heights of the nodes
        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1
        right_child.height = max(self.get_height(right_child.left), self.get_height(right_child.right)) + 1

        return right_child

    def rotate_right(self, node):
        """
        Rotates the given node and its left child to the right
        """
        left_child = node.left
        node.left = left_child.right

        if left_child.right is not None:
            left_child.right.parent = node

        left_child.parent = node.parent

        if node.parent is None:
            self.root = left_child
        elif node is node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child

        left_child.right = node
        node.parent = left_child

        # Update the heights of the nodes
        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1
        left_child.height = max(self.get_height(left_child.left), self.get_height(left_child.right)) + 1

        return left_child


    def insert(self, val):
        """
        Inserts a node with the given value into the AVL tree while maintaining
        the balance of the tree
        """
        super().insert(val)  # call parent insert method. insert(int val)
        self.balance(self.root)  # balance the tree starting from the root

    
    def delete(self, val):
        """
        Deletes the node with the given value from the AVL tree while maintaining
        the balance of the tree
        """
        node = self._find_node(val, self.root)
        if node is None:
            print(f"Value {val} is not in the tree.")
        else:
            super().delete(val)  # call parent delete method
            self.balance(node.parent)  # balance the tree starting from the parent of the deleted node
        
    def _find_node(self, val, node):
        """
        Helper function to find a node with the given value in the AVL tree
        """
        if node is None:
            return None
        elif val == node.data:
            return node
        elif val < node.data:
            return self._find_node(val, node.left)
        else:
            return self._find_node(val, node.right)

    def insert_node(self, node):
        self.root = self._insert_node(self.root, node)

    def _insert_node(self, current_node, node):
        if not current_node:
            return node
        elif node.data < current_node.data:
            current_node.left = self._insert_node(current_node.left, node)
        else:
            current_node.right = self._insert_node(current_node.right, node)
        
        # Update the height of the current node
        current_node.height = 1 + max(self.get_height(current_node.left), self.get_height(current_node.right))
        
        # Check if the current node is balanced
        balance = self.get_balance(current_node)
        if balance > 1 and node.data < current_node.left.data:
            return self.right_rotate(current_node)
        if balance < -1 and node.data > current_node.right.data:
            return self.left_rotate(current_node)
        if balance > 1 and node.data > current_node.left.data:
            current_node.left = self.left_rotate(current_node.left)
            return self.right_rotate(current_node)
        if balance < -1 and node.data < current_node.right.data:
            current_node.right = self.right_rotate(current_node.right)
            return self.left_rotate(current_node)
        
        return current_node

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def Search(self, val):
        """
        Searches the AVL tree for a node with the given value and returns the node
        if it exists, otherwise returns None
        """
        return self._find_node(val, self.root)

    def printInOrder(self):
        """
        Prints the values of nodes in the AVL tree in order
        """
        if self.root is not None:
            self._printInOrder(self.root)

    def _printInOrder(self, node):
        """
        Helper function to print the values of nodes in the AVL tree in order
        """
        if node is not None:
            self._printInOrder(node.left)
            print(node.data, end=' ')
            self._printInOrder(node.right)

    def printBF(self):
        """
        Prints the values of nodes in the AVL tree in breadth-first order
        """
        if self.root is None:
            return

        queue = [self.root]
        while queue:
            node = queue.pop(0)
            print(node.data, end=' ')
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

