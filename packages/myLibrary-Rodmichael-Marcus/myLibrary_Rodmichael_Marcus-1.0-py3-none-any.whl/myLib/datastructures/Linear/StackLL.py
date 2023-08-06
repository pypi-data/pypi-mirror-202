from .SLL import SLL

class StackLL(SLL):
    def __init__(self, head=None):
        super().__init__(head)

    def push(self, node):                   # Inserts head, named push to go with stack naming conventions
        super().insert_head(node)

    def pop(self):                          # Deletes head, named pop to go with stack naming conventions
        if self.size == 0:
            raise RuntimeError("Cannot Pop From An Empty Stack")
        node = self.head                    # Get the top of stack
        super().delete_head()               # Delete the top of stack
        return node                         # Return the popped node 

    def peek(self):
        if self.size == 0:
            raise RuntimeError("Cannot peek from an empty stack")
        return self.head

    # The methods below are not applicable for a stack
    def insert_tail(self, node):
        pass

    def insert(self, node, index):
        pass

    def sorted_insert(self, node):
        pass

    def delete_tail(self):
        pass

    def delete(self, data):
        pass

    def sort(self):
        pass
