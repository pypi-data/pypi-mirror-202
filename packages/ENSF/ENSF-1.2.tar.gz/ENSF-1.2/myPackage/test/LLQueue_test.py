import pytest
import sys
import io
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from datastructures.Linear.LLQueue import LLQueue
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
    testQueue = LLQueue()
    assert testQueue.head == None
    assert testQueue.tail == None

    testQueue2 = LLQueue(Node(2))
    assert testQueue2.head.data == 2
    assert testQueue2.tail.data == 2

@pytest.mark.test_enqueue
def test_enqueue():
    testQueue = LLQueue()
    testQueue.enqueue(testNode1)
    assert testQueue.head.data == 6
    testQueue.enqueue(testNode2)
    testQueue.enqueue(testNode3) 
    testQueue.enqueue(testNode4)
    testQueue.enqueue(testNode5)
    assert testQueue.head.next.next.data == 2
    testQueue.enqueue(testNode6)
    testQueue.enqueue(testNode7) # test enqueue at tail
    currentTestNode = testQueue.head 
    testList = []
    for i in range(0, testQueue.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next
    assert testList == [6, 1, 2, 7, 10, 3, 4]
    testQueue.enqueue(testNode6_2)
    testList = []
    currentTestNode = testQueue.head
    for i in range(0, testQueue.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next

    assert testList == [6, 1, 2, 7, 10, 3, 4, 3]

def setup():
    testQueue = LLQueue()
    testQueue.enqueue(testNode1) # 6
    testQueue.enqueue(testNode2) # 1
    testQueue.enqueue(testNode3) # 2
    testQueue.enqueue(testNode4) # 7
    testQueue.enqueue(testNode5) # 10
    testQueue.enqueue(testNode6) # 3
    testQueue.enqueue(testNode6_2) # 3
    testQueue.enqueue(testNode7) # 4
    return testQueue

@pytest.mark.test_dequeue
def test_dequeue():
    testQueue = setup()
    testQueue.dequeue()
    assert testQueue.head.data != 6
    testQueue.dequeue()
    testQueue.dequeue()
    currentTestNode = testQueue.head
    testList = []
    for i in range(0, testQueue.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next
    assert testList == [7, 10, 3, 3, 4]
    testQueue.clear()
    assert testQueue.size == 0 and testQueue.head == None

@pytest.mark.test_search
def test_Search():
    testQueue = setup()
    testNode6Search = testQueue.search(testNode7)
    assert testNode6Search == testNode7
    nonListNode = Node(99)
    testNonListNode = testQueue.search(nonListNode)
    assert testNonListNode == None

@pytest.mark.test_print
def test_print():
    testQueue = setup()
    captured_output = io.StringIO()
    sys.stdout = captured_output
    testQueue.print()
    actual_output = captured_output.getvalue()

    sys.stdout = sys.__stdout__

    expected_output = "The size of this singly linked list queue is 8.\nThis singly linked list queue is not sorted.\nThis singly linked list queue contains:\n6\n1\n2\n7\n10\n3\n3\n4\n"
    assert actual_output ==  expected_output

@pytest.mark.test_detreimentFunctionality
def test_detrimentFunctionality():
    testQueue = LLQueue(testNode7)
    testQueue.insertHead(testNode1)
    testQueue.insert(testNode2,1)
    testQueue.insertTail(testNode3)
    testQueue.deleteHead()
    testQueue.deleteTail()
    testQueue.delete(testNode7)
    testQueue.insertTail(Node(2))
    testQueue.enqueue(Node(2))
    testQueue.sort()
    testQueue.sortedInsert(Node(3))
    testList = []
    currentTestNode = testQueue.head
    for i in range(testQueue.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next
    assert testList == [4, 2]