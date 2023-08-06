
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from datastructures.nodes.SNode import Node
from datastructures.Linear.singlyLL import SinglyLL

class LLStack(SinglyLL):
    def __init__(self, head=None):
        super().__init__(head)
        
    def push(self, node):
        self.InsertHead(node)
    
    def pop(self):
        return self.DeleteHead()
    
    def peek(self):
        if self.head:
            return self.head.data
        return None
    
    def is_empty(self):
        return self.head is None
    
    def clear(self):
        super().Clear()
    
    def print(self):
        if not self.head:
            print("Stack is empty.")
            return
        # Count the number of nodes in the list
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        # Check if the list is sorted
        is_sorted = True
        current = self.head
        while current.next:
            if current.data > current.next.data:
                is_sorted = False
                break
            current = current.next
        # Print the list information
        print("List length:", count)
        print("Sorted status:", "Yes" if is_sorted else "No")
        print("List content:")
        current = self.head
        while current:
            print(current.data)
            current = current.next



# Test the LLStack class
def main():
    # Initialize the stack
    stack = LLStack()

    # Test is_empty() function
    print("Is stack empty?", stack.is_empty())

    # Push nodes onto the stack
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)
    node5 = Node(5)
    stack.push(node1)

    # Test push() and print() functions
    print("Pushed node:", node1.data)
    stack.print()

    stack.push(node2)
    stack.push(node3)

    # Test is_empty() function
    print("Is stack empty?", stack.is_empty())

    # Print the stack
    stack.print()

    # Test peek() function
    print("Peek:", stack.peek())

    # Push more nodes onto the stack
    stack.push(node4)
    stack.push(node5)

    # Test push() and print() functions
    print("Pushed node:", node4.data)
    stack.print()

    print("Pushed node:", node5.data)
    stack.print()

    # Test peek() function
    print("Peek:", stack.peek())

    # Test pop() function
    print("Popped node:", stack.pop().data)
    print("Popped node:", stack.pop().data)

    # Test pop() and print() functions
    stack.print()

    # Test clear() function
    stack.clear()

    # Test is_empty() function
    print("Is stack empty?", stack.is_empty())

    # Print the stack
    stack.print()

    # Push nodes onto the stack
    node6 = Node(6)
    node7 = Node(7)
    node8 = Node(8)
    stack.push(node6)

    # Test push() and print() functions
    print("Pushed node:", node6.data)
    stack.print()

    stack.push(node7)
    stack.push(node8)

    # Test is_empty() function
    print("Is stack empty?", stack.is_empty())

    # Print the stack
    stack.print()

    # Test peek() function
    print("Peek:", stack.peek())

    # Test pop() function
    print("Popped node:", stack.pop().data)

    # Test clear() function
    stack.clear()

    # Test is_empty() function
    print("Is stack empty?", stack.is_empty())

    # Print the stack
    stack.print()


if __name__ == '__main__':
    main()

