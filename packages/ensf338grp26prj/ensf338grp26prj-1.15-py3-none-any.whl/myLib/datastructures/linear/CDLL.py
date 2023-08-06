import inspect
import os
import sys
sys.path.append("..")
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from linear.DLL import DLL

class CDLL(DLL):
    """
    Circular doubly linked list implementation.
    """
    def __init__(self, node = None):
        """
        Initializes the circular doubly linked list.

        Args:
        - node (optional): the first node to be added to the list. Defaults to None.
        """
        super().__init__(node)

    def InsertTail(self, new_node):
        """
        Inserts a new node at the tail of the list.

        Args:
        - new_node: the new node to be inserted at the tail.
        """
        super().InsertTail(new_node)
        self.tail.next = self.head
        self.head.prev = self.tail
        
    def InsertHead(self, new_node):
        """
        Inserts a new node at the head of the list.

        Args:
        - new_node: the new node to be inserted at the head.
        """

        # self.ValidateIsSNode(new_node)
        self.isSorted = False
        super().InsertHead(new_node)
        self.tail.next = self.head
        self.head.prev = self.tail
        # self.listSize  += 1
        
    def Delete(self, node):
        """
        Deletes a node from the list.

        Args:
        - node: the node to be deleted from the list.
        """
        super()._validate_DNode(node)
        if self.head is None:
            return
        
        curr_node = self.head
        while curr_node != node and curr_node.next != self.head:
            curr_node = curr_node.next

        if curr_node == node:
            if curr_node == self.head:
                self.head = self.head.next
                self.head.prev = self.tail
                self.tail.next = self.head
            elif curr_node == self.tail:
                self.tail = self.tail.prev
                self.tail.next = self.head
                self.head.prev = self.tail
            else:
                curr_node.prev.next = curr_node.next
                curr_node.next.prev = curr_node.prev
        
        self.listSize -= 1

            
    def Insert(self, new_node, position):
        """
        Inserts a new node at a specific position in the list.

        Args:
        - new_node: the new node to be inserted.
        - position: the position in the list where the new node should be inserted.
        """

        super()._validate_DNode(new_node)
        self.isSorted = False
            
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return
        
        if position == 0:
            self.InsertHead(new_node)
            return
        
        curr_node = self.head
        curr_pos = 1
        
        while curr_pos != position and curr_node.next != self.head:
            curr_node = curr_node.next
            curr_pos += 1
            
        if curr_pos == position:
            curr_node.prev.next = new_node
            new_node.prev = curr_node.prev
            new_node.next = curr_node
            curr_node.prev = new_node
        else:
            self.InsertTail(new_node)
            
    def SortedInsert(self, new_node):
        """
        Inserts a new node in a sorted position in the list.

        Args:
        - new_node: the new node to be inserted in a sorted position in the list.
        """

        super()._validate_DNode(new_node)
        if(self.isSorted == False):
            self.Sort()
            
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return
        
        if new_node.data < self.head.data:
            self.InsertHead(new_node)
            return
        
        curr_node = self.head
        
        while curr_node.next != self.head and curr_node.next.data < new_node.data:
            curr_node = curr_node.next
            
        curr_node.next.prev = new_node
        new_node.next = curr_node.next
        new_node.prev = curr_node
        curr_node.next = new_node
        
        if curr_node == self.tail:
            self.tail = new_node
            
        self.listSize += 1

    def Search(self, key):
        """
        Searches for a node in the list.

        Args:
        - key: the key to search for in the list.

        Returns:
        - the node if found, or None if not found.
        """
        super()._validate_DNode(key)
        if self.head is None:
            return None
        
        curr_node = self.head
        
        while curr_node != key:
            curr_node = curr_node.next
            
            if curr_node == self.head:
                return None
                
        return curr_node
        
    def DeleteHead(self):
        """
        Deletes the node at the head of the list.
        """
        if self.head is None:
            return
        super().DeleteHead()
        if(self.head is not None):
            self.head.prev = self.tail
            self.tail.next = self.head
            
    def DeleteTail(self):
        """
        Deletes the node at the tail of the list.
        """
        if self.head is None:
            return
        
        super().DeleteTail()
        if(self.head is not None):
            self.head.prev = self.tail
            self.tail.next = self.head        
        

    def Sort(self):
        """
        Sorts the CDLL using the insertion sort algorithm.
        """
        if self.head is None:
            return
            
        curr_node = self.head.next
        while curr_node != self.head:
            key = curr_node.data
            prev_node = curr_node.prev
            while prev_node != self.head.prev and prev_node.data > key:
                prev_node.next.data = prev_node.data
                prev_node = prev_node.prev
            prev_node.next.data = key
            curr_node = curr_node.next
        self.isSorted = True

    def Print(self):
        """
        Prints the nodes in the list.
        """
        if(self.listSize == 0):
            print("There are no items in the data structure.")
            return
        sortedStatus = "sorted" if self.isSorted else "not sorted"
        print(f"The data structure has {self.listSize} elements and it's {sortedStatus}.")
        print("Here is the content of the list:")
        current_node = self.head
        while True:
            print(f" - {current_node.data}")
            current_node = current_node.next
            if current_node == self.head:
                break
            