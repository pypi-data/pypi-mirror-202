from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from datastructures.nodes.TNode import TNode

class BST():

    def __init__(self, root=None):
        if root is None:
            self.root = None
        elif isinstance(root, int):
            self.root = TNode(root)
        elif isinstance(root, TNode):
            self.root = root


    def set_root(self, root):
        if self.root is None:

            if isinstance(root, TNode):
                self.root = root
            elif isinstance(root, int):
                self.root = TNode(data=root)
            else:
                raise TypeError("Root must be an integer or TNode object.")

        else:
            print("A root has already been set")


    def get_root(self):
        return self.root

    def Insert(self, valOrNode):                
        if isinstance(valOrNode, int):          
            node = TNode(valOrNode)             

            current = self.root
            parent = None
            while current is not None:
                parent = current 
                if valOrNode <= current.data:
                    current = current.left
                else:
                    current = current.right

            if self.root is None:
                self.root = node
            elif valOrNode <= parent.data:
                parent.left = node
                node.parent = parent
            else:
                parent.right = node
                node.parent = parent

        elif isinstance(valOrNode, TNode):
            current = self.root
            parent = None
            while current is not None:
                parent = current 
                if valOrNode.data <= current.data:
                    current = current.left
                else:
                    current = current.right

            if self.root is None:
                self.root = valOrNode
            elif valOrNode.data <= parent.data:
                parent.left = valOrNode
                valOrNode.parent = parent
            else:
                parent.right = valOrNode
                valOrNode.parent = parent


    def Delete(self, val):
        counter = 0 
        while(1):
            counter += 1
            parent = None
            current = self.root

            while current is not None:
                if val == current.data:
                    break
                elif val < current.data:
                    parent = current
                    current = current.left
                else:
                    parent = current
                    current = current.right

            if current is None:
                if counter == 1:
                    print("Value was not found in the tree.")
                return

            # Case 1: node has no children
            if current.left is None and current.right is None:
                if parent is None:
                    self.root = None
                elif parent.left == current:
                    parent.left = None
                else:
                    parent.right = None

            # Case 2: node has one child
            elif current.left is None:
                if parent is None:
                    self.root = current.right           
                    current.right.parent = None
                elif parent.left == current:
                    parent.left = current.right
                    current.right.parent = parent

                else:
                    parent.right = current.right
                    current.right.parent = parent

            elif current.right is None:
                if parent is None:
                    self.root = current.left
                    current.left.parent = None
                elif parent.left == current:
                    parent.left = current.left
                    current.left.parent = parent
                else:
                    parent.right = current.left
                    current.left.parent = parent

            # Case 3: node has two children
            else:
                successor_parent = current
                successor = current.right 

                while successor.left is not None:
                    successor_parent = successor
                    successor = successor.left

                current.data = successor.data

                if successor_parent.left == successor:
                    successor_parent.left = successor.right

                else:
                    successor_parent.right = successor.right



    def search(self, val):
        node = self.root
        while node is not None and node.data != val:
            if val < node.data:
                node = node.left
            else:
                node = node.right
        if node != None:
            return node
        else:
            return None                    


    def printInOrder(self):
        if self.root is not None:
            stack = []
            current = self.root
            done = False
            while not done:
                if current is not None:
                    stack.append(current)
                    current = current.left
                else:
                    if len(stack) > 0:
                        current = stack.pop()
                        print(current.toString(), end=" ")
                        current = current.right
                    else:
                        done = True

    def printBF(self):
        queue = [self.root] if self.root is not None else []
        while queue:
            current_level = []
            for _ in range(len(queue)):
                node = queue.pop(0)
                current_level.append(node.toString())
                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)
            print(*current_level, sep=" ")



