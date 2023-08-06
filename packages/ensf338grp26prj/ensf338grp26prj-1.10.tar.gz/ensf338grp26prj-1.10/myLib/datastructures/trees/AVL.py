import inspect
import os
import sys
sys.path.append("..")
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from trees.BST import BST
from nodes.TNode import TNode

class AVL(BST):
    """
    An implementation of AVL tree, which is a self-balancing binary search tree.
    Inherits from BST (Binary Search Tree) class.

    Attributes:
    - root: The root node of the BST.
    """

    def __init__(self, arg=None):
        """
        Initializes a new AVL tree object.

        Parameters:
        - arg (optional): If provided, can be an integer or a TNode object.
        """
        super().__init__(arg)
        if self.root is not None:
            self._full_tree_balancing()

    def set_root(self, node):
        """
        Sets the root node of the AVL tree.

        Parameters:
        - node: A BSTNode object to be set as the new root node.
        """
        self.root = node
        if self.root is not None:
            self._full_tree_balancing()

    def get_root(self):
        """
        Returns 
        - The root node of the AVL tree.
        """
        return self.root    
    
    def _full_tree_balancing(self):
        """
        Balances the entire AVL tree to ensure it is height-balanced.
        """
        nodes = self._nodes()
        root = self._tree_balance(nodes, 0, len(nodes)-1)
        root.set_parent(None)
        self.root = root

    def _tree_balance(self, nodes, start, end):
        """
        Recursively balances a sub-tree of the AVL tree.

        Parameters:
        - nodes: A list of BSTNode objects to be balanced.
        - start: The starting index of the sub-tree.
        - end: The ending index of the sub-tree.
        Returns:
        - The root node of the balanced sub-tree.
        """
        if start > end:
            return None
        mid = int((start + end)/2)
        sub_root = nodes[mid]

        left_child = self._tree_balance(nodes, start, mid-1)
        sub_root.set_left(left_child)
        if left_child is not None:
            left_child.set_parent(sub_root)

        right_child = self._tree_balance(nodes, mid+1, end)
        sub_root.set_right(right_child)
        if right_child is not None:
            right_child.set_parent(sub_root)

        self._update(sub_root)
        
        return sub_root

    def _nodes(self):
        """
        Returns 
        - The list of all nodes in the AVL tree in ascending order.
        """
        nodes = []
        def traverse(node):
            if node is not None:
                traverse(node.left)
                nodes.append(node)
                traverse(node.right)
        traverse(self.root)
        return nodes

    def Insert(self, arg):
        """
        Inserts a new node into the AVL tree.

        Parameters:
        - arg: The value of the new node to be inserted. Can be an integer or a BSTNode object.
        """
        if isinstance(arg, int):
            super().Insert(arg)
            node = self.Search(arg)
            self._bring_balance(node)
        elif str(type(arg).__name__) == "TNode":
            super().Insert(arg)
            self._bring_balance(arg)
        else:
            raise TypeError("Invalid argument type")

    def Delete(self, val):
        """
        Deletes a node with the given value from the AVL tree.

        Parameters:
        - val: The value of the node to be deleted.
        """
        node = self.Search(val)
        super().Delete(val)
        if node is not None:
            parent = node.get_parent() 
            self._bring_balance(parent)

    def _bring_balance(self, node):
        """
        Bring balance to the tree by rotating nodes as necessary after an insert or delete operation.

        Parameters:
        - node (TNode): The node to start balancing the tree from.
        """
        unbalanced_node = self._unbalanced_node(node)
        if unbalanced_node:
            unbalance = unbalanced_node.get_balance()
            unbalanced_parent = unbalanced_node.get_parent()
            balanced_node = self._balanced_node(unbalanced_node)
            balanced_node.set_parent(unbalanced_parent)
            if unbalanced_parent is None:
                self.set_root(balanced_node)
            elif unbalance == -2:
                unbalanced_parent.set_left(balanced_node)
            else:
                unbalanced_parent.set_right(balanced_node)
        while node is not None:
            self._update(node)
            node = node.get_parent()        
    
    def _unbalanced_node(self, node):
        """
        Recursively check if any node is unbalanced and return the first unbalanced node found.

        Parameters:
        - node (TNode): The node to start checking for balance from.
        Returns:
        - The first unbalanced node found, or None if no unbalanced nodes were found.
        """
        if node is None:
            return None
        elif node.get_balance() == -2 or node.get_balance() == 2:
            return node
        else:
            return self._unbalanced_node(node.get_parent())

    def _right_rotate(self, node):
        """
        Perform a right rotation around the given node.

        Parameters:
        - node (TNode): The node around which to perform the rotation.
        Returns:
        - The new root node of the subtree after rotation.
        """
        left_child = node.get_left()
        node.set_left(left_child.get_right())
        left_child.set_right(node)
        node.set_parent(left_child)
        if node.get_left() is not None:
            node.get_left().set_parent(node)

        self._update(node)
        self._update(left_child)

        return left_child
    
    def _left_rotate(self, node):
        """
        Perform a left rotation around the given node.

        Parameters:
        - node (TNode): The node around which to perform the rotation.
        Returns:
        - The new root node of the subtree after rotation.
        """
        right_child = node.get_right()
        node.set_right(right_child.get_left())
        right_child.set_left(node)
        node.set_parent(right_child)
        if node.get_right() is not None:
            node.get_right().set_parent(node)

        self._update(node)
        self._update(right_child)

        return right_child
    
    def _balanced_node(self, node):
        """
        Determine which rotation case to use for the given node and perform the appropriate rotation.

        Parameters:
        - node (TNode): The node to balance.
        Returns:
        - The new root node of the subtree after rotation.
        """
        if node.get_balance() == -2:
            if node.get_left().get_balance() <= 0:
                return self._left_left_case(node)
            else:
                return self._left_right_case(node)
        elif node.get_balance() == 2:
            if node.get_right().get_balance() >= 0:
                return self._right_right_case(node)
            else:
                return self._right_left_case(node)
        return node

    def _left_left_case(self, node):
        """
        Perform a left-left rotation around the given node.

        Parameters:
        - node (TNode): The node around which to perform the rotation.
        Returns:
        - The new root node of the subtree after rotation.
        """
        return self._right_rotate(node)

    def _left_right_case(self, node):
        """
        Perform a left-right rotation around the given node.

        Parameters:
        - node (TNode): The node around which to perform the rotation.
        Returns:
        - The new root node of the subtree after rotation.
        """
        node.set_left(self._left_rotate(node.get_left()))
        return self._left_left_case(node)

    def _right_right_case(self, node):
        """
        Perform a right-right rotation around the given node.

        Parameters:
        - node (TNode): The node around which to perform the rotation.
        Returns:
        - The new root node of the subtree after rotation.
        """
        return self._left_rotate(node)

    def _right_left_case(self, node):
        """
        Perform a right-left rotation around the given node.

        Parameters:
        - node (TNode): The node around which to perform the rotation.
        Returns:
        - The new root node of the subtree after rotation.
        """
        node.set_right(self._right_rotate(node.get_right()))
        return self._right_right_case(node) 

