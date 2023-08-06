
class TNode:
    def __init__(self, data=None, balance=0, P=None, L=None, R=None) -> None:
        self.data = data
        self.balance = balance
        self.P = P
        self.L = L
        self.R = R

    @classmethod
    def TNode(cls, data, balance=0, P=None, L=None, R=None):
        return cls(data, balance, P, L , R)

    def setData(self, data):
        self.data = data

    def setBalance(self, balance):
        self.balance = balance

    def setP(self, P):
        self.P = P

    def setL(self, L):
        self.L = L

    def setR(self, R):
        self.R = R

    def getData(self):
        return self.data
        
    def getBalance(self):
        return self.balance
    
    def getP(self):
        return self.P
    
    def getL(self):
        return self.L
    
    def getR(self):
        return self.R

    def print(self):
        if self.balance == None:
            print("Does not exist in tree")
            return
        print(f"Data: {self.data}, Balance: {self.balance}, P: {self.P}, L: {self.L}, R: {self.R}")
    
    def toString(self):
        return str(self.data)