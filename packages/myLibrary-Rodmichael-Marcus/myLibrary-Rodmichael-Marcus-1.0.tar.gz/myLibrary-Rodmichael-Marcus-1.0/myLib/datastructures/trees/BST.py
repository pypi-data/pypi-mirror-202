from myLib.datastructures.nodes.TNode import TNode


class BST:
    def __init__(self, val=None, obj=None):
        if obj:
            self.root = obj            ##Takes existing TNode object as arg and sets it to root of BST
        elif val is not None:
            self.root = TNode(val, 0, None, None, None)     ##takes int value as arg and creates new TNode object and is set as BST root
        else:
            self.root = None        ##initializes root to none

    def set_root(self, node):       ##setter for root
        self.root = node

    def get_root(self):             ##getter for root
        return self.root

    def insert(self, val):          ##create new node with val and insert into tree
        if self.root is None:       ## if none, inserted value is can be set to root
            self.root = TNode(val, 0, None, None, None)
        else:                       ##tree has nodes, calls _insert to to find correct spot
            self._insert(val, self.root)

    def _insert(self, val, node, depth=0, max_depth=100):
        if depth >= max_depth:
            raise RuntimeError("Maximum recursion depth exceeded")
        if node is None:
            new_node = TNode(val, 0, None, None, None)
            return new_node
        elif val < node.get_data():
            if node.get_left() is None:
                new_node = TNode(val, 0, node, None, None)
                node.set_left(new_node)
                return new_node
            else:
                return self._insert(val, node.get_left(), depth+1, max_depth)
        else:
            if node.get_right() is None:
                new_node = TNode(val, 0, node, None, None)
                node.set_right(new_node)
                return new_node
            else:
                return self._insert(val, node.get_right(), depth+1, max_depth)

    def insert_node(self, val):
        """
        Inserts the given value into the AVL tree while maintaining the balance
        of the tree
        """
        self.insert(val)  # call AVL insert method to insert the value

    def delete(self, val):
        if self.root is None:
            return False
        else:
            return self._delete(val, self.root)

    def _delete(self, val, node):
        # If the current node's value is equal to the value to be deleted, handle the four cases:
        if val == node.get_data():
            # If the current node is a leaf node (i.e., has no children):
            if node.get_left() is None and node.get_right() is None:
                if node.get_parent() is not None:
                    # If the current node has a parent node, remove the current node from the parent's child nodes:
                    if node.get_parent().get_left() == node:
                        node.get_parent().set_left(None)
                    else:
                        node.get_parent().set_right(None)
                else:
                    # If the current node is the root node, set the root to None:
                    self.root = None
            # If the current node has only one child node (i.e., only a left or right child):
            elif node.get_left() is None:
                # Promote the right child node to replace the current node's position in the tree:
                node.get_right().set_parent(node.get_parent())
                if node == self.root:
                    self.root = node.get_right()
                elif node.get_parent().get_left() == node:
                    node.get_parent().set_left(node.get_right())
                else:
                    node.get_parent().set_right(node.get_right())
            elif node.get_right() is None:
                # Promote the left child node to replace the current node's position in the tree:
                node.get_left().set_parent(node.get_parent())
                if node == self.root:
                    self.root = node.get_left()
                elif node.get_parent().get_left() == node:
                    node.get_parent().set_left(node.get_left())
                else:
                    node.get_parent().set_right(node.get_left())
            # If the current node has two child nodes:
            else:
                # Find the minimum value node in the right subtree of the current node, 
                # replace the current node's value with it, and then delete the minimum node:
                min_right = self._find_min(node.get_right())
                node.set_data(min_right.get_data())
                self._delete(min_right.get_data(), node.get_right())
            return True
        # If the value to be deleted is less than the current node's value, go left:
        elif val < node.get_data() and node.get_left() is not None:
            return self._delete(val, node.get_left())
        # If the value to be deleted is greater than the current node's value, go right:
        elif val > node.get_data() and node.get_right() is not None:
            return self._delete(val, node.get_right())
        # If the value to be deleted is not found in the tree:
        else:
            return False

    def _find_min(self, node):
        while node.get_left() is not None:
            node = node.get_left()
        return node

    def _update_balance(self, node):
        if node is not None:
            node.update_balance()
            if node.get_balance() == -2:
                if node.get_left().get_balance() <= 0:
                    self._rotate_right(node)
                else:
                    self._rotate_left_right(node)
            elif node.get_balance() == 2:
                if node.get_right().get_balance() >= 0:
                    self._rotate_left(node)
                else:
                    self._rotate_right_left(node)
            self._update_balance(node.get_parent())
        
    def _rotate_left(self, node):
        pivot = node.get_right()
        pivot.set_parent(node.get_parent())
        if node == self.root:
            self.root = pivot

    def search(self, val):
    # Public method that searches for a node with the given value in the tree
    # and returns the node object if found, otherwise returns None.
        return self._search(val, self.root)

    def _search(self, val, node):
        # Private recursive method to search for a node with the given value in the subtree rooted at node
        # If the node is found, returns the node object, otherwise continues searching in the appropriate subtree
        if node is None:
            return None
        elif val == node.get_data():
            return node
        elif val < node.get_data() and node.get_left() is not None:
            return self._search(val, node.get_left())
        elif val > node.get_data() and node.get_right() is not None:
            return self._search(val, node.get_right())


    def print_in_order(self):
        self._print_in_order(self.root)
        print()

    def _print_in_order(self, node):
        if node is not None:
            self._print_in_order(node.get_left())
            print(node)


    def printBF(self,root):
        if root is None:
            return

        queue = [root]
        next_level_count = 0
        current_level_count = 1

        while queue:
            node = queue.pop(0)
            current_level_count -= 1

            print(node.data, end=" ")

            if node.left:
                queue.append(node.left)
                next_level_count += 1

            if node.right:
                queue.append(node.right)
                next_level_count += 1

            if current_level_count == 0:
                print()
                current_level_count = next_level_count
                next_level_count = 0
               

