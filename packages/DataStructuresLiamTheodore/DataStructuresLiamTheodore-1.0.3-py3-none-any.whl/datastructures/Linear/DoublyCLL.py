from pathlib import Path
import sys
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from Nodes.DoublyNode import Node
from Linear.DoublyLL import doublyLL

class doublyCLL(doublyLL):
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
            
    def insertHead(self, newNode):
        super().insertHead(newNode)
        self.tail.next = self.head
        self.head.prev = self.tail
        

    def insertTail(self, newNode):
        super().insertTail(newNode)
        self.tail.next = self.head
        self.head.prev = self.tail


    def insert(self, newNode, position):
        super().insert(newNode, position)
        if position == 1 or position == self.size:
            self.tail.next = self.head
            self.head.prev = self.tail

    def sortedInsert(self, newNode): # INCOMPLETE IMPLEMENTATION
        sortNeeded = self.isSorted()
        if sortNeeded == False:
            self.sort()

        if self.size == 0:
            self.insertHead(newNode)
        elif newNode.data < self.head.data:
            self.insertHead(newNode)
        elif newNode.data > self.tail.data:
            self.insertTail(newNode)
        else:
            current_node = self.head
            while current_node.next is not self.head and current_node.next.data < newNode.data:
                current_node = current_node.next
            newNode.prev = current_node
            newNode.next = current_node.next
            current_node.next.prev = newNode
            current_node.next = newNode
            self.size += 1


    def isSorted(self):
        return super().isSorted()

    def sort(self):
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

    def search(self, newNode):
        return(super().search(newNode))

    def deleteHead(self):
        super().deleteHead()
        self.tail.next = self.head
        self.head.prev = self.tail

    def deleteTail(self):
        super().deleteTail()
        self.tail.next = self.head
        self.head.prev = self.tail

    def delete(self, delNode):
        
        super().delete(delNode)
        
        self.tail.next = self.head
        self.head.prev = self.tail

    def clear(self):
        super().clear()

    def print(self):
        print(f'The size of this doubly circular linked list is {self.size}.')
        if self.isSorted():
            print("This doubly circular linked list is sorted.")
        if not self.isSorted():
            print("This doubly circular linked list is not sorted.")
        print("This doubly circular linked list contains:")
        current = self.head
        for i in range(self.size):
            print(current.data)
            current = current.next




# def main():
#     test1 = doublyCLL()
#     test1.insertHead(Node(1))
#     test1.insertHead(Node(2))
#     test1.insertTail(Node(11))
#     test1.insertTail(Node(7))
#     test1.insertTail(Node(3))
#     test1.insertTail(Node(60))
#     test1.insertTail(Node(4))
#     print(test1.search(Node(4)))
#     test1.sort()
#     test1.print()

#     # test2 = doublyCLL()
#     # test2.insertHead(Node(4))
#     # test2.insertHead(Node(3))
#     # test2.insertHead(Node(2))
#     # test2.sort()
#     # test2.print()

# if __name__ == "__main__":
#     main()

    
    
