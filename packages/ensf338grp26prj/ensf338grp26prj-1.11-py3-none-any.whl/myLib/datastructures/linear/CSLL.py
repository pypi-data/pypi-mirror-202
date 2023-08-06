import inspect
import os
import sys
sys.path.append("..")
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from linear.SLL import SLL

class CSLL(SLL):
    """
    Circular singly linked list implementation.
    """
    def __init__(self, node=None):
        """
        Initializes the CSLL object with the head and tail as None and the list size as 0. 

        Args:
        - node (SNode): The node object to initialize the list with.
        """
        super().__init__(node)
        if(node is not None):
            self.head.next = node
            self.tail.next = node
    
    def InsertHead(self, new_node):
        """
        Inserts a new node at the beginning of the linked list.

        Args:
        - new_node (SNode): The node object to be inserted.

        Raises:
        - ValueError: If the given object is not of type SNode.
        """
        super().InsertHead(new_node)
        self.tail.next = self.head
        self.head.prev = self.tail
        
    def InsertTail(self, new_node):
        """
        Inserts a new node at the end of the linked list.

        Args:
        - new_node (SNode): The node object to be inserted.

        Raises:
        - ValueError: If the given object is not of type SNode.
        """
        super()._validate_SNode(new_node)
        self.isSorted = False
        
        if self.tail is None:
            new_node.next = new_node
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.tail.next = new_node
            self.tail = new_node
        self.listSize += 1
    
    def Insert(self, new_node, position):
        """
        Inserts a new node at the specified position in the linked list.

        Args:
        - new_node (SNode): The node object to be inserted.
        - position (int): The position at which the node is to be inserted.

        Raises:
        - ValueError: If the position is greater than the size of the linked list or if the given object is not of type SNode.
        """
        # self._validate_SNode(new_node)
        self.isSorted = False
        
        if position > self.listSize - 1:
            raise ValueError('The insert position is greater than the linked list size.')
        if position == 0:
            if self.head is None:
                new_node.next = new_node
                self.head = new_node
                self.tail = new_node
            else:
                new_node.next = self.head
                self.head = new_node
                self.tail.next = new_node
        else:
            curr_node = self.head
            for i in range(position - 1):
                curr_node = curr_node.next

            new_node.next = curr_node.next
            curr_node.next = new_node
            if curr_node == self.tail:
                self.tail = new_node
        self.listSize += 1
        
    def SortedInsert(self, new_node):
        """
        Inserts a new node in the sorted position in the linked list.

        Args:
        - new_node (SNode): The node object to be inserted.

        Raises:
        - ValueError: If the given object is not of type SNode.
        """
        # self._validate_SNode(new_node)
        if not self.isSorted:
            self.Sort()
        if self.head is None:
            new_node.next = new_node
            self.head = new_node
            self.tail = new_node
            self.listSize += 1
            return

        if new_node.data < self.head.data:
            new_node.next = self.head
            self.head = new_node
            self.tail.next = new_node
            self.listSize += 1
            return

        current_node = self.head
        while current_node.next != self.head and current_node.next.data < new_node.data:
            current_node = current_node.next

        new_node.next = current_node.next
        current_node.next = new_node
        self.listSize += 1
        
    def Delete(self, data):
        """
        Removes the first occurrence of the specified data from the circular linked list.

        Args:
        - data: the data to be removed from the list

        Returns:
        - None
        """
        if self.head is None:
            return

        if self.head == self.tail and self.head == data:
            self.head = None
            self.tail = None
            self.listSize -= 1
            return

        if self.head == data:
            self.head = self.head.next
            self.tail.next = self.head
            self.listSize -= 1
            return

        current_node = self.head.next
        prev_node = self.head
        while current_node != self.head:
            if current_node == data:
                prev_node.next = current_node.next
                if current_node == self.tail:
                    self.tail = prev_node
                self.listSize -= 1
                return
            prev_node = current_node
            current_node = current_node.next
            

    def DeleteTail(self):
        """
        Removes the tail node from the circular linked list.
        """
        if self.tail is None:
            return

        if self.head == self.tail:
            self.head = None
            self.tail = None
            self.listSize = 0
            return

        current_node = self.head
        while current_node.next != self.tail:
            current_node = current_node.next
        current_node.next = self.head
        self.tail = current_node
        self.listSize -= 1

    def Clear(self):
        """
        Clears the circular linked list by resetting its head, tail, and size.
        """
        super().Clear()
        
    def Search(self, node):
        """
        Searches for the specified node in the circular linked list.

        Args:
        - node: the node to search for in the list

        Returns:
        - the node object if found, None otherwise
        """
        # self._validate_SNode(new_node)
        curr_node = self.head  
        while curr_node is not None:
            if curr_node is node:
                return curr_node
            if(curr_node.next == self.tail):
                return None
            curr_node = curr_node.next
        return None
    
    def Print(self):
        """
        Prints the contents of the circular linked list.
        """
        if(self.listSize == 0):
            print("There are no items in the data structure.")
            return
        sortedStatus = "sorted" if self.isSorted else "not sorted"
        print(f"The data structure has {self.listSize} elements and it's {sortedStatus}.")
        print("Here is the content of the list:")
        current_node = self.head
        for i in range(self.listSize):
            print(f" - {current_node.data}")
            current_node = current_node.next

    def DeleteHead(self):
        """
        Removes the head node from the circular linked list.
        """
        if self.head is None:
            return
        if self.head.next is self.tail:
            self.head = None
            self.tail = None
            self.listSize = 0
            return

        self.head = self.head.next
        self.tail.next = self.head
        self.listSize -= 1
    



    def Sort(self):
        if self.head is None or self.head == self.tail:
            return

        sorted_tail = self.head
        unsorted_head = self.head.next

        while unsorted_head != self.head:
            curr_node = unsorted_head
            unsorted_head = unsorted_head.next

            if curr_node.data < self.head.data:
                sorted_tail.next = curr_node.next
                curr_node.next = self.head
                self.head = curr_node
            elif curr_node.data >= sorted_tail.data:
                sorted_tail = curr_node
            else:
                prev_node = self.head
                while prev_node.next != curr_node and prev_node.next.data <= curr_node.data:
                    prev_node = prev_node.next
                sorted_tail.next = curr_node.next
                curr_node.next = prev_node.next
                prev_node.next = curr_node
        self.isSorted = True