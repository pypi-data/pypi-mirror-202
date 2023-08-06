from .SLL import SLL

class QueueLL(SLL):
    def __init__(self):
        super().__init__()

    # Enqueue: Add an element to the end of the queue
    def enqueue(self, node):
        if node is None:
            raise TypeError("None is not a valid input for enqueue")
        super().insert_tail(node)


    # Dequeue: Remove an element from the front of the queue
    def dequeue(self):
        if self.size == 0:
            raise RuntimeError("Cannot dequeue from an empty queue")
        value = self.head.data
        super().delete_head()
        return value
    
    def peek(self):
        if self.size == 0:
            raise RuntimeError("Cannot peek at an empty queue")
        return self.head.data

    def is_empty(self):
        return self.size == 0

    def size(self):
        return self.size

    # Override other methods that don't apply to queues
    def insert_head(self, node):
        pass

    def insert(self, node, index):
        pass

    def sorted_insert(self, node):
        pass

    def delete_head(self):
        pass

    def delete_tail(self):
        pass

    def delete(self, data):
        pass

    def sort(self):
        pass
