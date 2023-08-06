import pytest
from myLib.datastructures.Linear.DLL import DLL
from myLib.datastructures.nodes.DNode import DNode

def test_dll_insert_head():
    dll = DLL()
    dll.insert_head(DNode(1))
    assert dll.head.data == 1
    assert dll.tail.data == 1
    assert dll.head.prev is None
    assert dll.head.next is None
    assert dll.size == 1

    dll.insert_head(DNode(2))
    assert dll.head.data == 2
    assert dll.tail.data == 1
    assert dll.head.prev is None
    assert dll.head.next.data == 1
    assert dll.tail.prev.data == 2
    assert dll.tail.next is None
    assert dll.size == 2

def test_dll_insert_tail():
    dll = DLL()
    dll.insert_tail(DNode(1))
    assert dll.head.data == 1
    assert dll.tail.data == 1
    assert dll.head.prev is None
    assert dll.head.next is None
    assert dll.size == 1

    dll.insert_tail(DNode(2))
    assert dll.head.data == 1
    assert dll.tail.data == 2
    assert dll.head.prev is None
    assert dll.head.next.data == 2
    assert dll.tail.prev.data == 1
    assert dll.tail.next is None
    assert dll.size == 2

def test_dll_insert():
    dll = DLL()
    dll.insert(DNode(1), 0)
    dll.insert(DNode(2), 1)
    dll.insert(DNode(3), 2)
    dll.insert(DNode(4), 3)
    
    assert dll.size == 4
    assert dll.head.data == 1
    assert dll.head.next.data == 2
    assert dll.head.next.prev.data == 1
    assert dll.head.next.next.data == 3
    assert dll.head.next.next.prev.data == 2
    assert dll.tail.data == 4
    assert dll.tail.prev.data == 3

    dll.insert(DNode(0), 0)
    assert dll.size == 5
    assert dll.head.data == 0
    assert dll.head.prev is None
    assert dll.head.next.data == 1

def test_dll_sorted_insert():
    dll = DLL()
    dll.sorted_insert(DNode(1))
    dll.sorted_insert(DNode(3))
    dll.sorted_insert(DNode(2))

    assert dll.size == 3
    assert dll.head.data == 1
    assert dll.head.next.data == 2
    assert dll.head.next.prev.data == 1
    assert dll.tail.data == 3
    assert dll.tail.prev.data == 2

def test_dll_search():
    dll = DLL()
    dll.insert(DNode(1), 0)
    dll.insert(DNode(2), 1)
    dll.insert(DNode(3), 2)

    assert dll.search(2).data == 2
    assert dll.search(4) is None

def test_dll_delete_head():
    dll = DLL()
    dll.insert(DNode(1), 0)
    dll.insert(DNode(2), 1)
    dll.insert(DNode(3), 2)

    dll.delete_head()
    assert dll.size == 2
    assert dll.head.data == 2
    assert dll.head.prev is None
    assert dll.head.next.data == 3
    assert dll.tail.data == 3
    assert dll.tail.prev.data == 2

def test_dll_delete_tail():
    dll = DLL()
    dll.insert(DNode(1), 0)
    dll.insert(DNode(2), 1)
    dll.insert(DNode(3), 2)

    dll.delete_tail()
    assert dll.size == 2
    assert dll.head.data == 1
    assert dll.head.next.data == 2
    assert dll.tail.data == 2
    assert dll.tail.prev.data == 1
    assert dll.tail.next is None

def test_dll_delete():
    dll = DLL()
    dll.insert(DNode(1), 0)
    dll.insert(DNode(2), 1)
    dll.insert(DNode(3), 2)
    dll.insert(DNode(4), 3)

    dll.delete(2)
    assert dll.size == 3
    assert dll.head.data == 1
    assert dll.head.next.data == 3
    assert dll.head.next.prev.data == 1
    assert dll.tail.data == 4
    assert dll.tail.prev.data == 3

    with pytest.raises(ValueError):
        dll.delete(5)

def test_dll_sort():
    dll = DLL()
    dll.insert(DNode(3), 0)
    dll.insert(DNode(1), 1)
    dll.insert(DNode(4), 2)
    dll.insert(DNode(2), 3)

    dll.sort()

    assert dll.size == 4
    assert dll.head.data == 1
    assert dll.head.next.data == 2
    assert dll.head.next.prev.data == 1
    assert dll.head.next.next.data == 3
    assert dll.head.next.next.prev.data == 2
    assert dll.tail.data == 4
    assert dll.tail.prev.data == 3

def test_dll_clear():
    dll = DLL()
    dll.insert(DNode(1), 0)
    dll.insert(DNode(2), 1)
    dll.insert(DNode(3), 2)

    dll.clear()
    assert dll.size == 0
    assert dll.head is None
    assert dll.tail is None

def test_dll_print(capfd):
    dll = DLL()
    dll.insert(DNode(1), 0)
    dll.insert(DNode(2), 1)
    dll.insert(DNode(3), 2)

    dll.print()
    
    captured = capfd.readouterr()
    expected_output = "List length: 3\nSorted status: Yes\nList content:\n1 <-> 2 <-> 3 <-> None\n"
    assert captured.out == expected_output

def test_dll_sorted_insert_reverse_order():
    dll = DLL()
    dll.sorted_insert(DNode(4))
    dll.sorted_insert(DNode(3))
    dll.sorted_insert(DNode(2))
    dll.sorted_insert(DNode(1))

    assert dll.size == 4
    assert dll.head.data == 1
    assert dll.head.next.data == 2
    assert dll.head.next.prev.data == 1
    assert dll.head.next.next.data == 3
    assert dll.head.next.next.prev.data == 2
    assert dll.tail.data == 4
    assert dll.tail.prev.data == 3

def test_dll_sorted_insert_mixed_order():
    dll = DLL()
    dll.sorted_insert(DNode(2))
    dll.sorted_insert(DNode(1))
    dll.sorted_insert(DNode(4))
    dll.sorted_insert(DNode(3))

    assert dll.size == 4
    assert dll.head.data == 1
    assert dll.head.next.data == 2
    assert dll.head.next.prev.data == 1
    assert dll.head.next.next.data == 3
    assert dll.head.next.next.prev.data == 2
    assert dll.tail.data == 4
    assert dll.tail.prev.data == 3

def test_dll_sorted_insert_duplicate_values():
    dll = DLL()
    dll.sorted_insert(DNode(1))
    dll.sorted_insert(DNode(3))
    dll.sorted_insert(DNode(2))
    dll.sorted_insert(DNode(2))

    assert dll.size == 4
    assert dll.head.data == 1
    assert dll.head.next.data == 2
    assert dll.head.next.prev.data == 1
    assert dll.head.next.next.data == 2
    assert dll.head.next.next.prev.data == 2
    assert dll.tail.data == 3
    assert dll.tail.prev.data == 2


