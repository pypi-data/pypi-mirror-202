import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from Trees.BST import BST
from Nodes.TNode import TNode

class AVL(BST):
    def __init__(self, arg = None):
        if arg == None:
            super().__init__()
        else:
            super().__init__(arg) # sets newNode as root 
            if self.root.leftChild is not None or self.root.rightChild is not None:
                node_list = self.inorder_traversal()
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
                        self.insert(node) 
    
    def inorder_traversal(self, node=None, node_list=None):
        if node_list is None:
            node_list = []
        if self.getRoot() is None:
            return
        if node is None:
            node = self.getRoot()
        queue = [node]
        while queue:
            curr_node = queue.pop(0)
            left_height = self.get_subtree_height(curr_node.leftChild)
            right_height = self.get_subtree_height(curr_node.rightChild)
            curr_node.balance = right_height - left_height
            node_list.append(curr_node)
            if curr_node.leftChild:
                queue.append(curr_node.leftChild)
            if curr_node.rightChild:
                queue.append(curr_node.rightChild)
        return node_list

    def get_subtree_height(self, node=None):
        if node is None:
            return -1
        left_height = self.get_subtree_height(node.leftChild)
        right_height = self.get_subtree_height(node.rightChild)
        return 1 + max(left_height, right_height)

    def balance_tree(self, insert):
        current = self.getRoot()
        pivot = current
        while current is not None:
            if current.balance > 0 or current.balance < 0:
                pivot = current
            if insert.data > current.data: # go right
                current = current.rightChild
            else:
                current = current.leftChild # go left

        if pivot.balance == 1 or pivot.balance == -1:
            if insert.data > pivot.data:
                son = pivot.rightChild
            else:
                son = pivot.leftChild
            ancestor = pivot.parent

            if pivot.balance == 1 and insert.data < pivot.data or pivot.balance == -1 and insert.data > pivot.data: # case 2:
                self.inorder_traversal()
                return
            
            insert = self.search(insert.data)

            if pivot.balance < 0 and insert.data <= son.data: # case 3a 
                self.rightRotate(pivot,son, ancestor, insert)
            
            elif pivot.balance > 0 and insert.data> son.data:  # case 3a
                self.leftRotate(pivot, son, ancestor, insert)
            
            else:
                if insert.data > son.data:
                    grandson = son.rightChild
                else:   
                    grandson = son.leftChild
                if pivot.balance < 0 and insert.data > son.data: # case 3b
                    self.leftRightRotate(pivot, son, grandson, ancestor,insert)
                
                elif pivot.balance > 0 and insert.data < son.data: # case 3b
                    self.rightLeftRotate(pivot, son, grandson,ancestor, insert)
        else: #case 1
            self.inorder_traversal()


    def rightRotate(self, pivot, son, ancestor, insert):
        if ancestor is not None:
            if ancestor.data > son.data:
                ancestor.leftChild = son
            else:
                ancestor.rightChild = son
            son.parent = ancestor
        pivot.leftChild = son.rightChild
        if son.rightChild is not None:
            son.rightChild.parent = pivot

        if pivot == self.getRoot():
            # pivot.leftChild = son.rightChild
            self.root = son
            son.parent = None
        son.rightChild = pivot
        pivot.parent = son
        
        #adjust balances
        pivot.balance = 0
        insert.balance = 0


    def leftRotate(self, pivot, son, ancestor, insert):
        if ancestor is not None:
            if ancestor.data < son.data:
                ancestor.rightChild = son
            else:
                ancestor.leftChild = son
            son.parent = ancestor

        pivot.rightChild = son.leftChild
        if son.leftChild is not None:
            son.leftChild.parent = pivot

        if pivot == self.getRoot():
            # pivot.rightChild = son.leftChild
            self.root = son
            son.parent = None
        son.leftChild = pivot
        pivot.parent = son
        
        #adjust balances
        pivot.balance = 0
        insert.balance = 0

    def rightLeftRotate(self, pivot, son, grandson, ancestor, insert):
        self.rightRotate(son, grandson, pivot, insert)
        self.leftRotate(pivot, grandson, ancestor, insert)
        if insert.balance > grandson.balance:
            pivot.balance = -1
        else:
            pivot.balance = 0
            son.balance = 1
        
        temp = insert
        while (temp != pivot.leftChild and temp != pivot.rightChild  and temp != son.leftChild and temp != son.rightChild) and grandson != insert:
            right = self.get_subtree_height(temp.rightChild)
            left = self.get_subtree_height(temp.leftChild)
            temp.balance = right - left
            temp = temp.parent

    def leftRightRotate(self, pivot, son, grandson,ancestor, insert):
        self.leftRotate(son,grandson,pivot, insert)
        self.rightRotate(pivot, grandson, ancestor, insert)
        if insert.balance < grandson.balance:
            pivot.balance = 1
        else:
            pivot.balance = 0
            son.balance = -1

        temp = insert
        while (temp != pivot.leftChild and temp != pivot.rightChild  and temp != son.leftChild and temp != son.rightChild) and grandson != insert:
            right = self.get_subtree_height(temp.rightChild)
            left = self.get_subtree_height(temp.leftChild)
            temp.balance = right - left
            temp = temp.parent

    def insert(self, arg):
        if isinstance(arg, int):
            node = TNode(arg)
        else:
            node = arg
        self.inorder_traversal()
        super().insert(node)
        self.balance_tree(node)
        
    def setRoot(self, newNode):
        if isinstance(newNode, int):
            newRoot = TNode(newNode)
        else:
            newRoot = newNode
        node_list = self.inorder_traversal() # store prexisting tree
        if newRoot.leftChild is not None or newRoot.rightChild is not None:
            self.root = newRoot
            node_list1 = self.inorder_traversal()
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
                    self.insert(node) 

        if node_list is not None: 
            self.root = newRoot
            for node in node_list:
                node.parent = None
                node.leftChild = None
                node.rightChild = None
                node.balance = 0
                self.insert(node)    
        else:
            self.root = newRoot

    def getRoot(self):
        return super().getRoot()
            
    def delete(self, data):
        super().delete(data)
        node_list = self.inorder_traversal()
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
                self.insert(node) 
    
    def search(self, data):
        return super().search(data)
    
    def printInOrder(self):
        super().printInOrder()
    
    def printBF(self):
        super().printBF()