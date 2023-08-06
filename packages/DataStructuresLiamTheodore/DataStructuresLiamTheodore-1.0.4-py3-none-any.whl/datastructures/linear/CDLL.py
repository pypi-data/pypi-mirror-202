from pathlib import Path
import sys
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from nodes.DNode import DNode
from linear.DLL import DLL

class CDLL(DLL):
    # Note that you can overload by including the exact same def statement (exact same method name, with same arguments) and when it is called on an instance of the child class, the override method will be called
    def __init__(self, newNode = None):
        self.head = newNode
        self.tail = newNode
        if newNode == None:
            self.size = 0
        else:
            self.head.next = self.head
            self.head.prev = self.head
            self.size = 1
            
    def InsertHead(self, newNode):
        super().InsertHead(newNode)
        self.tail.next = self.head
        self.head.prev = self.tail
        

    def InsertTail(self, newNode):
        super().InsertTail(newNode)
        self.tail.next = self.head
        self.head.prev = self.tail


    def Insert(self, newNode, position):
        super().Insert(newNode, position)
        if position == 1 or position == self.size:
            self.tail.next = self.head
            self.head.prev = self.tail

    def SortedInsert(self, newNode): # INCOMPLETE IMPLEMENTATION
        sortNeeded = self.IsSorted()
        if sortNeeded == False:
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
            newNode.prev = current_node
            newNode.next = current_node.next
            current_node.next.prev = newNode
            current_node.next = newNode
            self.size += 1


    def IsSorted(self):
        return super().IsSorted()

    def Sort(self):
        i = self.head.next
        j = self.head
        for a in range(1, self.size): # a is some random variable to set the loop iterations
            key = i.data
            while j != self.tail and key < j.data:
                j.next.data = j.data
                j = j.prev
            j.next.data = key
            i = i.next
            j = i.prev

    def Search(self, newNode):
        return(super().Search(newNode))

    def DeleteHead(self):
        super().DeleteHead()
        self.tail.next = self.head
        self.head.prev = self.tail

    def DeleteTail(self):
        super().DeleteTail()
        self.tail.next = self.head
        self.head.prev = self.tail

    def Delete(self, delNode):
        
        super().Delete(delNode)
        
        self.tail.next = self.head
        self.head.prev = self.tail

    def Clear(self):
        super().Clear()

    def Print(self):
        print(f'The size of this doubly circular linked list is {self.size}.')
        if self.IsSorted():
            print("This doubly circular linked list is sorted.")
        if not self.IsSorted():
            print("This doubly circular linked list is not sorted.")
        print("This doubly circular linked list contains:")
        current = self.head
        for i in range(self.size):
            print(current.data)
            current = current.next




