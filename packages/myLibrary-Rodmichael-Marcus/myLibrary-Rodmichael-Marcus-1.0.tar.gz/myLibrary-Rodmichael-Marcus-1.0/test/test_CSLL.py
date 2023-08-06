import pytest
from myLib.datastructures.Linear.CSLL import CSLL
from myLib.datastructures.nodes.SNode import SNode

def test_insert_head():
    csll = CSLL()
    csll.insert_head(SNode(1))
    csll.insert_head(SNode(2))
    assert csll.head.data == 2
    assert csll.tail.next == csll.head

def test_insert_tail():
    csll = CSLL()
    csll.insert_tail(SNode(1))
    csll.insert_tail(SNode(2))
    assert csll.tail.data == 2
    assert csll.tail.next == csll.head

def test_insert():
    csll = CSLL()
    csll.insert(SNode(1), 0)
    csll.insert(SNode(2), 1)
    csll.insert(SNode(3), 1)
    assert csll.head.data == 1
    assert csll.head.next.data == 3
    assert csll.tail.data == 2
    assert csll.tail.next == csll.head

def test_sorted_insert():
    csll = CSLL()
    csll.sorted_insert(SNode(3))
    csll.sorted_insert(SNode(1))
    csll.sorted_insert(SNode(2))
    assert csll.head.data == 1
    assert csll.head.next.data == 2
    assert csll.tail.data == 3
    assert csll.tail.next == csll.head

def test_search():
    csll = CSLL()
    csll.insert_tail(SNode(1))
    csll.insert_tail(SNode(2))
    csll.insert_tail(SNode(3))
    assert csll.search(2) == csll.head.next
    assert csll.search(4) == None

def test_delete_head():
    csll = CSLL()
    csll.insert_tail(SNode(1))
    csll.insert_tail(SNode(2))
    csll.delete_head()
    assert csll.head.data == 2
    assert csll.tail.next == csll.head

def test_delete_tail():
    csll = CSLL()
    csll.insert_tail(SNode(1))
    csll.insert_tail(SNode(2))
    csll.delete_tail()
    assert csll.tail.data == 1
    assert csll.tail.next == csll.head

def test_delete():
    csll = CSLL()
    csll.insert_tail(SNode(1))
    csll.insert_tail(SNode(2))
    csll.insert_tail(SNode(3))
    csll.delete(2)
    assert csll.head.data == 1
    assert csll.head.next.data == 3
    assert csll.tail.data == 3
    assert csll.tail.next == csll.head

def test_sort():
    csll = CSLL()
    csll.insert_tail(SNode(3))
    csll.insert_tail(SNode(1))
    csll.insert_tail(SNode(2))
    csll.sort()
    assert csll.head.data == 1
    assert csll.head.next.data == 2
    assert csll.tail.data == 3
    assert csll.tail.next == csll.head

def test_clear():
    csll = CSLL()
    csll.insert_tail(SNode(1))
    csll.insert_tail(SNode(2))
    csll.clear()
    assert csll.head == None
    assert csll.tail == None
    assert csll.size == 0

def test_csll_print(capfd):
    csll = CSLL()
    csll.insert(SNode(1), 0)
    csll.insert(SNode(2), 1)
    csll.insert(SNode(3), 2)

    csll.print()
    
    captured = capfd.readouterr()
    expected_output = "List length: 3\nSorted status: Yes\nList content:\n1 -> 2 -> 3 -> Tail next: 1\n"
    assert captured.out == expected_output

def test_empty_csll():
    csll = CSLL()
    assert csll.head == None
    assert csll.tail == None
    assert csll.size == 0

def test_delete_from_empty_csll():
    csll = CSLL()
    with pytest.raises(RuntimeError):
        csll.delete_head()

def test_delete_nonexistent_node():
    csll = CSLL()
    csll.insert(SNode(1), 0)
    csll.insert(SNode(2), 1)
    with pytest.raises(ValueError):
        csll.delete(SNode(3))

def test_insert_into_empty_csll():
    csll = CSLL()
    csll.insert(SNode(1), 0)
    assert csll.head.data == 1
    assert csll.tail.data == 1

def test_sorted_insert_into_empty_csll():
    csll = CSLL()
    csll.sorted_insert(SNode(1))
    assert csll.head.data == 1
    assert csll.tail.data == 1

def test_sorted_insert_into_csll_with_one_node():
    csll = CSLL()
    csll.sorted_insert(SNode(1))
    csll.sorted_insert(SNode(2))
    assert csll.head.data == 1
    assert csll.tail.data == 2

def test_sorted_insert_into_sorted_csll():
    csll = CSLL()
    csll.sorted_insert(SNode(1))
    csll.sorted_insert(SNode(2))
    csll.sorted_insert(SNode(3))
    csll.sorted_insert(SNode(4))
    assert csll.head.data == 1
    assert csll.tail.data == 4

def test_sorted_insert_into_reverse_sorted_csll():
    csll = CSLL()
    csll.sorted_insert(SNode(4))
    csll.sorted_insert(SNode(3))
    csll.sorted_insert(SNode(2))
    csll.sorted_insert(SNode(1))
    assert csll.head.data == 1
    assert csll.tail.data == 4

def test_sorted_insert_into_unsorted_csll():
    csll = CSLL()
    csll.sorted_insert(SNode(3))
    csll.sorted_insert(SNode(2))
    csll.sorted_insert(SNode(4))
    csll.sorted_insert(SNode(1))
    assert csll.head.data == 1
    assert csll.tail.data == 4

def test_sort_empty_csll():
    csll = CSLL()
    csll.sort()
    assert csll.head == None
    assert csll.tail == None
    assert csll.size == 0

def test_sort_csll_with_one_node():
    csll = CSLL()
    csll.insert(SNode(1), 0)
    csll.sort()
    assert csll.head.data == 1
    assert csll.tail.data == 1

def test_sort_sorted_csll():
    csll = CSLL()
    csll.sorted_insert(SNode(1))
    csll.sorted_insert(SNode(2))
    csll.sorted_insert(SNode(3))
    csll.sorted_insert(SNode(4))
    csll.sort()
    assert csll.head.data == 1
    assert csll.tail.data == 4

def test_sort_reverse_sorted_csll():
    csll = CSLL()
    csll.sorted_insert(SNode(4))
    csll.sorted_insert(SNode(3))
    csll.sorted_insert(SNode(2))
    csll.sorted_insert(SNode(1))
    csll.sort()
    assert csll.head.data == 1
    assert csll.tail.data == 4

def test_sorted_insert_duplicates():
    csll = CSLL()
    csll.sorted_insert(SNode(3))
    csll.sorted_insert(SNode(1))
    csll.sorted_insert(SNode(2))
    csll.sorted_insert(SNode(2))
    assert csll.head.data == 1
    assert csll.head.next.data == 2
    assert csll.head.next.next.data == 2
    assert csll.tail.data == 3
    assert csll.tail.next == csll.head

def test_delete_only_node():
    csll = CSLL()
    csll.insert_tail(SNode(1))
    csll.delete(1)
    assert csll.head == None
    assert csll.tail == None
    assert csll.size == 0

def test_delete_invalid_data():
    csll = CSLL()
    csll.insert_tail(SNode(1))
    with pytest.raises(ValueError):
        csll.delete(2)
    assert csll.head.data == 1
    assert csll.tail.data == 1
    assert csll.tail.next == csll.head

def test_sort_empty():
    csll = CSLL()
    csll.sort()
    assert csll.head == None
    assert csll.tail == None
    assert csll.size == 0

def test_csll_print_empty(capfd):
    csll = CSLL()
    csll.print()
    captured = capfd.readouterr()
    expected_output = "List length: 0\nSorted status: Yes\nList content:\nTail next: None\n"
    assert captured.out == expected_output

