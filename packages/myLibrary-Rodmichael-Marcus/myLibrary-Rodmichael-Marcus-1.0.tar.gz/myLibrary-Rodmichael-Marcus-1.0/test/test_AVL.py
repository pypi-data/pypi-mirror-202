from myLib.datastructures.trees.BST import BST
from myLib.datastructures.trees.AVL import AVL
from myLib.datastructures.nodes.TNode import TNode

def test_AVL_constructor():
    avl = AVL()
    assert avl.root == None

def test_AVL_constructor_with_value():
    avl = AVL(5)
    assert avl.root.data == 5

def test_AVL_insert():
    avl = AVL(5)
    avl.insert(3)
    avl.insert(7)
    avl.insert(2)
    avl.insert(4)
    avl.insert(6)
    avl.insert(8)
    avl.insert(9)
    assert avl.root.right.right.right.data == 9

def test_AVL_delete():
    avl = AVL(5)
    avl.insert(3)
    avl.insert(7)
    avl.insert(2)
    avl.insert(4)
    avl.insert(6)
    avl.insert(8)
    avl.delete(7)
    assert avl.root.right.data == 8

def test_AVL_search():
    avl = AVL(5)
    avl.insert(3)
    avl.insert(7)
    avl.insert(2)
    avl.insert(4)
    avl.insert(6)
    avl.insert(8)
    assert avl.Search(7).data == 7
    assert avl.Search(10) == None

def test_AVL_set_root():
    avl = AVL(5)
    class TNode:
        def __init__(self, val):
            self.data = val
            self.left = None
            self.right = None
    node = TNode(9)
    avl.set_root(node)
    assert avl.root.data == 9


def test_AVL_get_root():
    avl = AVL(5)
    assert avl.get_root().data == 5


def test_AVL_printInOrder(capsys):
    avl = AVL(5)
    avl.insert(3)
    avl.insert(7)
    avl.insert(2)
    avl.insert(4)
    avl.insert(6)
    avl.insert(8)
    avl.printInOrder()
    captured = capsys.readouterr()
    assert captured.out == "2 3 4 5 6 7 8 "


def test_AVL_printBF(capsys):
    avl = AVL(5)
    avl.insert(3)
    avl.insert(7)
    avl.insert(2)
    avl.insert(4)
    avl.insert(6)
    avl.insert(8)
    avl.printBF()
    captured = capsys.readouterr()
    assert captured.out == "5 3 7 2 4 6 8 "

"""
def test_AVL_balancing_performance():
        avl = AVL()
        for i in range(8191):
            avl.insert(i)
        assert avl.root.height <= 13
"""


def test_AVL_duplicate_values():
    avl = AVL(5)
    avl.insert(3)
    avl.insert(7)
    avl.insert(2)
    avl.insert(4)
    avl.insert(6)
    avl.insert(8)
    assert avl.search(5) is not None
    assert avl.search(9) is None
    avl.delete(5)
    assert avl.search(5) is None
    assert avl.search(4) is not None
    avl.delete(5)
    assert avl.search(5) is None

def test_delete():
    avl = AVL()
    avl.insert(1)
    avl.insert(2)
    avl.insert(3)
    avl.delete(1)
    assert avl.root.data == 2
    assert avl.root.left is None
    assert avl.root.right.data == 3

def test_insert_node():
    avl = AVL()
    root = TNode(2)
    node1 = TNode(1)
    node2 = TNode(3)
    avl.insert_node(root)
    avl.insert_node(node1)
    avl.insert_node(node2)
    assert avl.root.data == 2
    assert avl.root.left.data == 1
    assert avl.root.right.data == 3

def test_find():
    avl = AVL()
    avl.insert(1)
    avl.insert(2)
    avl.insert(3)
    assert avl.search(1) is not None
    assert avl.search(2) is not None
    assert avl.search(3) is not None
    assert avl.search(4) is None

def test_printInOrder_emptyTree():
    # Ensure printInOrder works correctly on an empty tree
    avl = AVL()
    avl.printInOrder()  # Should not raise any errors


def test_printInOrder_singleNode():
    # Ensure printInOrder works correctly on a tree with a single node
    avl = AVL()
    avl.insert(5)
    avl.printInOrder()  # Should print "5 " to stdout

def test_printInOrder_multipleNodes():
    # Ensure printInOrder works correctly on a tree with multiple nodes
    avl = AVL()
    avl.insert(5)
    avl.insert(3)
    avl.insert(7)
    avl.insert(1)
    avl.insert(4)
    avl.insert(6)
    avl.insert(9)
    avl.printInOrder()  # Should print "1 3 4 5 6 7 9 " to stdout

def test_printBF_emptyTree():
    # Ensure printBF works correctly on an empty tree
    avl = AVL()
    avl.printBF()  # Should not raise any errors

def test_printBF_singleNode():
    # Ensure printBF works correctly on a tree with a single node\
    avl = AVL()
    avl.insert(5)
    avl.printBF()  # Should print "5 " to stdout

def test_printBF_multipleNodes():
    # Ensure printBF works correctly on a tree with multiple nodes
    avl = AVL()
    avl.insert(5)
    avl.insert(3)
    avl.insert(7)
    avl.insert(1)
    avl.insert(4)
    avl.insert(6)
    avl.insert(9)
    avl.printBF()  # Should print "5 3 7 1 4 6 9 " to stdout

def test_set_root_with_none():
    avl = AVL()
    avl.set_root(None)
    assert avl.get_root() is None


def test_avl_insert():
    tree = AVL()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    assert tree.search(10) is not None
    assert tree.search(20)is not None
    assert tree.search(30) is not None

def test_avl_delete():
    tree = AVL()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    tree.delete(20)
    assert tree.search(10)is not None
    assert tree.search(20)is None
    assert tree.search(30) is not None

def test_avl_balance():
    tree = AVL()
    tree.insert(10)
    tree.insert(20)
    tree.insert(30)
    assert tree.root.data == 20
    assert tree.root.left.data == 10
    assert tree.root.right.data == 30

