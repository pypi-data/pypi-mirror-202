from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from datastructures.nodes.SNode import Node
from datastructures.Linear.singlyLL import SinglyLL



class LLQueue(SinglyLL):
    def __init__(self):
        super().__init__()

    def InsertHead(self, node):
        pass

    def InsertTail(self, node):
        super().InsertTail(node)

    def insert(self, node, position):
        if position == 0:
            self.InsertHead(node)
        else:
            super().Insert(node, position)

    def SortedInsert(self, node):
        super().InsertTail(node)

    def Search(self, node):
        return super().Search(node)

    def DeleteHead(self):
        return super().DeleteHead()

    def DeleteTail(self):
        return super().DeleteTail()

    def Delete(self, node):
        return super().Delete(node)

    def Sort(self):
        super().Sort()

    def is_sorted(self):
        if not self.head:
            return True
        current = self.head
        while current.next:
            if current.data > current.next.data:
                return False
            current = current.next
        
        return True
        
    def length(self):
        return self.size

    def Clear(self):
        super().Clear()

    def enqueue(self, node):
        self.InsertTail(node)

    def dequeue(self):
        return self.DeleteHead()
    
    def Print(self):
        # Print the list length
        print("List length:", self.length())

        # Check if the list is sorted
        sorted_status = "sorted" if self.is_sorted() else "not sorted"
        print("Sorted status:", sorted_status)

        # Print the list content
        current = self.head
        print("List content:", end=" ")
        while current is not None:
            print(current.data, end=" ")
            current = current.next
        print()


# TESTING THE LLQUEUE:
def main():
    # Create a new LLQueue
    queue = LLQueue()

    # Add some nodes to the queue
    queue.enqueue(Node(1))
    queue.enqueue(Node(3))
    queue.enqueue(Node(2))

    # Print the queue
    print("Queue contents:", end=" ")
    queue.Print()

    # Dequeue some nodes from the queue
    print("Dequeuing", queue.dequeue().data)
    print("Dequeuing", queue.dequeue().data)

    # Print the queue again
    print("Queue contents:", end=" ")
    queue.Print()

    # Add some more nodes to the queue
    queue.enqueue(Node(4))
    queue.enqueue(Node(1))

    # Print the queue once more
    print("Queue contents:", end=" ")
    queue.Print()

    # Test the InsertHead function
    queue.InsertHead(Node(5))
    print("Inserting 5 at the head")
    queue.Print()

    # Test the insert function
    queue.insert(Node(6), 3)
    print("Inserting 6 at position 3")
    queue.Print()

    # Test the SortedInsert function
    queue.SortedInsert(Node(0))
    print("Inserting 0 in a sorted manner")
    queue.Print()

    # Test the Search function
    node_to_search = Node(4)
    search_result = queue.Search(node_to_search)
    if search_result is not None:
        print(f"Searching for {node_to_search.data}, Found: {search_result.data}")
    else:
        print(f"Node with data {node_to_search.data} not found")

    # Test the Delete function
    node_to_delete = Node(2)
    delete_result = queue.Delete(node_to_delete)
    if delete_result is not None:
        print(f"Deleting {node_to_delete.data}, Deleted: {delete_result.data}")
    else:
        print(f"Node with data {node_to_delete.data} not found")

    queue.Print()

    # Test the Sort function
    print("Sorting the list")
    queue.Sort()
    queue.Print()

    # Test the length function
    print(f"Length of the queue: {queue.length()}")

    # Test the Clear function
    print("Clearing the queue")
    queue.Clear()
    queue.Print()


if __name__ == '__main__':
    main()
