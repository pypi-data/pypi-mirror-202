from myLib.datastructures.linear.QueueLL import LLQueue
from myLib.datastructures.linear.SLL import Node
def test_llqueue():
    q = LLQueue()
    assert q.isEmpty()

    # Test enqueue
    q.enqueue(Node(1))
    assert not q.isEmpty()
    assert q.peek() == 1

    q.enqueue(Node(2))
    assert not q.isEmpty()
    assert q.peek() == 1

    # Test dequeue
    assert q.dequeue() == 1
    assert not q.isEmpty()
    assert q.peek() == 2

    assert q.dequeue() == 2
    assert q.isEmpty()

test_llqueue()