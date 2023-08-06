
from mylibKIv1.datastructures.linear.SLL import SLL

class Queue(SLL):
    def __init__(self):
        super().__init__()

    def enqueue(self, node):
        super().InsertHead(node)

    def dequeue(self):
        if self.size == 1:
            node = self.head
            self.head = None
            self.size -= 1
            return node
        second_last = self.head
        last = self.head.get_next()
        while True:

            second_last = last
            
            if last.get_next() == None:
                break
            last = last.get_next()
        self.DeleteTail()
        return second_last

    # Overriding methods with empty bodies
    def InsertTail(self, node):
        pass

    def SortedInsert(self, node):
        pass

    def Insert(self, node, position):
        pass

    def SortedInsert(self, node):
        pass
