import pytest
import sys
import io
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from datastructures.Nodes.TNode import TNode
from datastructures.Trees.AVL import AVL
from datastructures.Trees.BST import BST

def is_avl_balanced(node):
    """
    Check if the given AVL tree node is balanced, i.e. all nodes to the left have values less than
    the node's value, and all nodes to the right have values greater than the node's value. Also
    checks that the tree is balanced according to the node's balance factor.
    """
    if node is None:
        return True

    if node.balance not in [-1, 0, 1]:
        # the node is unbalanced
        return False

    if node.leftChild and node.leftChild.data > node.data:
        # the left subtree contains a node with a value greater than or equal to the current node
        return False

    if node.rightChild and node.rightChild.data < node.data:
        # the right subtree contains a node with a value less than or equal to the current node
        return False

    # recursively check the subtrees
    return is_avl_balanced(node.leftChild) and is_avl_balanced(node.rightChild)

def inorderTraversal(node):
    values = []
    if node is not None:
        values += inorderTraversal(node.leftChild)
        values.append(node.data)
        values += inorderTraversal(node.rightChild)
    return values


@pytest.mark.test_constructor
def test_constructor():
    AVL1 = AVL()
    assert AVL1.root == None

    AVL2 = AVL(TNode(4))
    assert AVL2.root.data == 4
    assert AVL2.root.parent == None
    assert AVL2.root.leftChild == None
    assert AVL2.root.rightChild == None
    assert AVL2.root.balance == 0


    AVL3 = AVL(4)
    assert AVL3.root.data == 4
    assert AVL3.root.parent == None
    assert AVL3.root.leftChild == None
    assert AVL3.root.rightChild == None
    assert AVL3.root.balance == 0



@pytest.mark.test_insert
def test_insert():
    testAVL = AVL(TNode(6))
    testAVL.insert(TNode(4))
    testAVL.insert(9)
    testAVL.insert(2)
    testAVL.insert(5)
    testAVL.insert(TNode(7))
    testAVL.insert(TNode(3))
    testAVL.insert(1)
    testAVL.insert(0)
    currentTestNode = testAVL.root
    assert currentTestNode.data == 6
    assert currentTestNode.leftChild.data == 2
    assert currentTestNode.rightChild.data == 9
    assert currentTestNode.leftChild.leftChild.data == 1
    assert currentTestNode.leftChild.rightChild.data == 4
    assert currentTestNode.rightChild.leftChild.data == 7
    assert currentTestNode.leftChild.leftChild.leftChild.data == 0
    assert currentTestNode.leftChild.rightChild.rightChild.data == 5
    assert currentTestNode.leftChild.rightChild.leftChild.data == 3

    # assert is_avl_balanced(testAVL.root) == True

    # Case 1:
    AVL2 = AVL(TNode(4))
    AVL2.insert(TNode(2))
    AVL2.insert(TNode(7))
    AVL2.insert(1)
    AVL2.insert(6)
    AVL2.insert(9)
    AVL2.insert(8)
    assert AVL2.root.data == 4
    assert AVL2.root.leftChild.data == 2
    assert AVL2.root.rightChild.data == 7
    assert AVL2.root.leftChild.leftChild.data == 1
    assert AVL2.root.rightChild.leftChild.data == 6
    assert AVL2.root.rightChild.rightChild.data == 9
    assert AVL2.root.rightChild.rightChild.leftChild.data == 8

    # assert is_avl_balanced(AVL2.root) == True

    # Case 2
    AVL3 = AVL(TNode(4))
    AVL3.insert(TNode(2))
    AVL3.insert(TNode(7))
    AVL3.insert(1)
    AVL3.insert(6)
    AVL3.insert(9)
    AVL3.insert(8)
    AVL3.insert(10)
    assert AVL3.root.data == 4
    assert AVL3.root.leftChild.data == 2
    assert AVL3.root.rightChild.data == 7
    assert AVL3.root.leftChild.leftChild.data == 1
    assert AVL3.root.rightChild.leftChild.data == 6
    assert AVL3.root.rightChild.rightChild.data == 9
    assert AVL3.root.rightChild.rightChild.leftChild.data == 8
    assert AVL3.root.rightChild.rightChild.rightChild.data == 10

    # assert is_avl_balanced(AVL3.root) == True

    # Case 3a
    AVL4 = AVL(60)
    AVL4.insert(40)
    AVL4.insert(80)
    AVL4.insert(20)
    AVL4.insert(50)
    AVL4.insert(95)
    AVL4.insert(10)
    AVL4.insert(30)
    AVL4.insert(5)
    assert AVL4.root.data == 60
    assert AVL4.root.leftChild.data == 20
    assert AVL4.root.rightChild.data == 80
    assert AVL4.root.leftChild.leftChild.data == 10
    assert AVL4.root.leftChild.rightChild.data == 40
    assert AVL4.root.rightChild.rightChild.data == 95
    assert AVL4.root.leftChild.leftChild.leftChild.data == 5
    assert AVL4.root.leftChild.rightChild.rightChild.data == 50
    assert AVL4.root.leftChild.rightChild.leftChild.data == 30

    # assert is_avl_balanced(AVL4.root) == True

    # Case 3b
    AVL5 = AVL(TNode(2))
    AVL5.insert(TNode(1))
    AVL5.insert(6)
    AVL5.insert(4)
    AVL5.insert(7)
    AVL5.insert(5)
    assert AVL5.root.data == 4
    assert AVL5.root.leftChild.data == 2
    assert AVL5.root.rightChild.data == 6
    assert AVL5.root.leftChild.leftChild.data == 1
    assert AVL5.root.rightChild.rightChild.data == 7
    assert AVL5.root.rightChild.leftChild.data == 5

    # assert is_avl_balanced(AVL5.root) == True

    # Case with repeats
    AVL6 = AVL(TNode(4))
    AVL6.insert(TNode(2))
    AVL6.insert(7)
    AVL6.insert(2)
    AVL6.insert(2)
    assert AVL6.root.data == 4
    assert AVL6.root.leftChild.data == 2
    assert AVL6.root.rightChild.data == 7
    assert AVL6.root.leftChild.leftChild.data == 2
    assert AVL6.root.leftChild.rightChild.data == 2

    

@pytest.mark.test_setAndGetRoot
def test_setAndGetRoot():
    testAVL = AVL()
    testAVL.setRoot(2)
    assert testAVL.getRoot().data == 2

    AVL2 = AVL(TNode(4))
    AVL2.insert(TNode(2))
    AVL2.insert(TNode(7))
    AVL2.insert(1)
    AVL2.insert(6)
    AVL2.insert(9)
    AVL2.insert(8)
    assert AVL2.getRoot().data == 4
    AVL2.setRoot(5)
    assert AVL2.getRoot().data == 4
    AVL2.setRoot(0)
    assert is_avl_balanced(AVL2.root) == True

@pytest.mark.test_insertNode_hasChildren
def test_insertNode_hasChildren():
        node1 = TNode(2)
        node2 = TNode(1)
        node3 = TNode(6)
        node4 = TNode(4)
        node5 = TNode(7)
        node6 = TNode(5)
        AVL1 = AVL(node1)
        AVL1.insert(node2)
        AVL1.insert(node3)
        AVL1.insert(node4)
        AVL1.insert(node5)
        AVL1.insert(node6)
        node7 = TNode(8) 
        AVL2 = AVL(node7)
        AVL2.insert(TNode(3))
        AVL2.insert(TNode(12))
        AVL1.setRoot(node7)
        assert AVL1.root.data == 4
        assert AVL1.root.leftChild.data == 2
        assert AVL1.root.leftChild.leftChild.data == 1
        assert AVL1.root.leftChild.rightChild.data == 3
        assert AVL1.root.rightChild.data == 8
        assert AVL1.root.rightChild.rightChild.data == 12
        assert AVL1.root.rightChild.leftChild.data == 6
        assert AVL1.root.rightChild.leftChild.leftChild.data == 5
        assert AVL1.root.rightChild.leftChild.rightChild.data == 7
        Node8 = TNode(2)
        testBST = BST(Node8)
        testBST.insert(1)
        testBST.insert(6)
        testBST.insert(4)
        testBST.insert(7)
        testBST.insert(5)
        AVL3 = AVL(Node8)
        assert AVL3.root.data == 4
        assert AVL3.root.leftChild.data == 2
        assert AVL3.root.leftChild.leftChild.data == 1
        assert AVL3.root.rightChild.data == 6
        assert AVL3.root.rightChild.rightChild.data == 7
        assert AVL3.root.rightChild.leftChild.data == 5

@pytest.mark.test_delete
def test_delete():
    AVL1 = AVL(TNode(4))
    AVL1.insert(TNode(2))
    AVL1.insert(TNode(7))
    AVL1.insert(1)
    AVL1.insert(6)
    AVL1.insert(9)
    AVL1.insert(8)
    AVL1.delete(1)
    assert AVL1.root.data == 7
    assert AVL1.root.leftChild.data == 4
    assert AVL1.root.rightChild.data == 9
    assert AVL1.root.leftChild.leftChild.data == 2
    assert AVL1.root.rightChild.leftChild.data == 8
    assert AVL1.root.leftChild.rightChild.data == 6

    assert is_avl_balanced(AVL1.root) == True

    AVL1.delete(8)
    assert AVL1.root.data == 7
    assert AVL1.root.leftChild.data == 4
    assert AVL1.root.rightChild.data == 9
    assert AVL1.root.leftChild.leftChild.data == 2
    assert AVL1.root.rightChild.leftChild == None
    assert AVL1.root.leftChild.rightChild.data == 6

    assert is_avl_balanced(AVL1.root) == True   

    # Testing deleting duplicates
    AVL6 = AVL(TNode(4))
    AVL6.insert(TNode(2))
    AVL6.insert(7)
    AVL6.insert(2)
    AVL6.insert(2)
    AVL6.delete(2)
    nodes = inorderTraversal(AVL6.root)
    assert (2 not in nodes)

@pytest.mark.test_search
def test_search():
    AVL1 = AVL(TNode(4))
    AVL1.insert(TNode(2))
    AVL1.insert(TNode(7))
    AVL1.insert(1)
    AVL1.insert(6)
    AVL1.insert(9)
    AVL1.insert(8)
    assert AVL1.search(1).data == 1
    assert AVL1.search(4).data == 4
    assert AVL1.search(2).data == 2
    assert AVL1.search(7).data == 7
    assert AVL1.search(6).data == 6
    assert AVL1.search(9).data == 9
    assert AVL1.search(8).data == 8

@pytest.mark.test_print
def test_print():
    AVL1 = AVL(TNode(4))
    AVL1.insert(TNode(2))
    AVL1.insert(TNode(7))
    AVL1.insert(1)
    AVL1.insert(6)
    AVL1.insert(9)
    AVL1.insert(8)

    capturedOutput = io.StringIO()
    sys.stdout = capturedOutput
    AVL1.printInOrder()
    actual_output = capturedOutput.getvalue()
    sys.stdout = sys.__stdout__
    expected_output = "1\n2\n4\n6\n7\n8\n9\n"
    assert actual_output == expected_output

    actual_output = ""
    capturedOutput = io.StringIO()
    sys.stdout = capturedOutput
    AVL1.printBF()
    actual_output = capturedOutput.getvalue()
    expected_output = "4 \n2 7 \n1 6 9 \n8 \n"
    assert expected_output == actual_output

    