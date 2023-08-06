import pytest
from myLib.datastructures.Linear.CDLL import CDLL
from myLib.datastructures.nodes.DNode import DNode

def test_insert_head():
    cdll = CDLL()
    cdll.insert_head(DNode(1))
    cdll.insert_head(DNode(2))
    cdll.insert_head(DNode(3))

    assert cdll.head.data == 3
    assert cdll.tail.data == 1
    assert cdll.head.prev == cdll.tail
    assert cdll.tail.next == cdll.head
    assert cdll.size == 3

def test_insert_tail():
    cdll = CDLL()
    cdll.insert_tail(DNode(1))
    cdll.insert_tail(DNode(2))
    cdll.insert_tail(DNode(3))

    assert cdll.head.data == 1
    assert cdll.tail.data == 3
    assert cdll.head.prev == cdll.tail
    assert cdll.tail.next == cdll.head
    assert cdll.size == 3

def test_insert():
    cdll = CDLL()
    cdll.insert_head(DNode(1))
    cdll.insert_tail(DNode(3))
    cdll.insert(DNode(2), 1)

    assert cdll.head.data == 1
    assert cdll.head.next.data == 2
    assert cdll.tail.data == 3
    assert cdll.head.prev == cdll.tail
    assert cdll.tail.next == cdll.head
    assert cdll.size == 3

def test_sorted_insert():
    cdll = CDLL()
    cdll.sorted_insert(DNode(5))
    cdll.sorted_insert(DNode(1))
    cdll.sorted_insert(DNode(3))
    cdll.sorted_insert(DNode(2))
    cdll.sorted_insert(DNode(4))

    assert cdll.head.data == 1
    assert cdll.head.next.data == 2
    assert cdll.head.next.next.data == 3
    assert cdll.head.next.next.next.data == 4
    assert cdll.tail.data == 5
    assert cdll.head.prev == cdll.tail
    assert cdll.tail.next == cdll.head
    assert cdll.size == 5

def test_search():
    cdll = CDLL()
    cdll.insert_head(DNode(1))
    cdll.insert_tail(DNode(3))
    cdll.insert(DNode(2), 1)

    node = cdll.search(2)
    assert node.data == 2
    assert node.prev.data == 1
    assert node.next.data == 3

    node = cdll.search(4)
    assert node is None

def test_delete_head():
    cdll = CDLL()
    cdll.insert_head(DNode(1))
    cdll.insert_tail(DNode(3))
    cdll.insert(DNode(2), 1)

    cdll.delete_head()

    assert cdll.head.data == 2
    assert cdll.tail.data == 3
    assert cdll.head.prev == cdll.tail
    assert cdll.tail.next == cdll.head
    assert cdll.size == 2

def test_delete_tail():
    cdll = CDLL()
    cdll.insert_head(DNode(1))
    cdll.insert_tail(DNode(3))
    cdll.insert(DNode(2), 1)

    cdll.delete_tail()

    assert cdll.head.data == 1
    assert cdll.tail.data == 2
    assert cdll.head.prev == cdll.tail
    assert cdll.tail.next == cdll.head
    assert cdll.size == 2

def test_delete():
    cdll = CDLL()
    cdll.insert_head(DNode(1))
    cdll.insert_tail(DNode(3))
    cdll.insert(DNode(2), 1)

    cdll.delete(2)

    assert cdll.head.data == 1
    assert cdll.tail.data == 3
    assert cdll.head.prev == cdll.tail
    assert cdll.tail.next == cdll.head
    assert cdll.size == 2

def test_sort():
    cdll = CDLL()
    cdll.insert_head(DNode(5))
    cdll.insert_tail(DNode(2))
    cdll.insert(DNode(3), 1)

    cdll.sort()

    assert cdll.head.data == 2
    assert cdll.head.next.data == 3
    assert cdll.tail.data == 5
    assert cdll.head.prev == cdll.tail
    assert cdll.tail.next == cdll.head
    assert cdll.size == 3

def test_clear():
    cdll = CDLL()
    cdll.insert_head(DNode(1))
    cdll.insert_tail(DNode(3))
    cdll.insert(DNode(2), 1)

    cdll.clear()

    assert cdll.head is None
    assert cdll.tail is None
    assert cdll.size == 0

def test_cdll_print(capfd):
    csll = CDLL()
    csll.insert(DNode(1), 0)
    csll.insert(DNode(2), 1)
    csll.insert(DNode(3), 2)

    csll.print()
    
    captured = capfd.readouterr()
    expected_output = "List length: 3\nSorted status: Yes\nList content:\nHead prev: 3\n1 <-> 2 <-> 3\nTail next: 1\n"
    print(f"Captured output: {repr(captured.out)}")
    print(f"Expected output: {repr(expected_output)}")
    
    assert captured.out == expected_output

def test_size_update():
    cdll = CDLL()
    assert cdll.size == 0

    cdll.insert_head(DNode(1))
    assert cdll.size == 1

    cdll.insert_tail(DNode(3))
    assert cdll.size == 2

    cdll.insert(DNode(2), 1)
    assert cdll.size == 3

    cdll.delete(2)
    assert cdll.size == 2

    cdll.clear()
    assert cdll.size == 0

def test_chain_integrity():
    cdll = CDLL()
    nodes = [DNode(i) for i in range(1, 6)]

    for node in nodes:
        cdll.insert_tail(node)

    current = cdll.head
    for _ in range(cdll.size * 2):  # Traverse the list twice to check circularity
        assert current.data in [node.data for node in nodes]
        current = current.next

    current = cdll.tail
    for _ in range(cdll.size * 2):  # Traverse the list backwards twice to check circularity
        assert current.data in [node.data for node in nodes]
        current = current.prev

def test_single_node_list():
    cdll = CDLL()
    cdll.insert_head(DNode(1))

    assert cdll.head.data == 1
    assert cdll.tail.data == 1
    assert cdll.head.prev == cdll.tail
    assert cdll.tail.next == cdll.head
    assert cdll.size == 1

    cdll.delete_head()

    assert cdll.head is None
    assert cdll.tail is None
    assert cdll.size == 0

def test_delete_empty_list():
    cdll = CDLL()

    with pytest.raises(RuntimeError, match="Cannot Delete From an Empty List"):
        cdll.delete_head()

    with pytest.raises(RuntimeError, match="Cannot Delete From an Empty List"):
        cdll.delete_tail()

    with pytest.raises(RuntimeError, match="Cannot Delete From an Empty List"):
        cdll.delete(1)

def test_insert_delete_single_node():
    cdll = CDLL()
    cdll.insert_head(DNode(1))
    assert cdll.size == 1

    cdll.delete_head()
    assert cdll.size == 0

    cdll.insert_tail(DNode(1))
    assert cdll.size == 1

    cdll.delete_tail()
    assert cdll.size == 0

def test_delete_node_not_found():
    cdll = CDLL()
    cdll.insert_head(DNode(1))

    with pytest.raises(ValueError, match="Node Not Found"):
        cdll.delete(2)

