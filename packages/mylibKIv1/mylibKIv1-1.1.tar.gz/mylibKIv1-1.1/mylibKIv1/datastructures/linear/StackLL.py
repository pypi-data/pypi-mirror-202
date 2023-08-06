from mylibKIv1.datastructures.nodes.SNode import SNode
from mylibKIv1.datastructures.linear.SLL import SLL


class Stack(SLL):
    def __init__(self):
        super().__init__()

    def push(self, node):
        super().InsertHead(node)

    def pop(self):
        if not self.head:
            return None
        else:
            node = self.head
            self.head = self.head.get_next()
            self.size -= 1
            return node

    def peek(self):
        return self.head

    # Override non-stack methods from singlyLL with empty body
    def InsertTail(self, node):
        pass

    def Insert(self, node, position):
        pass

    def Delete(self, node):
        pass
