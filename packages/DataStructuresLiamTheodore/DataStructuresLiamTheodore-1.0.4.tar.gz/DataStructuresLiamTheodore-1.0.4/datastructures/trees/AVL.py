import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from trees.BST import BST
from nodes.TNode import TNode

class AVL(BST):
    def __init__(self, arg = None):
        if arg == None:
            super().__init__()
        else:
            super().__init__(arg) # sets newNode as root 
            if self.root.leftChild is not None or self.root.rightChild is not None:
                node_list = self._inorderTraversal()
                root = node_list[0]
                self.root = root
                root.balance = 0
                root.leftChild = None
                root.rightChild = None
                node_list.remove(root)
                for node in node_list:
                        node.parent = None
                        node.leftChild = None
                        node.rightChild = None
                        node.balance = 0
                        self.Insert(node) 
    
    def _inorderTraversal(self, node=None, node_list=None):
        if node_list is None:
            node_list = []
        if self.GetRoot() is None:
            return
        if node is None:
            node = self.GetRoot()
        queue = [node]
        while queue:
            curr_node = queue.pop(0)
            left_height = self._getSubtreeHeight(curr_node.leftChild)
            right_height = self._getSubtreeHeight(curr_node.rightChild)
            curr_node.balance = right_height - left_height
            node_list.append(curr_node)
            if curr_node.leftChild:
                queue.append(curr_node.leftChild)
            if curr_node.rightChild:
                queue.append(curr_node.rightChild)
        return node_list

    def _getSubtreeHeight(self, node=None):
        if node is None:
            return -1
        left_height = self._getSubtreeHeight(node.leftChild)
        right_height = self._getSubtreeHeight(node.rightChild)
        return 1 + max(left_height, right_height)

    def _balanceTree(self, Insert):
        current = self.GetRoot()
        pivot = current
        while current is not None:
            if current.balance > 0 or current.balance < 0:
                pivot = current
            if Insert.data > current.data: # go right
                current = current.rightChild
            else:
                current = current.leftChild # go left

        if pivot.balance == 1 or pivot.balance == -1:
            if Insert.data > pivot.data:
                son = pivot.rightChild
            else:
                son = pivot.leftChild
            ancestor = pivot.parent

            if pivot.balance == 1 and Insert.data < pivot.data or pivot.balance == -1 and Insert.data > pivot.data: # case 2:
                self._inorderTraversal()
                return
            
            Insert = self.Search(Insert.data)

            if pivot.balance < 0 and Insert.data <= son.data: # case 3a 
                self._rightRotate(pivot,son, ancestor, Insert)
            
            elif pivot.balance > 0 and Insert.data> son.data:  # case 3a
                self._leftRotate(pivot, son, ancestor, Insert)
            
            else:
                if Insert.data > son.data:
                    grandson = son.rightChild
                else:   
                    grandson = son.leftChild
                if pivot.balance < 0 and Insert.data > son.data: # case 3b
                    self._leftRightRotate(pivot, son, grandson, ancestor,Insert)
                
                elif pivot.balance > 0 and Insert.data < son.data: # case 3b
                    self._rightLeftRotate(pivot, son, grandson,ancestor, Insert)
        else: #case 1
            self._inorderTraversal()


    def _rightRotate(self, pivot, son, ancestor, Insert):
        if ancestor is not None:
            if ancestor.data > son.data:
                ancestor.leftChild = son
            else:
                ancestor.rightChild = son
            son.parent = ancestor
        pivot.leftChild = son.rightChild
        if son.rightChild is not None:
            son.rightChild.parent = pivot

        if pivot == self.GetRoot():
            # pivot.leftChild = son.rightChild
            self.root = son
            son.parent = None
        son.rightChild = pivot
        pivot.parent = son
        
        #adjust balances
        pivot.balance = 0
        Insert.balance = 0


    def _leftRotate(self, pivot, son, ancestor, Insert):
        if ancestor is not None:
            if ancestor.data < son.data:
                ancestor.rightChild = son
            else:
                ancestor.leftChild = son
            son.parent = ancestor

        pivot.rightChild = son.leftChild
        if son.leftChild is not None:
            son.leftChild.parent = pivot

        if pivot == self.GetRoot():
            # pivot.rightChild = son.leftChild
            self.root = son
            son.parent = None
        son.leftChild = pivot
        pivot.parent = son
        
        #adjust balances
        pivot.balance = 0
        Insert.balance = 0

    def _rightLeftRotate(self, pivot, son, grandson, ancestor, Insert):
        self._rightRotate(son, grandson, pivot, Insert)
        self._leftRotate(pivot, grandson, ancestor, Insert)
        if Insert.balance > grandson.balance:
            pivot.balance = -1
        else:
            pivot.balance = 0
            son.balance = 1
        
        temp = Insert
        while (temp != pivot.leftChild and temp != pivot.rightChild  and temp != son.leftChild and temp != son.rightChild) and grandson != Insert:
            right = self._getSubtreeHeight(temp.rightChild)
            left = self._getSubtreeHeight(temp.leftChild)
            temp.balance = right - left
            temp = temp.parent

    def _leftRightRotate(self, pivot, son, grandson,ancestor, Insert):
        self._leftRotate(son,grandson,pivot, Insert)
        self._rightRotate(pivot, grandson, ancestor, Insert)
        if Insert.balance < grandson.balance:
            pivot.balance = 1
        else:
            pivot.balance = 0
            son.balance = -1

        temp = Insert
        while (temp != pivot.leftChild and temp != pivot.rightChild  and temp != son.leftChild and temp != son.rightChild) and grandson != Insert:
            right = self._getSubtreeHeight(temp.rightChild)
            left = self._getSubtreeHeight(temp.leftChild)
            temp.balance = right - left
            temp = temp.parent

    def Insert(self, arg):
        if isinstance(arg, int):
            node = TNode(arg)
        else:
            node = arg
        self._inorderTraversal()
        super().Insert(node)
        self._balanceTree(node)
        
    def SetRoot(self, newNode):
        if isinstance(newNode, int):
            newRoot = TNode(newNode)
        else:
            newRoot = newNode
        node_list = self._inorderTraversal() # store prexisting tree
        if newRoot.leftChild is not None or newRoot.rightChild is not None:
            self.root = newRoot
            node_list1 = self._inorderTraversal()
            root = node_list1[0]
            node_list1.remove(root)
            root.balance = 0
            root.leftChild = None
            root.rightChild = None
            for node in node_list1:
                    node.parent = None
                    node.leftChild = None
                    node.rightChild = None
                    node.balance = 0
                    self.Insert(node) 

        if node_list is not None: 
            self.root = newRoot
            for node in node_list:
                node.parent = None
                node.leftChild = None
                node.rightChild = None
                node.balance = 0
                self.Insert(node)    
        else:
            self.root = newRoot

    def GetRoot(self):
        return super().GetRoot()
            
    def Delete(self, data):
        super().Delete(data)
        node_list = self._inorderTraversal()
        root = node_list[0]
        self.root = root
        root.balance = 0
        root.leftChild = None
        root.rightChild = None
        node_list.remove(root)
        for node in node_list:
                node.parent = None
                node.leftChild = None
                node.rightChild = None
                node.balance = 0
                self.Insert(node) 
    
    def Search(self, data):
        return super().Search(data)
    
    def printInOrder(self):
        super().printInOrder()
    
    def printBF(self):
        super().printBF()

  

  
