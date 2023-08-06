from .SLL import SLL

class CSLL(SLL):
    def __init__(self, head=None):
        super().__init__(head)
        if head:                        
            self.tail.next = self.head      # For CSLL, the next value of tail must be head to maintain circularity
        
    def insert_head(self, node):
        super().insert_head(node)
        self.tail.next = self.head          # To maintain circularity
    
    def insert_tail(self, node):
        super().insert_tail(node)
        self.tail.next = self.head          # To maintain circularity

    def insert(self, node, index):
        super().insert(node, index)
        self.tail.next = self.head      # If its inserted into first value, we must change tail node to point to the head node now
    
    def sorted_insert(self, node):
        current = self.head
        sorted_status = True

        index = 0
        while index < self.size - 1 and current.next:                             # Checks if the list is sorted
            if current.data > current.next.data:
                sorted_status = False
                break
            current = current.next
            index += 1

        if not sorted_status:                           # If not list is not sorted, sort the list
            self.sort()
        
        if self.head is None or self.head.data >= node.data:
            self.insert_head(node)
        else:
            current = self.head
            index = 0
            while index < self.size and current.next.data < node.data:      # Iterate until we find where data should be inserted
                current = current.next
                index += 1
            node.next = current.next
            current.next = node
            if index == self.size:
                self.tail = node
            self.size += 1
            self.tail.next = self.head                                               # Maintain circularity

    def search(self, data):
        current = self.head
        for element in range(self.size):        # Iterate through the size of the linked list
            if current.data == data:
                return current                  # Return correct value if it is found
            current = current.next
        return None                             # If it is not found, do not return anything

    def delete_head(self):
        if self.head is None:
            raise RuntimeError("Cannot Delete From an Empty List")
        if self.head == self.tail:              # Special case when there is only one node
            self.head = None
            self.tail = None
        else:                                   # Else, set tail next to the head next and self.head to head.next
            self.tail.next = self.head.next
            self.head = self.head.next
        self.size -= 1

    def delete_tail(self):
        super().delete_tail()
        if self.tail:                       # Maintain circularity, next of tail node now points to head
            self.tail.next = self.head

    def delete(self, data):
        if self.head is None:                           # Cannot delete from empty list, raise an error
            raise RuntimeError("Cannot Delete From an Empty List")
        
        if self.head and self.head.data == data:
            self.delete_head()                          # If data is at head node, undergo normal head deletion
            return
       
        current = self.head
        index = 0
        while current.next.data != data and index < self.size:       # Find Node with data, or until we iterate to end of linked list
            current = current.next
            index += 1                                                                                                              

        if index == self.size:                                        # Means we iterate through entire list
            raise ValueError("Node Not Found")

        if index == self.size - 1:                                    # The case of tail deltion, desired node is tail node
            self.delete_tail()
            return

        current.next = current.next.next                              # Set the Node next to the next of the next node            
        self.size -= 1
    
    def sort(self):
        if self.size <= 1:
            return

        sorted_list = CSLL()
        current = self.head
        for element in range(self.size):                    # Iterate through size of CSLL
            next_node = current.next
            current.next = None
            sorted_list.sorted_insert(current)              # Use sorted insert to put in correct place each time
            current = next_node

        self.head = sorted_list.head                        # Set head pointer to sorted_list head
        self.tail = sorted_list.tail                        # Set tail pointer to sorted_list tail
        self.tail.next = self.head                          # maintain circularity
    
    def clear(self):
        super().clear()
    
    def print(self):
        sorted_status = True
        index = 0
        current = self.head
        while index < self.size - 1 and current.next:                             # Checks if the list is sorted
            if current.data > current.next.data:
                sorted_status = False
                break
            current = current.next
            index += 1
        print(f"List length: {self.size}")
        print(f"Sorted status: {'Yes' if sorted_status else 'No'}")
        print("List content:")
        index = 0
        current = self.head
        while index < self.size:
            print(current.data, end=" -> ")
            current = current.next
            index += 1
        print("Tail next:", self.tail.next.data if self.tail else None)