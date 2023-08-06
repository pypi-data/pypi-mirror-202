import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from Trees.BST import BST
from myLib.datastructures.Nodes.TNode import TNode

class AVL(BST):
        
    def __init__(self, root = None):
        if isinstance(root, TNode):
            if root.left or root.right is None:
                self.root = root
            else:
                self.avlCreator(root)
        elif isinstance(root, int):
            self.root = TNode(data=root)
        else:
            self.root = None
        self.updateBalance(self.root)
        self.balance_avl()


    

    def balance_avl(self):
        # Update the heights of all nodes in the tree
        self.update_heights(self.root)

        # Balance the tree by performing rotations
        self.root = self.balance_tree(self.root)
        self.updateBalance(self.root)
        

    def update_heights(self, node):
        # Recursively update the height of a node and its children
        if node is None:
            return -1
        node.height = 1 + max(self.update_heights(node.left), self.update_heights(node.right))
        return node.height

    def balance_tree(self, node):
        # Balance a tree rooted at the given node
        if node is None:
            return None

        # Balance the left and right subtrees
        node.left = self.balance_tree(node.left)
        node.right = self.balance_tree(node.right)

        # Check the balance factor and perform rotations if necessary
        balance_factor = self.get_balance_factor(node)
        if balance_factor > 1:
            if self.get_balance_factor(node.left) < 0:
                node.left = self.rotate_left(node.left)
            node = self.rotate_right(node)
        elif balance_factor < -1:
            if self.get_balance_factor(node.right) > 0:
                node.right = self.rotate_right(node.right)
            node = self.rotate_left(node)

        return node

    def get_balance_factor(self, node):
        # Get the balance factor of a node
        left_height = node.left.height if node.left else -1
        right_height = node.right.height if node.right else -1
        return left_height - right_height

    def rotate_left(self, node):
        # Perform a left rotation on a node
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        self.update_heights(node)
        self.update_heights(new_root)
        return new_root

    def rotate_right(self, node):
        # Perform a right rotation on a node
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        self.update_heights(node)
        self.update_heights(new_root)
        return new_root

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
                    if parent_node.left is None:
                        parent_node.left = TNode(param)
                        parent_node.left.parent = parent_node
                    else:
                        self.Insert(param)  # Recursively insert duplicate node to the left
                else:
                    if parent_node.right is None:
                        parent_node.right = TNode(param)
                        parent_node.right.parent = parent_node
                    else:
                        self.Insert(param)  # Recursively insert duplicate node to the right
            self.updateBalance(self.root)
            self.balance_avl()





    def set_root(self, root):
        if isinstance(root, TNode): 
            self.root = root 
        elif isinstance(root, int):
            self.root = TNode(data=root)
        else:
            self.root = None        
        self.updateBalance(self.root)
        self.balance_avl()
    

    def Delete(self,val):
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
        self.updateBalance(self.root)
        self.balance_avl()
        if self.Search(val) is not None:
            self.Delete(val)




    


