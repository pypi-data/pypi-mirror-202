from pathlib import Path
import sys
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from Nodes.TNode import TNode

class BST:
    def __init__(self, arg = None):
        if arg == None:
            self.root = None
        elif isinstance(arg, int):
            self.root = TNode(arg)
        else: # If the argument is a TNode
            self.root = arg

    def setRoot(self, newRoot):
        nodesList = []
        def traverse(node):
            if node is not None:
                traverse(node.leftChild)
                nodesList.append(node)
                traverse(node.rightChild)
        traverse(self.root)

        if isinstance(newRoot, int):
            self.root = TNode(newRoot)
        elif isinstance(newRoot, TNode):
            self.root = newRoot
    
        for node in nodesList:
            self.insert(node)

    def getRoot(self):
        return self.root

    def insert(self, arg): 
        if isinstance(arg, int):
            node = TNode(arg)
        else: # If the argument is a TNode
            node = arg
        data = node.data
        
        current = self.root
        parent = None

        while current is not None:
            parent = current
            if data <= current.data:
                current = current.leftChild
            else:
                current = current.rightChild
        
        if self.root is None:
            self.root = node
        elif data <= parent.data:
            parent.leftChild = TNode(data, parent)
        else:
            parent.rightChild = TNode(data, parent)
    
    # NOTE: NEED TO WRITE UNIT TESTS FOR THE BOUNDARY CASE WHERE THERE ARE MANY NODES WITH THE SAME VALUE
    # Finds the node with val as data and delete it, if not found prints a statement that the value is not in the tree.
    def delete(self, value):
        # if self.root:
        while self.search(value):
            self.root = self._delete(value, self.root)
    
    def _delete(self, value, node): # HELPER METHOD
        if not node:
            return None
        
        if value < node.data:
            node.leftChild = self._delete(value, node.leftChild)
        elif value > node.data:
            node.rightChild = self._delete(value, node.rightChild)
        else:
            if not node.leftChild:
                return node.rightChild
            elif not node.rightChild:
                return node.leftChild
            else:
                min_node = self._find_min_node(node.rightChild)
                node.data = min_node.data
                node.rightChild = self._delete(min_node.data, node.rightChild)
        return node
    
    def _find_min_node(self, node): # HELPER METHOD
        while node.leftChild:
            node = node.leftChild
        return node


    def search(self, val):
        current = self.root
        while current is not None:
            if val == current.data:
                return current
            elif val < current.data:
                current = current.leftChild
            else:
                current = current.rightChild

    def printInOrder(self):
        def traverse(node):
            if node is not None:
                traverse(node.leftChild)
                print(node.data)
                traverse(node.rightChild)
        traverse(self.root)

    def printBF(self):
        queue = []
        queue.append(self.root)
        current_level_count = 1  # number of nodes in the current level
        next_level_count = 0  # number of nodes in the next level
        while len(queue) > 0:
            current = queue.pop(0) # Remove from the front of the queue
            print(current.data, end=' ')  # print without new line
            current_level_count -= 1
            if current.leftChild is not None:
                queue.append(current.leftChild)
                next_level_count += 1
            if current.rightChild is not None:
                queue.append(current.rightChild)
                next_level_count += 1
            if current_level_count == 0:
                # All nodes in the current level have been printed
                # Move to the next line and update counts
                print()
                current_level_count = next_level_count
                next_level_count = 0

    

def main():
    testNode1 = TNode(6)
    testNode2 = TNode(4)
    testNode3 = TNode(9)
    testNode4 = TNode(2)
    testNode5 = TNode(5)   
    testNode6 = TNode(7)
    testNode7 = TNode(3)
    testBST = BST(testNode1)
    testBST.insert(testNode2)
    testBST.insert(9)
    testBST.insert(2)
    testBST.insert(5)
    testBST.insert(testNode6)
    testBST.insert(testNode7)
    testBST.insert(2)
    testBST.insert(2)
    testBST.printBF()

if  __name__  == "__main__":
    main()    