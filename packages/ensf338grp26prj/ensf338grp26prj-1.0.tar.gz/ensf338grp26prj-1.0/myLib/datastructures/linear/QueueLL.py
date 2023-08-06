import inspect
import os
import sys
sys.path.append("..")
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from linear.SLL import SLL

class QueueLL(SLL):
    """
    A queue class.
    """
    def __init__(self, node=None):
        """
        Initializes a new instance of the QueueLL class.
        """
        super().__init__(node)
        
    def InsertHead(self, node):
        pass

    def InsertTail(self, node):
        pass

    def Insert(self, node, position):
        pass

    def SortedInsert(self, node):
        pass

    def DeleteHead(self):
        pass

    def DeleteTail(self):
        pass
    
    def Delete(self, data):
        pass

    def Search(self, node):
        pass

    def Sort(self):
        pass

    def Clear(self):
        """
        Removes all nodes from the queue.
        """
        super().Clear()

    def Print(self):
        """
        Prints the contents of the queue.
        """
        super().Print()
    
    def enqueue(self, node):
        """
        Adds a new node to the tail of the queue.
        """
        super().InsertTail(node)

    def dequeue(self):
        """
        Removes the node at the head of the queue and returns it.
        """
        node = self.head
        super().DeleteHead()
        return node

    def front(self):
        """
        Returns the node at the head of the queue.
        """
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.tail

    def is_empty(self):
        """
        Returns True if the queue is empty, else False.
        """
        return self.head is None

    def size(self):
        """
        Returns the number of elements in the queue.
        """
        return self.listSize



