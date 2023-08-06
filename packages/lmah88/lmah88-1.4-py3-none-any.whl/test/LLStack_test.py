import pytest
import sys
import io
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from datastructures.Linear.LLStack import LLStack
from datastructures.Nodes.SinglyNode import Node

testNode1 = Node(6)
testNode2 = Node(1)
testNode3 = Node(2)
testNode4 = Node(7)
testNode5 = Node(10)   
testNode6 = Node(3)
testNode6_2 = Node(3)
testNode7 = Node(4)

@pytest.mark.test_constructor
def test_constructor():
    testStack = LLStack()
    assert testStack.head == None
    assert testStack.tail == None
    testStack2 = LLStack(Node(2))
    assert testStack2.head.data == 2
    assert testStack2.tail.data == 2

@pytest.mark.test_push
def test_push():
    testStack = LLStack()
    testStack.push(testNode1)
    assert testStack.head.data == 6
    testStack.push(testNode2)
    testStack.push(testNode3) 
    testStack.push(testNode4)
    testStack.push(testNode5)
    assert testStack.head.next.next.data == 2
    testStack.push(testNode6)
    testStack.push(testNode7) # test push at head
    currentTestNode = testStack.head 
    testList = []
    for i in range(0, testStack.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next
    assert testList == [4,3,10,7,2,1,6]
    testStack.push(testNode6_2)
    testList = []
    currentTestNode = testStack.head
    for i in range(0, testStack.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next

    assert testList == [3,4,3,10,7,2,1,6]
    
def setup():
    testStack = LLStack()
    testStack.push(testNode1)
    testStack.push(testNode2)
    testStack.push(testNode3) 
    testStack.push(testNode4)
    testStack.push(testNode5)
    testStack.push(testNode6)
    testStack.push(testNode6_2)
    testStack.push(testNode7)
    return testStack

@pytest.mark.test_pop
def test_pop():
    testStack = setup()
    testStack.pop()
    assert testStack.head.data != 6
    testStack.pop()
    testStack.pop()
    currentTestNode = testStack.head
    testList = []
    for i in range(0, testStack.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next
    assert testList == [10,7,2,1,6]
    testStack.clear()
    assert testStack.size == 0 and testStack.head == None
        
@pytest.mark.test_search
def test_search():
    testStack = setup()
    testNode6Search = testStack.search(testNode7)
    assert testNode6Search == testNode7
    nonListNode = Node(99)
    testNonListNode = testStack.search(nonListNode)
    assert testNonListNode == None

@pytest.mark.test_print
def test_print():
    testStack = setup()
    captured_output = io.StringIO()
    sys.stdout = captured_output
    testStack.print()
    actual_output = captured_output.getvalue()

    sys.stdout = sys.__stdout__

    expected_output = "The size of this singly linked list stack is 8.\nThis singly linked list stack is not sorted.\nThis singly linked list stack contains:\n4\n3\n3\n10\n7\n2\n1\n6\n"
    assert actual_output ==  expected_output

@pytest.mark.test_detreimentFunctionality
def test_detrimentFunctionality():
    testStack = LLStack(testNode7)
    testStack.insertHead(testNode1)
    testStack.insert(testNode2,1)
    testStack.insertTail(testNode3)
    testStack.deleteHead()
    testStack.deleteTail()
    testStack.delete(testNode7)
    testList = []
    currentTestNode = testStack.head
    for i in range(testStack.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next
    assert testList == [4]
    testStack.push(Node(6))
    testStack.sort()
    testStack.sortedInsert(Node(8))

    testList = []
    currentTestNode = testStack.head
    for i in range(testStack.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next
    assert testList == [6, 4]
    
