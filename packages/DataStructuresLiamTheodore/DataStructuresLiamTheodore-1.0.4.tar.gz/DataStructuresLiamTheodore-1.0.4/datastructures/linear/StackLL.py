import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from linear.SLL import SLL
from nodes.SNode import SNode
class StackLL(SLL):
    def __init__(self, newNode = None):
        super().__init__(newNode)
    
    def Push(self, newNode): # Renamed push
        super().InsertHead(newNode)

    def InsertHead(self, newNode): # For overriding superclass method (now renamed to push)
        return

    def InsertTail(self, newNode): # Do nothing
        return

    def Insert(self, newNode, position): # Do nothing
        return

    def SortedInsert(self, newNode): # Do nothing
        return

    def IsSorted(self):
        return super().IsSorted()

    def Sort(self):
        return

    def Search(self, newNode):
        return (super().Search(newNode))

    def Pop(self): # Renamed pop
        super().DeleteHead()
    
    def DeleteHead(self): # For overriding superclass method
        return

    def DeleteTail(self): # Do nothing
        return

    def Delete(self, delNode): # Do nothing
        return

    def Clear(self):
        super().Clear()

    def Print(self):
        print(f'The size of this singly linked list stack is {self.size}.')
        if self.IsSorted():
            print("This singly linked list stack is sorted.")
        if not self.IsSorted():
            print("This singly linked list stack is not sorted.")
        print("This singly linked list stack contains:")
        current = self.head
        while current != None:
            print(current.data)
            current = current.next





