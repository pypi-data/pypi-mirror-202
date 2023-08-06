class DNode:
    """A class representing a node in a doubly-linked list.

    Attributes:
        data (object): The data stored in the node.
        prev (DNode): The previous node in the list.
        next (DNode): The next node in the list.
    """

    def __init__(self, data):
        """
        Initializes a new instance of the DNode class.
        
        Args:
            data: The data to be stored in the node.
        """
        self.data = data
        self.prev = None
        self.next = None
