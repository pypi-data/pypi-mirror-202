import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from Linear.SinglyLL import singlyLL
from Nodes.SinglyNode import Node
class singlyCLL(singlyLL):
     
    def __init__(self, newNode = None):
        if newNode == None:   
            super().__init__()
        else:
            self.head = newNode
            self.head.next = self.head
            self.tail = newNode
            self.size = 1

    def insertHead(self, newNode):
        super().insertHead(newNode)
        self.tail.next = self.head
    
    def insertTail(self, newNode):
        super().insertTail(newNode)
        self.tail.next = self.head

    def insert(self, newNode, position):
        super().insert(newNode, position)
        if position == 1:
            self.tail.next = newNode
        if position == self.size:
            self.tail.next = self.head
             
            
    def sortedInsert(self, newNode): 
        isSorted = self.isSorted()
        if isSorted == False:
            self.sort()

        if self.size == 0:
            self.insertHead(newNode)

        # else:
        #     if newNode.data < self.head.data:
        #         self.insertHead(newNode) # need to use insert head and tail where the loop is created
        #     if newNode.data > self.tail.data:
        #         self.insertTail(newNode)
        #     else:
        #         current = self.head.next
        #         while current != self.tail:
        #             if newNode.data > current.data :          
        #                 newNode.next = current.next
        #                 current.next = newNode
        #                 self.size += 1
        #                 break
        elif newNode.data < self.head.data:
            self.insertHead(newNode)
        elif newNode.data > self.tail.data:
            self.insertTail(newNode)
        else:
            current_node = self.head
            while current_node.next is not self.head and current_node.next.data < newNode.data:
                current_node = current_node.next
            newNode.next = current_node.next
            current_node.next = newNode
            self.size += 1

        
        
                   
                
    def isSorted(self):
        return super().isSorted()

    def sort(self): # nope
        super().sort()
        self.tail.next = self.head

    def search(self, newNode):
        return(super().Search(newNode))

    def deleteHead(self):
        super().deleteHead()
        self.tail.next = self.head

    def deleteTail(self):
        super().deleteTail()
        self.tail.next = self.head

    def delete(self, delNode):
        tailModNeeded = False
        if delNode == self.head or delNode == self.tail:
            tailModNeeded = True
        super().delete(delNode)
        if tailModNeeded:
            self.tail.next = self.head
    
    def clear(self):
        super().clear()

    def print(self):
        print(f'The size of this singly circular linked list is {self.size}.')
        if self.isSorted():
            print("This singly circular linked list is sorted.")
        if not self.isSorted():
            print("This singly circular linked list is not sorted.")
        print("This singly circular linked list contains:")
        current = self.head
        for i in range(self.size):
            print(current.data)
            current = current.next
        

# def main():  # Delete later
#     testNode1 = Node(0)
#     testNode2 = Node(1)
#     testNode3 = Node(6)
#     testNode4 = Node(10)
#     testNode5 = Node(2)
#     testNode6 = Node(6)

#     testLL = singlyCLL()
#     testLL.insertTail(testNode1)
#     testLL.insertTail(testNode2)
#     testLL.insertTail(testNode3)
#     testLL.insertTail(testNode4)
#     testLL.insertTail(testNode6)
#     testLL.insertTail(testNode5)
#     testLL.delete(testNode6)
#     testLL.print()
# if  __name__  == "__main__":
#     main()

