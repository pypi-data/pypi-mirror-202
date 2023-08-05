import pytest
import sys
import io
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from datastructures.Nodes.TNode import TNode
from datastructures.Trees.BST import BST

testNode1 = TNode(6)
testNode2 = TNode(4)
testNode3 = TNode(9)
testNode4 = TNode(2)
testNode5 = TNode(5)   
testNode6 = TNode(7)
testNode7 = TNode(3)


def is_bst_balanced(node):
    """
    Check if the given AVL tree node is balanced, i.e. all nodes to the left have values less than
    the node's value, and all nodes to the right have values greater than the node's value. Also
    checks that the tree is balanced according to the node's balance factor.
    """
    if node is None:
        return True

    if node.leftChild and node.leftChild.data > node.data:
        # the left subtree contains a node with a value greater than or equal to the current node
        return False

    if node.rightChild and node.rightChild.data < node.data:
        # the right subtree contains a node with a value less than or equal to the current node
        return False

    # recursively check the subtrees
    return is_bst_balanced(node.leftChild) and is_bst_balanced(node.rightChild)

def inorderTraversal(node):
    values = []
    if node is not None:
        values += inorderTraversal(node.leftChild)
        values.append(node.data)
        values += inorderTraversal(node.rightChild)
    return values

@pytest.mark.test_constructor
def test_constructor():
    testBST = BST()
    assert testBST.root == None

    testBST2 = BST(TNode(2))
    assert testBST2.root.data == 2
    assert testBST2.root.parent == None
    assert testBST2.root.leftChild == None
    assert testBST2.root.rightChild == None
    assert testBST2.root.balance == None

    testBST2 = BST(2)
    assert testBST2.root.data == 2
    assert testBST2.root.parent == None
    assert testBST2.root.leftChild == None
    assert testBST2.root.rightChild == None
    assert testBST2.root.balance == None

@pytest.mark.test_insert
def test_insert():
    testBST = BST(testNode1)
    testBST.insert(testNode2)
    testBST.insert(9)
    testBST.insert(2)
    testBST.insert(5)
    testBST.insert(testNode6)
    testBST.insert(testNode7)
    currentTestNode = testBST.root
    assert currentTestNode.data == 6
    assert currentTestNode.leftChild.data == 4
    assert currentTestNode.rightChild.data == 9
    assert currentTestNode.leftChild.leftChild.data == 2
    assert currentTestNode.leftChild.rightChild.data == 5
    assert currentTestNode.rightChild.leftChild.data == 7
    assert currentTestNode.leftChild.leftChild.rightChild.data == 3
    testBST.insert(2)
    testBST.insert(2)
    assert is_bst_balanced(testBST.root) == True

def setup():
    testBST = BST(6)
    testBST.insert(4)
    testBST.insert(9)
    testBST.insert(2)
    testBST.insert(5)
    testBST.insert(7)
    testBST.insert(3)
    return testBST

@pytest.mark.test_setAndGetRoot
def test_setAndGetRoot(): # does this new root need old root as a child along with it's children?
    testBST = setup()
    assert testBST.getRoot().data == 6
    testBST.setRoot(8)
    assert testBST.getRoot().data == 8
    assert testBST.getRoot().leftChild.data < 8
    assert testBST.getRoot().rightChild.data > 8
    assert is_bst_balanced(testBST.root) == True

@pytest.mark.test_delete
def test_delete():
    testBST = setup()
    testBST.insert(2)
    testBST.insert(2)
    testBST.delete(2)
    testBST.delete(6)
    testBST.delete(5)
    testBST.delete(4)
    testList = inorderTraversal(testBST.getRoot())
    assert (6 not in testList and 2 not in testList and 5 not in testList and 4 not in testList)
    assert is_bst_balanced(testBST.root) == True
    
@pytest.mark.test_search
def test_search():
    testBST = setup()
    assert testBST.search(2).data == 2
    assert testBST.search(6).data == 6
    assert testBST.search(5).data == 5
    assert testBST.search(4).data == 4
    assert testBST.search(1) == None
    assert testBST.search(8) == None
    assert testBST.search(10) == None

@pytest.mark.test_print
def test_print():
    testBST = setup()
    capturedOutput = io.StringIO()
    sys.stdout = capturedOutput
    testBST.printInOrder()
    actual_output = capturedOutput.getvalue()
    sys.stdout = sys.__stdout__
    expected_output = "2\n3\n4\n5\n6\n7\n9\n"
    assert actual_output == expected_output
    
    actual_output = ""
    capturedOutput = io.StringIO()
    sys.stdout = capturedOutput
    testBST.printBF()
    actual_output = capturedOutput.getvalue()
    expected_output = "6 \n4 9 \n2 5 7 \n3 \n"
    assert expected_output == actual_output

