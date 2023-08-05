import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from Linear.SinglyLL import singlyLL
from Nodes.SinglyNode import Node

class LLStack(singlyLL):
    def __init__(self, newNode = None):
        super().__init__(newNode)
    
    def push(self, newNode): # Renamed push
        super().insertHead(newNode)

    def insertHead(self, newNode): # For overriding superclass method (now renamed to push)
        return

    def insertTail(self, newNode): # Do nothing
        return

    def insert(self, newNode, position): # Do nothing
        return

    def sortedInsert(self, newNode): # Do nothing
        return

    def isSorted(self):
        return super().isSorted()

    def sort(self):
        return

    def search(self, newNode):
        return (super().search(newNode))

    def pop(self): # Renamed pop
        super().deleteHead()
    
    def deleteHead(self): # For overriding superclass method
        return

    def deleteTail(self): # Do nothing
        return

    def delete(self, delNode): # Do nothing
        return

    def clear(self):
        super().clear()

    def print(self):
        print(f'The size of this singly linked list stack is {self.size}.')
        if self.isSorted():
            print("This singly linked list stack is sorted.")
        if not self.isSorted():
            print("This singly linked list stack is not sorted.")
        print("This singly linked list stack contains:")
        current = self.head
        while current != None:
            print(current.data)
            current = current.next

# def main():
#     # test = LLStack(Node(2))
#     # test.push(Node(1))
#     # test.push(Node(3))
#     # test.pop()
#     # test.clear()
#     # newObj = (test.search(Node(1)))
#     # # print(newObj.data)
#     # test.print()

# if __name__ == "__main__":
#     main()



