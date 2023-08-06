import pytest
from myLib.datastructures.Linear.StackLL import StackLL
from myLib.datastructures.nodes.SNode import SNode


def test_push():
    stack = StackLL()
    assert stack.size == 0

    stack.push(SNode(10))
    assert stack.size == 1
    assert stack.peek().data == 10

    stack.push(SNode(20))
    assert stack.size == 2
    assert stack.peek().data == 20

def test_pop():
    stack = StackLL()
    stack.push(SNode(10))
    stack.push(SNode(20))

    node = stack.pop()
    assert node.data == 20
    assert stack.size == 1

    node = stack.pop()
    assert node.data == 10
    assert stack.size == 0

    with pytest.raises(RuntimeError, match="Cannot Pop From An Empty Stack"):
        stack.pop()

def test_peek():
    stack = StackLL()
    stack.push(SNode(10))
    assert stack.peek().data == 10

    stack.push(SNode(20))
    assert stack.peek().data == 20

    with pytest.raises(RuntimeError, match="Cannot peek from an empty stack"):
        empty_stack = StackLL()
        empty_stack.peek()

def test_invalid_operations():
    stack = StackLL()
    stack.push(SNode(10))
    stack.push(SNode(20))

    stack.insert_tail(SNode(30))
    stack.insert(SNode(40), 1)
    stack.sorted_insert(SNode(50))
    stack.delete_tail()
    stack.delete(20)
    stack.sort()

    # Verify that the invalid operations didn't change the stack
    assert stack.size == 2
    assert stack.peek().data == 20

    node = stack.pop()
    assert node.data == 20

    node = stack.pop()
    assert node.data == 10

    assert stack.size == 0

def test_push_pop_peek_combination():
    stack = StackLL()

    # Push 10 items onto the stack
    for i in range(10):
        stack.push(SNode(i))
        assert stack.size == i + 1
        assert stack.peek().data == i

    # Pop and verify items in reverse order
    for i in range(9, -1, -1):
        node = stack.pop()
        assert node.data == i
        assert stack.size == i

        if i != 0:
            assert stack.peek().data == i - 1

    with pytest.raises(RuntimeError, match="Cannot Pop From An Empty Stack"):
        stack.pop()

    with pytest.raises(RuntimeError, match="Cannot peek from an empty stack"):
        stack.peek()

def test_invalid_operations_complex():
    stack = StackLL()
    for i in range(10):
        stack.push(SNode(i))

    # Perform invalid operations
    stack.insert_tail(SNode(10))
    stack.insert(SNode(11), 5)
    stack.sorted_insert(SNode(12))
    stack.delete_tail()
    stack.delete(3)
    stack.sort()

    # Verify that the invalid operations didn't change the stack
    assert stack.size == 10
    for i in range(9, -1, -1):
        node = stack.pop()
        assert node.data == i
        assert stack.size == i

def test_simple_interleaved_operations():
    stack = StackLL()

    # Push 0, 1, 2
    for i in range(3):
        stack.push(SNode(i))
        assert stack.peek().data == i
        assert stack.size == i + 1

    # Pop 2, Peek 1
    node = stack.pop()
    assert node.data == 2
    assert stack.peek().data == 1
    assert stack.size == 2

    # Push 3
    stack.push(SNode(3))
    assert stack.peek().data == 3
    assert stack.size == 3

    # Pop 3, Peek 1
    node = stack.pop()
    assert node.data == 3
    assert stack.peek().data == 1
    assert stack.size == 2

    # Pop 1, Peek 0
    node = stack.pop()
    assert node.data == 1
    assert stack.peek().data == 0
    assert stack.size == 1

    # Pop 0
    node = stack.pop()
    assert node.data == 0
    assert stack.size == 0

    # Check for empty stack errors
    with pytest.raises(RuntimeError, match="Cannot Pop From An Empty Stack"):
        stack.pop()

    with pytest.raises(RuntimeError, match="Cannot peek from an empty stack"):
        stack.peek()

