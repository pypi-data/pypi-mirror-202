import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))


from myLib.datastructures.Nodes.TNode import TNode

class BST:
    def __init__(self, root=None):
        if isinstance(root, TNode): #isinstance determines what type of argument it is
            self.root = root 
        elif isinstance(root, int):
            self.root = TNode(data=root)
        else:
            self.root = None
    
    def set_root(self, root):
        if isinstance(root, TNode): 
            self.root = root 
        elif isinstance(root, int):
            self.root = TNode(data=root)
        else:
            self.root = None

    def get_root(self):
        return self.root

    def Insert(self, param):
        if isinstance(param, TNode):
            # If the parameter is a node, add it to the AVL tree
            self.Insert(param.data)
            # Then, add its children to the AVL tree
            if param.left is not None:
                self.Insert(param.left)
            if param.right is not None:
                self.Insert(param.right)
        elif isinstance(param, int):
            # If the parameter is an integer, insert it into the AVL tree
            if self.root is None:
                self.root = TNode(param)
            else:
                current_node = self.root
                parent_node = None
                while current_node is not None:
                    parent_node = current_node
                    if param <= current_node.data:
                        current_node = current_node.left
                    else:
                        current_node = current_node.right
                if param <= parent_node.data:
                    parent_node.left = TNode(param)
                    parent_node.left.parent = parent_node
                else:
                    parent_node.right = TNode(param)
                    parent_node.right.parent = parent_node




    def Delete(self, val):
        if self.root is None:
            return
        node = self.Search(val)
        if node is None:
            print("The node with value " + str(val) + " does not exist in the tree.")
            return

        parent = node.parent

        # case 1: node is a leaf node
        if node.left is None and node.right is None:
            if parent is None:
                self.root = None
            elif parent.left == node:
                parent.left = None
            else:
                parent.right = None

        # case 2: node has only one child
        elif node.left is None:
            if parent is None:
                self.root = node.right
            elif parent.left == node:
                parent.left = node.right
            else:
                parent.right = node.right
            node.right.parent = parent

        elif node.right is None:
            if parent is None:
                self.root = node.left
            elif parent.left == node:
                parent.left = node.left
            else:
                parent.right = node.left
            node.left.parent = parent


        # case 3: node has both left and right children
        else:
            # find the node with the smallest value in the right subtree
            temp = node.right
            while temp.left is not None:
                temp = temp.left
            # replace node's value with temp's value
            node.data = temp.data
            # delete the node with temp's value in the right subtree
            if temp.parent.left == temp:
                temp.parent.left = temp.right
            else:
                temp.parent.right = temp.right
            if temp.right is not None:
                temp.right.parent = temp.parent
        if self.Search(val) is not None:
            self.Delete(val)

    def Search(self, val):
        current = self.root
        while current is not None:
            if val == current.data:
                return current
            elif val <= current.data:
                current = current.left
            else:
                current = current.right
        return None

    def printInOrder(self):
        node = self.root
        if node is None:
            return

        stack = []
        current = node

        while True:
            if current is not None:
                stack.append(current)
                current = current.left
            elif stack:
                current = stack.pop()
                print(current.toString(), end="\n")
                current = current.right
            else:
                break




    def printBF(self):
        if self.root is None:
            return
        
        queue = [self.root]
        
        while queue:
            current_node = queue.pop(0)
            print(current_node.toString(), end="\n")
            
            if current_node.get_left():
                queue.append(current_node.get_left())
                
            if current_node.get_right():
                queue.append(current_node.get_right())
    def updateBalance(self, node):
        if node is None:
            return

        # Update balance factor for current node
        node.set_balance(self.getHeight(node.left) - self.getHeight(node.right))

        # Recursively update balance factors for children
        self.updateBalance(node.left)
        self.updateBalance(node.right)

    def getHeight(self, node):
        if node is None:
            return -1
        return max(self.getHeight(node.left), self.getHeight(node.right)) + 1
    