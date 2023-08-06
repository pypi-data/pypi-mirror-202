from mylibKIv1.datastructures.nodes.DNode import DNode
from mylibKIv1.datastructures.linear.DLL import DLL


class CDLL(DLL):
    def __init__(self, head=None):
        super().__init__(head)
        if self.head:
            self.head.set_prev(self.tail)
            self.tail.set_next(self.head)

    def InsertHead(self, node):
        super().InsertHead(node)
        self.head.set_prev(self.tail)
        self.tail.set_next(self.head)

    def InsertTail(self, node):
        super().InsertTail(node)
        self.head.set_prev(self.tail)
        self.tail.set_next(self.head)

    def Insert(self, node, position):
        super().Insert(node, position)
        self.head.set_prev(self.tail)
        self.tail.set_next(self.head)

    def DeleteHead(self):
        super().DeleteHead()
        self.head.set_prev(self.tail)
        self.tail.set_next(self.head)

    def DeleteTail(self):
        super().DeleteTail()
        self.head.set_prev(self.tail)
        self.tail.set_next(self.head)

    def Delete(self, node):
        if not self.head:
            return
        if node is self.head:
            self.DeleteHead()
        elif node is self.tail:
            self.DeleteTail()
        else:
            node.GetPrev().set_next(node.GetNext())
            node.GetNext().set_prev(node.GetPrev())
            self.size -= 1

    

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
        for i in range(self.size):
            if not self.is_empty() and not self.is_sorted():
                sorted_list = DLL()
                current = self.head
                count = 0
                while current is not None:
                    if count >= self.size:
                        break
                    node = DNode(current.get_data())
                    sorted_list.SortedInsert(node)
                    current = current.get_next()

                    count += 1
                self.head = sorted_list.head



# NOT NEEDED
    # def Sort(self):
    #     if not self.head or self.size <= 1:
    #         return
    #     current = self.head.GetNext()
    #     while current is not self.head:
    #         temp = current.GetPrev()
    #         while temp is not self.head.GetPrev() and temp.GetData() > current.GetData():
    #             temp = temp.GetPrev()
    #         if temp is not current.GetPrev():
    #             current.GetPrev().GetNext().set_prev(current.GetNext())
    #             current.GetNext().set_prev(current.GetPrev())
    #             if temp is self.head:
    #                 current.set_next(self.head)
    #                 self.head.set_prev(current)
    #                 self.head = current
    #             else:
    #                 current.GetPrev().set_next(current.GetNext())
    #                 current.GetNext().set_prev(current.GetPrev())
    #                 current.set_next(temp)
    #                 temp.set_prev(current)
    #             current = current.GetPrev()
    #         current = current.GetNext()
    #     self.sorted = True