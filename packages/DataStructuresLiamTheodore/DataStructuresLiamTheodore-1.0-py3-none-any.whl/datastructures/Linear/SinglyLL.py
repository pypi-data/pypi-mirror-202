import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from Nodes.SinglyNode import Node

class singlyLL():

    def __init__(self, newNode = None):
        if newNode is not None:
            self.head = newNode
            self.tail = newNode
            self.size = 1
        else:
            self.head = None
            self.tail = None
            self.size = 0
            
    def insertHead(self, newNode):
        if self.head is None:
            self.head = newNode
            self.tail = newNode
            self.size += 1
        else:
            newNode.next = self.head
            self.head = newNode
            self.size += 1
    
    def insertTail(self, newNode):
        if self.tail is None:
            self.head = newNode
            self.tail = newNode
            self.size += 1
        else:
            # newNode.tail = None
            self.tail.next = newNode
            self.tail = newNode
            self.size += 1

    def insert(self, newNode, position):
        if position < 1 or position > (self.size + 1):
            raise ValueError("Invalid position")
        
        if position == 1:
            self.insertHead(newNode)

        elif position == self.size + 1:
            self.insertTail(newNode)

        else:
            current = self.head
            for i in range(1, position - 1):
                current = current.next
            newNode.next = current.next
            current.next = newNode
            self.size += 1

    def sortedInsert(self, newNode):
        sortNeeded = self.isSorted()
        if sortNeeded == False:
            self.sort()

        if self.size == 0:
            self.insertHead(newNode)

        else:
            if newNode.data < self.head.data:
                self.insertHead(newNode)
            elif newNode.data > self.tail.data:
                self.insertTail(newNode)
            else:
                current = self.head.next
                while current.next != self.tail and current.next.data < newNode.data:
                    current = current.next
                newNode.next = current.next
                current.next = newNode
                self.size += 1
                    # if newNode.data > current.data :          
                    #     newNode.next = current.next
                    #     current.next = newNode
                    #     self.size += 1
                    #     break
                    # current = current.next
            
    def isSorted(self):
        if self.head is None or self.head.next is None:
            return True
        current = self.head
        for i in range(self.size-1):
            if current.next.data < current.data:
                return False
            current = current.next
        return True

    def sort(self):
        if self.head == None or self.head.next == None:
            return
        sorted_tail = self.head
        current = self.head.next        
        for i in range(self.size-1):
            if current.data < sorted_tail.data:
                sorted_tail.next = current.next # Cutting the current node out of the list 
               
                if current.data < self.head.data: # If the current node should be inserted at the beginning
                    current.next = self.head
                    self.head = current
                
                else:
                    sorted_node = self.head # Setting an additional pointer to the beginning of the list

                    while sorted_node != sorted_tail and current.data > sorted_node.next.data:
                        sorted_node = sorted_node.next # Iterates forwards and stops at a node where the current should be inserted after
                    current.next = sorted_node.next
                    sorted_node.next = current
            else:
                sorted_tail = current
            current = sorted_tail.next

        current = self.head
        for i in range(self.size-1): # better fix probably
            current = current.next
        self.tail = current

    def search(self, newNode):
        if self.size == 0:
            return None

        current = self.head
        for i in range(self.size):
            if current.data == newNode.data:
                return current
            else:
                current = current.next

        return None

    def deleteHead(self):
        if self.head is None:
            return
        elif self.head.next is None:
            self.head = None
            self.tail = None
            self.size -= 1
        else:
            self.head = self.head.next
            self.size -= 1

    def deleteTail(self):
        if self.tail is None:
            return
        current = self.head

        if current.next is None:
            self.tail = None
            self.head = None
            self.size -= 1
        while current.next != self.tail:
            current = current.next
        current.next = None
        self.tail = current
        self.size -= 1

    def delete(self, delNode):
        if self.size == 0:
            return
        elif self.size == 1:
            if self.head.data == delNode.data:
                self.head = None
                self.tail = None
                self.size -= 1
        else:
            current = self.head
            for i in range(1, self.size):
                if current == self.head and current.data == delNode.data:
                    self.head = current.next
                    self.size -= 1
                
                if current.next == None:
                    return
                
                elif current.next == self.tail:
                    if current.next.data == delNode.data:
                        self.deleteTail()
                    return
                
                elif current.next.data == delNode.data:
                    current.next = (current.next).next
                    current = current.next
                    self.size -= 1
                else:
                    current = current.next
    
    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0

    def print(self):
        print(f'The size of this singly linked list is {self.size}.')
        if self.isSorted():
            print("This singly linked list is sorted.")
        if not self.isSorted():
            print("This singly linked list is not sorted.")
        print("This singly linked list contains:")
        current = self.head
        while current != None:
            print(current.data)
            current = current.next
        
# def main():  # Delete later
#     testNode1 = Node(0)
#     testNode2 = Node(1)
#     testNode3 = Node(6)
#     testNode4 = Node(10)
#     testNode5 = Node(2)
#     testNode6 = Node(6)

#     testLL = singlyLL()
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


            



   
        



            

            




