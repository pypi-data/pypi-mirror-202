class DNode:
    def __init__(self, data=None, prev=None, next=None):
        self._data = data
        self._prev = prev
        self._next = next
    
    def get_data(self):
        return self._data
    
    def set_data(self, data):
        self._data = data
        
    def get_prev(self):
        return self._prev
    
    def set_prev(self, prev):
        self._prev = prev
        
    def get_next(self):
        return self._next
    
    def set_next(self, next):
        self._next = next
