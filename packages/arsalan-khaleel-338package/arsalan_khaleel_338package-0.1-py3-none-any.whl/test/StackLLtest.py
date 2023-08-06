from myLib.datastructures.linear.StackLL import LLStack
from myLib.datastructures.linear.SLL import Node

def test_llstack():
    s = LLStack()
    assert s.isEmpty()

    # Test push
    s.push(Node(1))
    assert not s.isEmpty()
    assert s.peek() == 1

    s.push(Node(2))
    assert not s.isEmpty()
    assert s.peek() == 2

    # Test pop
    assert s.pop() == 2
    assert not s.isEmpty()
    assert s.peek() == 1

    assert s.pop() == 1
    assert s.isEmpty()

test_llstack()