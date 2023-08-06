# Binary Search Tree
from mylibKIv1.datastructures.nodes.TNode import TNode

class BST:
    def __init__(self, root=None) -> None:
        self.root = root

    @classmethod
    def BST(cls, input):
        if isinstance(input, int):
            input = TNode.TNode(input)
        return cls(input)
    
    def setRoot(self, newRoot):
        self.root = newRoot

    def getRoot(self):
        return self.root
    
    def Insert(self, input):

        if isinstance(input, int):
            new_node = TNode.TNode(input)
        else:
            new_node = input

        if self.root is None:
            self.root = new_node
            return
    
        current_node = self.root

        while True:
            if new_node.data < current_node.data:
                if current_node.L is None:
                    new_node.setP(current_node)
                    current_node.L = new_node
                    return
                else:
                    current_node = current_node.L
            elif new_node.data > current_node.data:
                if current_node.R is None:
                    new_node.setP(current_node)
                    current_node.R = new_node
                    return
                else:
                    current_node = current_node.R
            else:
                return


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
        return self._search(val, self.root)

    def _search(self, val, cur_node):
        if cur_node is None:
            return TNode.TNode(data=0,balance=None)
        elif cur_node.data == val:
            return cur_node
        elif val < cur_node.data:
            return self._search(val, cur_node.L)
        else:
            return self._search(val, cur_node.R)
        
    # make print out nicer?
    def printInOrder(self):
        return self._printInOrder(self.root)

    def _printInOrder(self, cur_node):
        if cur_node is not None:
            self._printInOrder(cur_node.L)
            print(cur_node.data)
            self._printInOrder(cur_node.R)

    # make look nicer?
    def printBF(self):
        if self.root is None:
            return

        cur_level = [self.root]
        while cur_level:
            next_level = []
            for node in cur_level:
                print(node.data, end=" ")
                if node.L:
                    next_level.append(node.L)
                if node.R:
                    next_level.append(node.R)
            print()
            cur_level = next_level