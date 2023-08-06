import pytest
from myLib.datastructures.nodes.SNode import SNode
from myLib.datastructures.Linear.QueueLL import QueueLL

def test_queue_operations():
    queue = QueueLL()

    # Enqueue 0, 1, 2
    for i in range(3):
        queue.enqueue(SNode(i))
        assert queue.size == i + 1

    # Dequeue 0, Peek 1
    value = queue.dequeue()
    assert value == 0
    assert queue.peek() == 1
    assert queue.size == 2

    # Enqueue 3
    queue.enqueue(SNode(3))
    assert queue.peek() == 1
    assert queue.size == 3

    # Dequeue 1, Peek 2
    value = queue.dequeue()
    assert value == 1
    assert queue.peek() == 2
    assert queue.size == 2

    # Dequeue 2, Peek 3
    value = queue.dequeue()
    assert value == 2
    assert queue.peek() == 3
    assert queue.size == 1

    # Dequeue 3
    value = queue.dequeue()
    assert value == 3
    assert queue.size == 0

    # Check for empty queue errors
    with pytest.raises(RuntimeError, match="Cannot dequeue from an empty queue"):
        queue.dequeue()

    with pytest.raises(RuntimeError, match="Cannot peek at an empty queue"):
        queue.peek()

def test_queue_operations_depth():
    queue = QueueLL()

    # Test is_empty on an empty queue
    assert queue.is_empty()

    # Enqueue 0, 1, 2
    for i in range(3):
        queue.enqueue(SNode(i))

    # Check if the queue is not empty
    assert not queue.is_empty()

    # Test size of the queue
    assert queue.size == 3

    # Test peek
    assert queue.peek() == 0

    # Dequeue elements and check if they are in the correct order
    for i in range(3):
        assert queue.dequeue() == i

    # Test is_empty after dequeuing all elements
    assert queue.is_empty()

    # Test size of the empty queue
    assert queue.size == 0

    # Test error handling for peek and dequeue on an empty queue
    try:
        queue.peek()
    except RuntimeError as e:
        assert str(e) == "Cannot peek at an empty queue"

    try:
        queue.dequeue()
    except RuntimeError as e:
        assert str(e) == "Cannot dequeue from an empty queue"

    # Test enqueuing and dequeuing a large number of elements
    num_elements = 1000
    for i in range(num_elements):
        queue.enqueue(SNode(i))

    for i in range(num_elements):
        assert queue.dequeue() == i

    # Test is_empty after dequeuing all large number of elements
    assert queue.is_empty()


def test_enqueue_with_none():
    queue = QueueLL()
    with pytest.raises(TypeError):
        queue.enqueue(None)
    assert queue.is_empty()


def test_dequeue_with_empty_queue():
    queue = QueueLL()
    with pytest.raises(RuntimeError, match="Cannot dequeue from an empty queue"):
        queue.dequeue()
    assert queue.is_empty()

def test_peek_with_empty_queue():
    queue = QueueLL()
    with pytest.raises(RuntimeError, match="Cannot peek at an empty queue"):
        queue.peek()
    assert queue.is_empty()

def test_size_with_empty_queue():
    queue = QueueLL()
    assert queue.size == 0
    assert queue.is_empty()

def test_queue_operations_with_different_data_types():
    queue = QueueLL()
    data = [1, "string", 3.14, True, {"key": "value"}, [1, 2, 3]]

    # Enqueue elements with different data types
    for item in data:
        queue.enqueue(SNode(item))

    # Test size of the queue
    assert queue.size == len(data)

    # Dequeue elements and check if they match the input data
    for item in data:
        assert queue.dequeue() == item

    # Test is_empty after dequeuing all elements
    assert queue.is_empty()


def test_queue_operations_with_duplicates():
    queue = QueueLL()
    data = [1, 2, 3, 1, 2, 3]

    # Enqueue elements with duplicates
    for item in data:
        queue.enqueue(SNode(item))

    # Test size of the queue
    assert queue.size == len(data)

    # Dequeue elements and check if they match the input data
    for item in data:
        assert queue.dequeue() == item

    # Test is_empty after dequeuing all elements
    assert queue.is_empty()


def test_queue_operations_with_negative_numbers():
    queue = QueueLL()
    data = [-1, -2, -3, 0, 1, 2, 3]

    # Enqueue elements with negative numbers
    for item in data:
        queue.enqueue(SNode(item))

    # Test size of the queue
    assert queue.size == len(data)

    # Dequeue elements and check if they match the input data
    for item in data:
        assert queue.dequeue() == item

    # Test is_empty after dequeuing all elements
    assert queue.is_empty()





