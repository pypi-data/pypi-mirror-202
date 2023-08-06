class TNode():
    def __init__(self, data = None, parent = None, leftChild = None, rightChild = None, balance = None):
    # def __init__(self, data = None, balance = None, parent = None, leftChild = None, rightChild = None):
        if parent is None and leftChild is None and rightChild is None and balance == None:
            self.data = data
            self.parent = None
            self.leftChild = None
            self.rightChild = None 
            self.balance = 0
        else:
            self.data = data
            self.parent = parent
            self.leftChild = leftChild
            self.rightChild = rightChild
            self.balance = 0
    
    def setData(self, newData):
        self.data = newData
    
    def getData(self):
        return self.data
    
    def setBalance(self, newBalance):
        self.balance = newBalance
    
    def getBalance(self):
        return self.balance
    
    def setParent(self, newParent):
        self.parent = newParent
    
    def getParent(self):
        return self.parent
    
    def setLeftChild(self, newLeftChild):
        self.leftChild = newLeftChild
    
    def getLeftChild(self):
        return self.leftChild
    
    def setRightChild(self, newRightChild):
        self.rightChild = newRightChild
    
    def getRightChild(self):
        return self.rightChild
    
    def print(self):
        print(f'The balance of this node is {self.balance}.')
        print(f'This node contains value of {self.toString()}.')
        print(f'This node\'s parent is {self.parent}')
        print(f'This node\'s left child is {self.leftChild}')
        print(f'This node\'s right child is {self.rightChild}')
    
    def toString(self):
        return str(self.data)
    

    

