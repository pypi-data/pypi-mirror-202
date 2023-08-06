# AVL tree

from mylibKIv1.datastructures.nodes.TNode import TNode
from mylibKIv1.datastructures.trees.bst import BST

class AVL(BST):

    def __init__(self, root=None) -> None:
        super().__init__(root)

    @classmethod
    def AVL(cls, input):
        if isinstance(input, int):
            input = TNode.TNode(input)
        return cls(input)

    def setRoot(self, node):
        self.root = node
        AVL.update_balances(self.root)
        AVL.rebalance(node)

    def getRoot(self):
        return self.root
    
    def Insert(self, input):
        super().Insert(input)
        AVL.update_balances(self.root)
        self.root = AVL.rebalance(self.root)

    def Delete(self, val):
        self.root = self._delete(self.root, val)

    def _delete(self, cur_node, val):
        if cur_node is None:
            return cur_node

        if val < cur_node.data:
            cur_node.L = self._delete(cur_node.L, val)
        elif val > cur_node.data:
            cur_node.R = self._delete(cur_node.R, val)
        else:
            # Case 1: Node with no children
            if cur_node.L is None and cur_node.R is None:
                cur_node = None
            # Case 2: Node with one child
            elif cur_node.L is None:
                cur_node = cur_node.R
            elif cur_node.R is None:
                cur_node = cur_node.L
            # Case 3: Node with two children
            else:
                temp = self._find_min(cur_node.R)
                cur_node.data = temp.data
                cur_node.R = self._delete(cur_node.R, temp.data)
        return cur_node

    def _find_min(self, cur_node):
        while cur_node.L is not None:
            cur_node = cur_node.L
        return cur_node
    
    def Search(self, val):
        return super().Search(val)

    def printInOrder(self):
        return super().printInOrder()

    def printBF(self):
        super().printBF()

    def rebalance(root):
        # Check if the root is not None
        if root is not None:
            # Recursively rebalance the left subtree
            AVL.rebalance(root.L)
            
            # Recursively rebalance the right subtree
            AVL.rebalance(root.R)
            
            # Check if the balance factor of the root is greater than 1 or less than -1
            if root.balance < -1:
                # If the balance factor of the left child is greater than or equal to 0, perform a right rotation
                if root.L.balance <= 0:
                    root = AVL.rotate_right(root)
                # Otherwise, perform a left-right rotation
                else:
                    root.L = AVL.rotate_left(root.L)
                    root = AVL.rotate_right(root)
            elif root.balance > 1:
                # If the balance factor of the right child is less than or equal to 0, perform a left rotation
                if root.R.balance >= 0:
                    root = AVL.rotate_left(root)
                # Otherwise, perform a right-left rotation
                else:
                    root.R = AVL.rotate_right(root.R)
                    root = AVL.rotate_left(root)
            
            # Recalculate the balance factor of the root
            AVL.update_balances(root)
            
            # Check if the rebalancing caused the root node to change
            if root.P is None:
                return root
            else:
                return root.P
            
        return None


    def rotate_left(node):
        """
        Performs a left rotation on the given node and returns the new root node.
        """
        new_root = node.R
        node.R = new_root.L
        new_root.L = node
        node.balance = node.balance + 1 - min(new_root.balance, 0)
        new_root.balance = new_root.balance + 1 + max(node.balance, 0)
        if node.R is not None:
            node.R.P = node
        if node.P is not None:
            node.P.R = new_root
        new_root.P = node.P
        node.P = new_root
        return new_root


    def rotate_right(node):
        """
        Performs a right rotation on the given node and returns the new root node.
        """
        new_root = node.L
        node.L = new_root.R
        new_root.R = node
        node.balance = node.balance - 1 - max(new_root.balance, 0)
        new_root.balance = new_root.balance - 1 + min(node.balance, 0)
        if node.L is not None:
            node.L.P = node
        # if node.P is not None:
        #     node.P.L = new_root
        new_root.P = node.P
        node.P = new_root
        return new_root
    
    def update_balances(node):
        """
        Recursively updates the balance values for an AVL tree rooted at the given node.
        """
        if node is None:
            return 0
        left_height = AVL.update_balances(node.L)
        right_height = AVL.update_balances(node.R)
        node.balance = right_height - left_height
        return max(left_height, right_height) + 1