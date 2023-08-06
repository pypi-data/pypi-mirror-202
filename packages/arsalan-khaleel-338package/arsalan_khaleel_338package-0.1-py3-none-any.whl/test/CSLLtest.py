from myLib.datastructures.linear.CSLL import SinglyCLL
from myLib.datastructures.linear.SLL import Node
def test_singly_cll():
    cll = SinglyCLL()
    assert cll.size == 0

    # Test insertHead
    cll.insertHead(Node(1))
    assert cll.size == 1
    assert cll.head.data == 1
    assert cll.tail.data == 1

    cll.insertHead(Node(2))
    assert cll.size == 2
    assert cll.head.data == 2
    assert cll.tail.data == 1

    # Test insertTail
    cll.insertTail(Node(3))
    assert cll.size == 3
    assert cll.head.data == 2
    assert cll.tail.data == 3

    # Test deleteHead
    cll.deleteHead()
    assert cll.size == 2
    assert cll.head.data == 1
    assert cll.tail.data == 3

    # Test deleteTail
    cll.deleteTail()
    assert cll.size == 1
    assert cll.head.data == 1
    assert cll.tail.data == 1

test_singly_cll()