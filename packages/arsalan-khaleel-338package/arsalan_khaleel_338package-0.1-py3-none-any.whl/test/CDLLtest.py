from myLib.datastructures.linear.CDLL import DoublyCLL

def test_doubly_cll():
    cdll = DoublyCLL()
    assert cdll.size == 0

    # Test insert_head
    cdll.insert_head(1)
    assert cdll.size == 1
    assert cdll.head.data == 1
    assert cdll.tail.data == 1

    cdll.insert_head(2)
    assert cdll.size == 2
    assert cdll.head.data == 2
    assert cdll.tail.data == 1

    # Test insert_tail
    cdll.insert_tail(3)
    assert cdll.size == 3
    assert cdll.head.data == 2
    assert cdll.tail.data == 3

    # Test delete_head
    cdll.delete_head()
    assert cdll.size == 2
    assert cdll.head.data == 1
    assert cdll.tail.data == 3

    # Test delete_tail
    cdll.delete_tail()
    assert cdll.size == 1
    assert cdll.head.data == 1
    assert cdll.tail.data == 1

test_doubly_cll()