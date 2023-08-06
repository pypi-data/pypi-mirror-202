import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from linear.SLL import SLL
from nodes.SNode import SNode

class QueueLL(SLL):

    def __init__(self, newNode = None):
        super().__init__(newNode)

    def Enqueue(self, newNode):
        super().InsertTail(newNode)

    def Dequeue(self):
        super().DeleteHead()

    def Clear(self):
        super().Clear()
           
            
    def IsSorted(self):
        return

    def Sort(self):
        return

    def Search(self, newNode):
        return super().Search(newNode)


    def Print(self):
        print(f'The size of this singly linked list queue is {self.size}.')
        if self.IsSorted():
            print("This singly linked list queue is sorted.")
        if not self.IsSorted():
            print("This singly linked list queue is not sorted.")
        print("This singly linked list queue contains:")
        current = self.head
        while current != None:
            print(current.data)
            current = current.next

    def InsertHead(self, newNode):
        return
    
    def Insert(self, newNode, position):
        return 
    
    def Delete(self, delNode):
        return 
    
    def DeleteTail(self):
        return 
    
    def DeleteHead(self):
        return
    
    def InsertTail(self, newNode):
        return
    
    def SortedInsert(self, newNode):
        return
        
