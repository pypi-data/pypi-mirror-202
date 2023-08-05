import pytest
import sys
import io
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from datastructures.Linear.SinglyLL import singlyLL
from datastructures.Nodes.SinglyNode import Node

testNode1 = Node(6)
testNode2 = Node(1)
testNode3 = Node(2)
testNode4 = Node(7)
testNode5 = Node(10)   
testNode6 = Node(3)
testNode6_2 = Node(3)
testNode7 = Node(4)

def setup():
    testSLL = singlyLL()
    testSLL.insertTail(testNode1)
    testSLL.insertTail(testNode2)
    testSLL.insertTail(testNode3) 
    testSLL.insertTail(testNode4)
    testSLL.insertTail(testNode5)
    testSLL.insertTail(testNode6)
    testSLL.insertTail(testNode6_2)
    testSLL.insertTail(testNode7)
    return testSLL

@pytest.mark.test_constructor
def test_constructor():
    testSLL = singlyLL()
    assert testSLL.head == None
    assert testSLL.tail == None
    assert testSLL.size == 0

    testSLL2 = singlyLL(testNode1)
    assert testSLL2.head == testNode1
    assert testSLL2.tail == testNode1
    assert testSLL2.size == 1

@pytest.mark.test_insert
def test_insert():
    testSLL = singlyLL()
    testSLL.insert(testNode1, 1)
    assert testSLL.head.data == 6
    testSLL.insertHead(testNode2)
    testSLL.insertTail(testNode3) 
    testSLL.insertTail(testNode4)
    assert testSLL.tail.data == 7
    testSLL.insert(testNode5, 3)
    assert testSLL.head.next.next.data == 10
    # Added these insert tests - test boundary cases
    testSLL.insert(Node(0), 1)
    assert testSLL.head.data == 0
    testSLL.insert(Node(0), 7)
    assert testSLL.tail.data == 0


    testSLL.insert(testNode6, 5)
    testSLL.insert(testNode7, 1) # test insert at head
    currentTestNode = testSLL.head 
    testList = []
    for i in range(0, testSLL.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next
    assert testList == [4, 0, 1, 6, 10, 3, 2, 7, 0]
    testSLL.insertTail(testNode6_2)
    currentTestNode = testSLL.head 
    testList = []
    for i in range(0, testSLL.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next    
    assert testList == [4, 0, 1, 6, 10, 3, 2, 7, 0, 3]

@pytest.mark.test_delete
def test_delete():
    testNothing = singlyLL()
    testNothing.deleteHead()
    testNothing.deleteTail()
    assert testNothing.head == None
    assert testNothing.tail == None

    testNothing.insertTail(Node(1))
    testNothing.delete(Node(1))
    assert testNothing.head == None
    assert testNothing.tail == None
    assert testNothing.size == 0

    testNothing.insertTail(Node(1))
    testNothing.insertTail(Node(2))
    testNothing.delete(Node(2))

    assert testNothing.head.data == 1
    assert testNothing.tail.data == 1

    testNothing2 = singlyLL(Node(1))
    testNothing2.insertTail(Node(2))
    testNothing2.delete(Node(1))
    assert testNothing2.head.data == 2
    assert testNothing2.tail.data == 2

    testSLL = setup()
    testSLL.deleteHead()
    assert testSLL.head.data != 6
    testSLL.deleteTail()
    assert testSLL.tail.data != 4
    testSLL.delete(testSLL.tail)
    testSLL.delete(testNode6)
#*********************************
    # These 4 lines are new
    testSLL.insertHead(Node(11))
    testSLL.insert(Node(11),3)
    testSLL.insertTail(Node(11)) # insert 3 new duplicates
    testSLL.delete(Node(11))


    currentTestNode = testSLL.head
    testList = []
    for i in range(0, testSLL.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next
    assert testList == [1, 2, 7, 10]
    testSLL.delete(Node(10))
    testSLL.delete(Node(1))
    currentTestNode = testSLL.head
    testList = []
    for i in range(0, testSLL.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next
    assert testList == [2, 7]
    testSLL.clear()
    assert testSLL.size == 0 and testSLL.head == None and testSLL.tail == None

@pytest.mark.test_search
def test_search():
    testSLL = setup()
    testNode6Search = testSLL.search(testNode6)
    assert testNode6Search == testNode6
    nonListNode = Node(99)
    testNonListNode = testSLL.search(nonListNode)
    assert testNonListNode == None

@pytest.mark.test_sorting
def test_sorting():
    testSLL = setup()
    testSLL.sort()
    testList = []
    currentTestNode = testSLL.head
    for i in range(0, testSLL.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next

    assert testList == [1, 2, 3, 3, 4, 6, 7, 10]

    testIsSorted = testSLL.isSorted()

    assert testIsSorted == True

    newTestNode = Node(8)
    duplicateTestNode = Node(4)
    # Added sorted inserts for boundary cases (heads and tails) -- Added sortedInsert for Node(11) and Node(0)
    testSLL.sortedInsert(newTestNode)
    testSLL.sortedInsert(duplicateTestNode)
    testSLL.sortedInsert(Node(11))
    testSLL.sortedInsert(Node(0))
    currentTestNode = testSLL.head
    testList2 = []
    for i in range(0, testSLL.size):
        testList2.append(currentTestNode.data)
        currentTestNode = currentTestNode.next

    assert testList2 == [0, 1, 2, 3, 3, 4, 4, 6, 7, 8, 10, 11]

@pytest.mark.test_print
def test_print():
    testSLL = setup()
    captured_output = io.StringIO()
    sys.stdout = captured_output
    testSLL.print()
    actual_output = captured_output.getvalue()

    sys.stdout = sys.__stdout__

    expected_output = "The size of this singly linked list is 8.\nThis singly linked list is not sorted.\nThis singly linked list contains:\n6\n1\n2\n7\n10\n3\n3\n4\n"
    assert actual_output ==  expected_output