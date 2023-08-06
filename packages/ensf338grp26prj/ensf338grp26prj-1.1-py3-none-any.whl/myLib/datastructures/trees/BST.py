import inspect
import os
import sys
sys.path.append("..")
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from nodes.TNode import TNode

class BST:
    """
    A Binary Search Tree class.

    Attributes:
    - root: The root node of the BST.
    """
    def __init__(self, arg=None):
        """
        Initializes a new instance of BST.

        Parameters:
        - arg: An optional argument to initialize the BST.
            If None, the root node will be None.
            If an integer, the root node will be created with the value of arg.
            If a TNode object, the root node will be set to arg.
            Otherwise, raises a TypeError.

        Returns:
        - None.
        """
        if not arg:
            self.root = None
        elif isinstance(arg, int):
            self.root = TNode(arg)
        elif str(type(arg).__name__) == "TNode":
            self.root = arg
        else:
            raise TypeError("Invalid argument type")

    def set_root(self, node):
        """
        Sets the root node of the BST.

        Parameters:
        - node: A TNode object to be set as the new root node.

        Returns:
        - None.

        Raises:
        - TypeError: If node is not a TNode object.
        """
        if isinstance(node, TNode):
            self.root = node
        else:
            raise TypeError("Invalid argument type")

    def get_root(self):
        """
        Returns the root node of the BST.

        Parameters:
        - None.

        Returns:
        - The root node of the BST.
        """
        return self.root

    def Insert(self, arg):
        """
        Inserts a node into the BST.

        Parameters:
        - arg: The value or TNode object to be inserted into the BST.

        Returns:
        - None.

        Raises:
        - TypeError: If arg is not an integer or a TNode object.
        """
        if isinstance(arg, int):
            node = TNode(arg)
        elif str(type(arg).__name__) == "TNode":
            node = arg
        else:
            raise TypeError("Invalid argument type")

        if self.root is None:
            self.root = node
            return
        curr = self.root
        while True:
            if node.get_data() == curr.get_data():
                break
            elif node.get_data() < curr.get_data():
                if curr.get_left() is None:
                    curr.set_left(node)
                    curr.get_left().set_parent(curr)
                    break
                else:
                    curr = curr.get_left()
            else:
                if curr.get_right() is None:
                    curr.set_right(node)
                    curr.get_right().set_parent(curr)
                    break
                else:
                    curr = curr.get_right()
        
        curr = node
        while curr is not None:
            self._update(curr)
            curr = curr.get_parent()

    def Delete(self, val):
        """
        Deletes a node with the given value from the BST.

        Parameters:
        - val: The value to be deleted from the BST.

        Returns:
        - None.
        
        Raises:
        - None.
        """
        if self.root is None:
            print("Value not found in the tree")
            return
        curr = self.root
        parent = None
        while curr is not None:
            if curr.get_data() == val:
                if curr.get_left() is None and curr.get_right() is None:
                    if parent is None:
                        self.root = None
                    elif curr == parent.get_left():
                        parent.set_left(None)
                    else:
                        parent.set_right(None)
                elif curr.get_left() is not None and curr.get_right() is None:
                    if parent is None:
                        self.root = curr.get_left()
                        curr.get_left().set_parent(parent)
                    elif curr == parent.get_left():
                        parent.set_left(curr.get_left())
                        curr.get_left().set_parent(parent)
                    else:
                        parent.set_right(curr.get_left())
                        curr.get_left().set_parent(parent)
                elif curr.get_left() is None and curr.get_right() is not None:
                    if parent is None:
                        self.root = curr.get_right()
                        curr.get_right().set_parent(parent)
                    elif curr == parent.get_left():
                        parent.set_left(curr.get_right())
                        curr.get_right().set_parent(parent)
                    else:
                        parent.set_right(curr.get_right())
                        curr.get_right().set_parent(parent)
                else:
                    min_node = self._find_min_node(curr.get_right())
                    self.Delete(min_node.get_data())
                    curr.set_data(min_node.get_data())

                node = parent
                while node is not None:
                    self._update(node)
                    node = node.get_parent()
                return

            elif val < curr.get_data():
                parent = curr
                curr = curr.get_left()
            else:
                parent = curr
                curr = curr.get_right()
        print("Value not found in the tree")

    def _find_min_node(self, node):
        """
        Finds the minimum node in a sub-tree.

        Parameters:
        - node: The root node of the sub-tree.

        Returns:
        - The minimum node in the sub-tree.
        """
        while node.get_left() is not None:
            node = node.get_left()
        return node

    def Search(self, val):
        """
        Searches for a node with the given value in the BST.

        Parameters:
        - val: The value to search for.

        Returns:
        - The node with the given value if found, None otherwise.
        """
        curr = self.root
        while curr is not None:
            if curr.get_data() == val:
                return curr
            elif val < curr.get_data():
                curr = curr.get_left()
            else:
                curr = curr.get_right()
        return None

    def printInOrder(self):
        """
        Prints the BST in-order traversal.

        Parameters:
        - None.

        Returns:
        - None.
        """
        self._print_in_order(self.root)
        print()

    def _print_in_order(self, node):
        """
        Recursive helper function to print the BST in-order traversal.

        Parameters:
        - node: The current node in the traversal.

        Returns:
        - None.
        """
        if node is not None:
            self._print_in_order(node.get_left())
            print(node.get_data(), end=" ")
            self._print_in_order(node.get_right())

    def printBF(self):
        """
        Prints the values of the tree's nodes in breadth-first order.
        """
        if self.root is None:
            print("Tree is empty.")
            return 
        current_level = [self.root]
        while current_level:
            next_level = []
            for node in current_level:
                print(node.get_data(), end=" ")
                if node.get_left():
                    next_level.append(node.get_left())
                if node.get_right():
                    next_level.append(node.get_right())
            print()
            current_level = next_level
        
    def _update(self, node):
        """
        Updates the balance factor of the given node and rebalances the subtree if necessary.

        Parameters:
        - node: The node to update.
        """
        left_height = self._height(node.get_left())
        right_height = self._height(node.get_right())
        node.set_balance(right_height - left_height)

    def _height(self, node):
        """
        Computes the height of the subtree rooted at the given node.

        Parameters:
        - node: The root node of the subtree to compute the height of.

        Returns:
        - The height of the subtree.
        """
        if node is None:
            return 0 
        else:
            left_height = self._height(node.get_left())
            right_height = self._height(node.get_right())
            return 1 + max(left_height, right_height)