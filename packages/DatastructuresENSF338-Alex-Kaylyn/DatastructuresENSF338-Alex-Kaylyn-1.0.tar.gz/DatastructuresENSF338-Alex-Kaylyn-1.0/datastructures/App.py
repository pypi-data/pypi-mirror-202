from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from mylib.datastructures.nodes.SNode import Node
from mylib.datastructures.nodes.DNode import DNode
from mylib.datastructures.Linear.LLStack import LLStack
from mylib.datastructures.Linear.LLQueue import LLQueue
from mylib.datastructures.Linear.singlyLL import SinglyLL
from mylib.datastructures.Linear.doublyLL import DoublyLL
from mylib.datastructures.Linear.singlyCLL import CircularSinglyLL
from mylib.datastructures.Linear.doublyCLL import doublyCLL
from datastructures.nodes.TNode import TNode
from mylib.datastructures.treestructures.BST import BST
from mylib.datastructures.treestructures.AVL import AVL 

def main():
    print("\nBeginning of Linear tests!\n")

    # TESTING THE SINGLYLL:
    print("TESTING THE SINGLYLL")
    
    # create a singly linked list
    sll = SinglyLL()

    # insert nodes at head and tail
    sll.InsertHead(Node(2))
    sll.InsertHead(Node(4))
    sll.InsertHead(Node(1))
    sll.InsertTail(Node(5))

    # test printing the list
    sll.Print()  # should print 1, 4, 2, 5
    sll.Sort() 

    # test sorted insert
    sll.SortedInsert(Node(3))
    sll.SortedInsert(Node(0))
    sll.SortedInsert(Node(6))
    sll.Print()  # should print 0, 1, 2, 3, 4, 5, 6

    # test insert at position
    sll.Insert(Node(7), 7)
    sll.Insert(Node(-1), 0)
    sll.Print()  # should print -1, 0, 1, 2, 3, 4, 5, 6, 7

    # test search
    node = sll.Search(Node(3))
    if node:
        print("Node found:", node.data)  # should print "Node found: 3"
    else:
        print("Node not found")

    # test delete
    node = sll.Delete(Node(0))
    if node:
        print("Node deleted:", node.data)  # should print "Node deleted: 0"
    else:
        print("Node not found")
    sll.Delete(Node(7))
    sll.Delete(Node(6))
    sll.Print()  # should print -1, 1, 2, 3, 4, 5

    # test sort
    sll.InsertHead(Node(9))
    sll.Sort()
    sll.Print()  # should print -1, 1, 2, 3, 4, 5, 9

    # test clear
    sll.Clear()
    sll.Print()  # should print "List is empty."



# TESTING THE DOUBLYLL:
    print()
    print()
    print()
    print()

    print("TESTING THE DOUBLYLL")
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



# TESTING THE SINGLYCLL:
    print()
    print()
    print()
    print()
    print("TESTING THE SINGLYCLL")
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




# TESTING THE DOUBLYCLL:
    print()
    print()
    print()
    print()
    print("TESTING THE DOUBLYCLL")
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



# TESTING THE LLStack
    print()
    print()
    print()
    print()
    print("TESTING THE LLStack")    
    stack = LLStack()           # Initialize the stack

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


# TESTING THE LLQUEUE
    print()
    print()
    print()
    print()
    print("TESTING THE LLQUEUE")    
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

    print("\n\nEnd of Linear Tests!\n\n")




    print("\nBeginning of Tree Structure tests!")
    """
    Tests for TNode
    """

    print("\n\nTest constructor with no arguments and test getters:")
    default_constructor = TNode()
    print("\nExpected None: ", str(default_constructor.get_data()))
    print("Expected None: ", str(default_constructor.get_parent()))
    print("Expected None: ", str(default_constructor.get_left()))
    print("Expected None: ", str(default_constructor.get_right()))
    print("Expected 0: ", str(default_constructor.get_balance()))

    print("\n\nTest set_data (helps for next test):")
    default_constructor.set_data(1)
    print("\nExpected 1: ", str(default_constructor.get_data()))

    print("\n\nTest constructor with arguments and test getters:")
    arguments_constructor = TNode(data=338, P=default_constructor, L=TNode(100), R=TNode(400), balance=0)
    print("\nExpected 338: ", str(arguments_constructor.get_data()))
    print("Expected 1: ", arguments_constructor.get_parent().toString())
    print("Expected 100: ", arguments_constructor.get_left().toString())
    print("Expected 400: ", arguments_constructor.get_right().toString())
    print("Expected 0: ", str(arguments_constructor.get_balance()))

    print("\n\nTest setters and print_node:")
    setters_printNode_test = TNode()
    setters_printNode_test.set_data(5)
    setters_printNode_test.set_right(TNode(6))
    setters_printNode_test.set_parent(TNode(9))
    setters_printNode_test.set_balance(1)

    print()
    setters_printNode_test.print_node()

    print("\n\nTest intializing and setting parents or children that aren't TNodes:")
    print("\nExpected: Child must be a TNode object:")
    initialize_wrong_child_type = TNode(data=338, P=default_constructor, L=TNode(100), R=400, balance=0)
    
    print("\nExpected: Parent must be a TNode object:")
    initialize_wrong_parent_type = TNode(data=338, P=11, L=TNode(100), R=TNode(400), balance=0)

    set_wrong_child_type = TNode()
    print("\nExpected: Left child must be a TNode object:")
    set_wrong_child_type.set_left(11)

    set_wrong_parent_type = TNode()
    print("\nExpected: Parent must be a TNode object:")
    set_wrong_parent_type.set_parent(11)

    print("\n\nTest toString:")
    toString_test = TNode(2, TNode(9), TNode(1), TNode(3), 0)
    print("\nExpected 9: ", toString_test.parent.toString())
    print("Expected 1: ", toString_test.left.toString())
    print("Expected 3: ", toString_test.right.toString())


    """
    Tests for BST
    """

    print("\n\nTest constructor with no argument:")
    default_constructor = BST()
    print("\nExpected None: ", default_constructor.root) 

    print("\n\nTest constructor with int argument:")
    int_constructor = BST(7)
    print("\nExpected 7: ", int_constructor.root.get_data()) 
    print("Expected None: ", int_constructor.root.get_left()) 
    print("Expected None: ", int_constructor.root.get_right()) 

    print("\n\nTest constructor with TNode argument:")
    temp = TNode(data=7, P=None, L=TNode(6), R=TNode(8), balance=0)

    TNode_constructor = BST(temp)
    print("\nExpected 7: ", TNode_constructor.root.get_data()) 
    print("Expected 6: ", TNode_constructor.root.get_left().toString()) 
    print("Expected 8: ", TNode_constructor.root.get_right().toString()) 

    print("\n\nTest setter and getter:")
    setter_getter_int = BST()
    setter_getter_int.set_root(5)
    print("\nExpected 5: ", setter_getter_int.get_root().toString())

    setter_getter_int = BST()
    setter_getter_int.set_root(TNode(20))
    print("Expected 20: ", setter_getter_int.get_root().toString())

    print("\n\nTest setting root when root has already been set_get:")
    setter_getter_int = BST(TNode(10))
    print("Expected A root has already been set_get: ") 
    setter_getter_int.set_root(TNode(25))

    print("\n\nTest Insert val with without initialized root and test printBF() function:")
    tree_without_root = BST()

    tree_without_root.Insert(10)
    tree_without_root.Insert(20)
    tree_without_root.Insert(5)
    tree_without_root.Insert(1)
    tree_without_root.Insert(6)
    tree_without_root.Insert(11)
    tree_without_root.Insert(16)

    print("\nExpecteed: \n10\n5 20\n1 6 11\n16\n")
    tree_without_root.printBF()

    print("\n\nTest Insert val with with initialized root and test search() function:")
    tree_with_root = BST()

    tree_with_root.Insert(10)
    tree_with_root.Insert(15)
    tree_with_root.Insert(12)
    tree_with_root.Insert(17)
    tree_with_root.Insert(5)
    tree_with_root.Insert(1)

    ten = tree_with_root.search(10)
    print("\nExpected Data: 10, Parent: None, Left Child: 5, Right Child: 15, Balance: 0")
    ten.print_node()

    fifteen = tree_with_root.search(15)
    print("\nExpected Data: 15, Parent: 10, Left Child: 12, Right Child: 17, Balance: 0")
    fifteen.print_node()

    twelve = tree_with_root.search(12)
    print("\nExpected Data: 12, Parent: 15, Left Child: None, Right Child: None, Balance: 0")
    twelve.print_node()

    seventeen = tree_with_root.search(17)
    print("\nExpected Data: 17, Parent: 15, Left Child: None, Right Child: None, Balance: 0")
    seventeen.print_node()

    five = tree_with_root.search(5)
    print("\nExpected Data: 5, Parent: 10, Left Child: 1, Right Child: None, Balance: 0")
    five.print_node()

    one = tree_with_root.search(1)
    print("\nExpected Data: 1, Parent: 5, Left Child: None, Right Child: None, Balance: 0")
    one.print_node()

    print("\n\nTest insert TNode:")
    insert_TNode = BST()
    insert_TNode.Insert(TNode(2))
    insert_TNode.Insert(TNode(1))
    insert_TNode.Insert(TNode(0))
    insert_TNode.Insert(TNode(4))
    insert_TNode.Insert(TNode(3))
    print("\nExpecteed: \n2\n1 4\n0 3\n")
    insert_TNode.printBF()

    tree_with_root.Insert(TNode(13, L=TNode(12.5), R=TNode(14)))
    print("\nExpecteed: \n10\n5 15\n1 12 17\n13\n12.5 14\n")
    tree_with_root.printBF()

    print("\n\nTest Delete:")
    delete_nodes = tree_with_root

    print("Delete a node with no children:")
    delete_nodes.Delete(12.5)
    print("\nExpected 12.5 gone:")    
    delete_nodes.printBF()

    print("\nDelete a node with children and a parent:")
    delete_nodes.Delete(12)
    print("\nExpected 12 gone:")      
    delete_nodes.printBF()
    print("\nTo show properly deleted node 13's parent should be 15 and right child should be 14:")
    print("Expected 15:", delete_nodes.search(13).get_parent().toString())
    print("Expected 14:", delete_nodes.search(13).get_right().toString())

    print("\nDelete root node:")
    delete_nodes.Delete(10)
    print("\nExpected 10 gone:")    
    delete_nodes.printBF()

    print("\n\nTest delete with value not found:")
    print("\nExpected 'Value was not found in the insert_node.':")
    delete_nodes.Delete(100)
    
    print("\n\nTest delete with double value:")
    delete_nodes.Insert(13)
    delete_nodes.Insert(13)
    print("\nAfter duplicate 13's inserted:")
    delete_nodes.printBF()
    delete_nodes.Delete(13)
    print("Expected all 13's gone:")
    delete_nodes.printBF()

    print("\n\nTest print in order:")
    order = insert_TNode
    print("\nExpected 0 1 2 3 4:")
    order.printInOrder()


    """
    Tests for AVL
    """

    print("\n\nTest constructor with no argument:")
    default_constructor = AVL()
    print("\n\nExpected None: ", default_constructor.root) 
    
    print("\n\nTest constructor with int argument:")
    int_constructor = BST(7)
    print("\nExpected 7: ", int_constructor.root.get_data()) 
    print("Expected None: ", int_constructor.root.get_left()) 
    print("Expected None: ", int_constructor.root.get_right()) 

    print("\n\nTest constructor with TNode argument:")
    temp = TNode(data=7, P=None, L=TNode(6), R=TNode(8), balance=0)

    TNode_constructor = BST(temp)
    print("\nExpected 7: ", TNode_constructor.root.get_data()) 
    print("Expected 6: ", TNode_constructor.root.get_left().toString()) 
    print("Expected 8: ", TNode_constructor.root.get_right().toString()) 

    print("\n\nTest constructor with TNode argument that is the head of a BST insert_node, requiring full balancing algorithm:")
    print("Additionally testing printBF() inherited from BST:")
    BST_tree = BST(10)
    BST_tree.Insert(9)
    BST_tree.Insert(8)
    BST_tree.Insert(7)
    BST_tree.Insert(6)
    BST_tree.Insert(5)
    print("\nTree as a BST:")
    BST_tree.printBF()
    print("Tree as an AVL, should be balanced with 10 no longer the root:")
    TNode_arg_constructor = AVL(BST_tree.root)
    TNode_arg_constructor.printBF()

    print("\n\nTest that newly balanced insert_node's nodes have properly edited members:.")
    print("Additionally test search() inherited from BST:")
    print("\nCheck each node is updated properly:")

    eight = TNode_arg_constructor.search(8)
    print("\nExpected Data: 8, Parent: None, Left Child: 6, Right Child: 10, Balance: 0")
    eight.print_node()

    six = TNode_arg_constructor.search(6)
    print("\nExpected Data: 6, Parent: 8, Left Child: 5, Right Child: 7, Balance: 0")
    six.print_node()

    ten = TNode_arg_constructor.search(10)
    print("\nExpected Data: 10, Parent: 8, Left Child: 9, Right Child: None, Balance: -1")
    ten.print_node()

    five = TNode_arg_constructor.search(5)
    print("\nExpected Data: 5, Parent: 6, Left Child: None, Right Child: None, Balance: 0")
    five.print_node()

    seven = TNode_arg_constructor.search(7)
    print("\nExpected Data: 7, Parent: 6, Left Child: None, Right Child: None, Balance: 0")
    seven.print_node()

    nine = TNode_arg_constructor.search(9)
    print("\nExpected Data: 9, Parent: 10, Left Child: None, Right Child: None, Balance: 0")
    nine.print_node()


    print("\n\nTest setter:")
    BST_tree2 = BST(10)
    BST_tree2.Insert(9)
    BST_tree2.Insert(8)
    BST_tree2.Insert(14)
    BST_tree2.Insert(15)
    BST_tree2.Insert(16)
    BST_tree2.Insert(20)
    set_get = AVL()
    print("\nTree as a BST:")
    BST_tree2.printBF()
    set_get.set_root(BST_tree2.root)
    print("\nTree as AVL, should be balanced with 10 no longer the root:")
    set_get.printBF()

    print("\n\nTest balance values are correct for nodes and show that none exceed -1 or 1:")
    print("\nExpected 1: ", set_get.search(10).get_balance())
    print("Expected -1: ", set_get.search(9).get_balance())
    print("Expected -1: ", set_get.search(16).get_balance())
    print("Expected 0: ", set_get.search(8).get_balance())
    print("Expected 1: ", set_get.search(14).get_balance())
    print("Expected 0: ", set_get.search(20).get_balance())
    print("Expected 0: ", set_get.search(15).get_balance())

    print("\n\nTest getter:")
    print("\nExpected 10: ", set_get.get_root().toString())

    print("\n\nTest insert with int val with no root argument constructor:")
    insert_val = AVL()
    insert_val.Insert(4)
    insert_val.Insert(2)
    insert_val.Insert(3)
    insert_val.Insert(1)
    insert_val.Insert(5)
    insert_val.Insert(7)
    insert_val.Insert(9)
    print("\nExpected: \n3\n2 5\n1 4 7\n9")
    print("Result:")
    insert_val.printBF()

    print("\n\nTest insert with TNode node with root argument constructor:")
    insert_node = AVL(TNode(4))
    insert_node.Insert(TNode(2))
    insert_node.Insert(TNode(1))
    insert_node.Insert(TNode(5))
    insert_node.Insert(TNode(7))
    insert_node.Insert(TNode(9))
    insert_node.Insert(TNode(6))
    insert_node.Insert(TNode(8))
    insert_node.Insert(TNode(3))
    insert_node.Insert(TNode(0)) 
    print("\nExpected:\n5\n2 7\n1 4 6 9\n0 3 8")
    print("Result:")
    insert_node.printBF()

    print("\n\nTest Delete:")
    delete_nodes = insert_node

    print("Delete a node with no children:")
    delete_nodes.Delete(6)
    print("\nExpected 6 gone:")    
    delete_nodes.printBF()

    print("\nDelete a node with children and a parent:")
    delete_nodes.Delete(2)
    print("\nExpected 2 gone:")      
    delete_nodes.printBF()

    print("\nDelete root node:")
    delete_nodes.Delete(5)
    print("\nExpected 5 gone:")    
    delete_nodes.printBF()

    print("\n\nTest after deletions all nodes still have a balance between -1 and 1:")
    print("\nExpected -1: ", delete_nodes.search(7).get_balance())
    print("Expected -1: ", delete_nodes.search(3).get_balance())
    print("Expected 1: ", delete_nodes.search(8).get_balance())
    print("Expected -1: ", delete_nodes.search(1).get_balance())
    print("Expected 0: ", delete_nodes.search(4).get_balance())
    print("Expected 0: ", delete_nodes.search(9).get_balance())
    print("Expected 0: ", delete_nodes.search(0).get_balance())

    print("\n\nTest delete with value not found:")
    print("\nExpected 'Value was not found in the insert_node.':")
    delete_nodes.Delete(100)
    
    print("\n\nTest delete with double value:")
    delete_nodes.Insert(3)
    delete_nodes.Insert(3)
    print("\nAfter duplicate 3's inserted:")
    delete_nodes.printBF()
    delete_nodes.Delete(3)
    print("Expected all 3's gone:")
    delete_nodes.printBF()

    print("\n\nTest print in order:")
    order = insert_val
    print("\nExpected 1 2 3 4 7 9:")
    order.printInOrder()
    
    
    print("\n\nEnd of Tree Structure Tests!")

if __name__ == '__main__':
    main()