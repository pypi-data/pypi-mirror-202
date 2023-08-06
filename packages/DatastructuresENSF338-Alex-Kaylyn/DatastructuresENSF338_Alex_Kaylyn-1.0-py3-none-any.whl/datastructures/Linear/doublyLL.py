from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from datastructures.nodes.DNode import DNode
from datastructures.Linear.singlyLL import SinglyLL

class DoublyLL(SinglyLL):
    def __init__(self, head=None):
        self.head = head
        self.tail = head
        self.size = 0
        if head:
            current = head
            while current.next:
                current = current.next
            self.tail = current
            self.size = 1

    def InsertHead(self, node):
        if not self.head:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self.size += 1

    def InsertTail(self, node):
        if not self.tail:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
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
            current.next.prev = node
            current.next = node
            node.prev = current
            self.size += 1

    def DeleteHead(self):
        if not self.head:
            return None
        temp = self.head
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        temp.next = None
        self.size -= 1
        if not self.head:
            self.tail = None
        return temp

    def DeleteTail(self):
        if not self.tail:
            return None
        temp = self.tail
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
        temp.prev = None
        self.size -= 1
        if not self.tail:
            self.head = None
        return temp

    def Delete(self, node):
        if not node or not self.head:
            return None
        if self.head.data == node.data:
            return self.DeleteHead()
        current = self.head
        prev = None
        while current:
            if current.data == node.data:
                break
            prev = current
            current = current.next
        if not current:
            return None
        if current == self.tail:
            return self.DeleteTail()
        if prev:
            prev.next = current.next
        else:
            self.head = current.next
        current.next = None
        self.size -= 1
        return current
    
    def Sort(self):
        if not self.head:
            return
        new_head = self.head
        new_tail = self.head
        current = self.head.next
        new_head.next = None
        while current:
            next_node = current.next
            if current.data <= new_head.data:
                current.next = new_head
                new_head = current
            elif current.data >= new_tail.data:
                new_tail.next = current
                new_tail = current
                new_tail.next = None
            else:
                search = new_head
                while search.next and search.next.data < current.data:
                    search = search.next
                current.next = search.next
                search.next = current
            
            current = next_node

        self.head = new_head
        self.tail = new_tail
    

# TESTING THE DOUBLYLL:
def main():
    # Create some nodes
    node1 = DNode(1)
    node2 = DNode(2)
    node3 = DNode(3)
    node4 = DNode(4)
    
    # Create an empty DoublyLL object
    dllist = DoublyLL()
    
    # Test InsertHead function
    dllist.InsertHead(node2)
    dllist.InsertHead(node1)
    dllist.Print() # should print 1 <-> 2
    
    # Test InsertTail function
    dllist.InsertTail(node3)
    dllist.Print() # should print 1 <-> 2 <-> 3
    
    # Test Insert function
    dllist.Insert(node4, 1)
    dllist.Print() # should print 1 <-> 4 <-> 2 <-> 3
    
    # Test DeleteHead function
    dllist.DeleteHead()
    dllist.Print() # should print 4 <-> 2 <-> 3
    
    # Test DeleteTail function
    dllist.DeleteTail()
    dllist.Print() # should print 4 <-> 2
    
    # Test Delete function
    dllist.Delete(node2)
    dllist.Print() # should print 4
    
    # Test Sort function
    node5 = DNode(5)
    node6 = DNode(6)
    node7 = DNode(7)
    dllist.InsertHead(node6)
    dllist.InsertTail(node5)
    dllist.InsertTail(node7)
    dllist.Print() # should print 6 <-> 4 <-> 5 <-> 7
    dllist.Sort()
    dllist.Print() # should print 4 <-> 5 <-> 6 <-> 7
    
    # Test Search function
    result = dllist.Search(DNode(6))
    if result:
        print("Node found:", result.data) # should print Node found: 6
    else:
        print("Node not found")
        
    result = dllist.Search(DNode(8))
    if result:
        print("Node found:", result.data)
    else:
        print("Node not found") # should print Node not found

if __name__ == '__main__':
    main()
