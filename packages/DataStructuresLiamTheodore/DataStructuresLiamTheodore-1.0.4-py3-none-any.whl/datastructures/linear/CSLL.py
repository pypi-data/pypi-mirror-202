import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from linear.SLL import SLL
from nodes.SNode import SNode
class CSLL(SLL):
     
    def __init__(self, newNode = None):
        if newNode == None:   
            super().__init__()
        else:
            self.head = newNode
            self.head.next = self.head
            self.tail = newNode
            self.size = 1

    def InsertHead(self, newNode):
        super().InsertHead(newNode)
        self.tail.next = self.head
    
    def InsertTail(self, newNode):
        super().InsertTail(newNode)
        self.tail.next = self.head

    def Insert(self, newNode, position):
        super().Insert(newNode, position)
        if position == 1:
            self.tail.next = newNode
        if position == self.size:
            self.tail.next = self.head
             
            
    def SortedInsert(self, newNode): 
        isSorted = self.IsSorted()
        if isSorted == False:
            self.Sort()

        if self.size == 0:
            self.InsertHead(newNode)

        elif newNode.data < self.head.data:
            self.InsertHead(newNode)
        elif newNode.data > self.tail.data:
            self.InsertTail(newNode)
        else:
            current_node = self.head
            while current_node.next is not self.head and current_node.next.data < newNode.data:
                current_node = current_node.next
            newNode.next = current_node.next
            current_node.next = newNode
            self.size += 1
    
    def IsSorted(self):
        return super().IsSorted()

    def Sort(self): # nope
        super().Sort()
        self.tail.next = self.head

    def Search(self, newNode):
        return(super().Search(newNode))

    def DeleteHead(self):
        super().DeleteHead()
        self.tail.next = self.head

    def DeleteTail(self):
        super().DeleteTail()
        self.tail.next = self.head

    def Delete(self, delNode):
        tailModNeeded = False
        if delNode == self.head or delNode == self.tail:
            tailModNeeded = True
        super().Delete(delNode)
        if tailModNeeded:
            self.tail.next = self.head
    
    def Clear(self):
        super().Clear()

    def Print(self):
        print(f'The size of this singly circular linked list is {self.size}.')
        if self.IsSorted():
            print("This singly circular linked list is sorted.")
        if not self.IsSorted():
            print("This singly circular linked list is not sorted.")
        print("This singly circular linked list contains:")
        current = self.head
        for i in range(self.size):
            print(current.data)
            current = current.next
        

# def main():  # Delete later
#     testNode1 = SNode(0)
#     testNode2 = SNode(1)
#     testNode3 = SNode(6)
#     testNode4 = SNode(10)
#     testNode5 = SNode(2)
#     testNode6 = SNode(6)

#     testLL = SCLL()
#     testLL.InsertTail(testNode1)
#     testLL.InsertTail(testNode2)
#     testLL.InsertTail(testNode3)
#     testLL.InsertTail(testNode4)
#     testLL.InsertTail(testNode6)
#     testLL.InsertTail(testNode5)
#     testLL.Delete(testNode6)
#     testLL.Print()
# if  __name__  == "__main__":
#     main()

