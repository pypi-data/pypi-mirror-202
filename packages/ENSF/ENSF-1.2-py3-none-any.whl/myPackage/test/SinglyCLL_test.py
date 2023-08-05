import pytest
import sys
import io
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from datastructures.Linear.SinglyCLL import singlyCLL
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
    testSCLL = singlyCLL()
    assert testSCLL.head == None
    assert testSCLL.tail == None
    
    testSCLL2 = singlyCLL(testNode1)
    assert testSCLL2.head.data == 6
    assert testSCLL2.tail.data == 6
    assert testSCLL2.size == 1
    assert testSCLL2.tail.next.data == 6

@pytest.mark.test_insert
def test_insert():
    testSCLL = singlyCLL()
    testSCLL.insertHead(testNode1)
    assert testSCLL.head.next.data == 6 # Added this additional test to ensure circular with one element
    assert testSCLL.head.data == 6
    testSCLL.insertHead(testNode2)
    testSCLL.insertTail(testNode3) 
    testSCLL.insertTail(testNode4)
    assert testSCLL.tail.data == 7
    testSCLL.insert(testNode5, 3)
    assert testSCLL.head.next.next.data == 10
    assert testSCLL.tail.next.data == 1 # Added this additional test to ensure circular with multiple elements
    testSCLL.insert(testNode6,5)
    testSCLL.insert(Node(11), 7)  # Added this additional test
    assert testSCLL.tail.data == 11 # Added this additional test
    testSCLL.insert(testNode7,1) # test insert at head
    currentTestNode = testSCLL.head 
    testList = []
    for i in range(0, testSCLL.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next
    assert testList == [4,1,6,10,2,3,7,11]
    testSCLL.insertTail(testNode6_2)
    currentTestNode = testSCLL.head 
    testList = []
    for i in range(0, testSCLL.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next
    assert testList == [4,1,6,10,2,3,7,11,3]
    assert testSCLL.tail.next.data == 4 # Added this additional test to ensure circular with multiple elements


def setup():
    testSCLL = singlyCLL()
    testSCLL.insertTail(testNode1)
    testSCLL.insertTail(testNode2)
    testSCLL.insertTail(testNode3) 
    testSCLL.insertTail(testNode4)
    testSCLL.insertTail(testNode5)
    testSCLL.insertTail(testNode6)
    testSCLL.insertTail(testNode6_2)
    testSCLL.insertTail(testNode7)
    return testSCLL

@pytest.mark.test_isCircular
def test_isCircular():
    testSCLL = setup()
    circTestNode = testSCLL.tail
    assert testSCLL.head.data == circTestNode.next.data

@pytest.mark.test_delete
def test_delete():
    testSCLL = setup()
    testSCLL.deleteHead()
    assert testSCLL.head.data != 6
    assert testSCLL.tail.next.data == 1 # Added this additional test
    testSCLL.deleteTail()
    assert testSCLL.tail.data != 4
    assert testSCLL.tail.next.data == 1 # Added this additional test
    testSCLL.delete(testSCLL.tail)
    testSCLL.delete(testNode6)
    #*********************************
    # These 4 lines are new
    testSCLL.insertHead(Node(11))
    testSCLL.insert(Node(11), 3)
    testSCLL.insertTail(Node(11)) # insert 3 new duplicates
    testSCLL.delete(Node(11))
    currentTestNode = testSCLL.head
    testList = []
    for i in range(0, testSCLL.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next
    assert testList == [1,2,7,10]
    testSCLL.clear()
    assert testSCLL.size == 0 and testSCLL.head == None and testSCLL.tail == None

@pytest.mark.test_search
def test_Search():
    testDCLL = setup()
    testNode6Search = testDCLL.search(testNode6)
    assert testNode6Search == testNode6
    nonListNode = Node(99)
    testNonListNode = testDCLL.search(nonListNode)
    assert testNonListNode == None

@pytest.mark.test_sorting
def test_Sorting():
    testSCLL = setup()
    testSCLL.sort()
    testList = []
    currentTestNode = testSCLL.head
    for i in range(0, testSCLL.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next

    assert testList == [1,2,3,3,4,6,7,10]

    testIsSorted = testSCLL.isSorted()

    assert testIsSorted == True

    newTestNode = Node(8)
    duplicateTestNode = Node(4)

    testSCLL.sortedInsert(newTestNode)
    testSCLL.sortedInsert(duplicateTestNode)
    currentTestNode = testSCLL.head
    testList2 = []
    for i in range(0, testSCLL.size):
        testList2.append(currentTestNode.data)
        currentTestNode = currentTestNode.next

    assert testList2 == [1,2,3,3,4,4,6,7,8,10]

    testSCLL2 = setup()
    testSCLL2.sortedInsert(Node(11))
    testSCLL2.sortedInsert(Node(0))
    current = testSCLL2.head
    testList3 = []
    for i in range(0, testSCLL2.size):
        testList3.append(current.data)
        current = current.next
    assert testList3 == [0,1,2,3,3,4,6,7,10,11]

    testSCLL3 = singlyCLL()
    testSCLL3.sortedInsert(Node(4))
    assert testSCLL3.head.data == 4
    assert testSCLL3.tail.data == 4


@pytest.mark.test_print
def test_Print():
    testSCLL = setup()
    captured_output = io.StringIO()
    sys.stdout = captured_output
    testSCLL.print()
    actual_output = captured_output.getvalue()
    sys.stdout = sys.stdout
    expected_output = "The size of this singly circular linked list is 8.\nThis singly circular linked list is not sorted.\nThis singly circular linked list contains:\n6\n1\n2\n7\n10\n3\n3\n4\n"
