from .SLL import SLL

class DLL(SLL):
    def __init__(self, head=None):
        super().__init__(head)          # Sane initiation for head and tail
        if head:
            head.prev = None            # Set node prev to None

    def insert_head(self, node):
        super().insert_head(node)
        if self.size > 1:               # If DLL is bigger than 1, set the next nodes prev pointer to the head node
            self.head.next.prev = self.head

    def insert_tail(self, node):        
        node.prev = self.tail           # Set the prev to current tail
        super().insert_tail(node)       # Same insertion otherwise

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
            current.next.prev = node                         # Update the prev pointer of the next node
            current.next = node
            node.prev = current                              # Update the prev pointer of the newly inserted node
            self.size += 1            

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
            node.prev = current                                         # Update the prev pointer of the newly inserted node
            current.next = node

            if node.next:  # Update the prev pointer of the next node if it exists
                node.next.prev = node
            else:  # If the new insertion is the last in the linked list, set the tail equal to it
                self.tail = node
            self.size += 1                                              # Increment size


    def search(self, data):                 # Not needed, but for readability, search is same as SLL
        return super().search(data)
    
    def delete_head(self):                  # Normal deletion, but set head node prev to None 
        super().delete_head()
        if self.head:
            self.head.prev = None

    def delete_tail(self):
        if self.size == 1:                  # If only 1 node, we can delete from head since its the same
            self.delete_head()
        else:
            self.tail = self.tail.prev
            self.tail.next = None
            self.size -= 1

    def delete(self, data):
        if self.head.data == data:        # For the case what we wanna delete is at the head
            self.delete_head()
        elif self.tail.data == data:      # For the case what we wanna delete is at the tail    
            self.delete_tail()
        else:
            node = self.search(data)      # Find node at with that 
            if node:                      # If it was able to find the node, delete it 
                node.prev.next = node.next
                node.next.prev = node.prev
                self.size -= 1
            else:                         # If it cannot find the node, raise ValueError
                raise ValueError("Node Not Found")
            
    def sort(self):
        if self.size <= 1:                # It is sorted if size is 0 or 1
            return

        sorted_list = DLL()               # Create new DLL to work from
        current = self.head
        while current:                    # Iterates through the DLL that contains the unsorted values
            next_node = current.next
            current.next = None
            current.prev = None
            sorted_list.sorted_insert(current)      # Efficiently uses sorted_insert() to insert into our sorted list
            if sorted_list.head.prev:               # Update the prev pointer of the head of the sorted_list
                sorted_list.head.prev = None
            current = next_node

        self.head = sorted_list.head                # Set head to the head of the sorted list
        self.tail = sorted_list.tail                # Set tail to the tail of the sorted list
    
    def clear(self):                                # Empty's the DLL, clears tail and head of each node
        current = self.head
        while current:
            next_node = current.next
            current.next = None
            current.prev = None
            current = next_node

        self.head = self.tail = None
        self.size = 0

    def print(self):
        current = self.head
        sorted_status = True
        while current and current.next:
            if current.data > current.next.data:
                sorted_status = False
                break
            current = current.next

        print(f"List length: {self.size}")
        print(f"Sorted status: {'Yes' if sorted_status else 'No'}")
        print("List content:")
        current = self.head
        while current:
            print(current.data, end=" <-> ")
            current = current.next
        print("None")    
