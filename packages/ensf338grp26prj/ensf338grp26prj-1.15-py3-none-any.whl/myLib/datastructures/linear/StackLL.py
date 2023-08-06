import inspect
import os
import sys
sys.path.append("..")
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from linear.SLL import SLL

class StackLL(SLL):
    """
    A stack class
    """
    def __init__(self, node=None):
        """
        Initializes a new instance of the StackLL class.
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
        Removes all nodes from the stack.
        """
        super().Clear()

    def Print(self):
        """
        Prints the data of all nodes in the stack.
        """
        super().Print()
    
    def push(self, node):
        """
        Adds a new node to the top of the stack.
        """
        super().InsertHead(node)
    
    def pop(self):
        """
        Removes and returns the node at the top of the stack.
        """
        if self.is_empty():
            return
        first_in = self.head
        super().DeleteHead()
        return first_in
    
    def peek(self):
        """
        Returns the node at the top of the stack without removing it.
        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.head
    
    def is_empty(self):
        """
        Returns True if the stack is empty, False otherwise.
        """
        return self.head is None
    
    def size(self):
        """
        Returns the number of nodes in the stack.
        """
        return self.listSize



