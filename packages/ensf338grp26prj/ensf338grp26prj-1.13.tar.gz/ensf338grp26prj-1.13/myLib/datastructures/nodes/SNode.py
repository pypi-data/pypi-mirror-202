class SNode:
    """
    A class representing a node in a singly linked list.
    
    Attributes:
        data: The data stored in the node.
        next: The next node in the linked list.
    """
    
    def __init__(self, data):
        """
        Initializes a new instance of the SNode class.
        
        Args:
            data: The data to be stored in the node.
        """
        self.data = data
        self.next = None
