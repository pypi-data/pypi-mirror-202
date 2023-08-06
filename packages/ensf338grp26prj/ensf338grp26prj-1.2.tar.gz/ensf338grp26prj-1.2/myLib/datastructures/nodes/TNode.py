class TNode:
    """
    Represents a node in a binary tree.

    Attributes:
    - data: the data stored in the node
    - balance: the balance factor of the node in an AVL tree
    - parent: the parent node of this node
    - left: the left child node of this node
    - right: the right child node of this node
    """

    def __init__(self, data=None, balance=0, parent=None, left=None, right=None):
        """
        Initializes a new TNode object.

        Parameters:
        - data: the data to be stored in the node (default: None)
        - balance: the balance factor of the node (default: 0)
        - parent: the parent node of this node (default: None)
        - left: the left child node of this node (default: None)
        - right: the right child node of this node (default: None)
        """
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent
        self.balance = balance

    def set_data(self, data):
        """
        Sets the data of the node.

        Parameters:
        - data: the new data to be stored in the node
        """
        self.data = data

    def set_left(self, left):
        """
        Sets the left child node of the node.

        Parameters:
        - left: the new left child node
        """
        self.left = left

    def set_right(self, right):
        """
        Sets the right child node of the node.

        Parameters:
        - right: the new right child node
        """
        self.right = right

    def set_parent(self, parent):
        """
        Sets the parent node of the node.

        Parameters:
        - parent: the new parent node
        """
        self.parent = parent

    def set_balance(self, balance):
        """
        Sets the balance factor of the node.

        Parameters:
        - balance: the new balance factor
        """
        self.balance = balance

    def get_data(self):
        """
        Returns the data stored in the node.
        """
        return self.data

    def get_left(self):
        """
        Returns the left child node of the node.
        """
        return self.left

    def get_right(self):
        """
        Returns the right child node of the node.
        """
        return self.right

    def get_parent(self):
        """
        Returns the parent node of the node.
        """
        return self.parent

    def get_balance(self):
        """
        Returns the balance factor of the node.
        """
        return self.balance

    def print(self):
        """
        Prints the attributes of the node.
        """
        print("Data:", self.data)
        print("Left Child:", self.left)
        print("Right Child:", self.right)
        print("Parent:", self.parent)
        print("Balance:", self.balance)

    def __str__(self):
        """
        Return a string representation of the object.
        """
        return str(self.data)