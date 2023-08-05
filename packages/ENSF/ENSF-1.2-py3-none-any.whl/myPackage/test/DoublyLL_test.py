import pytest
import sys
import io
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from datastructures.Linear.DoublyLL import doublyLL
from datastructures.Nodes.DoublyNode import Node

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
    testDLL = doublyLL()
    assert testDLL.head == None
    assert testDLL.tail == None
    assert testDLL.size == 0
    testDLL2 = doublyLL(Node(4))
    assert testDLL2.head.data == 4
    assert testDLL2.tail.data == 4
    assert testDLL2.size == 1


@pytest.mark.test_insert
def test_insert():
    testDLL = doublyLL()
    testDLL.insertHead(testNode1)
    assert testDLL.head.data == 6
    testDLL.insertHead(testNode2)
    testDLL.insertTail(testNode3) 
    testDLL.insertTail(testNode4)
    assert testDLL.tail.data == 7
    testDLL.insert(testNode5, 3)
    assert testDLL.head.next.next.data == 10

    # #NEW
    testDLL.insert(Node(0), 1)
    assert testDLL.head.data == 0
    testDLL.insert(Node(2), 7)
    assert testDLL.tail.data == 2
    
    testDLL.insert(testNode6, 5)
    testDLL.insert(testNode7,1) # test insert at head
    currentTestNode = testDLL.head 
    testList = []
    for i in range(0, testDLL.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next
    assert testList == [4, 0, 1, 6, 10, 3, 2, 7, 2]
    testDLL.insertTail(testNode6_2)
    testDLL.insert(Node(10), 11)
    currentTestNode = testDLL.head 
    testList = []
    for i in range(0, testDLL.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next    
    assert testList == [4, 0, 1, 6, 10, 3, 2, 7, 2, 3, 10]

    
def setup():
    testDLL = doublyLL()
    testDLL.insertTail(testNode1)
    testDLL.insertTail(testNode2)
    testDLL.insertTail(testNode3) 
    testDLL.insertTail(testNode4)
    testDLL.insertTail(testNode5)
    testDLL.insertTail(testNode6)
    testDLL.insertTail(testNode6_2)
    testDLL.insertTail(testNode7)
    return testDLL

@pytest.mark.test_isDoubly
def test_isDoubly():
    testDLL = setup()
    nextNode = testDLL.head.next
    prevNode = nextNode.prev
    assert prevNode.data == testDLL.head.data

@pytest.mark.test_delete
def test_delete():
    testDLL = setup()
    testDLL.deleteHead()
    assert testDLL.head.data != 6
    testDLL.deleteTail()
    assert testDLL.tail.data != 4
    testDLL.delete(testDLL.tail)
    testDLL.delete(testNode6)
    testDLL.insertHead(Node(11))
    testDLL.insert(Node(11), 3)
    testDLL.insertTail(Node(11))
    testDLL.insertTail(Node(11)) # insert 3 new duplicates
    testDLL.delete(Node(11))
    currentTestNode = testDLL.head
    testList = []
    for i in range(0, testDLL.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next
    assert testList == [1,2,7,10]
    testDLL.clear()
    assert testDLL.size == 0 and testDLL.head == None and testDLL.tail == None
        
@pytest.mark.test_search
def test_Search():
    testDLL = setup()
    testNode6Search = testDLL.search(testNode6)
    assert testNode6Search == testNode6
    nonListNode = Node(99)
    testNonListNode = testDLL.search(nonListNode)
    assert testNonListNode == None

@pytest.mark.test_sorting
def test_Sorting():
    testDLL = setup()
    testDLL.sort()
    testList = []
    currentTestNode = testDLL.head
    for i in range(0, testDLL.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next

    assert testList == [1,2,3,3,4,6,7,10]

    testIsSorted = testDLL.isSorted()

    assert testIsSorted == True

    newTestNode = Node(8)
    duplicateTestNode = Node(4)
    # Current size of the list is 8
    testDLL.sortedInsert(newTestNode)
    testDLL.sortedInsert(duplicateTestNode)
    testDLL.sortedInsert(Node(11)) #new
    testDLL.sortedInsert(Node(0)) #new
    currentTestNode = testDLL.head
    testList2 = []
    for i in range(0, testDLL.size):
        testList2.append(currentTestNode.data)
        currentTestNode = currentTestNode.next

    assert testList2 == [0, 1, 2, 3, 3, 4, 4, 6, 7, 8, 10, 11]


@pytest.mark.test_print
def test_print():
    testDLL = setup()
    captured_output = io.StringIO()
    sys.stdout = captured_output
    testDLL.print()
    actual_output = captured_output.getvalue()

    sys.stdout = sys.__stdout__

    expected_output = "The size of this doubly linked list is 8.\nThis doubly linked list is not sorted.\nThis doubly linked list contains:\n6\n1\n2\n7\n10\n3\n3\n4\n"
    assert actual_output ==  expected_output