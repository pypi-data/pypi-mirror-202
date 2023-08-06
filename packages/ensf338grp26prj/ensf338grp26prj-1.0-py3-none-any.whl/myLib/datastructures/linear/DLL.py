import inspect
import os
import sys
sys.path.append("..")
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from nodes.DNode import DNode

class DLL:
    """
    Doubly linked list implementation.
    """
    def __init__(self, node = None):
        """
        Initializes the doubly linked list.

        Args:
        - node (optional): the first node to be added to the list. Defaults to None.
        """
        self.head = node
        self.tail = node
        self.listSize = 0
        self.isSorted = True
        if(node is not None):
            self.tail.next = node
            self.tail.prev = node
            self.head.next = node
            self.tail.prev = node
            self.listSize = 1

    def _validate_DNode(self,node):
        """
        Validates that the passed object is a DNode object.

        Parameters:
        - node (DNode): the node object to be validated.
            
        Raises:
        - ValueError: If the passed object is not an instance of DNode.
        """
        if str(type(node).__name__) != "DNode":
            raise ValueError('Invalid parameter. The method excpects a DNode object to be passed to it.') 

    def InsertTail(self, new_DNode):
        """
        Inserts a new node at the end of the list.

        Parameters:
        - new_DNode (DNode): the new node to be inserted.
        """
        self._validate_DNode(new_DNode)
        self.isSorted = False
        if not self.head:
            self.head = new_DNode
            self.tail = self.head
        else:
            self.tail.next = new_DNode
            new_DNode.prev = self.tail
            self.tail = new_DNode
        self.listSize +=  1

    def InsertHead(self, new_DNode):
        """
        Inserts a new node at the beginning of the list.

        Parameters:
        - new_DNode (DNode): the new node to be inserted.
        """
        self._validate_DNode(new_DNode)
        self.isSorted = False
        if not self.head:
            self.head = new_DNode
            self.tail = self.head
        else:
            new_DNode.next = self.head
            self.head.prev = new_DNode
            self.head = new_DNode
        self.listSize +=  1

    def Delete(self, data):
        """
        Deletes the specified node from the list.

        Parameters:
        - data (DNode): the node to be deleted.
        """
        self._validate_DNode(data)
        current_DNode = self.head
        while current_DNode:
            if current_DNode == data:
                if current_DNode == self.head:
                    self.head = current_DNode.next
                    self.head.prev = None
                elif current_DNode == self.tail:
                    self.tail = current_DNode.prev
                    self.tail.next = None
                else:
                    current_DNode.prev.next = current_DNode.next
                    current_DNode.next.prev = current_DNode.prev
            current_DNode = current_DNode.next
        self.listSize -=  1

    def Search(self, node_data):
        """
        Searches for a node with the given data in the list.
        
        Args:
        - node_data: The data to be searched for.
            
        Returns:
        - The first node containing the data, or None if the data is not found.
        """
        self._validate_DNode(node_data)
        current_node = self.head

        while current_node is not None:
            if current_node == node_data:
                return current_node

            current_node = current_node.next

        return None
    
    def DeleteHead(self):
        """
        Deletes the first node in the list.
        """
        if self.head is None:
            return

        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self.listSize -=  1

    def Insert(self, new_DNode,index):
        """
        Insert a new node at the specified index in the linked list.

        Args:
        - new_DNode: A new node to be inserted.
        - index (int): Index at which the new node should be inserted.

        Raises:
        - ValueError: If the index is invalid.

        Returns:
        - None.
        """
        self._validate_DNode(new_DNode)
        if index < 0 or index > self.listSize:
            raise ValueError("Invalid index")
        self.isSorted = False

        if index == 0:
            self.InsertHead(new_DNode)
        elif index == self.listSize:
            self.InsertTail(new_DNode)
        else:
            current_node = self.head
            for i in range(index-1):
                current_node = current_node.next
            new_DNode.next = current_node.next
            new_DNode.prev = current_node
            current_node.next.prev = new_DNode
            current_node.next = new_DNode
            self.listSize += 1

    def DeleteTail(self):
        """
        Remove the last node from the linked list.
        """
        if self.tail is None:
            return

        if self.tail == self.head:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self.listSize -=  1
            
    def SortedInsert(self, new_node):
        """
        Inserts a new node into a doubly linked list while maintaining the list's sorted order.

        Args:
        - new_node: a node object to be inserted into the list

        Returns:
        - None
        """
        self._validate_DNode(new_node)
        if(self.isSorted == False):
            self.Sort()
        if self.head is None:
            self.head = new_node
            self.listSize +=  1
            return

        if new_node.data < self.head.data:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
            self.listSize +=  1
            return

        current_node = self.head
        while current_node.next is not None and current_node.next.data < new_node.data:
            current_node = current_node.next

        new_node.prev = current_node
        new_node.next = current_node.next

        if current_node.next is not None:
            current_node.next.prev = new_node

        current_node.next = new_node
        self.listSize +=  1
        
    def Print(self):
        """
        Prints the content of a doubly linked list and its current sorted status.
        """
        if(self.listSize == 0):
            print("There are no items in the data structure.")
            return
        sortedStatus = "sorted" if self.isSorted else "not sorted"
        print(f"The data structure has {self.listSize} elements and it's {sortedStatus}.")
        print("Here is the content of the list:")
        current_node = self.head
        while current_node is not None:
            print(f" - {current_node.data}")
            current_node = current_node.next
            
    def Clear(self):
        """
        Clears the content of a doubly linked list by setting head, tail, and listSize to None, None, and 0, respectively.

        Returns:
        - None
        """
        self.head = None
        self.tail = None  
        self.listSize = 0  
    
    def Sort(self):
        """
        Sorts a doubly linked list in non-descending order.

        Returns:
        - None
        """
        if self.head is None:
            return

        sorted_list = None
        current_node = self.head

        while current_node is not None:
            next_node = current_node.next
            sorted_list = self._sorted_insert(sorted_list, current_node)
            current_node = next_node

        self.head = sorted_list
        while self.head.prev is not None:
            self.head = self.head.prev
        self.isSorted = True
        
    def _sorted_insert(self, sorted_list, new_node):
        """
        Inserts a new node into a sorted doubly linked list.

        Args:
        - sorted_list: A node object that represents the head of the sorted list.
        - new_node: A node object that represents the node to be inserted.

        Returns:
        - A node object that represents the head of the updated sorted list.
        """
        if sorted_list is None:
            new_node.next = None
            new_node.prev = None
            return new_node

        if new_node.data < sorted_list.data:
            new_node.prev = None
            new_node.next = sorted_list
            sorted_list.prev = new_node
            return new_node

        current_node = sorted_list
        while current_node.next is not None and current_node.next.data < new_node.data:
            current_node = current_node.next

        new_node.prev = current_node
        new_node.next = current_node.next

        if current_node.next is not None:
            current_node.next.prev = new_node

        current_node.next = new_node

        return sorted_list


