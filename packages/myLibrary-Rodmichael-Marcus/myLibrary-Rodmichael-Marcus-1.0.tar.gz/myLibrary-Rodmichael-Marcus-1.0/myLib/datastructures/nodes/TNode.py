class TNode:
    def __init__(self, data=None, balance=0, parent=None, left=None, right=None):
        self.data = data
        self.balance = balance
        self.parent = parent
        self.left = left
        self.right = right

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def get_balance(self):
        return self.balance

    def set_balance(self, balance):
        self.balance = balance

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_left(self):
        return self.left

    def set_left(self, left):
        self.left = left

    def get_right(self):
        return self.right

    def set_right(self, right):
        self.right = right

    def __str__(self):
        return f"TNode(data={self.data}, balance={self.balance})"

    def __repr__(self):
        return self.__str__()

    def print(self):
        print("Node value: " + str(self.data))
        print("Left child: " + str(self.left))
        print("Right child: " + str(self.right))
        print("Parent: " + str(self.parent))
        print("Balance: " + str(self.balance))

    def to_string(self):
        return str(self.data)

    # Default constructor without arguments
    def TNode(self):
        self.data = None
        self.balance = 0
        self.parent = None
        self.left = None
        self.right = None   

    # Overloaded constructor that takes data, balance, parent, left, and right as arguments
    def TNode(self, data, balance, parent, left, right):
        self.data = data
        self.balance = balance
        self.parent = parent
        self.left = left
        self.right = right

    def update_balance(self):
            left_height = self.left.height() if self.left else -1
            right_height = self.right.height() if self.right else -1
            self.balance = right_height - left_height

    def height(self):
        left_height = self.left.height() if self.left else -1
        right_height = self.right.height() if self.right else -1
        return max(left_height, right_height) + 1