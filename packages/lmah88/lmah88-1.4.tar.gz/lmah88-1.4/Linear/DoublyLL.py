import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from Nodes.DoublyNode import Node

# This class does not extend the SLL class as it requires too much rewriting.

class doublyLL:
    def __init__(self, newNode = None):
        self.head = newNode
        self.tail = newNode
        if newNode == None:
            self.size = 0
        else:
            self.size = 1

    # InsertHead(node): Inserts node at the head of the list
    def insertHead(self, newNode):
        if self.head is None:
            self.head = newNode
            self.tail = newNode
        else:
            self.head.prev = newNode
            newNode.next = self.head
            self.head = newNode
        self.size += 1


    # InsertTail(node): Inserts node at the tail of the list
    def insertTail(self, newNode):
        if self.head is None:
            self.head = newNode
            self.tail = newNode
        else:
            self.tail.next = newNode
            self.tail.next.prev = self.tail
            self.tail = self.tail.next
        self.size += 1

    # Insert(node, position): Inserts node a the specified position
    def insert(self, newNode, position): # DOUBLE CHECK: ASSUMING THAT THE POSITION STARTS FROM ZERO AND NOT ONE
        if position < 1 or position > (self.size + 1):
            print("Error. Out of range. Operation exited.")
        else:
            if self.head is None:
                self.head = newNode
                self.tail = newNode
            elif position == 1:
                self.head.prev = newNode
                newNode.next = self.head
                self.head = newNode
            elif position == self.size + 1:
                self.tail.next = newNode
                self.tail.next.prev = self.tail
                self.tail = self.tail.next
            
            else: # Insert at a specific position
                current_node = self.head
                for i in range(position - 2):
                    current_node = current_node.next

                newNode.next = current_node.next
                current_node.next.prev = newNode
                current_node.next = newNode
                newNode.prev = current_node

            self.size += 1

    # isSorted(self): Checks the current DLL to see if it is already sorted
    def isSorted(self): # DOUBLE CHECK: HOW DO WE KNOW THAT IT IS SORTED IN THIS ORDER?
        if self.head is None or self.head.next is None:
            return True
        current = self.head
        for i in range(self.size-1):
            if current.next.data < current.data:
                return False
            current = current.next
        return True
    
    #  SortedInsert(node): Inserts the node into its proper position in a sorted list
    def sortedInsert(self, newNode):
        if self.isSorted() == False:
            self.sort()

        if self.head is None:
            self.insertHead(newNode)
        elif newNode.data < self.head.data:
            self.insertHead(newNode)
        else:
            current_node = self.head
            while current_node.next is not None and current_node.next.data < newNode.data: # We should insert the newNode in the spot after the node this loop stops at
                current_node = current_node.next
            
            # Insert the item at the found position
            newNode.prev = current_node
            newNode.next = current_node.next

            if current_node.next is not None:
                current_node.next.prev = newNode
            else:
                self.tail = newNode

            current_node.next = newNode

            self.size += 1
            
        
    
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
            print("Error. There are no items in the list.")
        else:
            self.head = self.head.next # Set the head to the next item in the list (or none)

            if self.head is not None:
                self.head.prev = None # So it's not pointing to the old head
            else:
                self.tail = None # So that tail is not corrupt
            
            self.size -= 1
    
    def deleteTail(self):
        if self.tail is None:
            print("Error. There are no items in the list.")
        else:
            self.tail = self.tail.prev
            if self.tail is not None:
                self.tail.next = None
            else:
                self.head = None
            self.size -= 1
    
    def delete(self, delNode):
        # DOUBLE CHECK: JUST THE DATA HAS TO MATCH IN ORDER TO DELETE THIS
        # DOUBLE CHECK: IF THE DATA IS THE SAME FOR MANY NODES, DO WE DELETE ALL THE NODES OR JUST THE FIRST ONE?
        if delNode is None:
            return # If the deleted node is nothing
        if self.size == 0:
            return # If the list is empty
        
        else:
            current = self.head
            for i in range(0, self.size):
                if current == self.head and current.data == delNode.data:
                    self.deleteHead()
                elif current == self.tail and current.data == delNode.data:
                    self.deleteTail()
                elif current.data == delNode.data:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                    self.size -= 1
                current = current.next
           
    
    def sort(self):
        if self.head is None or self.head.next is None:
            return

        sorted_tail = self.head  # tail of the sorted portion of the list
        current = self.head.next  # node to be inserted into the sorted portion

        while current is not None:
            if current.data < sorted_tail.data:
                # remove current from its current position
                current.prev.next = current.next
                if current.next is not None:
                    current.next.prev = current.prev

                # find the node to insert current before
                sorted_node = sorted_tail
                while sorted_node is not None and current.data < sorted_node.data:
                    sorted_node = sorted_node.prev

                # insert current before sorted_node
                if sorted_node is None:
                    # insert at the beginning
                    current.prev = None
                    current.next = self.head
                    self.head.prev = current
                    self.head = current
                else:
                    current.prev = sorted_node
                    current.next = sorted_node.next
                    sorted_node.next = current
                    if current.next is not None:
                        current.next.prev = current
            else:
                sorted_tail = current

            current = current.next
    
    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0

    def print(self):
        print(f'The size of this doubly linked list is {self.size}.')
        if self.isSorted():
            print("This doubly linked list is sorted.")
        if not self.isSorted():
            print("This doubly linked list is not sorted.")
        print("This doubly linked list contains:")
        current = self.head
        for i in range(self.size):
            print(current.data)
            current = current.next


            
        
# Test Cases
# def main():  # Delete later
#     testDLL = doublyLL()
#     testNode1 = Node(1)
#     testNode2 = Node(2)
#     testNode3 = Node(3)
#     testNode4 = Node(4)
#     testNode5 = Node(5)   
#     testNode6 = Node(6)
#     testNode6_2 = Node(6)
#     testNode7 = Node(3)
#     testDLL.insertTail(testNode1)
#     testDLL.insertTail(testNode2)
#     testDLL.insertTail(testNode3) 
#     testDLL.insertTail(testNode4)
#     testDLL.insertTail(testNode5,)
#     testDLL.insertTail(testNode6)
#     testDLL.insertTail(testNode6_2)
#     testDLL.insertTail(testNode7)
#     testDLL.Print()


# if  __name__  == "__main__":
#     main()