from mylibKIv1.datastructures.nodes.DNode import DNode


class DLL:
    def __init__(self, head=None):
        self.head = head
        self.tail = head
        self.size = 0
        self.sorted = True

    def get_tail(self):
        return self.tail

    def InsertHead(self, node):
        if not self.head:
            self.head = node
            self.tail = node
        else:
            node.set_next(self.head)
            self.head.set_next(node)
            self.head = node
        self.size += 1
        self.sorted = False



    def InsertTail(self, node):
        if not self.tail:
            self.head = node
            self.tail = node
        else:
            self.tail.set_next(node)
            node.set_prev(self.tail)
            self.tail = node
        self.size += 1
        self.sorted = False

    def Insert(self, node, position):
        if position <= 0:
            self.InsertHead(node)
        elif position >= self.size:
            self.InsertTail(node)
        else:
            current = self.head
            count = 0
            while count < position:
                current = current.get_next()
                count += 1
            node.set_next(current)
            node.set_prev(current.GetPrev())
            current.GetPrev().set_next(node)
            current.set_prev(node)
            self.size += 1
            self.sorted = False

    def SortedInsert(self, node):
        if not self.head:
            self.InsertHead(node)
        elif self.sorted and node.get_data() < self.head.get_data():
            self.InsertHead(node)
        elif self.sorted and node.get_data() > self.tail.get_data():
            self.InsertTail(node)
        else:
            current = self.head
            while current.get_next() and current.get_next().get_data() < node.get_data():
                current = current.get_next()
            if current is self.head:
                node.set_next(self.head)
                self.head.set_prev(node)
                self.head = node
            else:
                node.set_next(current.get_next())
                node.set_prev(current)
                if current.get_next() != None:
                    current.get_next().set_prev(node)
                current.set_next(node)
            self.size += 1

    def Search(self, node):
        current = self.head
        while current:
            if current.get_data() == node.get_data():
                return current
            current = current.get_next()
        return None

    def DeleteHead(self):
        if not self.head:
            return
        if self.head is self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.get_next()
            self.head.set_prev(None)
        self.size -= 1

    def DeleteTail(self):
        if not self.tail:
            return
        if self.head is self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.GetPrev()
            self.tail.set_next(None)
        self.size -= 1

    def Delete(self, node):
        current = self.head
        while current:
            if current == node:
                if current is self.head:
                    self.head = current.get_next()
                    self.head.set_prev(None)
                elif current is self.tail:
                    self.tail = current.GetPrev()
                    self.tail.set_next(None)
                else:
                    current.GetPrev().set_next(current.get_next())
                    current.get_next().set_prev(current.GetPrev())
                self.size -= 1
                return True
            current = current.get_next()
        return False

    def Sort(self):
        #this dont work, it sorts fine but it doesnt set the tail to the correct value
        sorted_list = DLL()
        sorted_list.head = self.head
        sorted_list.tail = self.tail
        while True:
            if self.is_sorted():
                sorted_list.head = self.head
                sorted_list.tail = self.tail
                break
            if not self.is_empty():
                sorted_list = DLL()
                current = self.head
                while current is not None:
                    node = DNode(current.get_data())
                    sorted_list.SortedInsert(node)
                    current = current.get_next()
                self.head = sorted_list.head
                self.tail = sorted_list.tail
        sorted_list.find_tail()
        self.tail = sorted_list.get_tail()
    
    def Clear(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.sorted = True

    def Print(self):
        self.is_sorted()
        print(f"List length: {self.size}")
        print(f"Sorted status: {'Sorted' if self.sorted else 'Unsorted'}")
        print("List content:")
        current = self.head
        while current:
            print(current.get_data())
            current = current.get_next()
  

# HELPER FUNCTIONS
    def display(self):
        current = self.head
        while current is not None:
            print(current.get_data(), end=' -> ')
            current = current.get_next()
        print("None")

   
    def is_empty(self):
        return self.head is None
    
    def is_sorted(self):
        # if self.sorted:
        #     return True
        current = self.head
        while current is not None and current.get_next() is not None:
            if current.get_data() > current.get_next().get_data():
                return False
            current = current.get_next()
        self.sorted = True
        return True

   
    def find_tail(self):
        current_node = self.head
        while current_node.get_next() is not None:
            current_node = current_node.get_next()
        # set the tail to the last node
        self.tail = current_node