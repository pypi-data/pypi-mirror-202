class SLL:
    def __init__(self, head=None):              # Acts as both default and normal constructor from the part: head = None
        self.head = head
        self.tail = head
        self.size = 1 if head else 0            # If head exists default val of 1, without head it is 0

    def insert_head(self, node):
        if self.head is None:                   # If the linked list is empty, initialize both head and tail to the node
            self.head = self.tail = node
        else:                                   # Else, do normal insertion on head
            node.next = self.head
            self.head = node
        self.size += 1                          # Increment size
        
    def insert_tail(self, node):                  
        if self.tail is None:                   # If it is an empty linked list, initialize head and tail pointeres to the node
            self.head = self.tail = node
        else:
            self.tail.next = node               # Set current tail to point to new tail
            self.tail = node                    # Set tail to point to new node now, as it is tail inserttion
        self.size += 1                          # Increment size

    def insert(self, node, index):
        if index < 0 or index > self.size:                   # Throw an error if invalid index
            raise IndexError("Invalid Insertion Position")

        if index == 0:                                       # Is insertion from head
            self.insert_head(node)
        elif index == self.size:                             # Is insertion from tail       
            self.insert_tail(node)              
        else:
            current = self.head
            for element in range(index - 1):                 # Iterate to correct index
                current = current.next
            node.next = current.next
            current.next = node
            self.size += 1                                   # Increment Size


    def sorted_insert(self, node):
        current = self.head
        sorted_status = True

        while current and current.next:                             # Checks if the list is sorted
            if current.data > current.next.data:
                sorted_status = False
                break
            current = current.next

        if not sorted_status:                           # If not list is not sorted, sort the list
            self.sort()

        # Insert the node
        if self.head is None or self.head.data >= node.data:          # If linked list is empty, or if current smallest node bigger than the new node
            self.insert_head(node)
        else:                                                           # Else, iterate through sorted list until value finds proper insertion
            current = self.head
            while current.next and current.next.data < node.data:     # While there is a next node and and the next node is smaller than the new node
                current = current.next
            node.next = current.next
            current.next = node
            if current == self.tail:                                    # If the new insertionis the last in the linked list, set the tail equal to it
                self.tail = node
            self.size += 1                                              # Increment size

    def search(self, data):
        current = self.head
        while current:                                                  # Iterate until value is found or current.next does not exist (end of linked list)
            if current.data == data:                                  # Returns the value if it is found            
                return current
            current = current.next                                      # Used to iterate to next node
        return None                                                     # Return none if it cannot find the value

    def delete_head(self):                                              
        if self.head is None:                                           # If the linked list is empty, throw an error
            raise RuntimeError("Cannot Delete From an Empty List")

        self.head = self.head.next
        if self.size == 1:                                              # If the size was 1, we set tail to None since new size is 0 nodes in linked list
            self.tail = None
        self.size -= 1                                                  # Decrement size

    def delete_tail(self):
        if self.head is None:                                           # If the linked list is empty, throw an error
            raise RuntimeError("Cannot Delete From an Empty List")

        if self.size == 1:
            self.head = self.tail = None                                # If the size was 1, we set tail and head to None since new size is 0 nodes in linked list
        else:
            current = self.head
            while current.next != self.tail:                            # Must iterate through entire SLL untik we hit the next node is the tail
                current = current.next      
            current.next = None                                         # Set the to the last node we iterated until, so it points to None
            self.tail = current                                         # Set tail to this last node we interated until
        self.size -= 1                                                  # Decrement size

    def delete(self, data):
        if self.head is None:                                           # If the linked list is empty, throw an error as we cannot delete
                   raise RuntimeError("Cannot Delete From an Empty List")

        if self.head.data == data:                                    # For the case what we want to delete is the first value
            self.delete_head()
        else:                                                           # Else, undergo normal deletion
            current = self.head
            while current.next and current.next.data != data:         # Iterate until we find the node with the value, or end of SLL
                current = current.next

            if current.next is None:                                    # If we iterated until end of SLL, we did not find the value so return a ValueError
                raise ValueError("Node Not Found")

            if current.next == self.tail:                               # For the case the node to be deleted is the last node
                self.delete_tail()
            else:                                           
                current.next = current.next.next                        # Set the next to the next value of our deleted node
                self.size -= 1                                          # Decrement size 

    def sort(self):
        if self.size <= 1:                                              # SLL is already sorted if the size is 0 or 1
            return

        sorted_list = SLL()                                             # Create new SLL to work from
        current = self.head
        while current:                                                  # Iterates through the SLL that contains the unsorted values
            next_node = current.next
            current.next = None
            sorted_list.sorted_insert(current)                          # Efficiently uses sorted_insert() to insert into our sorted list
            current = next_node

        self.head = sorted_list.head                                    # Set head to the head of the sorted list
        self.tail = sorted_list.tail                                    # Set tail to the tail of the sorted list

    def clear(self):                                                    # Empty's the SLL, clears tail and head
        self.head = self.tail = None            
        self.size = 0

    def print(self):
        # First block of code is to find the sorted status
        current = self.head
        sorted_status = True
        while current and current.next:
            if current.data > current.next.data:
                sorted_status = False
                break
            current = current.next

        # This block is used to display the length, sorted status as found above, and the content of this SLL.
        print(f"List length: {self.size}")
        print(f"Sorted status: {'Yes' if sorted_status else 'No'}")
        print("List content:")
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")


