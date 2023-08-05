import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from Linear.SinglyLL import singlyLL
from Nodes.SinglyNode import Node

class LLQueue(singlyLL):

    def __init__(self, newNode = None):
        super().__init__(newNode)

    def enqueue(self, newNode):
        super().insertTail(newNode)

    def dequeue(self):
        super().deleteHead()

    def clear(self):
        super().clear()
    
    # def sortedEneque(self, newNode): 
    #     sortNeeded = self.isSorted()
    #     if sortNeeded == False:
    #         self.enqueue(newNode)
    #         self.sort()
    #     else:
    #         self.enqueue(newNode)
       
            
    def isSorted(self):
        return

    def sort(self):
        return

    def search(self, newNode):
        return super().search(newNode)


    def print(self):
        print(f'The size of this singly linked list queue is {self.size}.')
        if self.isSorted():
            print("This singly linked list queue is sorted.")
        if not self.isSorted():
            print("This singly linked list queue is not sorted.")
        print("This singly linked list queue contains:")
        current = self.head
        while current != None:
            print(current.data)
            current = current.next

    def insertHead(self, newNode):
        return
    
    def insert(self, newNode, position):
        return 
    
    def delete(self, delNode):
        return 
    
    def deleteTail(self):
        return 
    
    def deleteHead(self):
        return
    
    def insertTail(self, newNode):
        return
    
    def sortedInsert(self, newNode):
        return
        
# def main():  # Delete later
#     testNode1 = Node(6)
#     testNode2 = Node(1)
#     testNode3 = Node(2)
#     testNode4 = Node(7)
#     testNode5 = Node(10)
#     testQueue = LLQueue(testNode1)
#     testQueue.enqueue(testNode2)
#     testQueue.enqueue(testNode3)
#     testQueue.enqueue(testNode4)
#     testQueue.enqueue(testNode5)
#     # testLL.sort()
#     testQueue.print()


# if  __name__  == "__main__":
#     main()


            



   
        


