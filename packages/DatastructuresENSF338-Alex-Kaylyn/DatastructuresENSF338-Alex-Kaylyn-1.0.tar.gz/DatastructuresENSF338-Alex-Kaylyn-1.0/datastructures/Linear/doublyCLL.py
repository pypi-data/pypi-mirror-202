from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from datastructures.nodes.DNode import DNode
from datastructures.Linear.doublyLL import DoublyLL

class doublyCLL(DoublyLL):
    def __init__(self):
        super().__init__()
        self.head = None
        self.tail = None
    
    def is_empty(self):
        return self.size == 0
    
    def InsertHead(self, node):
        if not self.head:
            node.prev = node
            node.next = node
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            node.prev = self.tail
            self.head.prev = node
            self.tail.next = node
            self.head = node
        self.size += 1
    
    def InsertTail(self, node):
        if not self.tail:
            self.InsertHead(node)
        else:
            node.next = self.head
            node.prev = self.tail
            self.head.prev = node
            self.tail.next = node
            self.tail = node
        self.size += 1
    
    def Insert(self, node, position):
        if position == 0:
            self.InsertHead(node)
        elif position >= self.size:
            self.InsertTail(node)
        else:
            current = self.head
            for i in range(1, position):
                current = current.next
            node.next = current.next
            node.prev = current
            current.next.prev = node
            current.next = node
            self.size += 1
    
    def SortedInsert(self, node):
        if not self.head:
            self.InsertHead(node)
        elif node.data <= self.head.data:
            self.InsertHead(node)
        elif node.data >= self.tail.data:
            self.InsertTail(node)
        else:
            current = self.head
            while current.next != self.head and current.next.data < node.data:
                current = current.next
            node.next = current.next
            node.prev = current
            current.next.prev = node
            current.next = node
            self.size += 1
    
    def is_sorted(self):
        if not self.tail:
            return True
        current = self.tail.next
        while current != self.tail:
            if current.data > current.next.data:
                return False
            current = current.next
        return True
    
    def length(self):
        return self.size

    def Search(self, node):
        current = self.head
        while current and current != self.tail:
            if current.data == node.data:
                return current
            current = current.next
        if current == self.tail and current.data == node.data:
            return current
        return None
    
    def DeleteHead(self):
        if not self.head:
            return None
        temp = self.head
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.tail.next = self.head
            self.head.prev = self.tail
        temp.next = None
        temp.prev = None
        self.size -= 1
        return temp
    
    def DeleteTail(self):
        if not self.tail:
            return None
        temp = self.tail
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = self.head
            self.head.prev = self.tail
        temp.next = None
        temp.prev = None
        self.size -= 1
        return temp
    
    def Delete(self, node):
        if not self.head:
            return
        current = self.head
        position = 0
        while current:
            if current == node:
                break
            current = current.next
            position += 1
            if current == self.head:
                return
        if position == 0:
            self.DeleteHead()
        elif position == self.size - 1:
            self.DeleteTail()
        else:
            current.prev.next = current.next
            current.next.prev = current.prev
            current.next = None
            current.prev = None
            self.size -= 1
    
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


# TESTING THE DOUBLYCLL:
def main():
    # Create nodes
    node1 = DNode(1)
    node2 = DNode(2)
    node3 = DNode(3)
    node4 = DNode(4)
    node5 = DNode(5)

    # Create circular linked list
    clist = doublyCLL()
    print("Creating new circular linked list:")
    clist.Print()

    # Test is_empty method
    print("\nTesting is_empty method:")
    print("List is empty:", clist.is_empty())

    # Test InsertHead method
    print("\nTesting InsertHead method:")
    clist.InsertHead(node1)
    clist.Print()

    # Test InsertTail method
    print("\nTesting InsertTail method:")
    clist.InsertTail(node2)
    clist.Print()

    # Test Insert method
    print("\nTesting Insert method:")
    clist.Insert(node3, 1)
    clist.Print()

    # Test SortedInsert method
    print("\nTesting SortedInsert method:")
    clist.SortedInsert(node4)
    clist.Print()

    # Test is_sorted method
    print("\nTesting is_sorted method:")
    print("List is sorted:", clist.is_sorted())

    # Test length method
    print("\nTesting length method:")
    print("List length:", clist.length())

    # Test Search method
    print("\nTesting Search method:")
    result = clist.Search(node3)
    if result:
        print("Node found with data value 3")
    else:
        print("Node not found with data value 3")

    # Test DeleteHead method
    print("\nTesting DeleteHead method:")
    clist.DeleteHead()
    clist.Print()

    # Test DeleteTail method
    print("\nTesting DeleteTail method:")
    clist.DeleteTail()
    clist.Print()

    # Test Delete method
    print("\nTesting Delete method:")
    clist.Delete(node3)
    clist.Print()

    # Test edge cases
    print("\nTesting edge cases:")
    clist.InsertHead(node5)
    clist.InsertTail(node1)
    clist.DeleteHead()
    clist.DeleteTail()
    clist.Delete(node2)
    clist.Print()

if __name__ == '__main__':
    main()
    
