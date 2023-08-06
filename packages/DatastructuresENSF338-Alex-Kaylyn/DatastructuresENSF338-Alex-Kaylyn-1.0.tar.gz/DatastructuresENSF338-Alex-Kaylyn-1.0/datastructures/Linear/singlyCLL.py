from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from datastructures.nodes.SNode import Node
from datastructures.Linear.singlyLL import SinglyLL

class CircularSinglyLL(SinglyLL):
    def __init__(self, node=None):
        if node:
            self.head = node
            self.tail = node
            node.next = node
            self.size = 1
        else:
            super().__init__()


    def is_empty(self):
        return self.size == 0

    def InsertHead(self, node):
        if self.is_empty():
            self.head = node
            self.tail = node
            node.next = node
        else:
            node.next = self.head
            self.head = node
            self.tail.next = node
        self.size += 1

    
    def InsertTail(self, node):
        if self.is_empty():
            self.InsertHead(node)
        else:
            node.next = self.head
            self.tail.next = node
            self.tail = node
            self.size += 1

    
    def Insert(self, node, position):
        if position < 0 or position > self.size:
            raise ValueError("Invalid position")
        elif position == 0:
            self.InsertHead(node)
        elif position == self.size:
            self.InsertTail(node)
        else:
            current = self.head
            for i in range(position - 1):
                current = current.next
            node.next = current.next
            current.next = node
            self.size += 1
    
    def DeleteHead(self):
        if self.is_empty():
            return None
        temp = self.head
        self.head = self.head.next
        self.tail.next = self.head
        temp.next = None
        self.size -= 1
        if self.is_empty():
            self.tail = None
        return temp

    
    def DeleteTail(self):
        if self.is_empty():
            return None
        current = self.head
        while current.next != self.tail:
            current = current.next
        temp = self.tail
        current.next = self.head
        self.tail = current
        self.size -= 1
        if self.is_empty():
            self.head = None
        return temp

    
    def Delete(self, position):
        if position < 0 or position >= self.size:
            return print("Invalid position, node does not exist")
        elif self.size == 1:
            return self.DeleteHead()
        elif position == 0:
            return self.DeleteHead()
        elif position == self.size - 1:
            return self.DeleteTail()
        else:
            current = self.head
            for i in range(position - 1):
                current = current.next
            temp = current.next
            current.next = temp.next
            temp.next = None
            self.size -= 1
            return temp

    
    def Search(self, node):
        if self.is_empty():
            return None
        current = self.head
        for i in range(self.size):
            if current.data == node.data:
                return current
            current = current.next
            if current == self.head:
                break
        return None

    def length(self):
        return self.size

    
    def Clear(self):
        while not self.is_empty():
            self.DeleteHead()

        
    def is_sorted(self):
        if not self.tail:
            return True
        current = self.tail.next
        while current != self.tail:
            if current.data > current.next.data:
                return False
            current = current.next
        return True
    
    def Sort(self):
        if not self.head:
            return
        current = self.head
        while current.next != self.head:
            index = current.next
            while index != self.head:
                if current.data > index.data:
                    current.data, index.data = index.data, current.data
                index = index.next
            current = current.next


    def Print(self):
        if self.is_empty():
            print("The list is empty.")
            return
        print("List length:", self.length())
        print("Sorted:", "Yes" if self.is_sorted() else "No")
        print("List content:", end=" ")
        current = self.head
        for i in range(self.size):
            print(current.data, end=" ")
            current = current.next
        print()


# TESTING THE SINGLYCLL:
def main():
    # Create a circular singly linked list with 3 nodes
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    cll = CircularSinglyLL()
    cll.InsertTail(node1)
    cll.InsertTail(node2)
    cll.InsertHead(node3)

    # Print initial list information
    print("Initial list:")
    cll.Print()  # Expected output: 3 -> 1 -> 2 -> 3

    # Delete the head and tail nodes, and then print the list again
    cll.DeleteHead()
    cll.DeleteTail()
    print("List after deleting head and tail nodes:")
    cll.Print()  # Expected output: 1

    # Insert a new node at position 1, and then print the list again
    node4 = Node(4)
    cll.Insert(node4, 1)
    print("List after inserting node at position 1:")
    cll.Print()  # Expected output: 1 -> 4

    # Insert a new node at the head, and then print the list again
    node5 = Node(5)
    cll.InsertHead(node5)
    print("List after inserting node at the head:")
    cll.Print()  # Expected output: 5 -> 1 -> 4

    # Insert a new node at the tail, and then print the list again
    node6 = Node(6)
    cll.InsertTail(node6)
    print("List after inserting node at the tail:")
    cll.Print()  # Expected output: 5 -> 1 -> 4 -> 6

    # Delete the node at position 2, and then print the list again
    cll.Delete(2)
    print("List after deleting node at position 2:")
    cll.Print()  # Expected output: 5 -> 4 -> 6

    # Delete a non-existing node, and then print the list again
    cll.Delete(3)
    print("List after deleting non-existing node:")
    cll.Print()  # Expected output: 5 -> 4 -> 6

    # Clear the list and print the final list information
    cll.Clear()
    print("Final list after clearing the linked list:")
    cll.Print()  # Expected output: Empty list

if __name__ == '__main__':
    main()
