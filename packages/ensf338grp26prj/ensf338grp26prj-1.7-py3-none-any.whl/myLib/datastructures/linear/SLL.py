import inspect
import os
import sys
sys.path.append("..")
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from nodes.SNode import SNode

class SLL:
    """
    A class representing a singly linked list.
    """
    def __init__(self,node = None):
        """
        Initializes a new instance of the SLL class.

        Args:
        - node (SNode): An SNode object representing the first node of the linked list.
        """
        self.head = node
        self.tail = node
        self.listSize = 0
        self.isSorted = True
        self.listsize = 0 if node == None else 1
        
    def _validate_SNode(self,node):
        """
        Validates that the input node is of type SNode.

        Args:
        - node (SNode): An SNode object.

        Raises:
        - ValueError: If the input node is not of type SNode.
        """
        if str(type(node).__name__) != "SNode":
            raise ValueError('Invalid parameter. The method excpects a SNode object to be passed to it.') 
    
    def InsertHead(self, new_node):
        """
        Inserts a new node at the beginning of the linked list.

        Args:
        - new_node (SNode): An SNode object representing the new node to be inserted.
        """
        if new_node is None:
            return
        self._validate_SNode(new_node)
        self.isSorted = False
        
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.listSize +=  1
        
        
    def InsertTail(self, new_node):
        """
        Inserts a new node at the end of the linked list.

        Args:
        - new_node (SNode): An SNode object representing the new node to be inserted.
        """
        if new_node is None:
            return
        
        self._validate_SNode(new_node)
        self.isSorted = False
        
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.listSize += 1
    
    
    def Insert(self,new_node,position):
        """
        Inserts a new node at the given position.

        Args:
            new_node (SNode): The new node to insert.
            position (int): The position at which to insert the new node.

        Raises:
            ValueError: If `position` is greater than or equal to the list size.

        Returns:
            None
        """
        self._validate_SNode(new_node)
        self.isSorted = False
        if position > self.listSize - 1:
            raise ValueError('the insert posistion is greater than the linked list size')
        if position == 0:
            new_node.next = self.head
            self.head = new_node
            if not self.tail:
                self.tail = new_node
        else:
            curr_node = self.head
            for i in range(position - 1):
                curr_node = curr_node.next

            new_node.next = curr_node.next
            curr_node.next = new_node
            if not new_node.next:
                self.tail = new_node
        self.listSize = self.listSize + 1
        
    def SortedInsert(self, new_node):
        """
        Inserts a new node in the sorted linked list.

        Args:
        - new_node: SNode object representing the new node to be inserted.

        Returns: None
        """
        self._validate_SNode(new_node)
            
        if(self.isSorted == False):
            self.Sort()
        
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.listSize += 1
            return

        if new_node.data < self.head.data:
            new_node.next = self.head
            self.head = new_node
            self.listSize += 1
            return

        current_node = self.head
        while current_node.next is not None and current_node.next.data < new_node.data:
            current_node = current_node.next

        new_node.next = current_node.next
        current_node.next = new_node
        self.listSize += 1

    def DeleteHead(self):
        """
        Deletes the head node of the linked list.

        Returns: None
        """
        self.head = self.head.next
        if(self.head is None):
            self.tail = None
        self.listSize -= 1
    
    def DeleteTail(self):
        """
        Deletes the tail node of the linked list.

        Returns: None
        """
        temp = self.head
        while(True and temp is not None):
            result = temp.next
            if(result is None):
                self.head = None
                self.tail = None
                self.listSize -= 1
                break
            if(result.next == None):
                self.tail = temp
                temp.next = None
                self.listSize -= 1
                break
            temp = temp.next
        
    def Sort(self):
        """
        Sorts the linked list in ascending order using the merge sort algorithm.

        Returns: None
        """
        if self.head is None:
            return

        left_half, right_half = self._split_list(self.head)

        left_half = self._merge_sort(left_half)
        right_half = self._merge_sort(right_half)

        self.head = self._merge(left_half, right_half)
        self.tail = self._get_last_node()
        self.isSorted = True
        
    def Delete(self, data):
        """
        Deletes a node from the linked list that contains the specified data.

        Args:
        - data: The data to be deleted from the linked list.

        Returns: None
        """
        self._validate_SNode(data)
        if self.head is None:
            return
        
        if self.head is data:
            self.head = self.head.next
        
        curr_node = self.head
        while curr_node is not None and curr_node.next is not None:
            if curr_node.next is data:
                temp = curr_node.next
                curr_node.next = temp.next
                self.listSize -= 1
                return
            curr_node = curr_node.next
            
        if self.head is None:
            self.tail = None
                
    def Clear(self):
        """
        Clears the linked list by setting its head, tail and size to None, None, and 0 respectively.

        Returns: None
        """
        self.head = None
        self.tail = None
        self.listSize = 0
               
    def Search(self, node):
        """
        Searches for a node in the linked list.

        Args:
        - node: The node to be searched for in the linked list.

        Returns:
        - The node object if it is found in the linked list, otherwise None.
        """
        self._validate_SNode(node)
        curr_node = self.head  
        while curr_node is not None:
            if curr_node is node:
                return curr_node
            curr_node = curr_node.next
        return None
    
    def _split_list(self, node):
        """
        Splits a linked list into two halves.

        Args:
        - node: The node to start the split from.

        Returns:
        - Two linked list halves, left and right.
        """
        if node is None:
            return None, None

        slow = node
        fast = node.next

        while fast is not None:
            fast = fast.next
            if fast is not None:
                slow = slow.next
                fast = fast.next

        left_half = node
        right_half = slow.next
        slow.next = None

        return left_half, right_half

    def _merge_sort(self, node):
        """
        Sorts a linked list using the merge sort algorithm.

        Args:
        - node: The node to start the sort from.

        Returns:
        - A sorted linked list.
        """
        if node is None or node.next is None:
            return node

        left_half, right_half = self._split_list(node)
        left_half = self._merge_sort(left_half)
        right_half = self._merge_sort(right_half)
        return self._merge(left_half, right_half)

    def _merge(self, left, right):
        """
        Merges two linked lists together.

        Args:
        - left: The left linked list to merge.
        - right: The right linked list to merge.

        Returns:
        - A merged linked list.
        """
        dummy = SNode(0)
        tail = dummy

        while left is not None and right is not None:
            if left.data < right.data:
                tail.next = left
                left = left.next
            else:
                tail.next = right
                right = right.next
            tail = tail.next

        if left is not None:
            tail.next = left
        else:
            tail.next = right

        return dummy.next


    def _get_last_node(self):
        """
        Returns the last node in the linked list.

        Returns:
        - The last node object.
        """
        current_node = self.tail
        while current_node.next is not None:
            current_node = current_node.next
        return current_node
    
    def Print(self):
        """
        Prints the contents of the linked list.

        Returns: None
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
            

