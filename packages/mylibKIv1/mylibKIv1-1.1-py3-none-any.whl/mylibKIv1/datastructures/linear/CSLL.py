from mylibKIv1.datastructures.nodes.SNode import SNode
from mylibKIv1.datastructures.linear.SLL import SLL



class CSLL(SLL):
    def __init__(self, head=None):
        super().__init__(head)

    def InsertTail(self, node):
        if not self.head:
            self.head = node
            self.head.set_next(self.head)
        else:
            current = self.head
            while current.get_next() != self.head:
                current = current.get_next()
            current.set_next(node)
            node.set_next(self.head)
        self.size += 1
    
    def InsertHead(self, node):
        if not isinstance(node, SNode):
            raise TypeError("node argument must be an SNode object")
        if self.size == 0:
            node.next = node
        else:
            node.next = self.head
        self.head = node
        self.size += 1

    def Delete(self, node):
        if not self.head:
            return
        if self.head == node:
            if self.head.get_next() == self.head:
                self.head = None
            else:
                self.head = self.head.get_next()
            self.size -= 1
            return
        prev = self.head
        current = self.head.get_next()
        while current != self.head:
            if current == node:
                prev.set_next(current.get_next())
                self.size -= 1
                return
            prev = current
            current = current.get_next()
    
    def display(self):
        current = self.head
        count = 0
        while current is not None:
            print(current.get_data(), end=' -> ')
            current = current.get_next()
            count += 1
            if count >= self.size:
                break
            
        print("Repeat")

    def Print(self):
        self.is_sorted()
        print(f"List length: {self.size}")
        print(f"Sorted status: {'Sorted' if self.sorted else 'Unsorted'}")
        print("List content:")
        current = self.head
        count = 0
        while current:
            print(current.get_data())
            current = current.get_next()
            count += 1
            if count >= self.size:
                break
        
    def Sort(self):
        if not self.is_empty() and not self.is_sorted():
            sorted_list = SLL()
            current = self.head
            count = 0
            while current is not None:
                if count >= self.size:
                    break
                node = SNode(current.get_data())
                sorted_list.SortedInsert(node)
                current = current.get_next()

                count += 1
            self.head = sorted_list.head


    def SortedInsert(self, node):
        if self.is_empty() or node.get_data() < self.head.get_data():
            self.insert_head(node)
        else:
            current = self.head
            while current.get_next() is not None and current.get_next().get_data() < node.get_data():
                current = current.get_next()
            node.set_next(current.get_next())
            current.set_next(node)
        self.size += 1
