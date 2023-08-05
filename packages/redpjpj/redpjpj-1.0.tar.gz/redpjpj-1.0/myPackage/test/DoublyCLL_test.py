import pytest
import sys
import io
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from datastructures.Linear.DoublyCLL import doublyCLL
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
    testDCLL = doublyCLL()
    assert testDCLL.head == None
    assert testDCLL.tail == None
    
    testDCLL2 = doublyCLL(testNode1)
    assert testDCLL2.head.data == 6
    assert testDCLL2.tail.data == 6
    assert testDCLL2.size == 1
    assert testDCLL2.tail.next.data == 6
    assert testDCLL2.head.prev.data == 6

@pytest.mark.test_insert
def test_insert():
    testDCLL = doublyCLL()
    testDCLL.insertHead(testNode1)
    assert testDCLL.head.next.data == 6
    testDCLL.insertHead(testNode2)
    testDCLL.insertTail(testNode3) 
    testDCLL.insertTail(testNode4)
    assert testDCLL.tail.data == 7
    testDCLL.insert(testNode5,3)
    assert testDCLL.head.next.next.data == 10
    assert testDCLL.tail.next.data == 1 # Added this additional test to ensure circular with multiple elements
    testDCLL.insert(testNode6,5)
    testDCLL.insert(Node(11),7)
    assert testDCLL.tail.data == 11
    testDCLL.insert(testNode7,1) # test insert at head
    currentTestNode = testDCLL.head 
    testList = []
    for i in range(0, testDCLL.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next
    assert testList == [4, 1, 6, 10, 2, 3, 7, 11]
    testDCLL.insertTail(testNode6_2)
    currentTestNode = testDCLL.head 
    testList = []
    for i in range(0, testDCLL.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next
    assert testList == [4, 1, 6, 10, 2, 3, 7, 11, 3]
    assert testDCLL.tail.next.data == 4

    testDCLL.sortedInsert(Node(0))
    testDCLL.sortedInsert(Node(12))
    currentTestNode2 = testDCLL.head 
    testList2 = []
    for i in range(0, testDCLL.size):
        testList2.append(currentTestNode2.data)
        currentTestNode2 = currentTestNode2.next
    assert testList2 == [0, 1, 2, 3, 3, 4, 6, 7, 10, 11, 12]
    

    testDCLL2 = doublyCLL()
    testDCLL2.sortedInsert(Node(2))
    assert testDCLL2.head.data == 2
    assert testDCLL2.tail.data == 2
    assert testDCLL2.head.prev.data == 2
    assert testDCLL2.tail.next.data == 2
    
def setup():
    testDCLL = doublyCLL()
    testDCLL.insertTail(testNode1)
    testDCLL.insertTail(testNode2)
    testDCLL.insertTail(testNode3) 
    testDCLL.insertTail(testNode4)
    testDCLL.insertTail(testNode5)
    testDCLL.insertTail(testNode6)
    testDCLL.insertTail(testNode6_2)
    testDCLL.insertTail(testNode7)
    return testDCLL

@pytest.mark.test_isDoubly
def test_isDoubly():
    testDCLL = setup()
    nextNode = testDCLL.head.next
    prevNode = nextNode.prev
    assert prevNode.data == testDCLL.head.data


@pytest.mark.test_isCircular
def test_isCircular():
    testDCLL = setup()
    circTestNode = testDCLL.tail
    circTestNode = circTestNode.next
    assert circTestNode.data == testDCLL.head.data


@pytest.mark.test_delete
def test_delete():
    testDCLL = setup()
    testDCLL.deleteHead()
    assert testDCLL.head.data == 1
    assert testDCLL.tail.next.data == 1
    testDCLL.deleteTail()
    assert testDCLL.tail.data != 4
    assert testDCLL.tail.next.data == 1
    testDCLL.delete(testDCLL.tail)
    testDCLL.delete(testNode6)
    testDCLL.insertHead(Node(11))
    testDCLL.insert(Node(11),3)
    testDCLL.insertTail(Node(11)) # insert 3 new duplicates
    testDCLL.delete(Node(11))
    currentTestNode = testDCLL.head
    testList = []
    for i in range(0, testDCLL.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next
    assert testList == [1,2,7,10]
    testDCLL.clear()
    assert testDCLL.size == 0 and testDCLL.head == None and testDCLL.tail == None
        
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
    testDCLL = setup()
    testDCLL.sort()
    testList = []
    currentTestNode = testDCLL.head
    for i in range(0, testDCLL.size):
        testList.append(currentTestNode.data)
        currentTestNode = currentTestNode.next

    assert testList == [1,2,3,3,4,6,7,10]

    testIsSorted = testDCLL.isSorted()

    assert testIsSorted == True

    newTestNode = Node(8)
    duplicateTestNode = Node(4)
    # with patch.object(DLL, 'sort') as mock_sort:
    #         # call sortedInsert
    #         dLL.sortedInsert(newTestNode)

    #         # assert that the sort method was not called
    #         mock_sort.assert_not_called()

    testDCLL.sortedInsert(newTestNode)
    testDCLL.sortedInsert(duplicateTestNode)
    currentTestNode = testDCLL.head
    testList2 = []
    for i in range(0, testDCLL.size):
        testList2.append(currentTestNode.data)
        currentTestNode = currentTestNode.next

    assert testList2 == [1,2,3,3,4,4,6,7,8,10]


@pytest.mark.test_print
def test_Print():
    testDCLL = setup()
    captured_output = io.StringIO()
    sys.stdout = captured_output
    testDCLL.print()
    actual_output = captured_output.getvalue()
    sys.stdout = sys.stdout
    expected_output = "The size of this doubly circular linked list is 8.\nThis doubly circular linked list is not sorted.\nThis doubly circular linked list contains:\n6\n1\n2\n7\n10\n3\n3\n4\n"